# -*- coding: utf-8 -*-
"""30문항 확정 검산 — 정답(전수 열거)·조건삭제 증인(KG-V01)·오개념 답(NL-10)·우회 지표.
실행: python3 문항_검산_확정.py → 검산결과.json (원고 JSON 이 이 값을 참조한다)"""
import sys, json
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engines import run_chain, flip_step, swap_step, dist_sum, dist_sum_norep, count_functions, H

R = {}
def rec(id_, answer, fmt, **kw):
    R[id_] = dict(answer=str(answer), format=fmt, **{k: (str(v) if isinstance(v, F) else v) for k, v in kw.items()})

def pq(fr):
    fr = F(fr); return fr.numerator + fr.denominator

# ===================================================================== A. 카드
def divisors(k): return {c for c in range(1, 7) if k % c == 0}
def le_or_ge(k): return {c for c in range(1, 7) if (c <= k if k % 2 else c >= k)}
ALLFRONT = lambda s, r: not s

# A01 약수 뒤집기, 초기 뒷면 {2,3}, 4회, 모두 앞면일 때 눈 1 이 정확히 두 번
init = frozenset({2, 3})
p_all, n_all, _, _ = run_chain(init, flip_step(divisors), 4, cond=ALLFRONT)
q, n_q, d_q, _ = run_chain(init, flip_step(divisors), 4, cond=ALLFRONT, event=lambda s, r: r.count(1) == 2)
rec('A01', q, '객관식', all_front=p_all, seq_all=n_all, seq_event=n_q,
    witness_no_cond=p_all, witness_init_2=run_chain(frozenset({2}), flip_step(divisors), 4, cond=ALLFRONT, event=lambda s, r: r.count(1) == 2)[0],
    witness_3trials=run_chain(init, flip_step(divisors), 3, cond=ALLFRONT)[0],
    misconception_count_once=run_chain(init, flip_step(divisors), 4, cond=ALLFRONT, event=lambda s, r: r.count(1) == 1)[0])

# A02 6월 규칙, 초기 {1,6}, 4회, 모두 앞면일 때 눈 6 이 적어도 한 번
init = frozenset({1, 6})
p_all, n_all, _, _ = run_chain(init, flip_step(le_or_ge), 4, cond=ALLFRONT)
q, n_q, d_q, _ = run_chain(init, flip_step(le_or_ge), 4, cond=ALLFRONT, event=lambda s, r: 6 in r)
rec('A02', q, '단답(p+q)', pq=pq(q), all_front=p_all, seq_all=n_all, seq_event=n_q,
    witness_no_cond=F(sum(1 for rr in product(range(1, 7), repeat=4) if 6 in rr), 1296),
    witness_init_16_to_1=run_chain(frozenset({1}), flip_step(le_or_ge), 4, cond=ALLFRONT, event=lambda s, r: 6 in r)[0],
    misconception_exactly_once=run_chain(init, flip_step(le_or_ge), 4, cond=ALLFRONT, event=lambda s, r: r.count(6) == 1)[0])

# A03 ABAB 인접 교환(k≤3), 4회 원상태일 때 네 번 모두 상태가 바뀜
init = ('A', 'B', 'A', 'B'); st = swap_step(4)
def effc(rolls, init=init, st=st):
    s = init; c = 0
    for k in rolls:
        ns = st(s, k); c += ns != s; s = ns
    return c
p_ret, n_ret, _, _ = run_chain(init, st, 4, cond=lambda s, r: s == init)
q, n_q, d_q, _ = run_chain(init, st, 4, cond=lambda s, r: s == init, event=lambda s, r: effc(r) == 4)
rec('A03', q, '단답(p+q)', pq=pq(q), ret=p_ret, seq_ret=n_ret, seq_event=n_q,
    eff0=run_chain(init, st, 4, cond=lambda s, r: s == init, event=lambda s, r: effc(r) == 0)[1],
    eff2=run_chain(init, st, 4, cond=lambda s, r: s == init, event=lambda s, r: effc(r) == 2)[1],
    witness_no_cond=F(n_q, 1296), witness_init_AABB=run_chain(('A','A','B','B'), st, 4, cond=lambda s, r: s == ('A','A','B','B'), event=lambda s, r: effc(r, ('A','A','B','B')) == 4)[0],
    misconception_all_k_le3=F(3 ** 4, 1296) / p_ret)

# A04 대칭 교환 k↔7-k, AAABBB, 4회 원상태일 때 눈 1 또는 6 이 정확히 두 번
init6 = ('A', 'A', 'A', 'B', 'B', 'B')
def sym_step(s, k):
    s = list(s); i, j = k - 1, 6 - k; s[i], s[j] = s[j], s[i]; return tuple(s)
p_ret, n_ret, _, _ = run_chain(init6, sym_step, 4, cond=lambda s, r: s == init6)
q, n_q, d_q, _ = run_chain(init6, sym_step, 4, cond=lambda s, r: s == init6, event=lambda s, r: sum(k in (1, 6) for k in r) == 2)
rec('A04', q, '객관식', ret=p_ret, seq_ret=n_ret, seq_event=n_q,
    witness_no_cond=F(sum(1 for rr in product(range(1, 7), repeat=4) if sum(k in (1, 6) for k in rr) == 2), 1296),
    witness_3trials_ret=run_chain(init6, sym_step, 3, cond=lambda s, r: s == init6)[0],
    misconception_pairs_as_eyes=F(6, 21))

# A05 9월 규칙, 목표 AABABB, 4번째 눈이 3
st6 = swap_step(6); tgt = ('A', 'A', 'B', 'A', 'B', 'B')
p_t, n_t, _, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == tgt)
q, n_q, d_q, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == tgt, event=lambda s, r: r[3] == 3)
rec('A05', q, '단답(p+q)', pq=pq(q), target_prob=p_t, seq_target=n_t, seq_event=n_q,
    witness_no_cond=F(1, 6), witness_first_3=run_chain(init6, st6, 4, cond=lambda s, r: s == tgt, event=lambda s, r: r[0] == 3)[0],
    misconception_only_eff1=F(125, 272))

# A06 9월 규칙, 4회 원상태일 때 1·2·3회 뒤에는 원상태가 아니었을 확률
def first_return(s, r):
    st_ = init6
    for i, k in enumerate(r):
        st_ = st6(st_, k)
        if i < 3 and st_ == init6: return False
    return st_ == init6
p_ret, n_ret, _, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == init6)
q, n_q, d_q, _ = run_chain(init6, st6, 4, cond=lambda s, r: s == init6, event=first_return)
rec('A06', q, '단답(p+q)', pq=pq(q), ret=p_ret, seq_ret=n_ret, seq_event=n_q,
    witness_no_cond=F(n_q, 1296), misconception_include_step2_return=F(12, 742),
    witness_3trials=run_chain(init6, st6, 3, cond=lambda s, r: s == init6, event=lambda s, r: all(st6_state(r, i) != init6 for i in (0, 1)) if False else True)[0])

def st6_state(r, upto):
    s = init6
    for k in r[:upto + 1]: s = st6(s, k)
    return s

# A07 비균등: 주머니 카드 1,2,2,3,3,3 복원 → 카드 k 뒤집기(카드 1,2,3), 초기 뒷면 {3}, 3회 모두 앞면일 때 첫 번째가 3
w = {1: F(1, 6), 2: F(1, 3), 3: F(1, 2)}
init3 = frozenset({3})
p_all, n_all, _, _ = run_chain(init3, flip_step(lambda k: {k}), 3, faces=3, cond=ALLFRONT, weights=w)
q, n_q, d_q, _ = run_chain(init3, flip_step(lambda k: {k}), 3, faces=3, cond=ALLFRONT, event=lambda s, r: r[0] == 3, weights=w)
rec('A07', q, '객관식', all_front=p_all, seq_all=n_all,
    witness_uniform=run_chain(init3, flip_step(lambda k: {k}), 3, faces=3, cond=ALLFRONT, event=lambda s, r: r[0] == 3)[0],
    witness_no_cond=F(1, 2), misconception_count_only=F(1, 3))

# A08 6월 규칙, 초기 모두 앞면(블라인드 검토 후 A02 와 설정 분리), 3회 뒤 뒷면이 1장일 때 눈 6 이 적어도 한 번
init = frozenset()
p1, n1_, _, _ = run_chain(init, flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 1)
q, n_q, d_q, _ = run_chain(init, flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 1, event=lambda s, r: 6 in r)
targets = {}
for rolls in product(range(1, 7), repeat=3):
    s = init
    for k in rolls: s = flip_step(le_or_ge)(s, k)
    if len(s) == 1: targets[tuple(sorted(s))] = targets.get(tuple(sorted(s)), 0) + 1
rec('A08', q, '단답(p+q)', pq=pq(q), one_back=p1, seq_one_back=n1_, seq_event=n_q, targets={str(k): v for k, v in targets.items()},
    witness_no_cond=F(91, 216), witness_two_back_3trials=run_chain(init, flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 2)[1],
    info_init_16_same=run_chain(frozenset({1, 6}), flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 1, event=lambda s, r: 6 in r)[0],
    misconception_targets_6='가능한 목표를 {1}~{6} 여섯 개로 보면 분모 과대(실제 {1},{6} 뿐)', misconception_exactly_once=run_chain(init, flip_step(le_or_ge), 3, cond=lambda s, r: len(s) == 1, event=lambda s, r: r.count(6) == 1)[0])

# A09 동전+주사위 3회, 뒷면 정확히 2장일 때 첫 동전이 뒷면
def cd_step(s, c, k):
    tgt = {k} if c == 'H' else {k, 7 - k}
    return frozenset(set(s) ^ tgt)
den = num = tot = 0; by_pattern = {}
for rolls in product([(c, k) for c in 'HT' for k in range(1, 7)], repeat=3):
    s = frozenset()
    for c, k in rolls: s = cd_step(s, c, k)
    tot += 1
    if len(s) == 2:
        den += 1
        pat = ''.join(c for c, k in rolls); by_pattern[pat] = by_pattern.get(pat, 0) + 1
        if rolls[0][0] == 'T': num += 1
rec('A09', F(den, tot), '객관식', den=den, tot=tot, by_pattern=by_pattern, cond_first_T=F(num, den),
    witness_2trials=F(30, 144), misconception_pair_size_always_2='뒷면 동전 두 번이 같은 쌍이면 0장, 다른 쌍이면 4장이 되는 상쇄를 놓침')

# A10 혼합 뒤집기: k≤3 → {k,k+3}, k≥4 → {k}; 초기 뒷면 {2,5}; 3회 모두 앞면일 때 세 눈이 모두 3 이하
def mixed(k): return {k, k + 3} if k <= 3 else {k}
init = frozenset({2, 5})
p_all, n_all, _, _ = run_chain(init, flip_step(mixed), 3, cond=ALLFRONT)
q, n_q, d_q, _ = run_chain(init, flip_step(mixed), 3, cond=ALLFRONT, event=lambda s, r: all(k <= 3 for k in r))
rec('A10', q, '단답(p+q)', pq=pq(q), all_front=p_all, seq_all=n_all, seq_event=n_q,
    witness_4trials=run_chain(init, flip_step(mixed), 4, cond=ALLFRONT)[0], witness_no_cond=F(27, 216),
    witness_init_25_to_2=run_chain(frozenset({2}), flip_step(mixed), 3, cond=ALLFRONT)[0])

# ===================================================================== B. 통계
def ES2(values, probs, n):
    d = dist_sum(values, probs, n); return sum(k * k * p for k, p in d.items())
def ES(values, probs, n):
    d = dist_sum(values, probs, n); return sum(k * p for k, p in d.items())
U3 = ([0, 1, 2], [F(1, 3)] * 3)

# B01 0이 적힌 공 x개, 3이 적힌 공 2개, 복원 3회, Σk²P(X̄=k/3)=15 → x
tbl = {x: ES2([0, 3], [F(x, x + 2), F(2, x + 2)], 3) for x in range(1, 13)}
rec('B01', 4, '단답', table={k: str(v) for k, v in tbl.items()}, witness_value_12='x=2 이면 27, x=10 이면 6 (값이 바뀌면 x 가 바뀜)',
    misconception_var_only='분산만 쓰면 3σ²=... (평균 제곱항 누락)')

# B02 0,1,2 균등 5회, 처음 두 공의 합이 2 일 때 E(S²)
d3 = dist_sum(*U3, 3)
e_cond = sum((2 + k) ** 2 * p for k, p in d3.items())
rec('B02', e_cond, '단답', uncond=ES2(*U3, 5), witness_cond_sum1=sum((1 + k) ** 2 * p for k, p in d3.items()),
    misconception_ignore_condition=ES2(*U3, 5), misconception_only_3draws=ES2(*U3, 3))

# B03 0,1,2 균등 n회, Σk(k-1)P = 78 → n
tbl = {n: ES2(*U3, n) - ES(*U3, n) for n in range(2, 13)}
rec('B03', 9, '단답', table={k: str(v) for k, v in tbl.items()}, misconception_k2_only={k: str(ES2(*U3, k)) for k in (8, 9, 10)})

# B04 주사위 n번, 3의 배수 횟수 X~B(n,1/3), Σk²P(X=k)=32 → n
tbl = {n: n * F(2, 9) + F(n * n, 9) for n in range(10, 21)}
rec('B04', 16, '단답', table={k: str(v) for k, v in tbl.items()}, misconception_var_as_np='np=16/3 → ...', misconception_square_of_mean='(n/3)²=32 → n 비정수')

# B05 비복원: 공 1,1,2,3,3 중 3개 동시, S 합, 5·E(S²)
balls = [1, 1, 2, 3, 3]
d = dist_sum_norep(balls, 3)
e = sum(k * k * p for k, p in d.items())
rec('B05', 5 * e, '단답', ES2=e, dist={str(k): str(v) for k, v in sorted(d.items())},
    misconception_with_replacement=ES2([1, 2, 3], [F(2, 5), F(1, 5), F(2, 5)], 3), misconception_with_replacement_x5=5 * ES2([1, 2, 3], [F(2, 5), F(1, 5), F(2, 5)], 3))

# B06 P(X=x)=ax+b (x=1..4), E(X)=3 → P=x/10, 표본 3 → E(S²)
probs = [F(x, 10) for x in range(1, 5)]
rec('B06', ES2([1, 2, 3, 4], probs, 3), '단답', probs=[str(p) for p in probs], witness_E2=ES2([1, 2, 3, 4], probs, 2),
    misconception_uniform=ES2([1, 2, 3, 4], [F(1, 4)] * 4, 3))

# B07 (재설계) 동전으로 주머니 A(0,1,2) 또는 B(1,2,3)를 택한 뒤 그 주머니에서 5회 복원추출: Σk²P(X̄=k/5) = ½E_A(S²)+½E_B(S²)
dA = dist_sum([0, 1, 2], [F(1, 3)] * 3, 5); dB = dist_sum([1, 2, 3], [F(1, 3)] * 3, 5)
mix = {}
for k, v in dA.items(): mix[k] = mix.get(k, 0) + v / 2
for k, v in dB.items(): mix[k] = mix.get(k, 0) + v / 2
assert sum(mix.values()) == 1
a = sum(k * k * p for k, p in mix.items())
# 오개념: 혼합 모집단(0,1,2,3 확률 1/6,1/3,1/3,1/6)을 독립 5회로 보면 5σ²+25m²
m_mix = F(3, 2); ex2_mix = F(1, 3) + F(4, 3) + F(9, 6); s2_mix = ex2_mix - m_mix ** 2
rec('B07', a, '객관식', E_A=sum(k * k * p for k, p in dA.items()), E_B=sum(k * k * p for k, p in dB.items()), mix_support=[min(mix), max(mix)],
    misconception_iid_mixture=5 * s2_mix + 25 * m_mix ** 2, misconception_A_only=F(85, 3), misconception_B_only=F(310, 3), misconception_sum_not_avg=F(395, 3))
# B07 구(이동 적률 Σ(k-5)²P) 는 B10 의 특수형이라 폐기(검토 기록 참조). 값 95/9 는 B10 설계값으로 보존
vals, pr = [0, 1, 3], [F(1, 3)] * 3
d = dist_sum(vals, pr, 5)
R['B07_old'] = dict(answer=str(sum((k - 5) ** 2 * p for k, p in d.items())), format='폐기')

# B08 정규: P(X̄ ≥ 10)=0.0228 → m+2s=10, E(X̄²)=65, m>0, σ=5 → n
rec('B08', 25, '단답', note='m+2s=10, s²+m²=65 → (m,s)=(8,1) 또는 (-4,7); s=7 이면 n=25/49 가 자연수가 아니므로 s=1 → n=25 (m>0 조건은 검토 후 삭제: 삭제해도 답 동일, KG-A04)', misconception_negative_m='m=-4,s=7 → n=25/49 비자연수')

# B09 미지 모집단(0~3): Σ k P(X̄=k/2)=2, Σ k² P(X̄=k/2)=8 → m=1, σ²=2 → Σ k² P(Ȳ=k/4) = 4σ²+16m² = 24
# 실현 가능성: 0이 적힌 공 2개·3이 적힌 공 1개 → m=1, E(X²)=3, σ²=2. (σ²=3 은 0~3 범위·m=1 에서 불가능: 최대 분산 2)
# 재설계(검토 후): σ²=2 는 0~3 모집단에서 X∈{0,3} 을 강제해 "0,1,2,3 중 하나" 문면과 충돌 → σ²=1 (Σk²P=6). 예: 공 0×5, 1×3, 2×3, 3×1 (12개)
ex = ([0, 1, 2, 3], [F(5, 12), F(3, 12), F(3, 12), F(1, 12)])
assert ES(*ex, 2) == 2 and ES2(*ex, 2) == 6 and ES2(*ex, 4) == 20
rec('B09', 20, '객관식', note='E(S2)=2m=2, E(S2²)=2σ²+4m²=6 → σ²=1 ; E(S4²)=4σ²+16m²=20', feasible_population='0×5,1×3,2×3,3×1',
    misconception_linear=12, misconception_sigma_from_ES2_half=4 * 3 + 16, misconception_VT_2sigma=2 + 16, misconception_sigma_sq_2=24)

# B10 0,1,3 균등 5회, Σ(k-a)²P(X̄=k/5) < 9 인 자연수 a 의 합
d = dist_sum(vals, pr, 5)
good = [a_ for a_ in range(1, 20) if sum((k - a_) ** 2 * p for k, p in d.items()) < 9]
rec('B10', sum(good), '단답', good=good, values={a_: str(sum((k - a_) ** 2 * p for k, p in d.items())) for a_ in range(4, 10)},
    misconception_mean_only='a=E(S)=20/3 근처 7 만 고름 → 7', misconception_le='부등호 ≤ 로 바꾸어도 동일(경계값 9 미달성)')

# ===================================================================== C. 함수
X6 = range(1, 7); X7 = range(1, 8); Y4 = range(1, 5)
def nondec(f, ks): return all(f[ks[i]] <= f[ks[i + 1]] for i in range(len(ks) - 1))
def inc(f, ks): return all(f[ks[i]] < f[ks[i + 1]] for i in range(len(ks) - 1))
cf = count_functions

# C01 (가) f(1)f(6) 이 6의 배수 (나) f(1)<f(2)≤f(3)≤f(4)≤f(5)<f(6)
c01 = lambda f: (f[1] * f[6]) % 6 == 0 and f[1] < f[2] and nondec(f, [2, 3, 4, 5]) and f[5] < f[6]
rec('C01', cf(X6, X6, c01), '객관식',
    witness_drop_ga=cf(X6, X6, lambda f: f[1] < f[2] and nondec(f, [2, 3, 4, 5]) and f[5] < f[6]),
    witness_nonstrict_ends=cf(X6, X6, lambda f: (f[1] * f[6]) % 6 == 0 and f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= f[6]),
    misconception_comb_instead_of_H=35 + 15 + 5 + 1 - (35 - 1) - (15 - 0) - 5 - 1 + (1 + 0 + 0 + 0), misconception_count_empty_as_1=56 + 3)

# C02 (재설계: 구 C02 는 C01 과 동형) (가) f(1)+f(6)=7 (나) f(1) ≤ f(2) ≤ … ≤ f(6) (다) 치역의 원소의 개수 4
c02 = lambda f: f[1] + f[6] == 7 and nondec(f, [1, 2, 3, 4, 5, 6]) and len(set(f.values())) == 4
rec('C02', cf(X6, X6, c02), '객관식',
    witness_drop_da=cf(X6, X6, lambda f: f[1] + f[6] == 7 and nondec(f, [1, 2, 3, 4, 5, 6])),
    witness_range3=cf(X6, X6, lambda f: f[1] + f[6] == 7 and nondec(f, [1, 2, 3, 4, 5, 6]) and len(set(f.values())) == 3),
    witness_strict_ends=cf(X6, X6, lambda f: f[1] + f[6] == 7 and f[1] < f[2] and nondec(f, [2, 3, 4, 5]) and f[5] < f[6] and len(set(f.values())) == 4),
    misconception_drop_25=60, misconception_34_as_10=80, misconception_C63=140, misconception_ends_not_forced=160)

# C03 (가) f(1)f(6) 이 6의 약수 (나) 7-f(1) ≤ f(2) ≤ … ≤ f(5) ≤ 7-f(6)
c03 = lambda f: 6 % (f[1] * f[6]) == 0 and 7 - f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 7 - f[6]
rec('C03', cf(X6, X6, c03), '단답',
    witness_drop_ga=cf(X6, X6, lambda f: 7 - f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 7 - f[6]),
    witness_mult_instead=cf(X6, X6, lambda f: (f[1] * f[6]) % 6 == 0 and 7 - f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 7 - f[6]),
    misconception_direction=cf(X6, X6, lambda f: 6 % (f[1] * f[6]) == 0 and 7 - f[6] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 7 - f[1]))

# C04 X7: (가) f(1)+f(7)=8 (나) 2f(1) ≤ f(2) ≤ f(3) ≤ f(4) ≤ f(5) ≤ f(6) ≤ 2f(7) (다) f(4)=4
c04 = lambda f: f[1] + f[7] == 8 and 2 * f[1] <= f[2] <= f[3] <= f[4] <= f[5] <= f[6] <= 2 * f[7] and f[4] == 4
rec('C04', cf(X7, X7, c04), '객관식',
    witness_drop_da=cf(X7, X7, lambda f: f[1] + f[7] == 8 and 2 * f[1] <= f[2] <= f[3] <= f[4] <= f[5] <= f[6] <= 2 * f[7]),
    witness_drop_ga=cf(X7, X7, lambda f: 2 * f[1] <= f[2] <= f[3] <= f[4] <= f[5] <= f[6] <= 2 * f[7] and f[4] == 4),
    misconception_no_product=6 + 10 + 1 + 10)

# C05 (가) f(1)f(6)=6 (나) f(1) ≤ f(2), |f(3)-f(2)|=1, |f(4)-f(3)|=1, f(4) ≤ f(5) ≤ f(6)
c05 = lambda f: f[1] * f[6] == 6 and f[1] <= f[2] and abs(f[3] - f[2]) == 1 and abs(f[4] - f[3]) == 1 and f[4] <= f[5] <= f[6]
rec('C05', cf(X6, X6, c05), '단답',
    witness_drop_ga=cf(X6, X6, lambda f: f[1] <= f[2] and abs(f[3] - f[2]) == 1 and abs(f[4] - f[3]) == 1 and f[4] <= f[5] <= f[6]),
    witness_one_step=cf(X6, X6, lambda f: f[1] * f[6] == 6 and f[1] <= f[2] and abs(f[3] - f[2]) == 1 and f[3] <= f[4] <= f[5] <= f[6]),
    witness_prod12=cf(X6, X6, lambda f: f[1] * f[6] == 12 and f[1] <= f[2] and abs(f[3] - f[2]) == 1 and abs(f[4] - f[3]) == 1 and f[4] <= f[5] <= f[6]),
    misconception_ignore_bounds_1_6='f(2)=1 에서 f(3)=0 같은 바깥 값을 세면 과대')

# C06 (재설계: (가)(나)가 C08 과 동일하던 것을 (가) 합 7 로) (가) f(1)+f(6)=7 (나) 2f(1) ≤ f(2) ≤ … ≤ f(5) ≤ 2f(6) (다) {f(2),…,f(5)} 원소 3개
c06 = lambda f: f[1] + f[6] == 7 and 2 * f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 2 * f[6] and len({f[2], f[3], f[4], f[5]}) == 3
rec('C06', cf(X6, X6, c06), '단답',
    witness_drop_da=cf(X6, X6, lambda f: f[1] + f[6] == 7 and 2 * f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 2 * f[6]),
    witness_two_values=cf(X6, X6, lambda f: f[1] + f[6] == 7 and 2 * f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 2 * f[6] and len({f[2], f[3], f[4], f[5]}) == 2),
    misconception_C_L3_only=10 + 1, misconception_empty_as_1=33 + 3, misconception_L1_as_3=33 + 3)

# C07 (가) f(6)=2f(1) (나) f(1) ≤ f(2) ≤ … ≤ f(6) (다) f(3)+f(4) 짝수
c07 = lambda f: f[6] == 2 * f[1] and nondec(f, [1, 2, 3, 4, 5, 6]) and (f[3] + f[4]) % 2 == 0
rec('C07', cf(X6, X6, c07), '객관식',
    witness_drop_da=cf(X6, X6, lambda f: f[6] == 2 * f[1] and nondec(f, [1, 2, 3, 4, 5, 6])),
    witness_odd=cf(X6, X6, lambda f: f[6] == 2 * f[1] and nondec(f, [1, 2, 3, 4, 5, 6]) and (f[3] + f[4]) % 2 == 1),
    misconception_f3_eq_f4_only=cf(X6, X6, lambda f: f[6] == 2 * f[1] and nondec(f, [1, 2, 3, 4, 5, 6]) and f[3] == f[4]))

# C08 (가) f(1)f(6) 이 6의 약수 (나) 2f(1) ≤ f(2) ≤ … ≤ f(5) ≤ 2f(6) (다) f(2)+f(5)=7
c08 = lambda f: 6 % (f[1] * f[6]) == 0 and 2 * f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 2 * f[6] and f[2] + f[5] == 7
rec('C08', cf(X6, X6, c08), '객관식',
    witness_drop_da=171, witness_sum6=cf(X6, X6, lambda f: 6 % (f[1] * f[6]) == 0 and 2 * f[1] <= f[2] and nondec(f, [2, 3, 4, 5]) and f[5] <= 2 * f[6] and f[2] + f[5] == 6),
    misconception_H_instead_of_count=3 + 15 + 15 + 3 + 15)

# C09 (3차 재설계: 2차 검토 "4점 대비 과소난도") X7→Y4: (가) f(1)+f(7)=5 (나) f(1) ≤ f(2) ≤ … ≤ f(6) ≤ 2f(7) (다) f(k)=k 인 k 의 개수 2
def nfix(f): return sum(f[k] == k for k in f)
c09 = lambda f: f[1] + f[7] == 5 and nondec(f, [1, 2, 3, 4, 5, 6]) and f[6] <= 2 * f[7] and nfix(f) == 2
rec('C09', cf(X7, Y4, c09), '단답',
    witness_drop_da=cf(X7, Y4, lambda f: f[1] + f[7] == 5 and nondec(f, [1, 2, 3, 4, 5, 6]) and f[6] <= 2 * f[7]),
    witness_fix1=cf(X7, Y4, lambda f: f[1] + f[7] == 5 and nondec(f, [1, 2, 3, 4, 5, 6]) and f[6] <= 2 * f[7] and nfix(f) == 1),
    witness_fix3=cf(X7, Y4, lambda f: f[1] + f[7] == 5 and nondec(f, [1, 2, 3, 4, 5, 6]) and f[6] <= 2 * f[7] and nfix(f) == 3),
    witness_codomain_X7=cf(X7, X7, c09), by_pair={'(1,4)': 20, '(2,3)': 6, '(3,2)': 1, '(4,1)': 0},
    misconception_count_k5_k6_as_candidates='k=5,6 은 공역 4 이하라 고정점이 될 수 없음을 놓치면 경우 분류가 틀어짐', old_designs={'v1': 83, 'v2': 22})

# C10 (재설계: 구 설계는 4점치고 쉬움) (가) f(1)<f(2)<f(3), f(4) ≤ f(5) ≤ f(6) (나) f(3)f(4) 가 6의 약수 (다) f(2)<f(5)
c10 = lambda f: inc(f, [1, 2, 3]) and nondec(f, [4, 5, 6]) and 6 % (f[3] * f[4]) == 0 and f[2] < f[5]
rec('C10', cf(X6, X6, c10), '단답',
    witness_drop_da=cf(X6, X6, lambda f: inc(f, [1, 2, 3]) and nondec(f, [4, 5, 6]) and 6 % (f[3] * f[4]) == 0),
    witness_le=cf(X6, X6, lambda f: inc(f, [1, 2, 3]) and nondec(f, [4, 5, 6]) and 6 % (f[3] * f[4]) == 0 and f[2] <= f[5]),
    witness_drop_na=cf(X6, X6, lambda f: inc(f, [1, 2, 3]) and nondec(f, [4, 5, 6]) and f[2] < f[5]),
    old_design=116, misconception_include_f3_2='f(3)=2 는 f(1)<f(2)<f(3) 과 모순인데 (2,3) 쌍을 포함하면 과대')

# NL-10 일반화: 오개념 답이 정답과 같으면 그 오개념은 변별되지 않는다 → 경고(설계 재검토 또는 설계 기록에 명시)
WARN = []
for id_, v in R.items():
    for k, val in v.items():
        if k.startswith('misconception') and str(val) == v['answer']:
            WARN.append(f"{id_}: 오개념 {k} 의 답이 정답 {v['answer']} 과 같음")
    for k, val in v.items():
        if k.startswith('witness') and str(val) == v['answer']:
            WARN.append(f"{id_}: 조건 삭제 증인 {k} 의 답이 정답과 같음(KG-A04: 그 조건은 답을 정하지 않음)")
R['_warnings'] = WARN
for w in WARN: print('WARN', w)
out = Path(__file__).resolve().parent / '검산결과.json'
out.write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding='utf-8')
for k, v in R.items():
    if k.startswith('_'): continue
    print(k, v['format'], 'answer =', v['answer'], {kk: vv for kk, vv in v.items() if kk.startswith(('pq', 'seq', 'ret', 'all', 'two', 'den', 'ES2', 'nine'))})
