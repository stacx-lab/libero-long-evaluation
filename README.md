# LIBERO Long Evaluation

[Open the evaluation website](https://stacx-lab.github.io/libero-long-evaluation/)

Ten LIBERO Long tasks, one episode per task, evaluated on September 16, 2026 with GPT-6 Astra at medium reasoning effort. Native verdicts: **7 successful, 3 unsuccessful**.

The site contains all ten edited dual-camera HD replays, twenty original camera recordings, per-task analyses, diagnostic images, complete session text, native predicate results, and the evaluation protocol. The combined all-task video is intentionally omitted; all individual task videos are retained at their original quality.

## Evaluation protocol

- Official initial state index 0 and seed 0; one attempt per task; no resets after initialization.
- 20-minute agent execution deadline per task; no action-step or model-loop limit.
- Agent observations: 256 x 256. Post-evaluation native replay: 768 x 768 per camera; edited dual-view video: 1536 x 976.
- Success uses LIBERO native predicates. This joint-device evaluation does not claim direct comparability with official OSC-policy scores.
- Task 09's deadline verdict was collected from the same paused native world after Harbor skipped its normal verifier. The site preserves the original exception, recovery receipt, and explanation.

See [protocol.json](protocol.json) and [data.json](data.json) for the configuration and complete results.

## Hosting

GitHub Pages serves the repository root from the `main` branch. `.nojekyll` preserves the static files without Jekyll processing. All assets are stored in this repository; the website has no dependency on a local server, external video host, or Git LFS.

In repository Settings > Pages, use **Deploy from a branch**, branch **main**, folder **/ (root)**. GitHub Free requires a public repository for Pages; private-repository Pages requires a supporting paid plan.

For local preview, run `python3 -m http.server 8000` from this directory and visit `http://localhost:8000/`.

## Asset integrity

`publication-manifest.json` records SHA-256 hashes for every published source-site file, the intentionally omitted compilation, and the limited publication changes. Run `python3 tools/verify_site.py` to verify integrity and required task assets.

All thirty individual MP4 files are byte-for-byte copies of the original website. Task descriptions, analyses, verdicts, session text, and diagnostic assets are preserved. Publication removes the compilation link and replaces machine-specific environment and evaluation prefixes in Task 09's exception traceback with `<python-environment>/` and `<evaluation>/`, preserving the traceback and its meaning.
