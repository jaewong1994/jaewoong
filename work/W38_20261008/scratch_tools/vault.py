#!/usr/bin/env python3
"""볼트(OneDrive SharePoint REST) 폴더 한정 조회. 사용: vault.py ls <rel> | get <rel> [out] | getdir <rel> <outdir>"""
import sys, json, pickle, urllib.parse, requests, os
from pathlib import Path
H=Path(__file__).parent/'vault'
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
ctx=json.load(open(H/'ctx.json'))
s=requests.Session(); s.headers['User-Agent']=UA; s.cookies=pickle.load(open(H/'cookies.pkl','rb'))
BASE='https://onedrive.live.com'+ctx['personal']+'/_api/web/'
def full(rel): return ctx['spopath']+('/'+rel if rel else '')
def ls(rel):
    p=urllib.parse.quote(full(rel),safe='')
    out=[]
    for kind in ('Folders','Files'):
        r=s.get(BASE+f"GetFolderByServerRelativePath(decodedurl=@p)/{kind}?@p='{p}'&$select=Name,TimeLastModified,Length",headers={'Accept':'application/json;odata=nometadata'},timeout=120)
        r.raise_for_status()
        for x in r.json()['value']:
            out.append(('D' if kind=='Folders' else 'F', x['Name'], x.get('TimeLastModified',''), x.get('Length')))
    return out
def get(rel):
    p=urllib.parse.quote(full(rel),safe='')
    r=s.get(BASE+f"GetFileByServerRelativePath(decodedurl=@p)/$value?@p='{p}'",timeout=300)
    r.raise_for_status(); return r.content
if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='ls':
        for k,n,t,l in ls(sys.argv[2] if len(sys.argv)>2 else ''): print(k,t[:10],l or '',n)
    elif cmd=='get':
        b=get(sys.argv[2]); out=sys.argv[3] if len(sys.argv)>3 else None
        if out: Path(out).parent.mkdir(parents=True,exist_ok=True); Path(out).write_bytes(b); print('saved',out,len(b))
        else: sys.stdout.write(b.decode('utf-8','replace'))
    elif cmd=='getdir':
        rel, outdir = sys.argv[2], Path(sys.argv[3]); outdir.mkdir(parents=True,exist_ok=True)
        for k,n,t,l in ls(rel):
            if k=='F' and n.endswith('.md'):
                (outdir/n).write_bytes(get(rel+'/'+n)); print('saved',n,l)
