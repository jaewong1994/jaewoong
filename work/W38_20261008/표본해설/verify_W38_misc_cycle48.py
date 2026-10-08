# -*- coding: utf-8 -*-
"""W38 CALCa·GEOa·ALGa (cycle48) 독립 검산 — 수치 극한·정의 대입. 읽기 전용, DB 없음.
(버킷별 파일 규칙상 verify_W38_CALCa/GEOa/ALGa 는 이 파일을 그대로 호출한다.)"""
import json
import sys

import sympy as sp

R = {}

# 17507: a_n = 10 + e_n (e_n→0) 을 수치로 대입해 n 이 커질 때 식의 값이 5 로 가는지 본다. 다른 경로: 임의의 감소 오차 e_n=1/n
n = sp.symbols("n", positive=True)
a_n = 10 + 1 / n  # lim (a_n+2)/2 = 6 을 만족하는 한 수열
val = sp.limit((n * a_n + 1) / (a_n + 2 * n), n, sp.oo)
a_n2 = 10 - 3 / sp.sqrt(n)  # 다른 수열로도 같은지
val2 = sp.limit((n * a_n2 + 1) / (a_n2 + 2 * n), n, sp.oo)
R[17507] = {"limit_seq1": val, "limit_seq2": val2, "answer_no": "⑤" if val == 5 and val2 == 5 else "?"}

# 18351: 포물선 y^2 = 8x 의 초점을 정의(초점 (p,0), 준선 x=-p 까지 거리가 같음)로 수치 확인
X, Y, P = sp.symbols("X Y P")
# 곡선 위 점 (2, 4): 초점 (P,0) 까지 거리 = 준선 x=-P 까지 거리
eq = sp.Eq(sp.sqrt((2 - P)**2 + 16), 2 + P)
sol = [s for s in sp.solve(eq, P) if s > 0]
R[18351] = {"p": sol, "answer_no": "②" if sol == [2] else "?"}

# 10722: f(x) 정의 없음 — 조건 결손. (참고: f(x)=a^x 이면 4a^9=2^8 → a=2^(2/3) 로 ② 가 나오지만 채우지 않는다)
R[10722] = {"status": "원문 결함: 조건 결손 — 함수 f 의 정의가 본문에 없음(상수 a 가 f 에만 등장). 검산 생략", "answer_no": "needs_review"}

for kk, v in R.items():
    print(kk, json.dumps({a_: str(b_) for a_, b_ in v.items()}, ensure_ascii=False))
ok = all(v["answer_no"] != "?" for v in R.values())
print("ALL_PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
