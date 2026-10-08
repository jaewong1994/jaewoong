# -*- coding: utf-8 -*-
"""W38 PRSTa (cycle48) 독립 검산 — 전수 탐색·sympy 전개. 읽기 전용, DB 없음."""
import json
import sys
from itertools import combinations, permutations

import sympy as sp

R = {}

# 8744: 0,0,0,1,1,1,1,1,1 의 서로 다른 나열을 전수로 만들어 0 이 이웃하지 않고 첫 자리가 1 인 것만 센다
seqs = set(permutations("000111111"))
cnt = sum(1 for s in seqs if s[0] == "1" and "00" not in "".join(s))
R[8744] = {"count": cnt, "answer_no": "⑤" if cnt == 20 else "?"}

# 8750: 1~9 격자(3×3)에서 두 수를 고르는 모든 조합 전수 → 행·열이 모두 다른 쌍
cells = {n: ((n - 1) // 3, (n - 1) % 3) for n in range(1, 10)}
cnt = sum(1 for u, v in combinations(range(1, 10), 2) if cells[u][0] != cells[v][0] and cells[u][1] != cells[v][1])
R[8750] = {"count": cnt, "answer_no": "④" if cnt == 18 else "?"}

# 17805: 다항식을 직접 전개해 x^2 계수
x = sp.symbols("x")
c2 = sp.Poly(sp.expand((x - 1)**6 * (2 * x + 1)**7), x).coeff_monomial(x**2)
R[17805] = {"coeff_x2": c2, "answer_no": "①" if c2 == 15 else "?"}

for kk, v in R.items():
    print(kk, json.dumps({a_: str(b_) for a_, b_ in v.items()}, ensure_ascii=False))
ok = all(v["answer_no"] != "?" for v in R.values())
print("ALL_PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
