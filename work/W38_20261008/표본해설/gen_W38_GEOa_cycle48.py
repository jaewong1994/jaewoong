# -*- coding: utf-8 -*-
"""W38 GEOa (cycle48) 생성기 — 패킷 W38_GEOa 1문항. 독립 검산은 verify_W38_GEOa_cycle48.py(= verify_W38_misc_cycle48.py).
실행: python -X utf8 gen_W38_GEOa_cycle48.py → W38_GEOa_cycle48.jsonl"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _w38_common import C, S, emit  # noqa: E402

R = [{
    "item_id": 18351, "course": "GEO", "unit": "이차곡선 - 포물선", "units": ["GEO-CONIC"],
    "problem_text": r"포물선 $y^{2}=8x$의 초점의 좌표가 $(p,\,0)$일 때, $p$의 값은? [2점] ① $1$ ② $2$ ③ $3$ ④ $4$ ⑤ $5$",
    "final_answer": "②", "difficulty": 1, "answer_type": "객관식", "calc_load": 1, "reasoning_load": 1,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"포물선 $y^{2}=4px$의 초점은 $(p,\,0)$, 준선은 $x=-p$이다. $y^{2}=8x=4\cdot2\cdot x$이므로 **초점**은 $(2,\,0)$이고 $p=2$이다. 따라서 답은 $\boxed{②}$ 이다.",
         "common_error": r"$y^{2}=8x$에서 $p=8$ 또는 $p=4$로 읽는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("포물선의 방정식과 초점·준선", [1])],
        "decisions": [],
        "skills": [S("S-GEO-04", "main", [1], "표준형 $y^{2}=4px$ 의 계수에서 초점 읽기")],
        "strategy": None,
        "pattern": {"name": "포물선의 표준형에서 초점의 좌표 구하기", "is_new": False},
        "loads": {"novel_decision": 1, "branching": 1, "execution": 1},
        "traps": [{"choice": "④", "step_no": None, "cause": "formula_confusion", "note": r"$y^{2}=4px$의 $4p$를 $2p$로 혼동해 $p=4$"},
                  {"choice": "①", "step_no": None, "cause": "formula_confusion", "note": r"$p=\dfrac{8}{8}$ 계열의 혼동"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 포물선의 표준형", "요구값: 초점의 좌표", "main 스킬 S-GEO-04", "답의 형식: 자연수"],
        "variable_elements": [{"name": "표준형의 계수", "role": "계수", "range_hint": "$4$의 배수", "answer_sensitive": True},
                              {"name": "묻는 요소(초점·준선·꼭짓점)", "role": "지표", "range_hint": "셋 중 하나", "answer_sensitive": True},
                              {"name": "축의 방향($x$축·$y$축)", "role": "함수형", "range_hint": "$y^{2}=4px$ 또는 $x^{2}=4py$", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "평행이동한 포물선 $(y-1)^{2}=8(x+2)$의 초점을 묻게 해 이동량 처리(S-CM2-17 연계)를 더한다", "keeps_course": True}],
        "recovery": [{"node": "S-GEO-04", "prerequisite": ["concept:포물선의 방정식과 초점·준선"], "prescription": "$y^{2}=4px$ 꼴에서 초점과 준선을 읽는 원자 문항", "descend_to": "GEO"}],
        "bottleneck_hypotheses": [{"step_no": 1, "node": "S-GEO-04", "why": "표준형의 $4p$ 를 계수 자체로 혼동한다", "evidence": "trap ④"}],
    },
    "diagnoses_if_correct": "포물선의 표준형에서 초점을 읽는 기본 수행을 갖춤",
    "diagnoses_if_wrong": "표준형 계수 해석",
    "assessment_note": "정의 대입 한 줄 문항이다.",
    "self_confidence": 0.99, "needs_review": False,
    "verification": "곡선 위의 점 (2,4) 에서 초점 (P,0) 까지의 거리와 준선 x=-P 까지의 거리가 같다는 정의를 sympy 로 풀어 P=2, 5지선다 정답 유일",
}]

if __name__ == "__main__":
    raise SystemExit(emit("W38_GEOa_cycle48", R))
