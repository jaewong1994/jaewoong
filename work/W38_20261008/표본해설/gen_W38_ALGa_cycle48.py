# -*- coding: utf-8 -*-
"""W38 ALGa (cycle48) 생성기 — 패킷 W38_ALGa 1문항(10722, 원문 결함: 조건 결손 — f 미정의). needs_review.
실행: python -X utf8 gen_W38_ALGa_cycle48.py → W38_ALGa_cycle48.jsonl"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _w38_common import C, S, emit  # noqa: E402

R = [{
    "item_id": 10722, "course": "ALG", "unit": "지수와 로그 - 지수", "units": ["ALG-EXP"],
    "problem_text": r"이차정사각행렬 $M$의 $(i,\,j)$ 성분 $m_{ij}$가 $m_{ij}=f(i)+f(j)$ ($i=j$), $m_{ij}=f(i)\times f(j)$ ($i \ne j$)일 때 행렬 $M$의 모든 성분의 곱이 $2^{8}$이다. 이때 상수 $a$의 값은? [3점] ① $2^{\frac{1}{3}}$ ② $2^{\frac{2}{3}}$ ③ $2$ ④ $2^{\frac{4}{3}}$ ⑤ $2^{\frac{5}{3}}$",
    "final_answer": "", "difficulty": 3, "answer_type": "객관식", "calc_load": 2, "reasoning_load": 2,
    "solution_steps": [
        {"step_no": 1, "role": "setup",
         "text": r"함수 $f$의 정의가 본문에 없어 성분을 나타낼 수 없다.",
         "common_error": r"정의 없이 $f$를 임의로 가정하는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("지수법칙", [1])],
        "decisions": [],
        "skills": [S("S-ALG-32", "main", [1], "원문 결손으로 추정 태그")],
        "strategy": None,
        "pattern": {"name": "행렬 성분의 곱 조건을 지수법칙으로 정리해 밑 구하기", "is_new": False},
        "loads": {"novel_decision": 1, "branching": 1, "execution": 2},
        "traps": [],
    },
    "v61_3": {
        "invariants": ["주어진 것: 성분이 함수 $f$로 정의된 이차정사각행렬과 성분의 곱 조건", "요구값: 상수 $a$", "main 스킬 S-ALG-32"],
        "variable_elements": [{"name": "함수 $f$ 의 정의", "role": "함수형", "range_hint": "원본 대조로 복원", "answer_sensitive": True},
                              {"name": "성분의 곱의 값", "role": "조건값", "range_hint": "$2$의 거듭제곱", "answer_sensitive": True}],
        "escalations": [],
        "recovery": [{"node": "S-ALG-32", "prerequisite": ["concept:지수법칙"], "prescription": "원문 복원 후 작성", "descend_to": "ALG"}],
        "bottleneck_hypotheses": [{"step_no": 1, "node": "S-ALG-32", "why": "원문 복원 전에는 판정 불가", "evidence": "없음"}],
    },
    "diagnoses_if_correct": "원문 복원 후 판정",
    "diagnoses_if_wrong": "원문 복원 후 판정",
    "assessment_note": r"원문 결함: 조건 결손 — 상수 $a$가 함수 $f$에만 들어 있는데 $f$의 정의가 본문에 없다(원문 첫 문장 앞의 조건 소실). 원문의 느낌표·등호로 적힌 부등 조건은 $i \ne j$ 로 읽는다(HWP 변환 잔재). 참고로 $f(x)=a^{x}$이면 성분의 곱 $4a^{9}=2^{8}$에서 $a=2^{\frac{2}{3}}$으로 저장 정답 ②와 맞지만, 결손 조건을 채워 풀지 않는다. 또한 행렬 성분 정의 자체는 2022 개정 공통수학1 범위이므로 복원 후 과목 재검토 필요. 표시 통과 상태이나 풀이 불가. 원본 대조 필요.",
    "self_confidence": 0.3, "needs_review": True,
    "verification": "검산 생략(원문 결손)",
}]

if __name__ == "__main__":
    raise SystemExit(emit("W38_ALGa_cycle48", R))
