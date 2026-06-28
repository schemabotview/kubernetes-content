# kubernetes-content

Content repo for the **Kubernetes** topic in graphl-ux. Designed to load at
runtime; no content logic lives in the app code. Follows the
**manifest + notebook-as-source-of-truth** contract.

## Layout

```
kubernetes-content/
  manifest.json     # wires modules: notebook ref + per-section overlay (scene/spine/role/audio/highlight/focus)
  DESIGN.md         # the visual house style (calm filled blocks, palette, reel chrome)
  notebooks/        # the 10 teaching .ipynb (the prose + code source of truth)
  scenes/           # reserved — scenes live in the graphl-ux app (src/scenes), not here
  tts/              # per-section narration scripts (plain spoken prose)
  audio/            # generated .wav narration
  scripts/          # colab_generate_audio.ipynb — TTS .tts -> .wav on a Colab GPU
```

## Generating audio

Narration `.wav`s are produced from the `tts/*.tts` scripts by
`scripts/colab_generate_audio.ipynb` (ChatterboxTTS on a Colab T4 GPU). It clones
this repo, generates one `audio/<stem>.wav` per `tts/<stem>.tts`, and commits +
pushes each clip straight from the Colab VM. Needs a Colab secret `GITHUB_TOKEN`
(a PAT with **Contents: Read/Write** on `schemabotview/kubernetes-content`).
Set `FORCE=True` to regenerate existing clips, or `ONLY_STEM="01-02-the-cluster"`
to do a single section.

## Contract

- The **notebook is the single source of truth** for a module's prose and code.
  The manifest only *wires* — it never duplicates notebook content.
- The app splits each notebook at every `## ` heading into **sections** (= pages).
  A section's diagram **images (`![]()`) are stripped** — the scene replaces them.
- The manifest overlay attaches, per section: a `scene` id (the diagram), a
  `spine` flag (drives feed-mode flow), an optional `role` (e.g. `hook`), an
  `audio` stem, and optional `highlight`/`focus` (scene node ids the camera frames
  / lights). Sections are matched to the overlay by normalized heading.
- A **scene** is a reusable `SceneSpec` referenced by id from many sections. The
  whole Kubernetes topic rides one dense 16:9 scene (`kubernetes`), authored and
  bundled in the **graphl-ux app** (`src/scenes/kubernetes.ts`) — it is **not**
  served from this repo. Styled per `DESIGN.md`.

## Source

Notebooks are copied from `~/Projects/kubernetes` (the runnable curriculum). The
source repo also carries a whole-notebook `.tts` per chapter; the per-section
`tts/NN-MM-*.tts` here are split out of those, one per manifest section.

## Status

Scaffold in place: the 10 notebooks are copied; `manifest.json` and per-section
`tts/` are authored module by module. Scenes are not served from here — the topic
rides the `kubernetes` scene in the graphl-ux app.

**Serving.** graphl-ux fetches this repo at runtime over raw GitHub
(`https://raw.githubusercontent.com/schemabotview/kubernetes-content/main/…`).
No app build bundles this content; the app ships only the render engine + scenes.
