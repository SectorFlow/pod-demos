#!/usr/bin/env python3
"""Add or update a pod on the pod-demos site.

Usage:
  python3 tools/add_pod.py --demo <demo.html> --arch <architecture.html> [--slug voice-concierge-pod]
                           [--name "Voice Concierge pod"] [--tagline "..."] [--no-commit]

Takes the two pages produced by the pod design kit (fragments starting with <title>),
wraps each as a full HTML document with noindex, writes them to <slug>/demo.html and
<slug>/architecture.html, adds or replaces the pod's card on index.html, and commits.
Run from the repo root. Re-running for the same slug replaces the pages and the card.
"""
import argparse, html, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex, nofollow">\n')


def wrap(text):
    """Fragment (<title>...</style>body...) -> full document. Already-wrapped files pass through."""
    if text.lstrip().lower().startswith("<!doctype"):
        return text
    i = text.index("</style>") + len("</style>")
    return HEAD + text[:i] + "\n</head>\n<body>\n" + text[i:] + "\n</body>\n</html>\n"


def grab(pattern, text, default=""):
    m = re.search(pattern, text, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else default


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def card(slug, name, tagline, beats):
    e = html.escape
    return (f'  <div class="pod" data-pod="{e(slug)}">\n'
            f'    <h2>{e(name)}</h2>\n'
            f'    <div class="tag">{e(tagline)}</div>\n'
            f'    <div class="links">\n'
            f'      <a class="primary" href="{e(slug)}/demo.html">Demo walkthrough ({beats} beats)</a>\n'
            f'      <a href="{e(slug)}/demo.html#step2-first">First meeting (7 beats)</a>\n'
            f'      <a href="{e(slug)}/architecture.html">Architecture and releases</a>\n'
            f'    </div>\n'
            f'  </div>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", required=True)
    ap.add_argument("--arch", required=True)
    ap.add_argument("--slug")
    ap.add_argument("--name")
    ap.add_argument("--tagline")
    ap.add_argument("--no-commit", action="store_true")
    a = ap.parse_args()

    demo = pathlib.Path(a.demo).read_text(encoding="utf-8")
    arch = pathlib.Path(a.arch).read_text(encoding="utf-8")
    name = a.name or grab(r'<div class="ttl">(.*?)</div>', demo) or grab(r"<title>(.*?)</title>", demo)
    slug = a.slug or slugify(name)
    tagline = a.tagline or grab(r'<div class="sub">(.*?)</div>', demo)
    beats = grab(r'id="counter">\s*\d+\s*/\s*(\d+)', demo, "27")
    if not name:
        sys.exit("could not find the pod name; pass --name")

    out = ROOT / slug
    out.mkdir(exist_ok=True)
    (out / "demo.html").write_text(wrap(demo), encoding="utf-8")
    (out / "architecture.html").write_text(wrap(arch), encoding="utf-8")

    idx_path = ROOT / "index.html"
    idx = idx_path.read_text(encoding="utf-8")
    start, end = "<!-- PODS START -->", "<!-- PODS END -->"
    if start not in idx or end not in idx:
        sys.exit("index.html is missing the PODS START/END markers")
    a_i, b_i = idx.index(start) + len(start), idx.index(end)
    cards = [(m.group(1), m.group(0)) for m in re.finditer(r'<div class="pod" data-pod="([^"]+)">.*?\n  </div>', idx[a_i:b_i], re.S)]
    new_card = card(slug, name, tagline, beats).strip()
    slugs = [s for s, _ in cards]
    if slug in slugs:
        cards[slugs.index(slug)] = (slug, new_card)
        action = "Update"
    else:
        cards.append((slug, new_card))
        action = "Add"
    block = "\n\n" + "\n\n".join("  " + c for _, c in cards) + "\n\n  "
    idx_path.write_text(idx[:a_i] + block + idx[b_i:], encoding="utf-8")
    print(f"{action} {slug}: {name} · {beats} beats · {tagline}")

    if a.no_commit:
        return
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    msg = f"{action} {name} demo and architecture pages"
    r = subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT)
    for lock in ["HEAD.lock", "index.lock", "objects/maintenance.lock"]:
        p = ROOT / ".git" / lock
        if p.exists():
            try: p.unlink()
            except OSError: print(f"warning: could not remove .git/{lock}; delete it before pushing")
    for p in (ROOT / ".git" / "objects").rglob("tmp_obj_*"):
        try: p.unlink()
        except OSError: pass
    print("committed" if r.returncode == 0 else "nothing to commit")
    print("next: git push")


if __name__ == "__main__":
    main()
