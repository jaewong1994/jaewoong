# -*- coding: utf-8 -*-
"""W38 CM1b (cycle48) 생성기 — 패킷 W38_CM1b 9문항. 직접 풀이 + verify_W38_CM1b_cycle48.py 독립 검산(먼저 실행) 결과만 인용.
실행: python -X utf8 gen_W38_CM1b_cycle48.py → W38_CM1b_cycle48.jsonl"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _w38_common import C, Dc, S, emit  # noqa: E402

R = []


def missing(item_id, unit, units, main, main_note, concept, pattern, note, diff=3, cl=2, rl=3, atype="객관식", step_text="", pre=None):
    return {
        "item_id": item_id, "course": "CM1", "unit": unit, "units": units,
        "final_answer": "", "difficulty": diff, "answer_type": atype, "calc_load": cl, "reasoning_load": rl,
        "solution_steps": [{"step_no": 1, "role": "setup", "text": step_text, "common_error": "정의되지 않은 함수를 임의로 가정하는 실수"}],
        "ontology_profile": {"concepts": [C(concept, [1])], "decisions": [], "skills": [S(main, "main", [1], main_note)], "strategy": None,
                             "pattern": {"name": pattern, "is_new": False}, "loads": {"novel_decision": 1, "branching": 1, "execution": 2}, "traps": []},
        "v61_3": {"invariants": ["주어진 것: 본문에서 소실된 함수·점의 정의(그림)", "요구값: 원문 복원 후 확정", f"main 스킬 {main}"],
                  "variable_elements": [{"name": "소실된 정의", "role": "함수형", "range_hint": "원본 대조로 복원", "answer_sensitive": True},
                                        {"name": "묻는 양", "role": "지표", "range_hint": "원문대로", "answer_sensitive": True}],
                  "escalations": [],
                  "recovery": [{"node": main, "prerequisite": pre or [f"concept:{concept}"], "prescription": "원문 복원 후 작성", "descend_to": "CM1"}],
                  "bottleneck_hypotheses": [{"step_no": 1, "node": main, "why": "원문 복원 전에는 판정 불가", "evidence": "없음"}]},
        "diagnoses_if_correct": "원문 복원 후 판정", "diagnoses_if_wrong": "원문 복원 후 판정",
        "assessment_note": note, "self_confidence": 0.3, "needs_review": True, "verification": "검산 생략(원문 결손)",
    }


# ---------------------------------------------------------------- 11253 결손
R.append(missing(11253, "방정식과 부등식 - 이차부등식", ["CM1-EQ"], "S-CM1-31", "원문 결손으로 추정 태그", "이차부등식과 이차함수의 그래프",
                 "그래프와 직선의 위치 관계로 부등식의 정수해 개수 조건 풀기",
                 r"원문 결함: 조건 결손 — $f(x)$, 직선 $l$, 상수 $p$의 정의가 본문에 없다(첫 문장 '직선 $l$의 방정식을 $y=g(x)$라 하자' 앞의 그림·조건 소실). 선지 ①의 '$32#$' 잔재도 있음. 표시 통과 상태이나 풀이 불가. 원본 대조 필요.",
                 step_text=r"이차함수 $f(x)$와 직선 $l$, 상수 $p$의 정의가 본문에 없어 부등식을 세울 수 없다.", pre=["S-CM1-22", "concept:이차부등식과 이차함수의 그래프"]))

# ---------------------------------------------------------------- 11941 삼차방정식 허근 (②)
R.append({
    "item_id": 11941, "course": "CM1", "unit": "방정식과 부등식 - 삼차방정식", "units": ["CM1-EQ"],
    "final_answer": "②", "difficulty": 3, "answer_type": "객관식", "calc_load": 3, "reasoning_load": 3,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"계수에 $a$가 섞여 있어도 $x=1$을 대입하면 $1-(2a+1)+(a+1)^{2}-(a^{2}+1)=0$이므로 **인수정리**로 $x-1$을 인수로 갖는다. 조립제법으로 나누면 $$x^{3}-(2a+1)x^{2}+(a+1)^{2}x-(a^{2}+1)=(x-1)\left(x^{2}-2ax+a^{2}+1\right)$$ 이다.",
         "common_error": r"$a$가 든 계수를 보고 인수를 찾지 못해 전개 상태에서 막히는 실수"},
        {"step_no": 2, "role": "execute",
         "text": r"이차 인수 $x^{2}-2ax+a^{2}+1$의 판별식은 $\dfrac{D}{4}=a^{2}-(a^{2}+1)=-1<0$이므로 실수 $a$에 관계없이 두 허근 $\alpha$, $\beta$는 이 이차방정식의 근이다. **근과 계수의 관계**에서 $\alpha+\beta=2a=8$이므로 $a=4$이고, $\alpha\beta=a^{2}+1=17$이다. 따라서 답은 $\boxed{②}$ 이다.",
         "common_error": r"허근의 곱을 삼차방정식 전체의 세 근의 곱 $a^{2}+1$과 혼동해 $1$로 나누지 않는 실수(여기서는 우연히 같음)"},
    ],
    "ontology_profile": {
        "concepts": [C("인수정리와 조립제법", [1]), C("이차방정식의 판별식", [2]), C("이차방정식의 근과 계수의 관계", [2])],
        "decisions": [Dc("D-15", "문자 계수가 든 삼차식인데 $x=1$에서 모든 $a$에 대해 $0$이 됨", "인수정리로 $x-1$을 떼어 이차식으로 낮춤", "근의 공식 없이 삼차식을 그대로 다룸", "막힘", 1),
                      Dc("D-10", "허근의 합이 주어지고 곱을 묻는 꼴", "허근을 구하지 않고 이차 인수의 근과 계수의 관계 사용", "허근을 근의 공식으로 구해 더함", "계산폭발", 2)],
        "skills": [S("S-CM1-20", "main", [1]), S("S-CM1-05", "aux", [2]), S("S-CM1-04", "aux", [2], "이차 인수가 항상 허근을 가짐을 확인")],
        "strategy": None,
        "pattern": {"name": "인수정리로 낮춘 이차 인수의 근과 계수의 관계로 허근의 곱 구하기", "is_new": False},
        "loads": {"novel_decision": 2, "branching": 1, "execution": 3},
        "traps": [{"choice": "①", "step_no": None, "cause": "concept_confusion", "note": r"$\alpha\beta=a^{2}=16$으로 상수항 $+1$을 빠뜨린 값"},
                  {"choice": "③", "step_no": None, "cause": "calculation", "note": r"$\alpha+\beta=2a$를 $2a+1=8$로 잘못 두어 생기는 값 근처"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 문자 계수가 든 삼차방정식(한 정수근 보장)과 허근의 합 조건", "요구값: 허근의 곱", "핵심 판단 D-15·D-10", "main 스킬 S-CM1-20"],
        "variable_elements": [{"name": "보장되는 정수근", "role": "상수", "range_hint": "$x=1$ 또는 $x=-1$ 등 대입이 쉬운 값", "answer_sensitive": True},
                              {"name": "이차 인수의 상수항 보정", "role": "계수", "range_hint": "판별식이 항상 음수가 되게 $a^{2}+c$, $c>0$", "answer_sensitive": True},
                              {"name": "허근의 합의 값", "role": "조건값", "range_hint": "짝수(2a 꼴)", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "허근의 합 대신 '$\\alpha^{2}+\\beta^{2}$의 값'을 주어 대칭식 변형(S-CM1-24)까지 거치게 한다", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-20", "prerequisite": ["S-CM1-26", "concept:인수정리와 조립제법"], "prescription": "문자 계수가 든 삼차식에서 $x=1$을 대입해 인수를 확인하고 조립제법으로 이차식을 얻는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-15", "prerequisite": ["S-CM1-26"], "prescription": "계수에 문자가 있어도 특정 값에서 사라지는 식을 찾아 인수를 읽는 짧은 문항", "descend_to": "CM1"},
                     {"node": "D-10", "prerequisite": ["S-CM1-05"], "prescription": "이차방정식의 두 허근의 합·곱을 근을 구하지 않고 말하는 원자 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 1, "node": "S-CM1-20", "why": "문자 계수 앞에서 인수를 찾지 못하면 이후 단계가 열리지 않는다", "evidence": "common_error 1단계"},
                                  {"step_no": 2, "node": "S-CM1-05", "why": "곱의 상수항 보정 $+1$을 빠뜨린다", "evidence": "trap ①"}],
    },
    "diagnoses_if_correct": "문자 계수 삼차식을 인수정리로 낮추고 허근 조건을 이차 인수의 근과 계수의 관계로 처리하는 능력을 갖춤",
    "diagnoses_if_wrong": "인수 찾기 / 허근 판별 / 합·곱 적용",
    "assessment_note": "허근이 이차 인수에서만 나온다는 판단이 핵심이다.",
    "self_confidence": 0.98, "needs_review": False,
    "verification": "a=-10..10 전수로 sympy 수치근 계산, 허근 두 개의 합이 8 인 a=4 유일, 그때 허근 곱 17.0, 5지선다 정답 유일",
})

# ---------------------------------------------------------------- 11223 결손
R.append(missing(11223, "방정식과 부등식 - 이차방정식과 이차함수", ["CM1-EQ"], "S-CM1-05", "원문 결손으로 추정 태그", "이차방정식의 근과 계수의 관계",
                 "두 근의 차 조건으로 이차함수의 계수를 정해 근의 곱 구하기",
                 r"원문 결함: 조건 결손 — $f(x)$, $g(x)$의 정의와 $b$가 들어 있는 식이 본문에 없다('$b=2$이고' 앞의 그림·조건 소실). 표시 통과 상태이나 풀이 불가. 원본 대조 필요.",
                 step_text=r"두 함수 $f(x)$, $g(x)$와 상수 $b$가 든 식의 정의가 본문에 없어 방정식 $f(x)=g(x)$를 세울 수 없다."))

# ---------------------------------------------------------------- 11317 비례식 (⑤)
R.append({
    "item_id": 11317, "course": "CM1", "unit": "다항식 - 식의 값과 비", "units": ["CM1-POLY"],
    "final_answer": "⑤", "difficulty": 2, "answer_type": "객관식", "calc_load": 1, "reasoning_load": 2,
    "solution_steps": [
        {"step_no": 1, "role": "decision",
         "text": r"두 질량을 각각 구할 수 없으므로 관계식의 **비**를 그대로 만든다. 거리의 비와 속력의 비가 주어졌으니 $M=\dfrac{rv^{2}}{G}$에서 $G$가 약분된다.",
         "common_error": r"$G$나 $r$의 값을 모른다고 보고 막히는 실수"},
        {"step_no": 2, "role": "execute",
         "text": r"$r_{A}=45r_{B}$, $v_{A}=\dfrac{2}{3}v_{B}$를 대입하면 $$\frac{M_{A}}{M_{B}}=\frac{r_{A}v_{A}^{2}}{r_{B}v_{B}^{2}}=45\times\left(\frac{2}{3}\right)^{2}=20$$ 이므로 답은 $\boxed{⑤}$ 이다.",
         "common_error": r"속력의 비를 제곱하지 않고 $45\times\dfrac{2}{3}=30$으로 두는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("곱으로 이루어진 식의 값의 비", [1, 2]), C("지수의 계산(비의 거듭제곱)", [2])],
        "decisions": [Dc("D-50", "두 질량 각각은 구할 수 없고 비만 묻는 꼴", "관계식의 비를 세워 공통 상수 $G$를 약분", "각 질량을 수치로 구하려고 시도", "막힘", 1)],
        "skills": [S("S-CM1-37", "main", [2])],
        "strategy": None,
        "pattern": {"name": "관계식의 비로 변량의 비의 거듭제곱 계산하기", "is_new": False},
        "loads": {"novel_decision": 1, "branching": 1, "execution": 1},
        "traps": [{"choice": "③", "step_no": None, "cause": "formula_confusion", "note": r"속력의 비를 제곱하지 않은 $45\times\dfrac{2}{3}=30$ 근처에서 고른 값"},
                  {"choice": "②", "step_no": None, "cause": "misread", "note": r"거리의 비를 거꾸로 두어 $\dfrac{1}{45}$ 계열로 계산하다 고른 값"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 곱·거듭제곱으로 된 관계식과 각 변량의 비", "요구값: 두 값의 비", "핵심 판단 D-50: 각각 구하지 않고 비로 통째로", "main 스킬 S-CM1-37"],
        "variable_elements": [{"name": "거리의 비", "role": "조건값", "range_hint": "정수, 속력 비의 제곱과 곱해 정수가 되게", "answer_sensitive": True},
                              {"name": "속력의 비", "role": "조건값", "range_hint": "기약분수", "answer_sensitive": True},
                              {"name": "관계식의 지수", "role": "지표", "range_hint": "$v^{2}$, $v^{3}$ 등", "answer_sensitive": True}],
        "escalations": [{"axis": "역방향", "description": "질량의 비와 거리의 비를 주고 속력의 비를 묻게 바꿔 제곱근 처리(S-CM1-37 역방향)를 요구한다", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-37", "prerequisite": ["concept:곱으로 이루어진 식의 값의 비"], "prescription": "$y=kx^{2}$ 꼴에서 $x$가 $3$배가 될 때 $y$의 비를 묻는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-50", "prerequisite": ["S-CM1-37"], "prescription": "각 값을 구할 수 없는 두 식의 비만 묻는 짧은 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 2, "node": "S-CM1-37", "why": "비를 제곱하는 자리에서 거듭제곱을 빠뜨린다", "evidence": "trap ③"}],
    },
    "diagnoses_if_correct": "관계식의 비를 세워 변량의 비의 거듭제곱으로 값을 구하는 수행을 갖춤",
    "diagnoses_if_wrong": "비 세우기 / 거듭제곱 처리",
    "assessment_note": "식의 값의 비 문항으로, 공통 상수 약분과 제곱 처리가 핵심이다.",
    "self_confidence": 0.99, "needs_review": False,
    "verification": "sympy Rational 계산 45·(2/3)^2 = 20, 5지선다 정답 유일",
})

# ---------------------------------------------------------------- 11133 결손
R.append(missing(11133, "방정식과 부등식 - 이차방정식과 이차함수", ["CM1-EQ"], "S-CM1-05", "원문 결손으로 추정 태그", "이차함수의 그래프의 평행이동",
                 "평행이동한 그래프와 직선의 교점의 좌표 합으로 이동량 구하기",
                 r"원문 결함: 조건 결손 — 이차함수 $f(x)$의 식이 본문에 없다(그림 소실). 표시 통과 상태이나 풀이 불가. 원본 대조 필요.",
                 step_text=r"이차함수 $f(x)$의 식이 본문에 없어 교점의 $x$좌표의 합을 세울 수 없다.", diff=4, cl=3, rl=3))

# ---------------------------------------------------------------- 11193 결손
R.append(missing(11193, "방정식과 부등식 - 이차방정식과 이차함수", ["CM1-EQ"], "S-CM1-06", "원문 결손으로 추정 태그", "이차함수의 꼭짓점",
                 "꼭짓점의 자취로 선분 길이의 최솟값 구하기",
                 r"원문 결함: 조건 결손 — 이차함수 $f(x)$의 식과 점 $A$의 정의가 본문에 없다(그림 소실). 표시 통과 상태이나 풀이 불가. 원본 대조 필요.",
                 step_text=r"이차함수 $f(x)$의 식과 점 $A$의 좌표가 본문에 없어 꼭짓점 $B$와 중점 $C$를 나타낼 수 없다.", diff=4, cl=3, rl=3))

# ---------------------------------------------------------------- 15274 좌석 배정 (396)
R.append({
    "item_id": 15274, "course": "CM1", "unit": "경우의 수 - 합의 법칙과 곱의 법칙", "units": ["CM1-COUNT"],
    "problem_text": r"교내 수학경시대회에 A 학급 학생 $3$명, B 학급 학생 $3$명, C 학급 학생 $2$명이 참가 신청하였다. 그림과 같이 두 분단, 네 줄의 좌석에 다음 조건을 만족시키도록 이 학생 $8$명을 배정하는 방법의 수를 구하시오. [4점] (가) 같은 줄의 바로 옆에 같은 학급 학생이 앉지 않도록 배정한다. (나) 같은 분단의 바로 앞뒤에 같은 학급 학생이 앉지 않도록 배정한다. (다) 같은 학급 학생을 같은 분단에 배정할 경우 학급 번호가 작을수록 교탁에 가까운 자리에 배정한다. (그림: 교탁 앞에 1분단과 2분단이 나란히 있고 각 분단은 첫째 줄부터 넷째 줄까지 한 자리씩, 모두 $8$자리)",
    "final_answer": "396", "difficulty": 4, "answer_type": "단답형", "calc_load": 3, "reasoning_load": 4,
    "solution_steps": [
        {"step_no": 1, "role": "setup",
         "text": r"먼저 $8$개 자리에 학급 $\mathrm{A}$, $\mathrm{B}$, $\mathrm{C}$를 배치하는 **학급 배치**를 세고, 그다음 각 학급 학생을 그 자리에 넣는 방법을 곱한다. (다)에 의해 같은 분단에 앉는 같은 학급 학생의 앞뒤 순서는 하나로 정해지므로, 학급의 $3$명이 두 분단에 $2$명·$1$명으로 나뉘면 학생을 넣는 방법은 혼자 앉는 학생을 고르는 $3$가지, $\mathrm{C}$의 $2$명이 두 분단에 $1$명씩이면 $2$가지, 한 분단에 $2$명이면 $1$가지이다.",
         "common_error": r"(다)를 무시하고 같은 분단의 같은 학급 학생을 $2!$로 세는 실수"},
        {"step_no": 2, "role": "decision",
         "text": r"$\mathrm{C}$ $2$명이 같은 분단에 앉는지로 경우를 나눈다. 각 분단은 $4$자리이고 앞뒤가 같은 학급일 수 없으므로 한 분단에 한 학급은 많아야 $2$명이다.",
         "common_error": r"$\mathrm{A}$나 $\mathrm{B}$의 배치부터 세어 경우가 폭발하는 실수"},
        {"step_no": 3, "role": "execute",
         "text": r"$\mathrm{C}$ $2$명이 다른 분단에 앉는 경우: $\mathrm{C}$가 있는 두 줄이 첫째 줄과 넷째 줄이면 가운데 두 줄이 모두 $\mathrm{A}$, $\mathrm{B}$ 한 명씩이 되어 앞뒤 조건을 만족할 수 없으므로 $\mathrm{C}$의 두 줄을 고르는 방법은 $_{4}\mathrm{C}_{2}-1=5$가지, 두 $\mathrm{C}$의 분단을 정하는 방법은 $2$가지이다. 남은 $6$자리는 $\mathrm{C}$가 없는 두 줄이 서로 반대 배치가 되어야 하므로 $2$가지로 채워지고, 이때 $\mathrm{A}$, $\mathrm{B}$는 각각 $2$명·$1$명으로 나뉜다. 학급 배치 $5\times2\times2=20$가지에 학생 배정 $3\times3\times2=18$을 곱해 $360$이다.",
         "common_error": r"$\mathrm{C}$의 두 줄이 첫째·넷째 줄인 경우를 빼지 않아 $6$가지로 두는 실수"},
        {"step_no": 4, "role": "execute",
         "text": r"$\mathrm{C}$ $2$명이 같은 분단에 앉는 경우: 그 분단은 $\mathrm{C}$, $\mathrm{A}$, $\mathrm{B}$가 $2$, $1$, $1$명이고 다른 분단은 $\mathrm{A}$, $\mathrm{B}$가 $2$명씩 번갈아 앉는다. $\mathrm{C}$가 첫째·넷째 줄에 앉을 때만 옆자리 조건을 맞출 수 있어 학급 배치는 분단 선택 $2$가지에 나머지 배치 $2$가지를 곱한 $4$가지이고, 학생 배정은 $3\times3\times1=9$이므로 $36$이다. 따라서 구하는 방법의 수는 $360+36=\boxed{396}$ 이다.",
         "common_error": r"$\mathrm{C}$가 둘째·셋째 줄 조합에 앉는 배치도 가능하다고 보아 과대 계산하는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("곱의 법칙", [1, 3, 4]), C("합의 법칙", [4]), C("조합", [3])],
        "decisions": [Dc("D-05", "인원이 가장 적은 $\\mathrm{C}$ 학급이 배치를 가장 강하게 제약함", "$\\mathrm{C}$ $2$명의 분단·줄부터 확정해 경우를 나눔", "$\\mathrm{A}$ 학급 $3$명의 자리부터 나열", "계산폭발", 2)],
        "skills": [S("S-CM1-13", "main", [3, 4], "학급 배치 수와 학생 배정 수의 곱, 두 경우의 합"), S("S-CM1-11", "aux", [1], "(다) 순서 고정으로 학생 배정 수를 조건에 맞게 세기")],
        "strategy": None,
        "pattern": {"name": "제약이 강한 집단을 먼저 배치해 좌석 배정의 수 구하기", "is_new": False},
        "loads": {"novel_decision": 3, "branching": 3, "execution": 3},
        "traps": [{"choice": None, "step_no": 1, "cause": "condition_missing", "note": r"(다)를 무시하면 학생 배정이 $2$배씩 커진다"},
                  {"choice": None, "step_no": 3, "cause": "case_missing", "note": r"첫째·넷째 줄 경우를 빼지 않으면 $24$가지 배치"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: $2$분단 $4$줄 좌석, 학급별 인원 $3$·$3$·$2$, 옆·앞뒤 같은 학급 금지, 같은 분단 내 순서 고정", "요구값: 배정 방법의 수", "핵심 판단 D-05: 가장 적은 학급부터 확정", "main 스킬 S-CM1-13"],
        "variable_elements": [{"name": "학급별 인원", "role": "조건값", "range_hint": "합 8, 한 학급 최대 4", "answer_sensitive": True},
                              {"name": "좌석 모양(줄·분단 수)", "role": "소재", "range_hint": "$2\\times4$ 또는 $2\\times3$", "answer_sensitive": True},
                              {"name": "순서 고정 조건 (다)의 유무", "role": "지표", "range_hint": "있으면 같은 분단 같은 학급 순서가 1가지", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "'$\\mathrm{A}$ 학급 학생은 모두 같은 분단'을 더해 분단 분할의 경우를 줄이는 대신 앞뒤 조건을 더 세게 만든다", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-13", "prerequisite": ["concept:곱의 법칙", "concept:합의 법칙"], "prescription": "$2\\times2$ 좌석에 두 학급 $2$명씩을 옆자리가 다른 학급이 되게 앉히는 방법의 수를 묻는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-05", "prerequisite": ["S-CM1-13"], "prescription": "인원이 가장 적은 집단의 자리를 먼저 정하면 나머지가 결정되는 작은 배치 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 2, "node": "D-05", "why": "제약이 센 학급부터 나누지 않으면 경우가 폭발한다", "evidence": "common_error 2단계"},
                                  {"step_no": 3, "node": "S-CM1-13", "why": "첫째·넷째 줄 예외와 나머지 $6$자리의 강제 배치를 보지 못한다", "evidence": "trap 3단계"}],
    },
    "diagnoses_if_correct": "순서 고정 조건을 배정 수로 번역하고 제약이 강한 집단부터 경우를 나눠 곱의 법칙으로 세는 능력을 갖춤",
    "diagnoses_if_wrong": "(다)의 번역 / 분류 기준 선택 / 예외 배치 제거 / 합산",
    "assessment_note": "학급 배치 수와 학생 배정 수를 분리해 세는 구조를 읽는지가 핵심이다.",
    "self_confidence": 0.96, "needs_review": False,
    "verification": "학생 8명(반·번호 구별)을 8자리에 놓는 8! 전수 탐색으로 (가)(나)(다) 를 모두 만족하는 배정 396건 확인, 학급 배치 수는 C 다른 분단 20·같은 분단 4 로 별도 전수 확인",
})

# ---------------------------------------------------------------- 12094 행렬 성분 (②)
R.append({
    "item_id": 12094, "course": "CM1", "unit": "행렬 - 행렬의 연산", "units": ["CM1-MAT"],
    "problem_text": r"세 이차정사각행렬 $A=\begin{pmatrix} 0 & 0 \\ 6 & 0 \end{pmatrix}$, $B$, $C$가 다음 조건을 만족시킨다. (가) $AB=CA=O$ (나) 행렬 $B$의 모든 성분의 합이 $3$이고, 행렬 $C$의 $(1,\,1)$ 성분과 $(2,\,1)$ 성분이 같다. $BC=A$일 때, 행렬 $C$의 모든 성분의 합은? (단, $O$는 영행렬이다.) [4점] ① $3$ ② $4$ ③ $5$ ④ $6$ ⑤ $7$",
    "final_answer": "②", "difficulty": 3, "answer_type": "객관식", "calc_load": 2, "reasoning_load": 3,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"$A=\begin{pmatrix} 0 & 0 \\ 6 & 0 \end{pmatrix}$이므로 $AB=O$, $CA=O$를 **성분**으로 쓴다. $B=\begin{pmatrix} b_{1} & b_{2} \\ b_{3} & b_{4} \end{pmatrix}$에서 $AB=\begin{pmatrix} 0 & 0 \\ 6b_{1} & 6b_{2} \end{pmatrix}=O$이므로 $b_{1}=b_{2}=0$이고, $C=\begin{pmatrix} c_{1} & c_{2} \\ c_{3} & c_{4} \end{pmatrix}$에서 $CA=\begin{pmatrix} 6c_{2} & 0 \\ 6c_{4} & 0 \end{pmatrix}=O$이므로 $c_{2}=c_{4}=0$이다.",
         "common_error": r"$AB=O$에서 $A \ne O$이므로 $B=O$라고 단정하는 실수"},
        {"step_no": 2, "role": "execute",
         "text": r"(나)에서 $b_{3}+b_{4}=3$, $c_{1}=c_{3}$이므로 $BC=\begin{pmatrix} 0 & 0 \\ b_{3} & b_{4} \end{pmatrix}\begin{pmatrix} c_{1} & 0 \\ c_{1} & 0 \end{pmatrix}=\begin{pmatrix} 0 & 0 \\ 3c_{1} & 0 \end{pmatrix}$이다. $BC=A$에서 $3c_{1}=6$이므로 $c_{1}=2$이고, $C$의 모든 성분의 합은 $c_{1}+c_{3}=4$이다. 따라서 답은 $\boxed{②}$ 이다.",
         "common_error": r"$BC$의 $(2,1)$ 성분을 $b_{3}c_{1}$만으로 두어 $b_{4}c_{1}$을 빠뜨리는 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("행렬의 곱셈", [1, 2]), C("행렬의 상등", [1, 2]), C("영행렬과 영인자", [1])],
        "decisions": [Dc("D-16", "조건이 행렬 등식 $AB=CA=O$, $BC=A$로 주어짐", "성분을 미지수로 두고 곱의 성분을 비교해 조건으로 환원", "$B=O$ 또는 $C=O$처럼 수의 곱셈 성질을 그대로 적용", "오답", 1)],
        "skills": [S("S-CM1-23", "main", [1, 2]), S("S-CM1-38", "aux", [2])],
        "strategy": None,
        "pattern": {"name": "행렬 곱의 성분 비교로 미지의 행렬의 성분 합 구하기", "is_new": False},
        "loads": {"novel_decision": 2, "branching": 1, "execution": 2},
        "traps": [{"choice": "④", "step_no": None, "cause": "concept_confusion", "note": r"$c_{1}=2$만 더하고 $c_{3}=c_{1}$을 반영하지 않거나 $6$을 그대로 고른 값"},
                  {"choice": "①", "step_no": None, "cause": "calculation", "note": r"$b_{3}+b_{4}=3$을 $BC$에 쓰지 않고 $c_{1}=3$ 등으로 두어 얻는 값"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 성분이 한 곳만 $0$이 아닌 행렬 $A$와 곱이 영행렬이 되는 두 조건, 성분 합·상등 조건", "요구값: 미지 행렬의 성분 합", "핵심 판단 D-16: 성분 비교로 환원", "main 스킬 S-CM1-23"],
        "variable_elements": [{"name": "$A$의 $0$이 아닌 성분의 값과 위치", "role": "상수", "range_hint": "$0$이 아닌 정수, $(2,1)$ 또는 $(1,2)$", "answer_sensitive": True},
                              {"name": "$B$의 성분 합", "role": "조건값", "range_hint": "정수, $A$의 성분을 나누어 떨어지게", "answer_sensitive": True},
                              {"name": "묻는 행렬($B$ 또는 $C$)", "role": "지표", "range_hint": "둘 중 하나", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "$A$의 $0$이 아닌 성분을 두 개로 늘려 영인자 조건이 두 성분의 비로 주어지게 한다(S-CM1-23 심화)", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-23", "prerequisite": ["S-CM1-38", "concept:행렬의 상등"], "prescription": "$AB=O$에서 $A$의 성분 하나만 $0$이 아닐 때 $B$의 어느 성분이 $0$이어야 하는지 묻는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-16", "prerequisite": ["concept:영행렬과 영인자"], "prescription": "$AB=O$인데 $A \\ne O$, $B \\ne O$인 예를 하나 만드는 짧은 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 1, "node": "D-16", "why": "수의 곱셈처럼 $AB=O$에서 한쪽이 $O$라고 단정한다", "evidence": "common_error 1단계"},
                                  {"step_no": 2, "node": "S-CM1-38", "why": "곱의 성분에서 두 항의 합을 빠뜨린다", "evidence": "trap ①"}],
    },
    "diagnoses_if_correct": "행렬 등식 조건을 성분 비교로 환원하고 영인자 성질을 바르게 다루는 능력을 갖춤",
    "diagnoses_if_wrong": "영인자 처리 / 곱의 성분 계산 / 조건 반영",
    "assessment_note": r"원문 결함: 행렬 표기 잔재 — 원문 '$\left( r \begin{matrix} 0 && 0 \\ 6 && 0 \end{matrix} \right)$' 의 'r' 과 '&&' 는 HWP 변환 잔재. 읽기: $A=\begin{pmatrix} 0 & 0 \\ 6 & 0 \end{pmatrix}$ (표시 화면에서는 정상). 행렬 곱의 비가환·영인자 성질을 성분으로 처리하는지가 핵심이다.",
    "self_confidence": 0.98, "needs_review": False,
    "verification": "sympy 로 B·C 성분 8개를 모두 미지수로 두고 AB=O·CA=O·합 조건·상등 조건·BC=A 를 연립, 해 1개에서 C 성분 합 4, 5지선다 정답 유일",
})

# ---------------------------------------------------------------- 10723 역행렬 빈칸 (④)
R.append({
    "item_id": 10723, "course": "CM1", "unit": "행렬 - 역행렬(구과정)", "units": ["CM1-MAT"],
    "problem_text": r"다음은 두 이차정사각행렬 $A$, $B$에 대하여 $2A^{2}+AB=E$ (㉠), $AB+2BA=2A+E$ (㉡)이 성립할 때, 행렬 $A$의 역행렬 $A^{-1}$를 $A$와 $E$로 나타내는 과정이다. (단, $E$는 단위행렬이다.) ㉠에서 $A^{-1}=$ (가) $\times A+B$ (㉢). 또한 $AA^{-1}=A^{-1}A$이므로 ㉢에서 $AB=BA$. 따라서 ㉡에서 $AB=$ (나) $\times A+\dfrac{1}{3}E$이고, ㉠에서 $AB=E-2A^{2}$이므로 $E-2A^{2}=$ (나) $\times A+\dfrac{1}{3}E$. 그러므로 $A^{-1}=$ (다) $\times A+E$이다. 위의 과정에서 (가), (나), (다)에 알맞은 수를 각각 $p$, $q$, $r$라 할 때, 세 수 $p$, $q$, $r$의 곱 $pqr$의 값은? [3점] ① $1$ ② $2$ ③ $3$ ④ $4$ ⑤ $5$",
    "final_answer": "④", "difficulty": 3, "answer_type": "객관식", "calc_load": 2, "reasoning_load": 3,
    "solution_steps": [
        {"step_no": 1, "role": "execute",
         "text": r"㉠의 좌변에서 **공통인수** $A$를 앞으로 묶으면 $A(2A+B)=E$이므로 $A^{-1}=2A+B$이고 (가)는 $2$이다.",
         "common_error": r"$2A^{2}+AB$에서 $A$를 뒤로 묶어 $(2A+B)A$로 쓰는 실수(여기서는 결과가 같지만 교환법칙을 전제한 것)"},
        {"step_no": 2, "role": "execute",
         "text": r"$AA^{-1}=A^{-1}A$에서 $AB=BA$이므로 ㉡은 $3AB=2A+E$가 되어 $AB=\dfrac{2}{3}A+\dfrac{1}{3}E$이고 (나)는 $\dfrac{2}{3}$이다.",
         "common_error": r"$AB=BA$를 쓰지 않고 ㉡을 그대로 두어 $AB$를 정리하지 못하는 실수"},
        {"step_no": 3, "role": "execute",
         "text": r"㉠의 $AB=E-2A^{2}$를 대입하면 $E-2A^{2}=\dfrac{2}{3}A+\dfrac{1}{3}E$, 즉 $A\left(A+\dfrac{1}{3}E\right)=\dfrac{1}{3}E$이므로 $A(3A+E)=E$에서 $A^{-1}=3A+E$이고 (다)는 $3$이다. 따라서 $pqr=2\times\dfrac{2}{3}\times3=4$이므로 답은 $\boxed{④}$ 이다.",
         "common_error": r"$2A^{2}=\dfrac{2}{3}E-\dfrac{2}{3}A$에서 양변을 $2$로 나누는 과정의 계수 실수"},
    ],
    "ontology_profile": {
        "concepts": [C("역행렬의 정의", [1, 3]), C("행렬의 곱셈의 성질(분배법칙·비가환)", [1, 2]), C("역행렬과 교환 가능성", [2])],
        "decisions": [Dc("D-15", "$A$가 공통으로 곱해진 항들의 합이 $E$와 같음", "$A(\\cdots)=E$로 묶어 역행렬을 바로 읽음", "역행렬 공식으로 성분을 직접 계산", "막힘", 1)],
        "skills": [S("S-CM1-34", "main", [1, 3]), S("S-CM1-23", "aux", [2], "$AB=BA$ 를 이용한 식 정리")],
        "strategy": None,
        "pattern": {"name": "공통인수 묶기로 행렬의 관계식에서 역행렬 구하기", "is_new": False},
        "loads": {"novel_decision": 2, "branching": 1, "execution": 2},
        "traps": [{"choice": "②", "step_no": None, "cause": "calculation", "note": r"(나)를 $\dfrac{1}{3}$으로 두어 $pqr=2$"},
                  {"choice": "③", "step_no": None, "cause": "concept_confusion", "note": r"(다)를 $\dfrac{3}{2}$ 등으로 잘못 정리해 얻는 값"}],
    },
    "v61_3": {
        "invariants": ["주어진 것: 두 행렬의 두 관계식(한쪽이 $A(\\cdots)=E$ 꼴)과 역행렬을 나타내는 빈칸 과정", "요구값: 빈칸 수의 곱", "핵심 판단 D-15: 공통인수 묶기", "main 스킬 S-CM1-34"],
        "variable_elements": [{"name": "㉠의 계수", "role": "계수", "range_hint": "정수, $A(kA+B)=E$ 꼴 유지", "answer_sensitive": True},
                              {"name": "㉡의 계수", "role": "계수", "range_hint": "$AB=BA$ 적용 후 $AB$가 $A$, $E$의 일차결합이 되게", "answer_sensitive": True},
                              {"name": "묻는 식(곱·합)", "role": "지표", "range_hint": "pqr 또는 p+q+r", "answer_sensitive": True}],
        "escalations": [{"axis": "조건 추가", "description": "빈칸 없이 $A^{-1}$를 $A$와 $E$로 나타내라고 하여 묶기와 치환을 스스로 설계하게 한다(S-CM1-34 전면)", "keeps_course": True}],
        "recovery": [{"node": "S-CM1-34", "prerequisite": ["S-CM1-23", "concept:역행렬의 정의"], "prescription": "$A^{2}+2A=E$에서 $A^{-1}$를 $A$와 $E$로 나타내는 원자 문항", "descend_to": "CM1"},
                     {"node": "D-15", "prerequisite": ["concept:행렬의 곱셈의 성질(분배법칙·비가환)"], "prescription": "$A^{2}+AB$를 $A(A+B)$로 묶을 수 있고 $(A+B)A$와는 다름을 확인하는 짧은 문항", "descend_to": "CM1"}],
        "bottleneck_hypotheses": [{"step_no": 3, "node": "S-CM1-34", "why": "대입 후 $A$의 다항식을 다시 $A(\\cdots)=E$ 꼴로 묶는 변형이 막힌다", "evidence": "common_error 3단계·trap ③"}],
    },
    "diagnoses_if_correct": "행렬 관계식에서 공통인수를 묶어 역행렬을 읽고 교환 가능성을 활용하는 능력을 갖춤",
    "diagnoses_if_wrong": "묶기 / 교환 가능성 적용 / 재묶기",
    "assessment_note": "구과정 역행렬 문항이나 2022 개정 공통수학1 행렬 범위에서 역행렬 정의만으로 풀 수 있다.",
    "self_confidence": 0.98, "needs_review": False,
    "verification": "A=tE, B=sE (3t^2+t-1=0, t=(-1+sqrt13)/6) 의 구체 행렬로 ㉠·㉡ 성립을 sympy 로 확인한 뒤 AB=(2/3)A+E/3, A^{-1}=3A+E 성립 확인, pqr=4, 5지선다 정답 유일",
})

if __name__ == "__main__":
    raise SystemExit(emit("W38_CM1b_cycle48", R))
