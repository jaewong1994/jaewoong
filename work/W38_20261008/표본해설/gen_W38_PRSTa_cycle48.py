# -*- coding: utf-8 -*-
"""W38 PRSTa (cycle48) 생성기 — 패킷 W38_PRSTa 3문항. 직접 풀이 + verify_W38_PRSTa_cycle48.py 독립 검산(먼저 실행) 결과만 인용.
8744·8750 은 패킷 과목 PRST 이나 내용은 2022 개정 공통수학1 '경우의 수' 범위(정본 분류층 bank_item_class 도 CM1) → 과목 오분류로 needs_review.
실행: python -X utf8 gen_W38_PRSTa_cycle48.py → W38_PRSTa_cycle48.jsonl"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _w38_common import C, Dc, S, emit  # noqa: E402

R = []

# ---------------------------------------------------------------- 8744 0 이 이웃하지 않는 아홉 자리 자연수 (⑤) — 과목 오분류(CM1)
R.append({
    "item_id": 8744, "course": "CM1", "unit": "경우의 수 - 조합", "units": ["CM1-COUNT"],
    "final_answer": "⑤", "difficulty": 3, "answer_type": "객관식", "calc_load": 1, "reasoning_load": 3,
    "solution_steps": [
        {"step_no": 1, "role": "decision",
         "text": r"$0$끼리 이웃하지 않아야 하므로 $1$ 여섯 개를 먼저 나열하고 그 **사이와 양 끝**에 $0$을 넣을 자리를 고른다.",
         "common_error": r"전체 나열에서 $0$이 이웃하는 경우를 빼려다 이웃하는 쌍의 중복을 놓치는 실수"},
        {"step_no": 2, "role": "execute",
         "text": r"$1$ 여섯 개 사이와 양 끝의 $7$자리 중 맨 앞자리는 아홉 자리 자연수가 되려면 쓸 수 없으므로, 나머지 $6$자리에서 $0$이 들어갈 $3$자리를 고르면 된다. $$_{6}\mathrm{C}_{3}=20$$ 이므로 답은 $\boxed{⑤}$ 이다.",
         "common_error": r"맨 앞자리를 빼지 않고 $_{7}\mathrm{C}_{3}=35$로 두는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("조합", [2]), C("이웃하지 않는 배열(사이 자리 배정)", [1, 2])],
        "decisions": [Dc("D-29", "같은 숫자 $0$이 이웃하면 안 된다는 조건", "$1$을 먼저 나열하고 사이·끝 자리에 $0$을 배정", "전체에서 $0$이 이웃하는 경우를 빼는 여사건", "계산폭발", 1)],
        "skills": [S("S-CM1-13", "main", [2], "사이 자리에서 조합으로 자리 선택")],
        "strategy": None,
        "pattern": {"name": "사이 자리 배정으로 이웃하지 않는 나열의 수 구하기", "is_new": False},
        "loads": {"novel_decision": 2, "branching": 1, "execution": 1},
        "traps": [{"choice": "①", "step_no": None, "cause": "misread", "note": r"$0$이 모두 이웃하지 않는 조건 대신 다른 조건으로 센 값"},
                  {"choice": "②", "step_no": None, "cause": "condition_missing", "note": r"맨 앞자리 $0$을 뺀 $35-15=20$ 대신 $35-21=14$처럼 빼는 양을 잘못 센 값"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 같은 숫자가 여럿 있는 숫자 묶음과 특정 숫자가 이웃하지 않는 조건, 맨 앞자리 제한", "요구값: 나열의 수", "핵심 판단 D-29: 사이 자리 배정", "main 스킬 S-CM1-13"],
        "variable_elements": [{"name": "$0$의 개수", "role": "조건값", "range_hint": "$1$의 개수보다 $1$ 이상 적게", "answer_sensitive": True},
                              {"name": "$1$의 개수", "role": "조건값", "range_hint": "자연수, 자리 수 합이 10 이하", "answer_sensitive": True},
                              {"name": "맨 앞자리 제한의 유무", "role": "지표", "range_hint": "자연수 조건이면 제한 있음", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "'$0$이 정확히 두 개만 이웃한다'로 바꿔 덩어리 묶기(D-44)와 사이 자리 배정을 함께 쓰게 한다", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-13", "prerequisite": ["concept:조합"], "prescription": "서로 다른 문자 $4$개를 나열한 뒤 사이·양 끝 $5$자리 중 $2$자리를 고르는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-29", "prerequisite": ["S-CM1-13"], "prescription": "같은 조건을 여사건과 사이 자리 배정으로 각각 세게 해 비용을 비교하는 짝 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 2, "node": "S-CM1-13", "why": "맨 앞자리 제한을 자리 선택에 반영하지 못한다", "evidence": "common_error 2단계"}],
    },
    "diagnoses_if_correct": "이웃 금지 조건을 사이 자리 배정으로 바꾸고 선두 제한을 반영해 조합으로 세는 능력을 갖춤",
    "diagnoses_if_wrong": "분류 기준 선택 / 선두 제한 반영",
    "assessment_note": "과목 오분류: 패킷(items.course_norm) PRST 이나 풀이는 조합(사이 자리 배정)만으로 완결되어 2022 개정 공통수학1 '경우의 수' 범위. 정본 분류층(bank_item_class)도 CM1 이므로 items.course_norm 을 CM1 로 바꾸는 것이 맞다. 2019 고2 가형 출제 당시에는 확률과 통계 범위였다.",
    "self_confidence": 0.98, "needs_review": True,
    "verification": "000111111 의 서로 다른 나열 전수(84가지)에서 첫 자리 1·'00' 미포함인 것 20개, 5지선다 정답 유일",
})

# ---------------------------------------------------------------- 8750 격자에서 두 수 선택 (④) — 과목 오분류(CM1)
R.append({
    "item_id": 8750, "course": "CM1", "unit": "경우의 수 - 조합", "units": ["CM1-COUNT"],
    "problem_text": r"$9$개의 칸으로 나누어진 정사각형의 각 칸에 $1$부터 $9$까지의 자연수가 적혀 있다. (표: 첫째 가로줄 $1$, $2$, $3$ / 둘째 가로줄 $4$, $5$, $6$ / 셋째 가로줄 $7$, $8$, $9$) 이 $9$개의 숫자 중 다음 조건을 만족시키도록 $2$개의 숫자를 선택하려고 한다. (가) 선택한 $2$개의 숫자는 서로 다른 가로줄에 있다. (나) 선택한 $2$개의 숫자는 서로 다른 세로줄에 있다. 예를 들어, 숫자 $1$과 $5$를 선택하는 것은 조건을 만족시키지만, 숫자 $3$과 $9$를 선택하는 것은 조건을 만족시키지 않는다. 조건을 만족시키도록 $2$개의 숫자를 선택하는 경우의 수는? [4점] ① $9$ ② $12$ ③ $15$ ④ $18$ ⑤ $21$",
    "final_answer": "④", "difficulty": 2, "answer_type": "객관식", "calc_load": 1, "reasoning_load": 2,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"첫 번째 숫자를 고르면 같은 가로줄과 같은 세로줄의 칸을 뺀 나머지에서 두 번째 숫자를 골라야 한다. 첫 숫자 $9$가지에 대해 가로줄 $3$칸과 세로줄 $3$칸이 그 칸 하나를 공유하므로 제외되는 칸은 $5$개이고, 두 번째 숫자는 $4$가지이다. **곱의 법칙**으로 순서가 있는 선택은 $9\times4=36$가지이다.",
         "common_error": r"같은 가로줄·세로줄 칸을 $6$개로 세어 두 번째 숫자를 $3$가지로 두는 실수"},
        {"step_no": 2, "role": "decision",
         "text": r"두 숫자의 선택에는 순서가 없으므로 $2$로 나눈다. $$\frac{36}{2}=18$$ 이므로 답은 $\boxed{④}$ 이다.",
         "common_error": r"순서 없는 선택임을 놓쳐 $36$을 그대로 답하는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("곱의 법칙", [1]), C("조합(순서 없는 선택)", [2])],
        "decisions": [Dc("D-35", "'$2$개의 숫자를 선택'이라는 순서 없는 고르기", "순서 있는 선택을 세고 $2$로 나눔", "순서쌍을 그대로 답함", "오답", 2)],
        "skills": [S("S-CM1-13", "main", [1])],
        "strategy": None,
        "pattern": {"name": "곱의 법칙과 순서 보정으로 조건을 만족하는 선택의 수 구하기", "is_new": False},
        "loads": {"novel_decision": 1, "branching": 1, "execution": 1},
        "traps": [{"choice": "⑤", "step_no": None, "cause": "calculation", "note": r"전체 $_{9}\mathrm{C}_{2}=36$에서 조건을 어기는 쌍을 $15$로 잘못 세어 $21$"},
                  {"choice": "①", "step_no": None, "cause": "concept_confusion", "note": r"가로줄 $3$가지와 세로줄 $3$가지를 곱한 $9$"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 정사각 격자의 칸과 서로 다른 가로줄·세로줄 조건", "요구값: 두 칸을 고르는 경우의 수", "핵심 판단 D-35: 순서 없는 선택의 보정", "main 스킬 S-CM1-13"],
        "variable_elements": [{"name": "격자 크기", "role": "소재", "range_hint": "$3\\times3$, $4\\times4$", "answer_sensitive": True},
                              {"name": "고르는 개수", "role": "조건값", "range_hint": "$2$ 또는 $3$(순열 보정이 바뀜)", "answer_sensitive": True},
                              {"name": "조건 종류(가로·세로·대각)", "role": "지표", "range_hint": "줄 조건의 조합", "answer_sensitive": True}],
        "escalations": [{"axis": "횟수·차수 일반화", "description": "$3$개의 숫자를 서로 다른 가로줄·세로줄에서 고르게 바꿔 $3!$ 보정과 순열 구조(S-CM1-13 심화)를 요구한다", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-13", "prerequisite": ["concept:곱의 법칙"], "prescription": "$2\\times2$ 격자에서 같은 줄에 있지 않은 두 칸을 고르는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-35", "prerequisite": ["S-CM1-13"], "prescription": "순서 있는 고르기와 순서 없는 고르기의 수를 같은 상황에서 비교하는 짝 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 2, "node": "D-35", "why": "순서 보정을 빠뜨려 두 배로 센다", "evidence": "common_error 2단계"}],
    },
    "diagnoses_if_correct": "곱의 법칙으로 순서 있는 선택을 센 뒤 순서 없는 선택으로 보정하는 수행을 갖춤",
    "diagnoses_if_wrong": "제외 칸 세기 / 순서 보정",
    "assessment_note": "과목 오분류: 패킷(items.course_norm) PRST 이나 곱의 법칙과 조합 보정만으로 완결되어 2022 개정 공통수학1 '경우의 수' 범위. 정본 분류층(bank_item_class)도 CM1 이므로 items.course_norm 을 CM1 로 바꾸는 것이 맞다. 원문의 격자 그림은 숫자 배열이 본문에 적혀 있어 글로 완결된다.",
    "self_confidence": 0.98, "needs_review": True,
    "verification": "1~9 격자 좌표로 _9C_2=36쌍 전수에서 행·열이 모두 다른 쌍 18개, 5지선다 정답 유일",
})

# ---------------------------------------------------------------- 17805 이항정리 x^2 계수 (①)
R.append({
    "item_id": 17805, "course": "PRST", "unit": "경우의 수 - 이항정리", "units": ["PRST-COUNT"],
    "final_answer": "①", "difficulty": 2, "answer_type": "객관식", "calc_load": 2, "reasoning_load": 2,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"$x^{2}$항은 두 전개식에서 차수의 합이 $2$가 되는 항끼리의 곱에서만 나온다. **이항정리**의 일반항으로 $(x-1)^{6}$의 상수항·$x$항·$x^{2}$항은 각각 $1$, $-6$, $15$이고 $(2x+1)^{7}$의 것은 $1$, $14$, $84$이다. $$1\times84+(-6)\times14+15\times1=15$$ 이므로 답은 $\boxed{①}$ 이다.",
         "common_error": r"$(x-1)^{6}$의 $x$항 계수의 부호를 $+6$으로 두어 $183$ 계열의 값을 얻는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("이항정리의 일반항", [1]), C("곱의 전개에서 특정 차수 항의 계수", [1])],
        "decisions": [Dc("D-03", "두 전개식의 곱에서 한 차수의 항을 구해야 함", "차수의 합이 $2$가 되는 쌍 $(0,2)$, $(1,1)$, $(2,0)$으로 나눠 합산", "전체를 전개", "계산폭발", 1)],
        "skills": [S("S-PRST-05", "main", [1])],
        "strategy": None,
        "pattern": {"name": "이항정리의 일반항으로 두 전개식의 곱에서 특정 항의 계수 구하기", "is_new": False},
        "loads": {"novel_decision": 1, "branching": 2, "execution": 2},
        "traps": [{"choice": "③", "step_no": None, "cause": "sign_error", "note": r"$-6$의 부호를 놓치면 $84+84+15$ 계열로 커지므로 선지 안에서 가까운 값을 고른 경우"},
                  {"choice": "②", "step_no": None, "cause": "case_missing", "note": r"$(2,0)$ 쌍 $15$를 빠뜨리거나 $(0,2)$만 세어 생기는 값"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 두 이항식의 거듭제곱의 곱", "요구값: 특정 차수 항의 계수", "핵심 판단 D-03: 차수 합으로 분할", "main 스킬 S-PRST-05"],
        "variable_elements": [{"name": "두 이항식의 지수", "role": "계수", "range_hint": "자연수, 합이 15 이하", "answer_sensitive": True},
                              {"name": "묻는 차수", "role": "지표", "range_hint": "$x^{2}$, $x^{3}$ 등 작은 차수", "answer_sensitive": True},
                              {"name": "이항식의 계수·부호", "role": "계수", "range_hint": "작은 정수, 부호 혼합", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "$(x+a)^{n}$의 미지수 $a$를 두고 $x^{2}$ 계수가 $0$이 되는 조건을 묻게 해 역방향 계산을 요구한다", "keeps_course": True}],
        "recovery": [{"node": "S-PRST-05", "prerequisite": ["concept:이항정리의 일반항"], "prescription": "$(2x+1)^{7}$ 전개식의 $x^{2}$ 계수 하나만 묻는 원자 문항", "descend_to": "PRST"},
                     {"node": "D-03", "prerequisite": ["S-PRST-05"], "prescription": "두 전개식의 곱에서 $x$항 계수를 차수 쌍 두 개로 나눠 구하는 짧은 문항", "descend_to": "PRST"}],
        "bottleneck_hypotheses": [{"step_no": 1, "node": "S-PRST-05", "why": "음수 부호가 든 이항식의 일반항 부호를 놓친다", "evidence": "common_error 1단계"}],
    },
    "diagnoses_if_correct": "이항정리의 일반항을 두 전개식에 적용하고 차수 쌍으로 나눠 합산하는 능력을 갖춤",
    "diagnoses_if_wrong": "부호 처리 / 차수 쌍 누락",
    "assessment_note": "차수 쌍 세 개의 합으로 끝나는 표준 문항이다.",
    "self_confidence": 0.99, "needs_review": False,
    "verification": "sympy 로 (x-1)^6 (2x+1)^7 전체 전개 후 x^2 계수 15, 5지선다 정답 유일",
})

if __name__ == "__main__":
    raise SystemExit(emit("W38_PRSTa_cycle48", R))
