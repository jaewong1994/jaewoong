#!/usr/bin/env python3
"""ADR086 문항분석초안(W38 만) → 어댑터 convert 로 W38 shadow 행 생성 → DB 재구성 프로파일과 합쳐 그래프·풀 재계산.
(원본 어댑터 build() 는 초안에 든 문항만으로 shadow·그래프를 덮어쓰므로, 클라우드에서는 DB 재구성본과 합치는 이 경로를 쓴다)
출력: scratch/W38_shadow_rows.jsonl, 데이터원장/{shadow,graph,pool} (rebuild_shadow_from_db.py --extra 호출)"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/user/ngd2-figtool")
S = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("adapter", ROOT / "공장/리커버리_v61_프로파일어댑터_20260905.py")
AD = importlib.util.module_from_spec(spec)
sys.modules["adapter"] = AD
spec.loader.exec_module(AD)
rows = AD.read_jsonl(AD.SOURCE_ANALYSIS)
skill_dict, decision_dict = AD.load_dictionaries()
profiles, rejected, stats = AD.convert(rows, skill_dict, decision_dict)
out = S / "W38_shadow_rows.jsonl"
out.write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in profiles) + "\n", encoding="utf-8")
print(json.dumps({"adr086_rows": len(rows), "converted": len(profiles), "rejected": rejected, "stats": stats}, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, "-I", str(S / "tools/rebuild_shadow_from_db.py"), "--extra", str(out)], capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-3000:], r.stderr[-2000:])
raise SystemExit(r.returncode or (1 if rejected else 0))
