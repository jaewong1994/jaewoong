# -*- coding: utf-8 -*-
"""원고 JSON(03_문항/원고_{A,B,C}.json) → HTML(KaTeX 로컬 vendor) → Chromium PDF (NL-09 방식).
산출: 06_출력/확통_제작30_문제지.{html,pdf}, 확통_제작30_해설지.{html,pdf}. 렌더 뒤 .katex-error 개수가 0 이어야 한다.
실행: python3 build_pdf.py  (Playwright chromium: /opt/pw-browsers/chromium-1194/chrome-linux/chrome 또는 PW_CHROME 환경변수)"""
import json, os, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CIRC = '①②③④⑤'
THEMES = ['A', 'B', 'C']
CHROME = os.environ.get('PW_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: 'Noto Sans CJK KR', 'Noto Sans KR', sans-serif; font-size: 11pt; line-height: 1.7; color: #111; }
h1 { font-size: 16pt; margin: 0 0 6pt; } h2 { font-size: 13pt; margin: 14pt 0 6pt; border-bottom: 1px solid #999; }
.item { page-break-after: always; }
.item:last-child { page-break-after: auto; }
.head { font-weight: bold; margin-bottom: 6pt; }
.stem p { margin: 0 0 8pt; text-align: justify; }
.box { border: 1px solid #333; padding: 6pt 10pt; margin: 8pt 0 10pt; display: inline-block; min-width: 60%; }
.box p { margin: 2pt 0; }
.choices { margin: 8pt 0 0; }
.choices span { display: inline-block; margin-right: 18pt; }
.space { height: 95mm; }
.ans { margin: 10pt 0 4pt; font-weight: bold; }
.sol p { margin: 0 0 7pt; text-align: justify; }
.rec { font-size: 9.5pt; color: #333; border-top: 1px dashed #999; margin-top: 10pt; padding-top: 6pt; }
.rec li { margin: 1pt 0; }
.intro { font-size: 10pt; color: #333; margin-bottom: 10pt; }
.katex-display { margin: 6pt 0; }
"""

HEAD = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="vendor/katex/katex.min.css">
<script src="vendor/katex/katex.min.js"></script>
<script src="vendor/katex/contrib/auto-render.min.js"></script>
<style>{css}</style></head><body>"""
TAIL = """<script>
document.addEventListener("DOMContentLoaded", function() {
  renderMathInElement(document.body, {delimiters: [{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}],
    throwOnError: false, strict: false});
  window.__rendered = true;
});
</script></body></html>"""


def esc(s):
    return html.escape(s, quote=False)


def paras(text):
    return ''.join(f'<p>{esc(p)}</p>' for p in text.split('\n\n') if p.strip())


def stem_html(it):
    h = f'<div class="stem">{paras(it["문면"])}'
    if it.get('조건상자'):
        h += '<div class="box">' + ''.join(f'<p>{esc(c)}</p>' for c in it['조건상자']) + '</div>'
    if it['type'] == '객관식':
        h += '<div class="choices">' + ''.join(f'<span>{CIRC[i]} {esc(c)}</span>' for i, c in enumerate(it['선지'])) + '</div>'
    return h + '</div>'


def problem_sheet(items):
    out = [HEAD.format(title='확통 제작 30문항 문제지', css=CSS), '<h1>확률과 통계 — 제작 문항 30제 (문제지)</h1>',
           '<p class="intro">A 카드 뒤집기·자리 바꾸기(10) / B 표본평균의 적률(10) / C 함수의 개수(10). 각 문항 4점. 단답형은 자연수. 2026-10-08 제작, 학생 실측 전.</p>']
    for i, it in enumerate(items, 1):
        out.append(f'<div class="item"><div class="head">{it["id"]}. [{it["type"]}] {esc(it["제목"])}</div>{stem_html(it)}<div class="space"></div></div>')
    out.append(TAIL)
    return '\n'.join(out)


def solution_sheet(items, titles):
    out = [HEAD.format(title='확통 제작 30문항 해설지', css=CSS), '<h1>확률과 통계 — 제작 문항 30제 (해설·제작 기록)</h1>']
    cur = None
    for it in items:
        t = it['id'][0]
        if t != cur:
            cur = t
            out.append(f'<h2>주제 {t} — {esc(titles[t])}</h2>')
        d = it['설계']
        ans = f'정답 {it["정답"]}' + (f' (값 {it["정답값"]})' if it.get('정답값') else '')
        rec = ['<div class="rec"><b>제작 기록</b><ul>',
               f'<li>출발 원문: {esc(it["출처"])}</li>',
               '<li>핵심 판단: ' + ' / '.join(esc(x) for x in d['핵심판단']) + '</li>',
               '<li>조건의 역할: ' + ' / '.join(esc(x) for x in d['조건역할']) + '</li>',
               f'<li>예상 난도(실측 전): {esc(d["난도"])}</li>',
               f'<li>원문과의 차이: {esc(d["원문과의차이"])}</li>',
               '<li>조건 삭제 증인: ' + ' / '.join(esc(x) for x in d['조건삭제']) + '</li>',
               '<li>오개념 풀이의 답: ' + ' / '.join(esc(x) for x in d['오개념']) + '</li>',
               f'<li>우회 풀이 검사: {esc(d["우회풀이"])}</li>']
        if it['type'] == '객관식':
            rec.append('<li>오답 근거: ' + ' / '.join(esc(x) for x in it['선지근거']) + '</li>')
        rec.append(f'<li>검산: {esc(d.get("검산", "04_검산 전수 열거"))}</li></ul></div>')
        out.append(f'<div class="item"><div class="head">{it["id"]}. [{it["type"]}] {esc(it["제목"])}</div>{stem_html(it)}'
                   f'<div class="ans">{esc(ans)}</div><div class="sol">' + ''.join(f'<p>{esc(p)}</p>' for p in it['해설']) + '</div>' + ''.join(rec) + '</div>')
    out.append(TAIL)
    return '\n'.join(out)


def render(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        pg.goto(html_path.as_uri())
        pg.wait_for_function('window.__rendered === true')
        n_err = pg.evaluate('document.querySelectorAll(".katex-error").length')
        n_math = pg.evaluate('document.querySelectorAll(".katex").length')
        pg.pdf(path=str(pdf_path), format='A4', print_background=True)
        b.close()
    return n_err, n_math


def main():
    sys.path.insert(0, str(ROOT / '03_문항'))
    items, titles = [], {}
    for t in THEMES:
        items += json.loads((ROOT / '03_문항' / f'원고_{t}.json').read_text(encoding='utf-8'))
        import importlib
        titles[t] = importlib.import_module(f'원고_{t}').TITLE
    report = {}
    for name, builder in (('확통_제작30_문제지', lambda: problem_sheet(items)), ('확통_제작30_해설지', lambda: solution_sheet(items, titles))):
        hp = HERE / f'{name}.html'
        hp.write_text(builder(), encoding='utf-8')
        n_err, n_math = render(hp, HERE / f'{name}.pdf')
        report[name] = dict(katex_error=n_err, katex_nodes=n_math, pdf_bytes=(HERE / f'{name}.pdf').stat().st_size)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if any(r['katex_error'] for r in report.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
