#!/usr/bin/env python3
"""Pracovní listy k poslechu pro sady otevřených otázek (openSets v tests/<id>.json).

Každá otázka sady dostane vlastní A4 stranu: text otázky, šedé „Co otázka chce" a linky
se šedými nadpisy, ke kterým se při poslechu píše. Nadpisy jdou z vypracovaných odpovědí
sady (openSets[].html) ve stejném pořadí: odpověď v jedné větě, klíčové pojmy, body
odpovědi (Opora, bez položek „Pozor"), na konci volné linky „Po poslechu". Pořadí stran
je openSets[].q, tedy pořadí v audiu. PDF tiskne headless Chrome.

Použití:
    python3 tools/pracovni-listy.py tests/inovace.json
Výstup: media/<id>/<id>-sada-N-pracovni-list.pdf. Cestu pak zapiš do openSets[].worksheet.
"""
import json, html, re, sys, subprocess, os, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LINES = 23  # kolik linek po 9 mm se vejde pod otázku a „Co otázka chce"
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #1d1d1f; }
.page { width: 210mm; height: 297mm; padding: 12mm 16mm 10mm; display: flex; flex-direction: column; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.head { display: flex; justify-content: space-between; gap: 8mm; font-size: 9pt; color: #6e6e73; border-bottom: 0.3mm solid #b0b0b5; padding-bottom: 2.5mm; }
.head b { color: #2f6b3a; }
.num { margin-top: 5mm; font-size: 10pt; font-weight: 700; letter-spacing: .6pt; text-transform: uppercase; color: #2f6b3a; }
.q { margin-top: 1.5mm; font-size: 15pt; font-weight: 700; line-height: 1.28; }
.want { margin-top: 3mm; font-size: 9pt; line-height: 1.4; color: #8e8e93; }
.want b { color: #6e6e73; }
.lines { flex: 1; margin-top: 2mm; overflow: hidden; display: flex; flex-direction: column; }
.line { height: 9mm; flex: none; border-bottom: 0.25mm solid #d1d1d6; display: flex; align-items: flex-end; padding-bottom: 1mm; font-size: 8.5pt; color: #aeaeb2; white-space: nowrap; overflow: hidden; }
.line.h { font-size: 8pt; font-weight: 700; letter-spacing: .6pt; text-transform: uppercase; color: #8e8e93; }
.line.h.first { height: 6mm; }
.line.t::after { content: '\\a0–'; }
.rest { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
.foot { margin-top: 2.5mm; display: flex; justify-content: space-between; font-size: 8pt; color: #aeaeb2; }
"""

def text(s):
    return html.unescape(re.sub(r'<.*?>', '', s)).strip()

def parse(doc):
    """Vypracované odpovědi sady -> {číslo otázky: {'want', 'terms', 'points'}}."""
    out = {}
    for part in re.split(r'(?=<h2>)', doc):
        m = re.search(r'<p><strong>Otázka:</strong>\s*(\d+)\.', part)
        if not m:
            continue
        want = re.search(r'<p><strong>Problém / jádro otázky:</strong>(.*?)</p>', part, re.S)
        lists = dict((n, re.findall(r'<li><strong>(.*?)</strong>', ul))
                     for n, ul in re.findall(r'<p><strong>([^<]*?):</strong></p>\s*<ul>(.*?)</ul>', part, re.S))
        out[int(m.group(1))] = {
            'want': text(want.group(1)) if want else '',
            'terms': [text(t).rstrip(':') for t in lists.get('Klíčové pojmy', [])],
            'points': [p for p in (text(t).rstrip(':') for t in lists.get('Opora', [])) if not p.lower().startswith('pozor')],
        }
    return out

def lines_for(g):
    """Šedé nadpisy na linkách. Body odpovědi dostanou 2 linky, když se to vejde."""
    rows = [('h first', 'Odpověď v jedné větě'), ('', ''), ('', '')]
    if g['terms']:
        rows += [('h', 'Klíčové pojmy')] + [('t', t) for t in g['terms']]
    pts = g['points']
    if pts:
        per = 2 if len(rows) + 1 + 2 * len(pts) + 3 <= LINES else 1
        rows.append(('h', 'Body odpovědi'))
        for p in pts:
            rows += [('t', p)] + [('', '')] * (per - 1)
    return rows

def main(src):
    d = json.load(open(src, encoding='utf-8'))
    root = os.path.join(os.path.dirname(os.path.abspath(src)), '..')
    out = os.path.join(root, 'media', d['id'])
    tmp = tempfile.mkdtemp()
    oq = d['openQuestions']
    for i, s in enumerate(d['openSets'], 1):
        guide = parse(open(os.path.join(root, s['html']), encoding='utf-8').read()) if s.get('html') else {}
        n = len(s['q'])
        pages = []
        for k, qn in enumerate(s['q'], 1):
            g = guide.get(qn, {'want': '', 'terms': [], 'points': []})
            rows = ''.join(f'<div class="line {c}">{html.escape(t)}</div>' for c, t in lines_for(g))
            rest = '<div class="line h">Po poslechu: co mi chybí</div>' + '<div class="line"></div>' * 30
            want = f'<div class="want"><b>Co otázka chce:</b> {html.escape(g["want"])}</div>' if g['want'] else ''
            pages.append(f"""<section class="page">
<div class="head"><span><b>{html.escape(d['title'])}</b> · Sada {i}: {html.escape(s['name'])}</span><span>audio {s.get('duration', '')}</span></div>
<div class="num">Otázka {k} z {n} · č. {qn}</div>
<div class="q">{html.escape(oq[qn - 1])}</div>
{want}
<div class="lines">{rows}<div class="rest">{rest}</div></div>
<div class="foot"><span>Při poslechu piš heslovitě k šedým nadpisům. Po poslechu doplň, co chybí.</span><span>{k}/{n}</span></div>
</section>""")
        doc = f"<!doctype html><html lang=cs><meta charset=utf-8><title>{html.escape(d['title'])} - sada {i}</title><style>{CSS}</style><body>{''.join(pages)}</body></html>"
        hp = os.path.join(tmp, f"sada-{i}.html")
        pp = os.path.join(out, f"{d['id']}-sada-{i}-pracovni-list.pdf")
        open(hp, 'w', encoding='utf-8').write(doc)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--user-data-dir={tmp}/chr',
                        f'--print-to-pdf={pp}', 'file://' + hp], stderr=subprocess.DEVNULL, check=True)
        print(os.path.relpath(pp), n, 'stran', hp)

if __name__ == '__main__':
    main(sys.argv[1])
