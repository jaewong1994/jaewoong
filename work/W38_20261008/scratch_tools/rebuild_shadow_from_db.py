#!/usr/bin/env python3
"""DB bank_item_profiles(6,084) → 데이터원장/리커버리_v61_item_profile_shadow_20260905.jsonl 재구성(읽기 전용 입력),
그 프로파일로 어댑터(공장/리커버리_v61_프로파일어댑터_20260905.py)의 build_graph/build_pool 을 호출해 그래프·처방 풀을 다시 만든다.
사용: rebuild_shadow_from_db.py [--extra <jsonl>...]   (--extra: 새 웨이브 shadow 행을 합쳐서 그래프·풀 재계산)"""
import json, sys, importlib.util, collections, argparse
from pathlib import Path
from datetime import datetime
ROOT=Path('/home/user/ngd2-figtool'); S=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--extra',nargs='*',default=[]); ap.add_argument('--no-db',action='store_true'); a=ap.parse_args()
cache=S/'db_bank_item_profiles.json'
if not cache.exists() and not a.no_db:
    from supabase import create_client
    c=json.load(open(ROOT/'공장/적재설정.json')); db=create_client(c['url'],c['key'])
    rows=[]; off=0
    while True:
        page=db.table('bank_item_profiles').select('*').order('ref').range(off,off+999).execute().data
        rows+=page
        if len(page)<1000: break
        off+=1000
    cache.write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
rows=json.loads(cache.read_text(encoding='utf-8'))
def to_shadow(r):
    return {"ref":r['ref'],"ver":r.get('profile_version') or '1.1-v61',
            "curriculum":{"course":r.get('course'),"unit":r.get('unit'),"unit_main":r.get('unit_main'),"subunit":r.get('subunit')},
            "type":{"code":None,"name":r.get('type_name'),"source":r.get('type_source') or 'ai'},
            "skills":r.get('skills') or [],"decisions":r.get('decisions') or [],"difficulty":r.get('difficulty') or {},
            "traps":r.get('traps') or [],"recovery":r.get('recovery') or [],"bottleneck":r.get('bottleneck') or [],
            "status":{"display":"대기" if r.get('needs_review') else "통과","usable":False},
            "provenance":r.get('provenance') or {}}
profiles=[to_shadow(r) for r in rows]
refs={p['ref'] for p in profiles}
extra_n=0
for f in a.extra:
    for l in Path(f).read_text(encoding='utf-8').splitlines():
        if l.strip():
            p=json.loads(l)
            if p['ref'] in refs: raise SystemExit('이미 DB 에 있는 ref: '+p['ref'])
            profiles.append(p); refs.add(p['ref']); extra_n+=1
profiles.sort(key=lambda x:x['ref'])
spec=importlib.util.spec_from_file_location('adapter',ROOT/'공장/리커버리_v61_프로파일어댑터_20260905.py'); AD=importlib.util.module_from_spec(spec); sys.modules['adapter']=AD; spec.loader.exec_module(AD)
skill_dict,decision_dict=AD.load_dictionaries()
graph=AD.build_graph(profiles,skill_dict,decision_dict)
pool=AD.build_pool(profiles,skill_dict)
graph['provenance']={'source':'db-reconstructed: bank_item_profiles → adapter.build_graph','at':datetime.now().isoformat(timespec='seconds'),'db_profiles':len(rows),'extra_profiles':extra_n}
AD.OUT_PROFILES.parent.mkdir(parents=True,exist_ok=True)
AD.OUT_PROFILES.write_text('\n'.join(json.dumps(p,ensure_ascii=False) for p in profiles)+'\n',encoding='utf-8')
AD.OUT_GRAPH.write_text(json.dumps(graph,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
AD.OUT_POOL.write_text(json.dumps(pool,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
# DB 간선과 대조
dbp=json.load(open(S/'db_bank_skill_prereq.json',encoding='utf-8'))
dbe={(r['from_code'],r['to_code'],r['kind']) for r in dbp if r['kind']!='concept'}
ge={(e['from'],e['to'],e['kind']) for e in graph['edges']}
print(json.dumps({'profiles':len(profiles),'extra':extra_n,'graph':graph['stats'],'pool':pool['stats'],
                  'db_edges':len(dbe),'rebuilt_edges':len(ge),'only_db':len(dbe-ge),'only_rebuilt':len(ge-dbe),
                  'only_db_sample':sorted(dbe-ge)[:5],'only_rebuilt_sample':sorted(ge-dbe)[:5]},ensure_ascii=False))
