# -*- coding: utf-8 -*-
"""원문 4제 전수 열거 검산(Fraction). 출처: 2026 6월 28번(25019), 9월 28번(27035), 9월 30번(27037), 2025 수능 28번(24943)."""
from fractions import Fraction as F
from itertools import product
from collections import Counter

# 6월 28번: 카드 1~6, 초기 뒷면={1,6}. k 홀수 → ≤k 뒤집기, k 짝수 → ≥k 뒤집기. 4회 뒤 모두 앞면.
def june28():
    def flip(state, k):
        s = set(state)
        tgt = {c for c in range(1, 7) if (c <= k if k % 2 else c >= k)}
        return frozenset(s ^ tgt)
    init = frozenset({1, 6})  # 뒷면 집합
    cnt = 0
    for rolls in product(range(1, 7), repeat=4):
        s = init
        for k in rolls: s = flip(s, k)
        if not s: cnt += 1
    return F(cnt, 6**4), cnt

# 9월 28번: AAABBB, k≤5 → k,k+1 교환, 6 → 유지. 4회 뒤 AAABBB 일 때 3번째가 6일 확률.
def sep28():
    init = ('A','A','A','B','B','B')
    num = den = 0
    for rolls in product(range(1, 7), repeat=4):
        s = list(init)
        for k in rolls:
            if k <= 5: s[k-1], s[k] = s[k], s[k-1]
        if tuple(s) == init:
            den += 1
            if rolls[2] == 6: num += 1
    return F(num, den), num, den

# 9월 30번: 0,1,2 복원추출 5회, S=합. Σ k^2 P(S=k)=E(S^2). 6a?
def sep30():
    c = Counter(sum(t) for t in product((0,1,2), repeat=5))
    a = sum(F(k*k*c[k], 3**5) for k in range(0, 11))
    return a, 6*a

# 2025 수능 28번: X={1..6}, f(1)f(6) | 6, 2f(1)≤f(2)≤f(3)≤f(4)≤f(5)≤2f(6)
def su28():
    cnt = 0
    for f in product(range(1, 7), repeat=6):
        f1, f2, f3, f4, f5, f6 = f
        if 6 % (f1*f6) == 0 and 2*f1 <= f2 <= f3 <= f4 <= f5 <= 2*f6: cnt += 1
    return cnt

if __name__ == "__main__":
    print("6월28", june28(), "기대 10/81")
    print("9월28", sep28(), "기대 69/371")
    print("9월30", sep30(), "기대 170")
    print("수능28", su28(), "기대 171")
