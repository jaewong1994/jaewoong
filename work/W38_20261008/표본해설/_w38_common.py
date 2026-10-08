# -*- coding: utf-8 -*-
"""W38(cycle48) 생성기 공통 자체검사·기록기. 로컬 파일만 읽는다(DB 없음).

규칙 출처: 공장/온톨로지_v61_해설교체_20260901.py validate · 공장/온톨로지_v61_웨이브마감_20260919.py PATS ·
W37 지시서 §3·§4·§4d~§4m · 사이클3 지침 §4·§5. 모든 문자열 필드에 금지 패턴을 적용한다.
선수 그래프 순환 검사는 데이터원장/리커버리_v61_prerequisite_graph_20260905.json(어댑터 하강 방향)을 읽는다(읽기 전용)."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = Path(__file__).resolve().parent
PK = D / "packets"
SKILLS = json.loads((ROOT / "회귀자료/온톨로지_v61_어휘병합_v61.4_20260905.json").read_text(encoding="utf-8"))["families"]
DECS = json.loads((ROOT / "회귀자료/온톨로지_v61_판단패밀리_v1.7_20260905.json").read_text(encoding="utf-8"))["families"]
UNITS = json.loads((D / "units_code_table_20260925.json").read_text(encoding="utf-8"))
GRAPH = ROOT / "데이터원장/리커버리_v61_prerequisite_graph_20260905.json"
SK = {f["id"]: f for f in SKILLS}
DE = {f["id"]: f for f in DECS}

BANNED = ["\\implies", "\\iff", "\\binom", "⟹", "⟺", "∴", "∵", "\\prod", "\\[", "WLOG", "s.t.", "QED", "MAX", "MIN"]
UNICODE_MATH = "×÷√°∠→≤≥−±≠∞"
THOUGHT_LEAK = ["다시 정리", "검산하면", "확인해 보면", "가 맞는지", "풀이지", "정답지", "해설지", "제시된 풀이", "위 그림", "그림과 같이"]
ROLES = {"setup", "decision", "execute", "compute", "conclude"}
CAUSES = {"sign_error", "condition_missing", "formula_confusion", "case_missing", "calculation", "concept_confusion", "misread", "domain_ignored"}
COSTS = {"오답", "계산폭발", "막힘"}
VE_ROLES = {"계수", "상수", "구간끝", "지표", "법", "소재", "함수형", "조건값"}
AXES = {"조건부확률 전환", "역방향", "확률변수 도입", "여사건·배반 결합", "횟수·차수 일반화", "조건 추가", "구간·정의역 제한", "매개변수 도입", "합성·역함수 결합", "도형 결합", "기타"}
COURSES = {"CM1", "CM2", "ALG", "M2", "PRST", "CALC", "GEO"}
REVIEW_HEADS = ("원문 결함: 조건 결손", "원문 결함: 조건 모순", "원문 결함: 요구값 결손", "원문 결함: 역함수 기호 소실 의심",
                "DB 정답 오류 의심:", "과목 오분류:", "DB 정답 미기입:")
PATS = {"stage_ref": r"\d\s*단계", "display_boxed": r"\$\$[^$]*\\boxed[^$]*\$\$", "bang_eq": r"!=",
        "frac_overline": r"\\d?frac\{\\overline", "big_paren": r"\\[bB]ig+[lrm]?\s*[()\[\]{}|]", "text_hangul": r"\\text\{[^}]*[가-힣]"}


def packet(name: str) -> dict[int, dict]:
    rows = json.loads((PK / f"{name}_packet.json").read_text(encoding="utf-8"))
    return {int(r["item_id"]): r for r in rows}


def split_prose_math(text: str) -> tuple[str, str]:
    no_disp = re.sub(r"\$\$.*?\$\$", "␣", text, flags=re.DOTALL)
    parts = no_disp.split("$")
    return "".join(parts[0::2]), "".join(parts[1::2])


def norm_answer(v) -> str:
    s = str(v if v is not None else "").strip().replace(" ", "").replace("$", "")
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    m = re.fullmatch(r"\\frac\{(-?\d+)\}\{(\d+)\}", s)
    return f"{m.group(1)}/{m.group(2)}" if m else s


def all_strings(o, path="") -> list[tuple[str, str]]:
    out = []
    if isinstance(o, str):
        out.append((path, o))
    elif isinstance(o, dict):
        for k, v in o.items():
            out += all_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += all_strings(v, f"{path}[{i}]")
    return out


def _graph_adj() -> dict[str, set[str]]:
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    adj: dict[str, set[str]] = defaultdict(set)
    for e in g["edges"]:
        a, b = (e["to"], e["from"]) if e["kind"] == "used_in" else (e["from"], e["to"])
        adj[a].add(b)
    return adj


def _reach(adj, src, dst) -> bool:
    seen, dq = {src}, deque([src])
    while dq:
        u = dq.popleft()
        if u == dst:
            return True
        for v in adj.get(u, ()):
            if v not in seen:
                seen.add(v)
                dq.append(v)
    return False


def check(rec: dict, pk: dict, adj) -> list[str]:
    e: list[str] = []
    iid = rec["item_id"]
    if rec.get("table") != "items":
        e.append("table")
    if rec.get("course") not in COURSES:
        e.append(f"course {rec.get('course')}")
    if not str(rec.get("problem_text") or "").strip():
        e.append("problem_text 비어 있음")
    if rec.get("answer_type") != pk["answer_type"]:
        e.append(f"answer_type {rec.get('answer_type')} != 패킷 {pk['answer_type']}")
    units = rec.get("units") or []
    valid_units = set(UNITS["course_codes"].get(rec.get("course"), {}))
    if not units or any(u not in valid_units for u in units):
        e.append(f"units {units} (허용 {sorted(valid_units)[:6]}…)")
    if not str(rec.get("verification") or "").strip():
        e.append("verification 없음")
    for k in ("difficulty", "calc_load", "reasoning_load"):
        v = rec.get(k)
        if not isinstance(v, int) or not 1 <= v <= 5:
            e.append(f"{k} 범위")
    steps = rec.get("solution_steps") or []
    if not 1 <= len(steps) <= 6:
        e.append(f"단계 수 {len(steps)}")
    body = "\n".join(str(s.get("text") or "") for s in steps)
    budget = max(600, len(pk.get("raw_text") or "") * 4)
    if len(body) > 1600 or len(body) > budget:
        e.append(f"길이 {len(body)} > {min(budget, 1600)}")
    fa = rec.get("final_answer")
    if fa != "" and "\\boxed" not in body:
        e.append("최종답 \\boxed 없음")
    if fa == "" and not rec.get("needs_review"):
        e.append("빈 final_answer 인데 needs_review 아님")
    nos = []
    for s in steps:
        if s.get("role") not in ROLES:
            e.append(f"step {s.get('step_no')} role")
        if not str(s.get("text") or "").strip():
            e.append(f"step {s.get('step_no')} 본문 없음")
        if "points" in s and rec.get("answer_type") != "서술형":
            e.append("객관식·단답형에 points")
        nos.append(int(s.get("step_no")))
    if nos != list(range(1, len(nos) + 1)):
        e.append(f"step_no 순서 {nos}")
    # 모든 문자열 필드 검사
    for path, t in all_strings(rec):
        for pat in BANNED:
            if pat in t:
                e.append(f"{path}: 금지 {pat}")
        prose, math = split_prose_math(t)
        uni = [c for c in UNICODE_MATH if c in prose]
        if re.search(r"\.decisions\[\d+\]\.name$", path):
            uni = []  # 판단 패밀리 사전 이름 원문('신호 → 선택')은 그대로 둔다(학생 화면 비노출)
        if uni:
            e.append(f"{path}: 산문 유니코드 {uni}")
        if t.count("$") % 2:
            e.append(f"{path}: $ 홀수")
        if re.findall(r"[가-힣]", math):
            e.append(f"{path}: 수식 안 한글 {re.findall(r'[가-힣]+', math)[:2]}")
        for w in THOUGHT_LEAK:
            if path == ".problem_text":
                break  # 문제 원문의 '그림과 같이' 등은 원문 그대로 둔다(해설교체 validate 는 해설 본문만 검사)
            if w in t:
                e.append(f"{path}: 사고 누설 '{w}'")
        for name, pat in PATS.items():
            if name in ("stage_ref", "display_boxed") and not path.startswith(".solution_steps"):
                continue  # 단계 번호 지칭·표시수식 boxed 금지는 학생용 해설 본문 규칙(웨이브마감 scan 범위)
            if re.search(pat, t):
                e.append(f"{path}: {name}")
    # 프로파일
    prof = rec.get("ontology_profile") or {}
    skills = prof.get("skills") or []
    mains = [s for s in skills if s.get("role") == "main"]
    auxs = [s for s in skills if s.get("role") == "aux"]
    if len(mains) != 1:
        e.append(f"main {len(mains)}")
    if len(auxs) > 2:
        e.append(f"aux {len(auxs)}")
    step_set = set(nos)
    for s in skills:
        fid = s.get("family_id")
        if fid not in SK:
            e.append(f"skill family_id {fid} 없음(새 노드 금지)")
        else:
            if s.get("name") != SK[fid]["name"]:
                e.append(f"skill name 불일치 {fid}: {s.get('name')}")
            if s.get("course_origin") != SK[fid]["course_origin"]:
                e.append(f"skill course_origin {fid}")
        if s.get("is_new"):
            e.append("is_new skill")
        if not s.get("step_nos") or any(int(n) not in step_set for n in s["step_nos"]):
            e.append(f"skill {fid} step_nos {s.get('step_nos')}")
    decs = prof.get("decisions") or []
    if len(decs) > 3:
        e.append("decisions > 3")
    for d in decs:
        if d.get("family") not in DE:
            e.append(f"decision family {d.get('family')} 없음")
        if d.get("cost") not in COSTS:
            e.append(f"decision cost {d.get('cost')}")
        if int(d.get("step_no") or 0) not in step_set:
            e.append(f"decision step_no {d.get('step_no')}")
        for k in ("trigger", "chosen", "alternative"):
            if not str(d.get(k) or "").strip():
                e.append(f"decision {k} 없음")
    for s in steps:
        n = int(s["step_no"])
        if s.get("role") == "decision" and not any(int(d.get("step_no") or 0) == n for d in decs):
            e.append(f"decision 단계 {n} 에 decisions 없음")
        if s.get("role") == "execute" and not any(n in [int(x) for x in sk.get("step_nos") or []] for sk in skills):
            e.append(f"execute 단계 {n} 이 skills.step_nos 에 없음")
    for c in prof.get("concepts") or []:
        if not c.get("name"):
            e.append("concept name")
        if any(int(n) not in step_set for n in c.get("step_nos") or []):
            e.append(f"concept {c.get('name')} step_nos")
    if not (prof.get("pattern") or {}).get("name"):
        e.append("pattern 없음")
    loads = prof.get("loads") or {}
    for k in ("novel_decision", "branching", "execution"):
        if loads.get(k) not in (1, 2, 3):
            e.append(f"loads.{k}")
    for t in prof.get("traps") or []:
        if t.get("cause") not in CAUSES:
            e.append(f"trap cause {t.get('cause')}")
        if rec.get("answer_type") == "객관식" and t.get("choice") not in (None, "①", "②", "③", "④", "⑤"):
            e.append(f"trap choice {t.get('choice')}")
        if t.get("choice") and t["choice"] == rec.get("final_answer"):
            e.append("trap 이 정답 선지")
    # v61_3
    v = rec.get("v61_3") or {}
    if len(v.get("invariants") or []) < 2:
        e.append("invariants < 2")
    ves = v.get("variable_elements") or []
    if len(ves) < 2:
        e.append("variable_elements < 2")
    for ve in ves:
        if ve.get("role") not in VE_ROLES or not isinstance(ve.get("answer_sensitive"), bool):
            e.append(f"variable_element {ve.get('name')}")
    for es in v.get("escalations") or []:
        if es.get("axis") not in AXES or es.get("keeps_course") is not True:
            e.append(f"escalation {es.get('axis')}")
    rec_hooks = v.get("recovery") or []
    if not rec_hooks:
        e.append("recovery 없음")
    main_code = mains[0]["family_id"] if mains else None
    if main_code and not any(h.get("node") == main_code for h in rec_hooks):
        e.append("recovery 에 main 노드 없음")
    for h in rec_hooks:
        node = h.get("node") or ""
        if not (node in SK or node in DE or node.startswith("concept:")):
            e.append(f"recovery node {node}")
        if not str(h.get("prescription") or "").strip():
            e.append("recovery prescription 없음")
        if h.get("descend_to") not in COURSES:
            e.append(f"recovery descend_to {h.get('descend_to')}")
        for pre in h.get("prerequisite") or []:
            if not (pre in SK or pre in DE or pre.startswith("concept:")):
                e.append(f"prerequisite {pre} 없음")
            elif pre == node:
                e.append("자기 선수")
            elif node in SK and pre in SK:
                if _reach(adj, pre, node):
                    e.append(f"선수 순환: {pre} 에서 {node} 로 기존 경로 있음({node} 의 선수로 {pre} 금지)")
                sc, pc = SK[node].get("course_origin"), SK[pre].get("course_origin")
                order = ["CM1", "CM2", "ALG", "M2", "CALC"]
                if sc in order and pc in order and order.index(pc) > order.index(sc):
                    e.append(f"과목 순서 역행 선수 {node}({sc}) 의 선수 {pre}({pc})")
    if not v.get("bottleneck_hypotheses"):
        e.append("bottleneck 없음")
    for bh in v.get("bottleneck_hypotheses") or []:
        if int(bh.get("step_no") or 0) not in step_set:
            e.append("bottleneck step_no")
        n = bh.get("node") or ""
        if not (n in SK or n in DE or n.startswith("concept:")):
            e.append(f"bottleneck node {n}")
    # 정답 대조
    nr = bool(rec.get("needs_review"))
    note = str(rec.get("assessment_note") or "")
    if nr and not note.startswith(REVIEW_HEADS):
        e.append("needs_review 사유 머리말")
    if not nr:
        a, b = norm_answer(pk["answer"]), norm_answer(fa)
        if a != b:
            e.append(f"정답 불일치 패킷 {a!r} vs {b!r} (needs_review 없이)")
    if not isinstance(rec.get("self_confidence"), (int, float)):
        e.append("self_confidence")
    return e


def emit(bucket: str, records: list[dict]) -> int:
    name = bucket.split("_")[1]
    pk = packet(f"W38_{name}")
    adj = _graph_adj()
    out = D / f"{bucket}.jsonl"
    errs = {}
    rows = []
    for r in records:
        iid = int(r["item_id"])
        if iid not in pk:
            errs[iid] = ["패킷에 없는 문항"]
            continue
        r.setdefault("table", "items")
        r.setdefault("alt_solutions", [])
        r.setdefault("problem_text", pk[iid]["raw_text"])
        r.setdefault("answer_type", pk[iid]["answer_type"])
        e = check(r, pk[iid], adj)
        if e:
            errs[iid] = e
        rows.append(r)
    missing = sorted(set(pk) - {int(r["item_id"]) for r in rows})
    if missing:
        errs["missing"] = missing
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    summary = {"bucket": bucket, "records": len(rows), "packet": len(pk), "needs_review": [r["item_id"] for r in rows if r.get("needs_review")],
               "errors": errs, "out": out.name}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 1 if errs else 0


def S(fid: str, role: str, step_nos: list[int], note: str | None = None) -> dict:
    f = SK[fid]
    d = {"name": f["name"], "family_id": fid, "role": role, "course_origin": f["course_origin"], "step_nos": step_nos, "is_new": False}
    if note:
        d["note"] = note
    return d


def Dc(fam: str, trigger: str, chosen: str, alternative: str, cost: str, step_no: int) -> dict:
    return {"family": fam, "name": DE[fam]["name"], "trigger": trigger, "chosen": chosen, "alternative": alternative,
            "cost": cost, "step_no": step_no, "is_new": False}


def C(name: str, step_nos: list[int]) -> dict:
    return {"name": name, "step_nos": step_nos, "is_new": False}
