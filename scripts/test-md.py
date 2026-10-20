#!/usr/bin/env python3
"""Export testu z tests/<id>.json do Markdownu pro NotebookLM.

Použití:
  python3 scripts/test-md.py <id> [výstupní.md]   jen export
  python3 scripts/test-md.py --upload <id> [<id> ...]
      export do .work/notebooklm/ a výměna zdroje bananovnik-test-<id>.md
      v notebooku podle tabulky v docs/notebooklm.md
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LETTERS = "ABCDEFGHIJ"


def read_line(r, sources):
    src = sources.get(r.get("src"), {})
    parts = [src.get("label", "")] if src else []
    if r.get("ref"):
        parts.append(r["ref"])
    if r.get("pages"):
        pages = f'{src.get("pageWord", "str.")} {r["pages"]}'
        if r.get("pagesPrint"):
            pages = f'{src.get("pageWord", "str.")} e-verze {r["pages"]} / tištěná {r["pagesPrint"]}'
        parts.append(pages)
    line = ", ".join(p for p in parts if p)
    if r.get("note"):
        line += f' ({r["note"]})'
    return line


def question_md(n, q, sources):
    out = [f'### {n}. {q["q"]}', ""]
    for i, o in enumerate(q["opts"]):
        mark = " ✅" if i in q["correct"] else ""
        out.append(f"- {LETTERS[i]}) {o}{mark}")
    out += ["", "Správně: " + ", ".join(LETTERS[i] for i in sorted(q["correct"])), ""]
    if q.get("info"):
        out.append("**Teorie:**")
        out.append("")
        for line in q["info"].split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("Pojem:"):
                line = line[len("Pojem:"):].strip()
            elif line.startswith("Rozpor:"):
                line = "**Rozpor:**" + line[len("Rozpor:"):]
            elif line.startswith("Kde to najdu:"):
                line = "**Kde to najdu:**" + line[len("Kde to najdu:"):]
            out += [line, ""]
    if q.get("read"):
        out.append("Ke studiu: " + "; ".join(read_line(r, sources) for r in q["read"]))
        out.append("")
    return out


def export(test_id):
    d = json.loads((ROOT / "tests" / f"{test_id}.json").read_text("utf-8"))
    qs = d["questions"]
    sources = d.get("sources", {})
    out = [
        f'# {d["title"]} - testové otázky z Banánovníku',
        "",
        f'Export z aplikace Banánovník, stav k {d.get("updatedAt", "")}. Obsahuje {len(qs)} otázek.',
        "",
        "Tento zdroj má přednost před staršími výpisy otázek v sešitu: klíč je opravený podle zkoušek.",
        "Správných odpovědí může být jedna i více. Správné odpovědi jsou označené ✅.",
        "Značka (bez záruky) = klíč je sporný. Řádek Rozpor popisuje, v čem se test liší od učebnice nebo zkoušky.",
        "",
    ]
    if d.get("rubric"):
        out += [f'Zkouška: {d["rubric"]}.', ""]
    if sources:
        out += ["## Studijní zdroje", ""]
        out += [f'- **{s["label"]}:** {s["title"]}' for s in sources.values()]
        out.append("")
    if d.get("glossary"):
        out += ["## Slovníček zkratek", ""]
        out += [f'- **{g["label"]}** - {g["text"]}' for g in d["glossary"]]
        out.append("")

    sets = d.get("sets") or []
    used = set()
    for s in sets:
        out += [f'## {s["name"]}', ""]
        if s.get("read"):
            out += ["Ke studiu: " + "; ".join(read_line(r, sources) for r in s["read"]), ""]
        for n in s["q"]:
            used.add(n)
            out += question_md(n, qs[n - 1], sources)
    rest = [n for n in range(1, len(qs) + 1) if n not in used]
    if rest:
        out += ["## Ostatní otázky" if sets else "## Otázky", ""]
        for n in rest:
            out += question_md(n, qs[n - 1], sources)

    if d.get("openQuestions"):
        out += ["## Otevřené otázky", ""]
        out += [f"{i}. {q}" for i, q in enumerate(d["openQuestions"], 1)]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def notebook_id(test_id):
    table = (ROOT / "docs" / "notebooklm.md").read_text("utf-8")
    for line in table.splitlines():
        cells = line.split(" | ")
        if len(cells) >= 3 and f"`{test_id}`" in cells[0]:
            m = re.search(r"`([0-9a-f-]{36})`", line)
            return m.group(1) if m else None
    return None


def upload(test_id):
    nb = notebook_id(test_id)
    if not nb:
        print(f"{test_id}: bez notebooku v docs/notebooklm.md, přeskočeno")
        return True
    title = f"bananovnik-test-{test_id}.md"
    dest = ROOT / ".work" / "notebooklm" / title
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(export(test_id), "utf-8")
    listing = subprocess.run(["notebooklm", "source", "list", "-n", nb, "--json"],
                             capture_output=True, text=True, check=True)
    for src in json.loads(listing.stdout)["sources"]:
        if src["title"] == title:
            subprocess.run(["notebooklm", "source", "delete", "-y", "-n", nb, src["id"]],
                           capture_output=True, check=True)
    add = subprocess.run(["notebooklm", "source", "add", "-n", nb, "--timeout", "180", str(dest)],
                         capture_output=True, text=True)
    print(f"{test_id}: {'nahráno' if add.returncode == 0 else 'CHYBA ' + add.stderr.strip()}")
    return add.returncode == 0


if __name__ == "__main__":
    if sys.argv[1] == "--upload":
        ok = all([upload(t) for t in sys.argv[2:]])
        sys.exit(0 if ok else 1)
    tid = sys.argv[1]
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / ".work" / "notebooklm" / f"bananovnik-test-{tid}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(export(tid), "utf-8")
    print(dest)
