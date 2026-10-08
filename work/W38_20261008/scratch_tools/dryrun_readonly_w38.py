#!/usr/bin/env python3
"""W38 해설교체·적재 dry-run 과 동등한 읽기 전용 대조 (DB 읽기만, 원장·백업·DB 쓰기 0).
해설교체 도구의 validate/answer_agrees/plan_for 를 import 해 같은 판정을 내고, 적재기와 같은 방식으로
bank_item_profiles 기존 ref·approved 보존 수를 센다. 사용: dryrun_readonly_w38.py <jsonl>... --report <out.json>"""
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/home/user/ngd2-figtool")
spec = importlib.util.spec_from_file_location("sol_replace", ROOT / "공장" / "온톨로지_v61_해설교체_20260901.py")
SR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SR)


def main() -> int:
    args = sys.argv[1:]
    report = Path(args[args.index("--report") + 1]) if "--report" in args else None
    files = [a for a in args if a.endswith(".jsonl")]
    objs = []
    for f in files:
        for l in Path(f).read_text(encoding="utf-8").splitlines():
            if l.strip():
                o = json.loads(l)
                o["_file"] = Path(f).name
                objs.append(o)
    db = SR.load_db()
    plans, actions = [], Counter()
    for o in objs:
        st = SR.fetch_state(db, int(o["item_id"]))
        p = SR.plan_for(o, st)
        p["file"] = o["_file"]
        p["raw_text_sha256_matches_packet"] = None
        plans.append(p)
        actions[p["action"]] += 1
    refs = [f"items:{int(o['item_id'])}" for o in objs if not o.get("needs_review")]
    existing = db.table("bank_item_profiles").select("ref,provenance").in_("ref", refs).execute().data or []
    out = {"mode": "read-only dry-run (해설교체 plan_for + 적재 existing 대조)", "items": len(objs), "actions": dict(actions),
           "commit_candidates": [p["item_id"] for p in plans if p["action"] in ("update", "insert")],
           "needs_review": [p["item_id"] for p in plans if p["action"] == "needs_review"],
           "errors": {p["item_id"]: p["errors"] for p in plans if p["errors"]},
           "answer_disagree": [p["item_id"] for p in plans if p["answer_agrees"] is False],
           "profiles_existing_in_db": len(existing), "approved_in_db": sum(1 for r in existing if (r.get("provenance") or {}).get("human_review_status") == "approved"),
           "plans": plans, "db_writes": 0}
    txt = json.dumps(out, ensure_ascii=False, indent=1)
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(txt, encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "plans"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
