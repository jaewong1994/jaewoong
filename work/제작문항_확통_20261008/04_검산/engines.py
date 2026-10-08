# -*- coding: utf-8 -*-
"""확통 제작 검산 엔진 — 전수 열거 + Fraction (NL-05). 설계값과 계산값을 대조하는 데만 쓴다.
A: 카드 상태 전이(뒤집기·자리 바꾸기)  B: 이산분포·표본합 적률  C: 함수 개수 전수."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
from math import comb


# ------------------------------------------------------------------ A. 상태 전이
def run_chain(init, step, trials, faces=6, cond=None, event=None, weights=None):
    """init: 초기 상태(해시 가능). step(state, k) → 새 상태. trials: 시행 횟수.
    cond(state, rolls) → 분모 사건, event(state, rolls) → 분자 사건(None 이면 cond 의 확률).
    weights: 눈 k 의 확률(None 이면 1/faces). 반환 (확률, 분자수, 분모수, 전체)"""
    num = den = 0
    tot = F(0)
    numw = denw = F(0)
    for rolls in product(range(1, faces + 1), repeat=trials):
        s = init
        for k in rolls:
            s = step(s, k)
        w = F(1)
        if weights:
            for k in rolls:
                w *= weights[k]
        else:
            w = F(1, faces ** trials)
        tot += w
        if cond is None or cond(s, rolls):
            den += 1
            denw += w
            if event is None or event(s, rolls):
                num += 1
                numw += w
    if event is None:
        return denw, den, 6 ** trials, tot
    return (numw / denw if denw else None), num, den, tot


def flip_step(flipset_of):
    """flipset_of(k) → 뒤집을 카드 집합. 상태 = 뒷면 카드 frozenset."""
    def step(s, k):
        return frozenset(set(s) ^ set(flipset_of(k)))
    return step


def swap_step(n):
    """k≤n-1 → 자리 k,k+1 교환, 그 외 유지. 상태 = tuple."""
    def step(s, k):
        if k <= n - 1:
            s = list(s)
            s[k - 1], s[k] = s[k], s[k - 1]
            return tuple(s)
        return s
    return step


# ------------------------------------------------------------------ B. 적률
def dist_sum(values, probs, n):
    """독립 n회 합 S 의 분포 {s: P}. values/probs 는 병렬 리스트(Fraction)."""
    d = {0: F(1)}
    for _ in range(n):
        nd = Counter()
        for s, p in d.items():
            for v, q in zip(values, probs):
                nd[s + v] += p * q
        d = dict(nd)
    return d


def moments(values, probs):
    m = sum(v * p for v, p in zip(values, probs))
    v = sum((x - m) ** 2 * p for x, p in zip(values, probs))
    return m, v


def dist_sum_norep(balls, n):
    """비복원 n개 동시 추출의 합 분포(공은 구별)."""
    c = Counter()
    for idx in combinations(range(len(balls)), n):
        c[sum(balls[i] for i in idx)] += 1
    tot = comb(len(balls), n)
    return {k: F(v, tot) for k, v in c.items()}


# ------------------------------------------------------------------ C. 함수 개수
def count_functions(X, Y, cond):
    """f: X→Y 전수. cond(f: dict) → bool."""
    cnt = 0
    xs = list(X)
    for vals in product(Y, repeat=len(xs)):
        f = dict(zip(xs, vals))
        if cond(f):
            cnt += 1
    return cnt


def H(n, r):
    """중복조합 nHr"""
    return comb(n + r - 1, r) if n > 0 or r == 0 else 0


def simplify_answer(fr):
    fr = F(fr)
    return fr, fr.numerator + fr.denominator
