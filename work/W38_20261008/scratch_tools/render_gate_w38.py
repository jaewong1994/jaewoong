#!/usr/bin/env python3
"""W38 렌더 게이트 — 공장/온톨로지_v61_해설교체_20260901.py render_gate 의 하네스를 그대로 재현하되
클라우드 환경에 맞게 Playwright chromium(/opt/pw-browsers)을 쓴다(원본은 channel="chrome"). DB 접근 없음, 파일 읽기만.
사용: render_gate_w38.py <jsonl> [<jsonl>...]  → 결과 JSON 출력, KaTeX 오류가 있으면 종료코드 1."""
import functools
import http.server
import json
import os
import sys
import threading
from pathlib import Path

ROOT = Path("/home/user/ngd2-figtool")
KATEX = "회귀자료/온톨로지_v60_wave1_사람판정_실행패키지_20260831/vendor/katex"


def main() -> int:
    objs = []
    for f in sys.argv[1:]:
        for l in Path(f).read_text(encoding="utf-8").splitlines():
            if l.strip():
                o = json.loads(l)
                if o.get("final_answer") == "":
                    continue  # 결손 문항은 커밋 대상이 아님
                objs.append(o)
    from playwright.sync_api import sync_playwright
    harness = ROOT / f"_v61_render_gate_w38_{os.getpid()}.html"
    bodies = {str(o["item_id"]): "\n".join(str(s["text"]) for s in o["solution_steps"]) for o in objs}
    harness.write_text(
        '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="' + KATEX + '/katex.min.css">'
        '<script src="' + KATEX + '/katex.min.js"></script>'
        '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>'
        '<script src="수식공통.js"></script><script src="표시공통.js"></script>'
        '<body><div id="root"></div><script>window.RESULT={};window.HARNESS_ERROR=null;try{const B=' + json.dumps(bodies, ensure_ascii=False) + ';'
        'for(const [id,b] of Object.entries(B)){const d=document.createElement("div");d.className="ngd2-body";'
        'd.innerHTML=(window.NGD2Display&&NGD2Display.solText)?NGD2Display.solText(b):NGD2Display.mathText(b);document.getElementById("root").appendChild(d);'
        'try{if(window.NGD2Math&&window.katex)NGD2Math.render(d)}catch(e){}const r=NGD2Display.render(d);'
        'RESULT[id]={errors:r.errors,katex:d.querySelectorAll(".katex").length,katexErrors:d.querySelectorAll(".katex-error").length,'
        'literalDollar:(d.innerText.match(/\\$/g)||[]).length,text:d.innerText.slice(0,120)};}}catch(e){window.HARNESS_ERROR=String(e&&e.stack||e)}'
        'window.RESULT_READY=true;</script>',
        encoding="utf-8")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
            page = browser.new_page()
            console = []
            page.on("console", lambda m: console.append(m.text) if m.type in ("error", "warning") else None)
            page.goto(f"http://127.0.0.1:{port}/{harness.name}", wait_until="load")
            page.wait_for_function("window.RESULT_READY===true", timeout=30000)
            page.wait_for_timeout(800)
            result = page.evaluate("window.RESULT")
            harness_error = page.evaluate("window.HARNESS_ERROR")
            has_display = page.evaluate("!!(window.NGD2Display && NGD2Display.render)")
            browser.close()
    finally:
        server.shutdown()
        harness.unlink(missing_ok=True)
    bad = {k: v for k, v in result.items() if v.get("errors") or v.get("katexErrors") or v.get("literalDollar")}
    out = {"items": len(objs), "display_loaded": has_display, "harness_error": harness_error, "bad": bad,
           "console_errors": console[:10], "sample": {k: v.get("text") for k, v in list(result.items())[:3]}}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 1 if (bad or harness_error or not has_display) else 0


if __name__ == "__main__":
    raise SystemExit(main())
