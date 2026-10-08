# -*- coding: utf-8 -*-
"""주제 A(카드 상태 전이 · 독립시행 + 조건부확률) 설계 후보 전수 계산. 수치 탐색용(설계 단계)."""
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engines import run_chain, flip_step, swap_step

def divisors(k): return {c for c in range(1, 7) if k % c == 0}
def multiples(k): return {c for c in range(1, 7) if c % k == 0}
def le_or_ge(k): return {c for c in range(1, 7) if (c <= k if k % 2 else c >= k)}

out = {}

# A01 약수 뒤집기: 초기 뒷면 집합·시행 횟수를 탐색해 '모두 앞면' 확률이 깔끔한 설계를 찾는다
res = []
for trials in (3, 4):
    for init in [frozenset(s) for r in (1, 2, 3) for s in __import__('itertools').combinations(range(1, 7), r)]:
        p, n, d, _ = run_chain(init, flip_step(divisors), trials, cond=lambda s, r: not s)
        if n:
            res.append((trials, tuple(sorted(init)), p, n))
res.sort(key=lambda t: (t[0], -t[3]))
out['A01_divisor_scan'] = [(t, i, str(p), n) for t, i, p, n in res if n >= 20][:30]

# A01 확정 후보: 초기 뒷면 {1}, 3회 → 모두 앞면 ; 조건부: 모두 앞면일 때 눈 1이 한 번도 안 나올 확률 등
for init in (frozenset({1}), frozenset({1, 2}), frozenset({1, 6}), frozenset({1, 4})):
    p, n, d, _ = run_chain(init, flip_step(divisors), 3, cond=lambda s, r: not s)
    q, n2, d2, _ = run_chain(init, flip_step(divisors), 3, cond=lambda s, r: not s, event=lambda s, r: 1 not in r)
    q3, n3, d3, _ = run_chain(init, flip_step(divisors), 3, cond=lambda s, r: not s, event=lambda s, r: r[0] == 6)
    out[f'A01_init{sorted(init)}'] = dict(all_front=str(p), n=n, cond_no1=str(q), n2=n2, cond_first6=str(q3), n3=n3)

# A02 6월 규칙 그대로 + 조건부(모두 앞면일 때 처음 두 눈이 같음 / 눈의 합이 짝수)
init = frozenset({1, 6})
p, n, d, _ = run_chain(init, flip_step(le_or_ge), 4, cond=lambda s, r: not s)
q1, a1, b1, _ = run_chain(init, flip_step(le_or_ge), 4, cond=lambda s, r: not s, event=lambda s, r: r[0] == r[1])
q2, a2, b2, _ = run_chain(init, flip_step(le_or_ge), 4, cond=lambda s, r: not s, event=lambda s, r: sum(r) % 2 == 0)
q3, a3, b3, _ = run_chain(init, flip_step(le_or_ge), 4, cond=lambda s, r: not s, event=lambda s, r: 6 in r)
out['A02_june_cond'] = dict(all=str(p), first_two_equal=str(q1), a1=a1, b1=b1, sum_even=str(q2), a2=a2, has6=str(q3), a3=a3)

# A03 AABB 4장, k≤3 교환, 4~6 유지, 4회 뒤 원상태일 때 유효 이동이 정확히 2번일 확률 / 3번째 눈이 2일 확률
init = ('A', 'A', 'B', 'B')
st = swap_step(4)
def eff_count(rolls):
    s = list(init); c = 0
    for k in rolls:
        ns = st(tuple(s), k)
        if ns != tuple(s): c += 1
        s = list(ns)
    return c
p, n, d, _ = run_chain(init, st, 4, cond=lambda s, r: s == init)
q, a, b, _ = run_chain(init, st, 4, cond=lambda s, r: s == init, event=lambda s, r: eff_count(r) == 2)
q2, a2, b2, _ = run_chain(init, st, 4, cond=lambda s, r: s == init, event=lambda s, r: r[2] == 2)
out['A03_AABB'] = dict(ret=str(p), n=n, eff2=str(q), a=a, third2=str(q2), a2=a2)

# A04 AAABBB, 눈 k → 자리 k 와 7-k 교환(3쌍 독립 홀짝), 4회 뒤 원상태 / 조건부: 3,4번째 눈이 같은 쌍
init = ('A', 'A', 'A', 'B', 'B', 'B')
def sym_step(s, k):
    s = list(s); i, j = k - 1, 6 - k
    s[i], s[j] = s[j], s[i]
    return tuple(s)
pair = lambda k: min(k, 7 - k)
p, n, d, _ = run_chain(init, sym_step, 4, cond=lambda s, r: s == init)
q, a, b, _ = run_chain(init, sym_step, 4, cond=lambda s, r: s == init, event=lambda s, r: pair(r[2]) == pair(r[3]))
q2, a2, b2, _ = run_chain(init, sym_step, 4, cond=lambda s, r: s == init, event=lambda s, r: len({pair(k) for k in r}) == 1)
out['A04_sym'] = dict(ret=str(p), n=n, last_two_same_pair=str(q), a=a, all_same_pair=str(q2), a2=a2)

# A05 AAABBB 인접 교환(9월 규칙) — 목표 상태가 원상태가 아닌 AABABB 일 때 조건부: 4번째 눈이 3
init6 = ('A', 'A', 'A', 'B', 'B', 'B'); st6 = swap_step(6)
tgt = ('A', 'A', 'B', 'A', 'B', 'B')
p, n, d, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == tgt)
q, a, b, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == tgt, event=lambda s, r: r[3] == 3)
q2, a2, b2, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == tgt, event=lambda s, r: r[0] == 3)
out['A05_target_AABABB'] = dict(p=str(p), n=n, last3=str(q), a=a, first3=str(q2), a2=a2)

# A06 처음으로 되돌아옴(first return): AAABBB 인접 교환, 4회 뒤 원상태이면서 1·2·3회 뒤에는 원상태가 아니었을 확률
def first_return_cond(s, r):
    st_ = list(init6)
    for i, k in enumerate(r):
        st_ = list(st6(tuple(st_), k))
        if i < 3 and tuple(st_) == init6: return False
    return tuple(st_) == init6
p, n, d, _ = run_chain(init6, st6, 4, cond=first_return_cond)
out['A06_first_return'] = dict(p=str(p), n=n)

# A07 비균등 눈: 주머니 카드 1,1,2,3 중 한 장(복원) → 눈 k(확률 1/2,1/4,1/4), 카드 3장 {1,2,3} 뒤집기: k → 카드 k 뒤집기, 초기 뒷면 {3}, 3회 뒤 모두 앞면
def flip_single(k): return {k}
w = {1: F(1, 2), 2: F(1, 4), 3: F(1, 4)}
init3 = frozenset({3})
p, n, d, _ = run_chain(init3, flip_step(flip_single), 3, faces=3, cond=lambda s, r: not s, weights=w)
q, a, b, _ = run_chain(init3, flip_step(flip_single), 3, faces=3, cond=lambda s, r: not s, event=lambda s, r: r[0] == 3, weights=w)
out['A07_weighted'] = dict(all=str(p), n=n, first3=str(q))

# A08 앞면 개수 조건: 6월 규칙, 초기 뒷면 {1,6}, 3회 뒤 앞면이 정확히 4장일 확률 / 조건부 2번째 눈 홀수
init = frozenset({1, 6})
p, n, d, _ = run_chain(init, flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 2)
q, a, b, _ = run_chain(init, flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 2, event=lambda s, r: r[1] % 2 == 1)
out['A08_count4front'] = dict(p=str(p), n=n, second_odd=str(q), a=a)

# A09 동전+주사위: 동전 앞면이면 카드 k 뒤집기, 뒷면이면 카드 k 와 7-k 뒤집기. 카드 6장 모두 앞면에서 시작, 3회 뒤 뒷면이 정확히 2장
def coin_dice_step(s, k):
    c, k = k  # k = (coin, die)
    tgt = {k} if c == 'H' else {k, 7 - k}
    return frozenset(set(s) ^ tgt)
num = den = 0; tot = 0
for rolls in product([(c, k) for c in 'HT' for k in range(1, 7)], repeat=3):
    s = frozenset()
    for r in rolls: s = coin_dice_step(s, r)
    tot += 1
    if len(s) == 2:
        den += 1
        if rolls[0][0] == 'T': num += 1
out['A09_coin_dice'] = dict(p=str(F(den, tot)), den=den, tot=tot, cond_firstT=str(F(num, den)) if den else None)

# A10 두 주머니 혼합: 눈 k 가 3 이하이면 카드 k 와 k+3 을, 4 이상이면 카드 k 만 뒤집기. 초기 뒷면 {2,5}, 4회 뒤 모두 앞면 / 조건부 눈 6 포함
def mixed(k): return {k, k + 3} if k <= 3 else {k}
init = frozenset({2, 5})
p, n, d, _ = run_chain(init, flip_step(mixed), 4, cond=lambda s, r: not s)
q, a, b, _ = run_chain(init, flip_step(mixed), 4, cond=lambda s, r: not s, event=lambda s, r: 6 in r)
q2, a2, b2, _ = run_chain(init, flip_step(mixed), 4, cond=lambda s, r: not s, event=lambda s, r: all(k <= 3 for k in r))
out['A10_mixed'] = dict(all=str(p), n=n, has6=str(q), a=a, all_le3=str(q2), a2=a2)

import json
for k,v in out.items(): print(k, json.dumps(v, ensure_ascii=False))
