# CLAUDE.md — kubernetes-content

Guidance for working in this repo. Read alongside `README.md` and `DESIGN.md` —
this file is the orientation; those are the source contracts.

## What this is

A **content repo**, not an app. It holds the **Kubernetes** topic that the
`graphl-ux` app (sibling repo) loads **at runtime**. No content logic, no render
engine, and no scenes live here — the app fetches this repo's `manifest.json` +
notebooks over the network and renders them.

There is **nothing to build, run, or test** in this repo. Changes are content and
JSON; correctness is verified by the `graphl-ux` app consuming them. (The one
executable is `scripts/colab_generate_audio.ipynb`, a Colab tool that turns the
`tts/` scripts into `audio/` `.wav`s.)

## The core contract (do not break)

1. **The notebook is the single source of truth** for a module's prose and code.
   The `manifest.json` only *wires* — it must never duplicate notebook content.
2. The app splits each notebook at every `## ` heading into **sections** (= pages).
   Sections are matched to the manifest overlay by **normalized heading text**, so
   a heading edit in a notebook must be mirrored in the manifest `heading` field.
3. A section's diagram **images (`![]()`) are stripped** by the app — a **scene**
   replaces them. Don't rely on inline notebook images surviving.
4. **Scenes live in the `graphl-ux` app** (`src/scenes/kubernetes.ts`), authored
   with the engine's pattern helpers — **not** in this repo. The local `scenes/`
   dir is reserved/empty (`.gitkeep`). Here you only reference a scene **by id**.
   The whole topic rides one dense 16:9 scene: `kubernetes`.

## Layout

```
manifest.json   # wires modules: notebook ref + per-section overlay (scene/spine/role/audio/highlight/focus)
DESIGN.md       # FIXED visual house style — palette, calm filled blocks, spotlight
notebooks/      # the teaching .ipynb (prose + code source of truth) — 01..10
tts/            # per-section narration scripts (plain spoken prose)
audio/          # generated .wav narration (per-section)
scenes/         # reserved/empty — real scenes live in graphl-ux app
scripts/        # colab_generate_audio.ipynb — TTS .tts -> .wav on a Colab GPU
```

## Content (the curriculum)

10 notebooks, a beginner-to-CKA textbook. Each chapter strictly assumes only what
came before (layer-cake order; no forward references). The reader finished the
`docker` topic — knows containers, images, volumes, the docker CLI, a Linux shell
— but has never touched Kubernetes.

| # | Topic |
|---|---|
| 01 | Getting Started with Kubernetes |
| 02 | Pods, Labels & the Object Model |
| 03 | Deployments, ReplicaSets & Rollouts |
| 04 | Services, DNS & Service Discovery |
| 05 | ConfigMaps, Secrets & Environment |
| 06 | Storage: Volumes, PVs & PVCs |
| 07 | Scheduling: Resources, Affinity, Taints & Tolerations |
| 08 | Cluster Architecture & kubeadm |
| 09 | Networking, Ingress & Network Policies |
| 10 | RBAC, Security, Troubleshooting & CKA Prep |

## TTS Guidelines

`.tts` files are read aloud by ChatterboxTTS. They must be plain spoken prose —
what a teacher would say at a whiteboard. Filenames are **per section**:
`NN-MM-section-slug.tts` (matching the manifest `audio` stem), one per manifest
section. They are split out of the source repo's whole-notebook `.tts`.

- **Plain prose only** — no markdown, no `#` headings, no bullets, no backticks,
  no asterisks. Section titles written as a plain sentence ending with a full stop
  (e.g. `What is a pod.`).
- **No raw code, YAML, or shell commands** — describe what a command or manifest
  does in prose. `kubectl run web --image=nginx` becomes "use kubectl run to
  launch a pod named web from the n-ginx image." A manifest with `replicas: 3`
  becomes "a deployment that asks Kubernetes to keep three identical pods running."
- **Spell out symbols, paths, and shorthand:**
  - Paths: `/etc/kubernetes/manifests` → "slash e-t-c slash kubernetes slash manifests", `~/.kube/config` → "tilde slash dot kube slash config", `/var/lib/etcd` → "slash var slash lib slash et-see-dee"
  - Object refs: `kube-system` → "kube system", `nginx:1.25` → "n-ginx tag one point twenty-five", `node/worker-1` → "node worker one"
  - kubectl shorthand: `-n` → "namespace flag", `-A` → "all namespaces", `-o yaml` → "output as yaml", `--dry-run=client` → "client dry run", `-l app=web` → "label selector app equals web", `k` → "kubectl"
  - Operators: `&&` → "and-and", `|` → "pipe", `>` → "redirect to", `--` → "double dash"
  - Acronyms: API → "ay-pee-eye", CRD → "custom resource definition" (first use), CNI → "container network interface", CSI → "container storage interface", CRI → "container runtime interface", RBAC → "are-back", PV → "persistent volume", PVC → "persistent volume claim", SC → "storage class", SA → "service account", HPA → "horizontal pod autoscaler", DS → "daemon set", STS → "stateful set", RS → "replica set", DNS → "dee-en-ess", TLS → "tee-el-ess", TCP → "tee-see-pee", IP → "eye-pee", VM → "virtual machine", CPU → "see-pee-you", OCI → "open container initiative", CKA → "see-kay-ay"
  - Components: `kube-apiserver` → "kube ay-pee-eye server", `kubelet` → "kube-let", `kube-proxy` → "kube proxy", `etcd` → "et-see-dee", `containerd` → "container-d", `coredns` → "core-d-en-ess", `calico` → "ka-lee-ko", `cilium` → "silly-um"
  - Kinds: `ReplicaSet` → "replica set", `StatefulSet` → "stateful set", `DaemonSet` → "daemon set", `CronJob` → "cron job", `ConfigMap` → "config map", `PersistentVolumeClaim` → "persistent volume claim", `ClusterRoleBinding` → "cluster role binding", `NetworkPolicy` → "network policy"
  - Resource units: `500m` (CPU) → "five hundred milli-cores", `1Gi` → "one gibibyte", `256Mi` → "two hundred and fifty-six mebibytes"
- **Natural spoken flow** — transitional phrases: "notice that", "the key insight here is", "to put it another way", "picture this".
- **Skip code outputs and tables** — never read aloud command output or a YAML
  block. Describe the takeaway instead.
- **Pace with paragraph breaks** — each paragraph = one idea; a blank line gives
  the TTS engine a natural pause. Aim for 2–4 sentences per paragraph.

## Source

Notebooks are copied from `~/Projects/kubernetes` (the runnable CKA curriculum),
which also carries the whole-notebook `.tts`/`.wav` per chapter and the original,
fuller content guidelines.
