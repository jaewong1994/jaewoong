#!/usr/bin/env python3
"""DB bank_skill_prereq(+bank_skill_families) → 데이터원장/리커버리_v61_prerequisite_graph_20260905.json 재구성 (읽기 전용 입력).
원본 어댑터 출력과 같은 최상위 키를 갖되 provenance 에 'db-reconstructed' 를 남긴다. resolved_conflicts/excluded_edges 는 DB 에 없으므로 빈 목록."""
import json, sys, collections
from pathlib import Path
from datetime import datetime
ROOT=Path('/home/user/ngd2-figtool'); S=Path(__file__).resolve().parents[1]
pre=json.load(open(S/'db_bank_skill_prereq.json',encoding='utf-8'))
fam=json.load(open(S/'db_bank_skill_families.json',encoding='utf-8'))
nodes={}
for f in fam:
    nodes[f['code']]={'id':f['code'],'kind':f['kind'],'course_origin':f.get('course_origin'),'name':f['name'],'item_count':0}
edges=[]; concept_links=[]
for r in pre:
    if r['kind']=='concept':
        concept_links.append({'node':r['from_code'],'prerequisite':r['to_code'],'reason':'concept_node_only','evidence':sorted(r['evidence'] or [])})
        for c in (r['from_code'],r['to_code']):
            if c.startswith('concept:') and c not in nodes:
                nodes[c]={'id':c,'kind':'concept','course_origin':None,'name':c.split('concept:',1)[1],'item_count':0}
    else:
        edges.append({'from':r['from_code'],'to':r['to_code'],'kind':r['kind'],'evidence':sorted(r['evidence'] or [])})
# item_count: 프로파일 링크 수는 DB bank_item_profile_skills 로 채울 수 있으나 그래프 소비자에 영향 없음 → 생략(0)
# 순환 검사(prerequisite+selects+used_in 전체)
adj=collections.defaultdict(list)
for e in edges:
    a,b=(e['to'],e['from']) if e['kind']=='used_in' else (e['from'],e['to'])  # 어댑터 descend 방향(used_in 은 to→from)
    adj[a].append(b)
color={}; cycles=[]
def dfs(u,stack):
    color[u]=1; stack.append(u)
    for v in adj[u]:
        if color.get(v,0)==0: dfs(v,stack)
        elif color[v]==1: cycles.append(stack[stack.index(v):]+[v])
    stack.pop(); color[u]=2
sys.setrecursionlimit(10000)
for n in list(adj):
    if color.get(n,0)==0: dfs(n,[])
stats={'nodes':len(nodes),'nodes_by_kind':dict(sorted(collections.Counter(x['kind'] for x in nodes.values()).items())),
       'edges':len(edges),'edges_by_kind':dict(sorted(collections.Counter(e['kind'] for e in edges).items())),
       'edges_before_cycle_break':len(edges),'excluded_edges':0,'cycles':len(cycles),'resolved_conflicts':0,'concept_links':len(concept_links),
       'descend_source_nodes':len({e['from'] if e['kind']!='used_in' else e['to'] for e in edges})}
g={'schema':'ngd2-recovery-v61-prerequisite-graph/1.0','read_only':True,'db_writes':0,
   'provenance':{'source':'db-reconstructed from bank_skill_prereq + bank_skill_families','at':datetime.now().isoformat(timespec='seconds'),'dictionary_ver':sorted({r['dictionary_ver'] for r in pre}),
                 'note':'원본 어댑터 산출(데이터원장)이 클라우드에 없어 DB 정본에서 재구성. resolved_conflicts/excluded_edges 는 DB 에 보존되지 않아 빈 목록.'},
   'dictionaries':{'skills':'ontology-v61-families-1.4','decisions':'ontology-v61-decision-family-1.2'},
   'course_order_chains':[['CM1','CM2','ALG','M2','CALC'],['CM1','CM2','PRST'],['CM2','GEO']],
   'nodes':sorted(nodes.values(),key=lambda x:x['id']),'edges':sorted(edges,key=lambda e:(e['from'],e['to'],e['kind'])),
   'excluded_edges':[],'cycles':cycles,'resolved_conflicts':[],'concept_links':sorted(concept_links,key=lambda c:(c['node'],c['prerequisite'])),'stats':stats}
out=ROOT/'데이터원장'/'리커버리_v61_prerequisite_graph_20260905.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(g,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False), 'cycles sample', cycles[:3])
