#!/usr/bin/env python3
"""Pracovní listy k psaní pro sady otevřených otázek (openSets v tests/<id>.json).

Každá otázka sady dostane vlastní A4 stranu: nahoře text otázky, pod ním linky po 9 mm.
Pořadí stran je pořadí v openSets[].q, tedy pořadí v audiu. PDF tiskne headless Chrome.

Použití:
    python3 tools/pracovni-listy.py tests/inovace.json
Výstup: media/<id>/<id>-sada-N-pracovni-list.pdf. Cestu pak zapiš do openSets[].worksheet.
"""
import json, html, sys, subprocess, os, tempfile
src = sys.argv[1]
d = json.load(open(src, encoding='utf-8'))
out = os.path.join(os.path.dirname(os.path.abspath(src)), '..', 'media', d['id'])
tmp = tempfile.mkdtemp()
oq = d['openQuestions']
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #1d1d1f; }
.page { width: 210mm; height: 297mm; padding: 14mm 16mm 12mm; display: flex; flex-direction: column; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.head { display: flex; justify-content: space-between; gap: 8mm; font-size: 9pt; color: #6e6e73; border-bottom: 0.3mm solid #b0b0b5; padding-bottom: 2.5mm; }
.head b { color: #2f6b3a; }
.num { margin-top: 6mm; font-size: 10pt; font-weight: 700; letter-spacing: .6pt; text-transform: uppercase; color: #2f6b3a; }
.q { margin-top: 2mm; font-size: 16pt; font-weight: 700; line-height: 1.3; }
.lines { flex: 1; margin-top: 5mm; overflow: hidden; }
.line { height: 9mm; border-bottom: 0.25mm solid #c9c9ce; }
.foot { margin-top: 3mm; font-size: 8pt; color: #9a9aa0; text-align: right; }
"""
for i, s in enumerate(d['openSets'], 1):
    n = len(s['q'])
    mins = s.get('duration', '')
    pages = []
    for k, qn in enumerate(s['q'], 1):
        pages.append(f"""<section class="page">
<div class="head"><span><b>{html.escape(d['title'])}</b> · Sada {i}: {html.escape(s['name'])}</span><span>audio {mins}</span></div>
<div class="num">Otázka {k} z {n} · č. {qn}</div>
<div class="q">{html.escape(oq[qn-1])}</div>
<div class="lines">{'<div class="line"></div>' * 40}</div>
<div class="foot">Banánovník · {html.escape(d['title'])} · sada {i} · strana {k}/{n}</div>
</section>""")
    doc = f"<!doctype html><html lang=cs><meta charset=utf-8><title>{html.escape(d['title'])} - sada {i}</title><style>{CSS}</style><body>{''.join(pages)}</body></html>"
    hp = os.path.join(tmp, f"{d['id']}-sada-{i}.html")
    pp = os.path.join(out, f"{d['id']}-sada-{i}-pracovni-list.pdf")
    open(hp, 'w', encoding='utf-8').write(doc)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--user-data-dir={tmp}/chr', f'--print-to-pdf={pp}', 'file://' + hp], stderr=subprocess.DEVNULL, check=True)
    print(os.path.relpath(pp), n, 'stran')
