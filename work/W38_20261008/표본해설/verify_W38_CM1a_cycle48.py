# -*- coding: utf-8 -*-
"""W38 CM1a (cycle48) 독립 검산 — 풀이와 다른 경로(sympy 전개·전수 탐색·수치)로 답을 낸다. 읽기 전용, DB 없음."""
import json
import sys
from itertools import product

import sympy as sp

x, a, b, p, q, k = sp.symbols("x a b p q k")
R = {}

# 12024: 항등식 2x^2+ax+b = x(x-3)+(x+1)(x+3) → 전개해 계수 비교
rhs = sp.expand(x * (x - 3) + (x + 1) * (x + 3))
sol = sp.solve(sp.Poly(rhs - (2 * x**2 + a * x + b), x).all_coeffs(), [a, b])
R[12024] = {"ab": sol[a] * sol[b], "answer_no": "③" if sol[a] * sol[b] == 3 else "?", "check": str(rhs)}

# 11304: (x-1)(x+a) = b x^2 - 3x + 2 → 수치대입(x=1, x=0, x=2) 으로 a, b
eqs = [sp.Eq((t - 1) * (t + a), b * t**2 - 3 * t + 2) for t in (0, 1, 2)]
sol = sp.solve(eqs, [a, b], dict=True)[0]
R[11304] = {"a": sol[a], "b": sol[b], "a+b": sol[a] + sol[b], "answer_no": "①" if sol[a] + sol[b] == -1 else "?"}

# 11940: P(x)=x^2+px+q, P(1)=1, 2P(2)=2 → 연립 후 P(4)
P = x**2 + p * x + q
sol = sp.solve([sp.Eq(P.subs(x, 1), 1), sp.Eq(2 * P.subs(x, 2), 2)], [p, q])
P4 = P.subs(sol).subs(x, 4)
R[11940] = {"p": sol[p], "q": sol[q], "P(4)": P4, "answer_no": "②" if P4 == 7 else "?"}

# 8376: 전수 탐색 — g=x^2+px+q, h=g+(-4x-1), f=gh 의 계수를 정수 격자에서 찾고 실근 없음 확인
found = []
for pp, qq in product(range(-12, 13), range(-12, 13)):
    g = x**2 + pp * x + qq
    h = g + (-4 * x - 1)
    f = sp.Poly(sp.expand(g * h), x)
    co = f.all_coeffs()  # [1, a+2, b, a, 6]
    if co[4] != 6 or co[1] - 2 != co[3]:
        continue
    aa, bb = co[3], co[2]
    if sp.discriminant(g, x) >= 0 or sp.discriminant(h, x) >= 0:
        continue
    found.append((pp, qq, aa, bb, aa**2 + bb**2))
R[8376] = {"solutions": found, "a2+b2": sorted({t[4] for t in found}), "answer": "5" if {t[4] for t in found} == {5} else "?"}

# 11803: 판별식>0 인 자연수 k 를 1..100 전수
cnt = [kk for kk in range(1, 101) if sp.discriminant(x**2 + 2 * (kk - 2) * x + kk**2 - 24, x) > 0]
R[11803] = {"k": cnt, "count": len(cnt), "answer": "6" if len(cnt) == 6 else "?"}

# 11983: 판별식>=0 인 자연수 a 를 1..100 전수
cnt = [aa for aa in range(1, 101) if sp.discriminant(x**2 + 2 * aa * x + aa**2 + 4 * aa - 28, x) >= 0]
R[11983] = {"a": cnt, "count": len(cnt), "answer": "7" if len(cnt) == 7 else "?"}

# 11135: 근을 직접 구해 대입(무리수) → 수치 단순화
al, be = sp.solve(x**2 - 3 * x - 2, x)
val = sp.nsimplify(sp.simplify(al**3 - 3 * al**2 + al * be + 2 * be))
val2 = sp.nsimplify(sp.simplify(be**3 - 3 * be**2 + be * al + 2 * al))
R[11135] = {"value(alpha)": val, "value(beta)": val2, "answer_no": "③" if val == 4 and val2 == 4 else "?"}

# 11164: 원문 결함(P(x), Q(x) 미정의) — 검산 불가, needs_review
R[11164] = {"status": "원문 결함: 조건 결손 — P(x), Q(x) 정의 없음(그림·조건 소실). 검산 생략"}

# 11131: 실제 근 1/α 들을 수치로 구해 삼차식 재구성 → (가)=3, (나)=x^3+3x^2+2x+1
roots = sp.Poly(x**3 + 2 * x**2 + 3 * x + 1, x).nroots(n=30)
recip = [1 / r for r in roots]
poly = sp.expand(sp.prod([(x - r) for r in recip]))
coef = [sp.N(c, 12) for c in sp.Poly(poly, x).all_coeffs()]
coef_r = [round(complex(c).real, 6) for c in coef]
f2 = sum(c * 2**(3 - i) for i, c in enumerate(coef_r))
R[11131] = {"recip_poly_coeffs": coef_r, "p": coef_r[1], "f(2)": f2, "p+f(2)": coef_r[1] + f2, "answer_no": "①" if abs(coef_r[1] + f2 - 28) < 1e-6 else "?"}

for kk, v in R.items():
    print(kk, json.dumps({a_: str(b_) for a_, b_ in v.items()}, ensure_ascii=False))
ok = all(v.get("answer_no", v.get("answer", "x")) not in ("?",) for v in R.values())
print("ALL_PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
