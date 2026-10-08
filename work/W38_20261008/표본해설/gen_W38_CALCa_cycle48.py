# -*- coding: utf-8 -*-
"""W38 CALCa (cycle48) 생성기 — 패킷 W38_CALCa 1문항. 독립 검산은 verify_W38_CALCa_cycle48.py(= verify_W38_misc_cycle48.py).
실행: python -X utf8 gen_W38_CALCa_cycle48.py → W38_CALCa_cycle48.jsonl"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _w38_common import C, Dc, S, emit  # noqa: E402

R = [{
    "item_id": 17507, "course": "CALC", "unit": "수열의 극한 - 수열의 극한", "units": ["CALC-LIM"],
    "problem_text": r"수열 $\left\{ a_{n} \right\}$에 대하여 $\lim_{n \to \infty} \dfrac{a_{n}+2}{2}=6$일 때, $\lim_{n \to \infty} \dfrac{n a_{n}+1}{a_{n}+2n}$의 값은? [3점] ① $1$ ② $2$ ③ $3$ ④ $4$ ⑤ $5$",
    "final_answer": "⑤", "difficulty": 2, "answer_type": "객관식", "calc_load": 1, "reasoning_load": 2,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"주어진 극한에서 **극한의 성질**로 $\lim_{n \to \infty} a_{n}=2\times6-2=10$이다.",
         "common_error": r"$\lim_{n \to \infty} a_{n}=6$으로 읽는 실수"},
        {"step_no": 2, "role": "execute",
         "text": r"분모·분자가 모두 한없이 커지는 꼴이므로 $n$으로 나눈다. $$\lim_{n \to \infty}\frac{na_{n}+1}{a_{n}+2n}=\lim_{n \to \infty}\frac{a_{n}+\dfrac{1}{n}}{\dfrac{a_{n}}{n}+2}=\frac{10+0}{0+2}=5$$ 이므로 답은 $\boxed{⑤}$ 이다.",
         "common_error": r"$\dfrac{a_{n}}{n}$이 $0$으로 수렴함을 쓰지 않고 $a_{n}$을 상수처럼 남겨 두는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("수열의 극한의 성질(합·차·실수배)", [1]), C("무한대 비의 극한(최고차항으로 나누기)", [2])],
        "decisions": [Dc("D-25", "분모·분자가 모두 발산하는 비의 꼴", "분모·분자를 $n$으로 나눠 수렴하는 항으로 바꿈", "$a_{n}=10$을 대입해 유한한 $n$에서 계산", "오답", 2)],
        "skills": [S("S-CALC-01", "main", [2]), S("S-CALC-22", "aux", [1], "주어진 극한식에서 수열 자체의 극한을 역산")],
        "strategy": None,
        "pattern": {"name": "주어진 수열의 극한을 역산해 발산하는 비의 극한 구하기", "is_new": False},
        "loads": {"novel_decision": 1, "branching": 1, "execution": 1},
        "traps": [{"choice": "③", "step_no": None, "cause": "misread", "note": r"$\lim a_{n}=6$으로 읽고 $6/2=3$"},
                  {"choice": "②", "step_no": None, "cause": "formula_confusion", "note": r"$n$으로 나누지 않고 분모의 $2n$만 남겨 $2$로 둔 값"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 수열의 일차변환의 극한값", "요구값: 수열과 $n$이 섞인 분수식의 극한", "핵심 판단 D-25: 최고차항으로 나누기", "main 스킬 S-CALC-01"],
        "variable_elements": [{"name": "주어진 극한의 일차변환 계수", "role": "계수", "range_hint": "$a_{n}$의 극한이 정수가 되게", "answer_sensitive": True},
                              {"name": "분수식의 $n$ 계수", "role": "계수", "range_hint": "분모·분자가 같은 차수", "answer_sensitive": True},
                              {"name": "상수항", "role": "상수", "range_hint": "극한에 영향 없음", "answer_sensitive": False}],
        "escalations": [{"axis": "횟수·차수 일반화", "description": "$\\lim (a_{n}-2n)=3$처럼 발산하는 수열의 조건으로 바꿔 $a_{n}=2n+b_{n}$ 치환(S-M2-21)을 요구한다", "keeps_course": True}],
        "recovery": [{"node": "S-CALC-01", "prerequisite": ["concept:무한대 비의 극한(최고차항으로 나누기)"], "prescription": "$\\lim_{n \\to \\infty}\\dfrac{3n+1}{n+2}$ 처럼 $n$으로 나누어 끝나는 원자 문항", "descend_to": "CALC"},
                     {"node": "D-25", "prerequisite": ["S-CALC-01"], "prescription": "발산 비의 꼴에서 대입과 나누기를 비교하게 하는 짝 문항", "descend_to": "CALC"}],
        "bottleneck_hypotheses": [{"step_no": 2, "node": "S-CALC-01", "why": "$a_{n}$이 상수로 수렴한다는 사실과 $n$으로 나눈 뒤의 극한을 함께 다루지 못한다", "evidence": "trap ②"}],
    },
    "diagnoses_if_correct": "주어진 극한을 역산하고 발산 비의 극한을 최고차항으로 나누어 구하는 수행을 갖춤",
    "diagnoses_if_wrong": "극한 역산 / 나누기 처리",
    "assessment_note": "수열의 극한 기본 성질 문항이다.",
    "self_confidence": 0.99, "needs_review": False,
    "verification": "sympy 로 조건을 만족하는 두 수열 a_n=10+1/n, 10-3/sqrt(n) 에 대해 식의 극한이 모두 5, 5지선다 정답 유일",
}]

if __name__ == "__main__":
    raise SystemExit(emit("W38_CALCa_cycle48", R))
