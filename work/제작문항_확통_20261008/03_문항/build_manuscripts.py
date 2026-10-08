# -*- coding: utf-8 -*-
"""원고(원고_A/B/C.py 의 ITEMS) → 형식 검사 → JSON + Markdown. 검산결과.json 의 정답과 대조한다.
검사: 응답 유형·발문 끝맺음(KG-A33)·단답 1~999(KG-V11)·객관식 5지 상이(KG-A37)·피할 발문(KG-A13)·사이시옷·해설 금지 기호·'정확히' 남용(KG-A06)."""
import json, re, sys, importlib
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VER = json.loads((ROOT / '04_검산' / '검산결과.json').read_text(encoding='utf-8'))
BAD_STEM = ['이 때', '일때', '라고 하자', '에 대해 ', '구하여라', '만족하는', '최대값', '최소값', '갯수', '음의 아닌', '정확히']
BAD_SOL = ['⟹', '⟺', '∴', '∵', '\\implies', '\\iff', '\\binom', 'WLOG', 's.t.', 'QED', '자명', '쉽게 알 수']
CIRC = '①②③④⑤'


def check(item):
    e = []
    stem = item['문면']
    for b in BAD_STEM:
        if b in stem:
            e.append(f"발문 피할 형태 '{b}'")
    if item['type'] == '객관식':
        if not re.search(r'(은|는)\?\s*(\(단,.*\)\s*)?(\[4점\])?$', stem.strip()):
            e.append('객관식 발문은 의문형으로 끝나야 함')
        ch = item['선지']
        if len(ch) != 5 or len(set(ch)) != 5:
            e.append('선지 5개 상이 필요')
        if item['정답'] not in CIRC:
            e.append('객관식 정답은 번호')
        if '선지근거' not in item or len(item['선지근거']) < 4:
            e.append('오답 4개 근거 필요(KG-A37)')
        vals = [choice_value(c) for c in ch]
        if None not in vals and vals != sorted(vals):
            e.append('객관식 선지는 오름차순(평가원 관례)')
    else:
        if not re.search(r'구하시오\.\s*(\(단,.*\)\s*)?(\[4점\])?$', stem.strip()):
            e.append('단답형 발문은 구하시오. 로 끝나야 함')
        try:
            v = int(item['정답'])
            if not 1 <= v <= 999:
                e.append('단답 정답 1~999 위반')
        except Exception:
            e.append('단답 정답은 자연수')
    sol = '\n'.join(item['해설'])
    for b in BAD_SOL:
        if b in sol:
            e.append(f"해설 금지 '{b}'")
    for t in (stem, sol):
        if t.count('$') % 2:
            e.append('$ 홀수')
        prose = ''.join(t.split('$')[0::2])
        for ch_ in '×÷√≤≥→≠∞':
            if ch_ in prose:
                e.append(f'산문 유니코드 {ch_}')
    # 검산 대조
    v = VER.get(item['id'])
    if not v:
        e.append('검산결과 없음')
    else:
        exp = v['answer']
        if item['type'] == '객관식':
            got = item['선지'][CIRC.index(item['정답'])]
            if item.get('정답값', got).replace(' ', '') != exp and str(F(exp)) != item.get('정답값', '').replace(' ', ''):
                e.append(f"객관식 정답값 {item.get('정답값')} ≠ 검산 {exp}")
        else:
            expected = str(v.get('pq', exp))
            if str(item['정답']) != expected:
                e.append(f"단답 정답 {item['정답']} ≠ 검산 {expected}")
    for k in ('핵심판단', '조건역할', '난도', '원문과의차이', '조건삭제', '오개념', '우회풀이'):
        if k not in item['설계']:
            e.append(f'설계.{k} 없음')
    return e


def choice_value(c):
    """선지 문자열 → 수치(분수 \\dfrac{a}{b}, 정수). 해석 불가면 None."""
    m = re.search(r'\\d?frac\{(-?\d+)\}\{(\d+)\}', c)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    m = re.search(r'-?\d+', c)
    return F(int(m.group(0))) if m else None


def duplicates(items):
    """세트 내 중복 서명 검사: 조건 상자의 앞 두 조건이 같거나, 문면 유사도가 0.9 이상이면 보고(블라인드 검토 교훈 PS-02)."""
    import difflib
    out = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            ba, bb = (a.get('조건상자') or [])[:2], (b.get('조건상자') or [])[:2]
            if ba and ba == bb:
                out.append(f"{a['id']}~{b['id']}: 조건 (가)(나) 동일")
            ta = a['문면'] + '\n'.join(a.get('조건상자') or []); tb = b['문면'] + '\n'.join(b.get('조건상자') or [])
            r = difflib.SequenceMatcher(None, ta, tb).ratio()
            if r >= 0.9:
                out.append(f"{a['id']}~{b['id']}: 문면 유사도 {r:.2f}")
    return out


def to_md(item):
    L = [f"## {item['id']} · {item['제목']}  ({item['type']}, 4점)", '']
    L.append(item['문면'])
    if item.get('조건상자'):
        L.append('')
        L.append('> ' + '  \n> '.join(item['조건상자']))
    if item['type'] == '객관식':
        L.append('')
        L.append('  '.join(f"{CIRC[i]} {c}" for i, c in enumerate(item['선지'])))
    L += ['', f"**정답 {item['정답']}**" + (f" (값 {item['정답값']})" if item.get('정답값') else ''), '', '### 해설']
    L += item['해설']
    d = item['설계']
    L += ['', '### 제작 기록', f"- 출발 원문: {item['출처']}", f"- 핵심 판단: " + ' / '.join(d['핵심판단']),
          '- 조건의 역할: ' + ' / '.join(d['조건역할']), f"- 예상 난도(실측 전): {d['난도']}", f"- 원문과의 차이: {d['원문과의차이']}",
          '- 조건 삭제 증인: ' + ' / '.join(d['조건삭제']), '- 오개념 풀이의 답: ' + ' / '.join(d['오개념']), f"- 우회 풀이 검사: {d['우회풀이']}"]
    if item['type'] == '객관식':
        L.append('- 오답 근거: ' + ' / '.join(item['선지근거']))
    L.append(f"- 검산: {d.get('검산', '04_검산/문항_검산_확정.py 전수 열거')}")
    return '\n'.join(L)


def main(themes):
    all_items = []
    bad = {}
    for t in themes:
        mod = importlib.import_module(f'원고_{t}')
        for it in mod.ITEMS:
            errs = check(it)
            if errs:
                bad[it['id']] = errs
            all_items.append(it)
        (HERE / f'원고_{t}.json').write_text(json.dumps(mod.ITEMS, ensure_ascii=False, indent=1), encoding='utf-8')
        (HERE / f'원고_{t}.md').write_text(f"# 주제 {t} — {mod.TITLE}\n\n" + mod.INTRO + '\n\n' + '\n\n---\n\n'.join(to_md(i) for i in mod.ITEMS) + '\n', encoding='utf-8')
    dup = {}
    for t in themes:
        mod = importlib.import_module(f'원고_{t}')
        d = duplicates(mod.ITEMS)
        if d:
            dup[t] = d
    print(json.dumps({'items': len(all_items), 'errors': bad, 'duplicate_warnings': dup}, ensure_ascii=False, indent=1))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    raise SystemExit(main(sys.argv[1:] or ['A', 'B', 'C']))
