# -*- coding: utf-8 -*-
"""주제 C(끝값이 가운데 범위를 정하는 함수 개수) 설계 후보 전수."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engines import count_functions

X6 = range(1, 7); X7 = range(1, 8)
out = {}
def nondec(f, ks): return all(f[ks[i]] <= f[ks[i + 1]] for i in range(len(ks) - 1))
def inc(f, ks): return all(f[ks[i]] < f[ks[i + 1]] for i in range(len(ks) - 1))

# C01 곱=12, 가운데 비감소, 양끝 엄격: f(1) < f(2) ≤ f(3) ≤ f(4) ≤ f(5) < f(6)
out['C01'] = count_functions(X6, X6, lambda f: f[1]*f[6] == 12 and f[1] < f[2] and nondec(f, [2,3,4,5]) and f[5] < f[6])
# C01b 곱이 6의 배수
out['C01b_mult6'] = count_functions(X6, X6, lambda f: (f[1]*f[6]) % 6 == 0 and f[1] < f[2] and nondec(f, [2,3,4,5]) and f[5] < f[6])

# C02 합=7 + 가운데 f(1)+1 ≤ f(2) ≤ … ≤ f(5) ≤ f(6)-1
out['C02'] = count_functions(X6, X6, lambda f: f[1]+f[6] == 7 and f[1]+1 <= f[2] and nondec(f, [2,3,4,5]) and f[5] <= f[6]-1)

# C03 대칭: 7-f(1) ≤ f(2) ≤ … ≤ f(5) ≤ 7-f(6), (가) f(1) f(6) 이 6의 약수
out['C03'] = count_functions(X6, X6, lambda f: 6 % (f[1]*f[6]) == 0 and 7-f[1] <= f[2] and nondec(f,[2,3,4,5]) and f[5] <= 7-f[6])
# C03b (가) f(1)+f(6)=7
out['C03b'] = count_functions(X6, X6, lambda f: f[1]+f[6] == 7 and 7-f[1] <= f[2] and nondec(f,[2,3,4,5]) and f[5] <= 7-f[6])

# C04 X7: f(1)+f(7)=8, 2f(1) ≤ f(2) ≤ f(3) ≤ 4 ≤ f(5) ≤ f(6) ≤ 2f(7), f(4)=4
out['C04'] = count_functions(X7, X7, lambda f: f[1]+f[7] == 8 and 2*f[1] <= f[2] <= f[3] <= 4 <= f[5] <= f[6] <= 2*f[7] and f[4] == 4)
# C04b f(4) 자유(4 ≤ 가 아니라 f(3) ≤ f(4) ≤ f(5))
out['C04b'] = count_functions(X7, X7, lambda f: f[1]+f[7] == 8 and 2*f[1] <= f[2] <= f[3] <= f[4] <= f[5] <= f[6] <= 2*f[7])

# C05 경로: (가) f(1)f(6) | 6 ; (나) f(1) ≤ f(2), |f(3)-f(2)|=|f(4)-f(3)|=|f(5)-f(4)|=1, f(5) ≤ f(6)
out['C05'] = count_functions(X6, X6, lambda f: 6 % (f[1]*f[6]) == 0 and f[1] <= f[2] and all(abs(f[k+1]-f[k]) == 1 for k in (2,3,4)) and f[5] <= f[6])
# C05b 2f(1) ≤ f(2), f(5) ≤ 2f(6)
out['C05b'] = count_functions(X6, X6, lambda f: 6 % (f[1]*f[6]) == 0 and 2*f[1] <= f[2] and all(abs(f[k+1]-f[k]) == 1 for k in (2,3,4)) and f[5] <= 2*f[6])

# C06 치역 2개: (가) f(1)f(6)|6, (나) 2f(1) ≤ f(2) ≤ … ≤ f(5) ≤ 2f(6), 가운데 네 값의 서로 다른 개수가 2
out['C06'] = count_functions(X6, X6, lambda f: 6 % (f[1]*f[6]) == 0 and 2*f[1] <= f[2] and nondec(f,[2,3,4,5]) and f[5] <= 2*f[6] and len({f[2],f[3],f[4],f[5]}) == 2)

# C07 f(6)=2f(1) ; f(1) ≤ f(2) ≤ … ≤ f(6), f(3)+f(4) 짝수
out['C07'] = count_functions(X6, X6, lambda f: f[6] == 2*f[1] and nondec(f,[1,2,3,4,5,6]) and (f[3]+f[4]) % 2 == 0)
out['C07b'] = count_functions(X6, X6, lambda f: f[6] == 2*f[1] and nondec(f,[1,2,3,4,5,6]))

# C08 가운데 합 고정: (가) f(1)f(6)|6 (나) 2f(1) ≤ f(2) ≤ … ≤ f(5) ≤ 2f(6) (다) f(2)+f(5)=7
out['C08'] = count_functions(X6, X6, lambda f: 6 % (f[1]*f[6]) == 0 and 2*f[1] <= f[2] and nondec(f,[2,3,4,5]) and f[5] <= 2*f[6] and f[2]+f[5] == 7)

# C09 X7→Y4: (가) f(1)+f(7)=5 (나) f(1) ≤ f(2) ≤ … ≤ f(6) ≤ f(7)+1 ; 공역 {1,2,3,4}
Y4 = range(1, 5)
out['C09'] = count_functions(X7, Y4, lambda f: f[1]+f[7] == 5 and nondec(f,[1,2,3,4,5,6]) and f[6] <= f[7]+1)

# C10 두 사슬: f(1) ≤ f(2) ≤ f(3), f(4) ≤ f(5) ≤ f(6), f(3) f(4) 가 6의 약수, f(1)·f(6) ≥ ... (추가 없음)
out['C10'] = count_functions(X6, X6, lambda f: nondec(f,[1,2,3]) and nondec(f,[4,5,6]) and 6 % (f[3]*f[4]) == 0)
out['C10b_strict'] = count_functions(X6, X6, lambda f: inc(f,[1,2,3]) and inc(f,[4,5,6]) and 6 % (f[3]*f[4]) == 0)

for k,v in out.items(): print(k, json.dumps(v, ensure_ascii=False))
