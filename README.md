# SectorFlow pod demos

Static site served by GitHub Pages. One folder per pod, each with `demo.html` (client walkthrough) and `architecture.html`.

- `index.html` lists every pod. Add a card when a pod folder is added.
- Pages are single self-contained files built from the pod design kit in `one/cowork/pod-design-kit`. Do not hand-edit them here; rebuild from the kit and copy over.
- Every page carries `noindex, nofollow`.
- Deploy: push to `main`. Pages serves from the repo root.

## Adding or updating a pod

From the repo root, with the two kit outputs (fragments starting with `<title>`):

    python3 tools/add_pod.py --demo ../<pod>-demo.html --arch ../<pod>-architecture.html

The script wraps both pages, writes `<slug>/demo.html` and `<slug>/architecture.html`, adds or replaces the card on `index.html` (name and tagline come from the demo's top bar; override with `--name`, `--tagline`, `--slug`), and commits. Then `git push`.
