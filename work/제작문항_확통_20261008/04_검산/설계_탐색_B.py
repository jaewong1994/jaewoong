# -*- coding: utf-8 -*-
"""주제 B(표본평균·적률 번역) 설계 후보 계산."""
import sys, json
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engines import dist_sum, moments, dist_sum_norep

def ES2(values, probs, n):
    d = dist_sum(values, probs, n)
    return sum(k * k * p for k, p in d.items())

out = {}
u3 = ([0, 1, 2], [F(1, 3)] * 3)

# B01 역방향: 1이 적힌 공 x개, 3이 적힌 공 2개 → 복원 3회, E(S^2) 가 정수가 되는 x 와 값
cands = []
for x in range(1, 13):
    vals = [1, 3]; probs = [F(x, x + 2), F(2, x + 2)]
    for n in (2, 3, 4):
        v = ES2(vals, probs, n)
        if v.denominator == 1: cands.append((x, n, int(v)))
out['B01_scan'] = cands

# B02 조건부: 0,1,2 균등 5회, 조건 '2가 한 번도 안 나옴' 하에서 E(S^2) ; 조건 '첫 공이 2' 하에서
d_full = dist_sum(*u3, 5)
# 조건 2 없음: 각 회 {0,1} 균등
es2_no2 = ES2([0, 1], [F(1, 2)] * 2, 5)
es2_first2 = sum((2 + k) ** 2 * p for k, p in dist_sum(*u3, 4).items())
out['B02'] = dict(E_S2_no2=str(es2_no2), E_S2_first2=str(es2_first2), E_S2_full=str(sum(k*k*p for k,p in d_full.items())))

# B03 Σ k(k-1)P = E(S^2)-E(S) 로 n 결정 (0,1,2 균등)
out['B03'] = {n: str(ES2(*u3, n) - n) for n in range(2, 11)}

# B04 이항분포: X~B(n,p), E(X^2)=np(1-p)+n^2p^2 가 정수가 되는 (n,p)
cands = []
for n in range(2, 21):
    for p in (F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 6)):
        v = n * p * (1 - p) + n * n * p * p
        if v.denominator == 1: cands.append((n, str(p), int(v)))
out['B04_binom'] = cands

# B05 비복원 vs 복원: 공 1,2,3,4 에서 2개 동시 / 복원 2회
S_norep = dist_sum_norep([1, 2, 3, 4], 2)
es2_norep = sum(k*k*p for k, p in S_norep.items())
es2_rep = ES2([1, 2, 3, 4], [F(1, 4)] * 4, 2)
out['B05'] = dict(norep=str(es2_norep), rep=str(es2_rep), sum=str(es2_norep + es2_rep))

# B06 분포 결정: P(X=x)=ax+b (x=1..4), E(X)=3 → a,b → 표본 2개 E(S^2)
import sympy as sp
a, b = sp.symbols('a b')
sol = sp.solve([sum((a*x + b) for x in range(1, 5)) - 1, sum(x*(a*x + b) for x in range(1, 5)) - 3], [a, b])
probs = [F(str(sol[a]*x + sol[b])) for x in range(1, 5)]
out['B06'] = dict(a=str(sol[a]), b=str(sol[b]), probs=[str(p) for p in probs], ES2_n2=str(ES2([1,2,3,4], probs, 2)), ES2_n3=str(ES2([1,2,3,4], probs, 3)))

# B07 Σ(k-c)^2 P: 모집단 0,1,3 균등 5회, c=5
vals = [0, 1, 3]; pr = [F(1, 3)] * 3
d = dist_sum(vals, pr, 5)
out['B07'] = {c: str(sum((k - c) ** 2 * p for k, p in d.items())) for c in (4, 5, 6, 7)}

# B08 정규 모집단: m+2s=10, s^2+m^2=65 → (m,s)=(8,1),(−4,7); σ=4 → n=16
out['B08'] = dict(note='m=8,s=1 → n=16 ; 또 다른 해 m=-4,s=7 → m>0 조건 필요')

# B09 1,2,3 균등 n회 E(S^2)
out['B09'] = {n: str(ES2([1, 2, 3], [F(1, 3)] * 3, n)) for n in range(2, 10)}

# B10 4개 공 1,1,2,4 복원 4회 E(S^2) (숫자변형 수준 → 보조/빌드업용)
out['B10_numeric'] = str(ES2([1, 1, 2, 4], [F(1, 4)] * 4, 4))

for k,v in out.items(): print(k, json.dumps(v, ensure_ascii=False))
