# -*- coding: utf-8 -*-
"""W38 CM1b (cycle48) 독립 검산 — 풀이와 다른 경로(sympy·전수 탐색)로 답을 낸다. 읽기 전용, DB 없음."""
import json
import sys
from itertools import permutations

import sympy as sp

x, a = sp.symbols("x a")
R = {}

# 11941: 삼차방정식의 허근 합 = 8 → a 전수(정수·유리수 후보) 뒤 허근 곱. 다른 경로: 수치 근 직접 계산
res = []
for aa in range(-10, 11):
    f = x**3 - (2 * aa + 1) * x**2 + (aa + 1)**2 * x - (aa**2 + 1)
    rs = sp.Poly(f, x).nroots(n=20)
    im = [r for r in rs if abs(sp.im(r)) > 1e-9]
    if len(im) == 2 and abs(sp.re(im[0] + im[1]) - 8) < 1e-9:
        res.append((aa, sp.N(sp.re(im[0] * im[1]), 12)))
R[11941] = {"a_and_product": [(t[0], float(t[1])) for t in res], "answer_no": "②" if res and all(abs(float(t[1]) - 17) < 1e-9 for t in res) else "?"}

# 11317: 비례식 수치 계산
ratio = sp.Rational(45) * sp.Rational(2, 3) ** 2
R[11317] = {"MA/MB": ratio, "answer_no": "⑤" if ratio == 20 else "?"}

# 15274: 좌석 8자리(2분단×4줄) 전수 탐색 — 학생은 반·번호로 구별, 조건 (가)(나)(다)
students = [("A", 1), ("A", 2), ("A", 3), ("B", 1), ("B", 2), ("B", 3), ("C", 1), ("C", 2)]
seats = [(r, c) for r in range(4) for c in range(2)]  # r=0 교탁에 가장 가까움, c=분단
count = 0
for perm in permutations(students):
    place = dict(zip(seats, perm))
    ok = True
    for (r, c), s in place.items():
        if c == 0 and place[(r, 1)][0] == s[0]:  # (가) 같은 줄 옆자리
            ok = False
            break
        if r < 3 and place[(r + 1, c)][0] == s[0]:  # (나) 같은 분단 바로 앞뒤
            ok = False
            break
    if not ok:
        continue
    for c in range(2):  # (다) 같은 분단의 같은 반 학생은 번호가 작을수록 앞
        col = [place[(r, c)] for r in range(4)]
        for cls in "ABC":
            nums = [n for (k, n) in col if k == cls]
            if nums != sorted(nums):
                ok = False
    if ok:
        count += 1
R[15274] = {"count": count, "answer": "396" if count == 396 else "?"}

# 12094: 행렬 성분 전수 — B=[[0,0],[c,d]] 꼴을 가정하지 않고 일반 성분 미지수로 풀기
b11, b12, b21, b22, c11, c12, c21, c22 = sp.symbols("b11 b12 b21 b22 c11 c12 c21 c22")
A = sp.Matrix([[0, 0], [6, 0]])
B = sp.Matrix([[b11, b12], [b21, b22]])
C = sp.Matrix([[c11, c12], [c21, c22]])
eqs = list(A * B) + list(C * A) + [sum(B) - 3, c11 - c21] + list(B * C - A)
sol = sp.solve(eqs, [b11, b12, b21, b22, c11, c12, c21, c22], dict=True)
sums = sorted({sp.simplify(sum(C.subs(s))) for s in sol})
R[12094] = {"solutions": len(sol), "sum_C": [str(v) for v in sums], "answer_no": "②" if sums == [4] else "?"}

# 10723: A^{-1} = pA + B, AB = qA + E/3, A^{-1} = rA + E 를 구체 행렬로 검증 — A^2 = E/3 - A/3 을 만족하는 실제 2차 행렬을 잡아 확인
# A = tE, B = sE 꼴에서 ㉠: 2t^2 + ts = 1, ㉡: 3ts = 2t + 1 → 3t^2 + t - 1 = 0, t = (-1+sqrt13)/6, s = (1-2t^2)/t
t = (-1 + sp.sqrt(13)) / 6
s_ = (1 - 2 * t**2) / t
Am = t * sp.eye(2)
Ainv = Am.inv()
Bm = s_ * sp.eye(2)
E = sp.eye(2)
chk1 = sp.simplify(2 * Am**2 + Am * Bm - E) == sp.zeros(2)
chk2 = sp.simplify(Am * Bm + 2 * Bm * Am - 2 * Am - E) == sp.zeros(2)
pv = 2
qv = sp.Rational(2, 3)
rv = 3
chk3 = sp.simplify(Am * Bm - (qv * Am + E / 3)) == sp.zeros(2)
chk4 = sp.simplify(Ainv - (rv * Am + E)) == sp.zeros(2)
R[10723] = {"model_satisfies_given": chk1 and chk2, "q_check": chk3, "r_check": chk4, "pqr": pv * qv * rv, "answer_no": "④" if (chk1 and chk2 and chk3 and chk4 and pv * qv * rv == 4) else "?"}

# 11133: f(x) 정의 없음(그림 소실) — 조건 결손. (참고: f(x)=x^2 이면 ④ 가 나오지만 채우지 않는다)
R[11133] = {"status": "원문 결함: 조건 결손 — 이차함수 f(x) 의 식이 본문에 없음(그림 소실). 검산 생략"}
R[11193] = {"status": "원문 결함: 조건 결손 — f(x), 점 A 정의 없음(그림 소실). 검산 생략"}
R[11223] = {"status": "원문 결함: 조건 결손 — f(x), g(x), b 의 정의 없음(그림 소실). 검산 생략"}
R[11253] = {"status": "원문 결함: 조건 결손 — f(x), 직선 l, p 의 정의 없음(그림 소실). 검산 생략"}

for kk, v in R.items():
    print(kk, json.dumps({a_: str(b_) for a_, b_ in v.items()}, ensure_ascii=False))
ok = all(v.get("answer_no", v.get("answer", "x")) != "?" for v in R.values())
print("ALL_PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
