#!/usr/bin/env python3
"""Generate manifest.json for kubernetes-content.

Headings are pulled verbatim from the notebooks (so they match the app's
normalized lookup); per-section metadata (audio slug, spine, role, highlight,
focus) is supplied here and zipped by index. Asserts the counts line up so a
heading edit in a notebook surfaces immediately.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks")


def headings(path):
    nb = json.load(open(path))
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        src = c["source"]
        src = "".join(src) if isinstance(src, list) else src
        for line in src.splitlines():
            s = line.strip()
            if s.startswith("## ") and not s.startswith("###"):
                out.append(s[3:].strip())
    return out


# Per-module: (module_id, title, notebook_stem, [ (slug, spine, role, [highlight], [focus]) ... ])
# Order MUST match the notebook's `## ` headings exactly (zipped by index).
H = True  # spine
L = False
MODULES = [
    ("01-getting-started", "Getting Started with Kubernetes", "01-getting-started-with-kubernetes", [
        ("what-is-kubernetes", H, "hook", ["k8s-cluster"], ["k8s-cluster"]),
        ("orchestration-problem", H, None, ["k8s-scheduler", "k8s-controllers"], ["k8s-control-plane"]),
        ("cluster-overview", H, None, ["k8s-control-plane", "k8s-worker"], ["k8s-cluster"]),
        ("the-pod", H, None, ["k8s-pods"], ["k8s-worker"]),
        ("why-kubernetes-matters", L, None, ["k8s-cluster"], ["k8s-cluster"]),
        ("local-cluster", L, None, ["k8s-worker"], ["k8s-cluster"]),
        ("first-pod", H, None, ["k8s-kubectl", "k8s-apiserver", "k8s-pods"], ["k8s-cluster"]),
        ("how-kubectl-works", H, None, ["k8s-kubectl", "k8s-apiserver"], ["k8s-client", "k8s-control-plane"]),
        ("kubectl-anatomy", L, None, ["k8s-kubectl"], ["k8s-client"]),
        ("pod-lifecycle", H, None, ["k8s-kc-get", "k8s-kc-describe", "k8s-kc-logs", "k8s-kc-exec"], ["k8s-client"]),
        ("imperative-vs-declarative", H, None, ["k8s-kc-apply", "k8s-apiserver"], ["k8s-client", "k8s-control-plane"]),
        ("getting-help", L, None, ["k8s-kubectl"], ["k8s-client"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("02-pods-object-model", "Pods, Labels & the Object Model", "02-pods-labels-and-the-object-model", [
        ("object-model", H, "hook", ["k8s-apiserver", "k8s-etcd"], ["k8s-control-plane"]),
        ("pod-manifest", H, None, ["k8s-pod-kind", "k8s-pod-containers"], ["k8s-pod-kind"]),
        ("pod-phases", L, None, ["k8s-pods"], ["k8s-worker"]),
        ("restart-policy", L, None, ["k8s-pods"], ["k8s-worker"]),
        ("init-containers", H, None, ["k8s-pod-init"], ["k8s-pod-kind"]),
        ("sidecar-pattern", H, None, ["k8s-pod-sidecar", "k8s-pod-containers"], ["k8s-pod-kind"]),
        ("probes", H, None, ["k8s-pod-probes"], ["k8s-pod-kind"]),
        ("labels", H, None, ["k8s-pod-kind"], ["k8s-workloads"]),
        ("label-selectors", H, None, ["k8s-service", "k8s-pod-kind"], ["k8s-networking"]),
        ("annotations", L, None, ["k8s-pod-kind"], ["k8s-pod-kind"]),
        ("namespaces", H, None, ["k8s-cluster"], ["k8s-cluster"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("03-deployments", "Deployments, ReplicaSets & Rollouts", "03-deployments-replicasets-and-rollouts", [
        ("why-controllers", H, "hook", ["k8s-pods"], ["k8s-worker"]),
        ("replicaset", H, None, ["k8s-replicaset"], ["k8s-workload-kinds"]),
        ("replicaset-vs-deployment", L, None, ["k8s-deployment", "k8s-replicaset"], ["k8s-workload-kinds"]),
        ("deployment-manifest", H, None, ["k8s-deployment"], ["k8s-workload-kinds"]),
        ("scaling", H, None, ["k8s-kc-scale", "k8s-replicaset"], ["k8s-workloads"]),
        ("rolling-updates", H, None, ["k8s-ro-rolling", "k8s-deployment"], ["k8s-rollout"]),
        ("rollout-history", L, None, ["k8s-kc-rollout", "k8s-deployment"], ["k8s-rollout"]),
        ("update-strategies", H, None, ["k8s-ro-rolling", "k8s-ro-recreate"], ["k8s-rollout"]),
        ("workload-family", H, None, ["k8s-statefulset", "k8s-daemonset", "k8s-job", "k8s-cronjob"], ["k8s-workload-kinds"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("04-services-dns", "Services, DNS & Service Discovery", "04-services-dns-and-service-discovery", [
        ("why-services", H, "hook", ["k8s-pods", "k8s-service"], ["k8s-networking"]),
        ("service-abstraction", H, None, ["k8s-service"], ["k8s-networking"]),
        ("service-ports", L, None, ["k8s-service"], ["k8s-networking"]),
        ("endpoints", L, None, ["k8s-service", "k8s-pods"], ["k8s-networking"]),
        ("service-types", H, None, ["k8s-service"], ["k8s-networking"]),
        ("kube-proxy", H, None, ["k8s-kube-proxy", "k8s-service"], ["k8s-worker"]),
        ("coredns", H, None, ["k8s-dns", "k8s-service"], ["k8s-networking"]),
        ("headless-services", L, None, ["k8s-dns", "k8s-pods"], ["k8s-networking"]),
        ("session-affinity", L, None, ["k8s-service"], ["k8s-networking"]),
        ("service-vs-ingress", L, None, ["k8s-service", "k8s-ingress"], ["k8s-networking"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("05-config-secrets", "ConfigMaps, Secrets & Environment", "05-configmaps-secrets-and-environment", [
        ("config-problem", H, "hook", ["k8s-configmap", "k8s-secret"], ["k8s-config"]),
        ("configmap", H, None, ["k8s-configmap"], ["k8s-config"]),
        ("consume-configmap", H, None, ["k8s-configmap", "k8s-cfg-env"], ["k8s-config"]),
        ("update-propagation", L, None, ["k8s-cfg-env"], ["k8s-config"]),
        ("immutable-config", L, None, ["k8s-configmap", "k8s-secret"], ["k8s-config"]),
        ("secrets", H, None, ["k8s-secret"], ["k8s-config"]),
        ("creating-secrets", L, None, ["k8s-secret"], ["k8s-config"]),
        ("consuming-secrets", L, None, ["k8s-secret", "k8s-cfg-env"], ["k8s-config"]),
        ("secret-types", L, None, ["k8s-secret"], ["k8s-config"]),
        ("image-pull-secrets", H, None, ["k8s-pullsecret", "k8s-registry"], ["k8s-registry"]),
        ("downward-api", L, None, ["k8s-cfg-env", "k8s-pod-kind"], ["k8s-config"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("06-storage", "Storage: Volumes, PVs & PVCs", "06-storage-volumes-pvs-and-pvcs", [
        ("why-storage", H, "hook", ["k8s-pods"], ["k8s-worker"]),
        ("volumes", H, None, ["k8s-storage"], ["k8s-storage"]),
        ("ephemeral-volumes", L, None, ["k8s-storage"], ["k8s-storage"]),
        ("persistent-storage", H, None, ["k8s-pv", "k8s-pvc", "k8s-sc"], ["k8s-storage"]),
        ("access-modes", L, None, ["k8s-pvc", "k8s-pv"], ["k8s-storage"]),
        ("storageclass", H, None, ["k8s-sc", "k8s-pv"], ["k8s-storage"]),
        ("reclaim-policies", L, None, ["k8s-pvc", "k8s-pv"], ["k8s-storage"]),
        ("csi", H, None, ["k8s-csi", "k8s-sc"], ["k8s-storage"]),
        ("statefulset-storage", H, None, ["k8s-statefulset", "k8s-pvc"], ["k8s-storage"]),
        ("resizing-pvcs", L, None, ["k8s-pvc"], ["k8s-storage"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("07-scheduling", "Scheduling: Resources, Affinity, Taints & Tolerations", "07-scheduling-resources-affinity-taints-tolerations", [
        ("scheduling-problem", H, "hook", ["k8s-scheduler"], ["k8s-scheduling"]),
        ("requests-limits", H, None, ["k8s-requests", "k8s-limits"], ["k8s-scheduling"]),
        ("qos-classes", L, None, ["k8s-requests", "k8s-limits"], ["k8s-scheduling"]),
        ("limitrange-quota", L, None, ["k8s-requests", "k8s-limits"], ["k8s-scheduling"]),
        ("nodeselector", H, None, ["k8s-nodeselector"], ["k8s-scheduling"]),
        ("node-affinity", H, None, ["k8s-affinity"], ["k8s-scheduling"]),
        ("pod-affinity", H, None, ["k8s-affinity"], ["k8s-scheduling"]),
        ("taints-tolerations", H, None, ["k8s-taints", "k8s-tolerations"], ["k8s-scheduling"]),
        ("eviction", L, None, ["k8s-limits", "k8s-pods"], ["k8s-scheduling"]),
        ("topology-spread", L, None, ["k8s-affinity"], ["k8s-scheduling"]),
        ("priorityclass", L, None, ["k8s-scheduler"], ["k8s-scheduling"]),
        ("scheduler-internals", H, None, ["k8s-scheduler"], ["k8s-control-plane"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("08-cluster-architecture", "Cluster Architecture & kubeadm", "08-cluster-architecture-and-kubeadm", [
        ("control-plane-overview", H, "hook", ["k8s-control-plane"], ["k8s-control-plane"]),
        ("etcd", H, None, ["k8s-etcd"], ["k8s-control-plane"]),
        ("apiserver", H, None, ["k8s-apiserver"], ["k8s-control-plane"]),
        ("scheduler-controllers", H, None, ["k8s-scheduler", "k8s-controllers"], ["k8s-control-plane"]),
        ("node-components", H, None, ["k8s-kubelet", "k8s-kube-proxy", "k8s-cri"], ["k8s-worker"]),
        ("plugin-interfaces", H, None, ["k8s-cri", "k8s-csi"], ["k8s-worker"]),
        ("static-pods", L, None, ["k8s-kubelet", "k8s-control-plane"], ["k8s-cluster"]),
        ("kubeadm", H, None, ["k8s-control-plane", "k8s-worker"], ["k8s-cluster"]),
        ("cluster-pki", L, None, ["k8s-apiserver", "k8s-etcd"], ["k8s-control-plane"]),
        ("etcd-backup", H, None, ["k8s-etcd"], ["k8s-control-plane"]),
        ("cluster-upgrade", L, None, ["k8s-control-plane"], ["k8s-cluster"]),
        ("what-to-practise", L, None, [], []),
    ]),
    ("09-networking", "Networking, Ingress & Network Policies", "09-networking-ingress-and-network-policies", [
        ("networking-model", H, "hook", ["k8s-networking", "k8s-pods"], ["k8s-networking"]),
        ("pod-ips", L, None, ["k8s-pods"], ["k8s-worker"]),
        ("cni-plugin", H, None, ["k8s-kubelet", "k8s-pods"], ["k8s-worker"]),
        ("communication-paths", H, None, ["k8s-service", "k8s-pods"], ["k8s-networking"]),
        ("why-ingress", H, None, ["k8s-service", "k8s-ingress"], ["k8s-networking"]),
        ("ingress-controllers", H, None, ["k8s-ingress"], ["k8s-networking"]),
        ("ingress-manifest", L, None, ["k8s-ingress"], ["k8s-networking"]),
        ("gateway-api", L, None, ["k8s-ingress", "k8s-service"], ["k8s-networking"]),
        ("networkpolicy", H, None, ["k8s-netpol"], ["k8s-networking"]),
        ("networkpolicy-semantics", L, None, ["k8s-netpol", "k8s-pods"], ["k8s-networking"]),
        ("networkpolicy-patterns", L, None, ["k8s-netpol"], ["k8s-networking"]),
        ("coredns-revisit", L, None, ["k8s-dns"], ["k8s-networking"]),
        ("cleaning-up", L, None, [], []),
    ]),
    ("10-rbac-security", "RBAC, Security, Troubleshooting & CKA Prep", "10-rbac-security-troubleshooting-and-cka-prep", [
        ("identity", H, "hook", ["k8s-sa", "k8s-apiserver"], ["k8s-rbac"]),
        ("serviceaccounts", H, None, ["k8s-sa"], ["k8s-rbac"]),
        ("rbac-roles", H, None, ["k8s-role", "k8s-crole"], ["k8s-rbac"]),
        ("rbac-bindings", H, None, ["k8s-rb", "k8s-crb", "k8s-subject"], ["k8s-rbac"]),
        ("aggregated-roles", L, None, ["k8s-crole"], ["k8s-rbac"]),
        ("security-context", H, None, ["k8s-sec-nonroot", "k8s-sec-readonly"], ["k8s-security"]),
        ("psa", H, None, ["k8s-sec-psa", "k8s-apiserver"], ["k8s-security"]),
        ("etcd-encryption", L, None, ["k8s-etcd"], ["k8s-control-plane"]),
        ("image-security", L, None, ["k8s-registry", "k8s-digest-pin"], ["k8s-registry"]),
        ("troubleshoot-apps", H, None, ["k8s-pods", "k8s-kc-logs"], ["k8s-worker"]),
        ("troubleshoot-control-plane", H, None, ["k8s-control-plane"], ["k8s-control-plane"]),
        ("troubleshoot-nodes", H, None, ["k8s-kubelet", "k8s-worker"], ["k8s-worker"]),
        ("troubleshoot-networking", H, None, ["k8s-service", "k8s-dns"], ["k8s-networking"]),
        ("cka-strategy", L, None, [], []),
        ("course-end", L, None, [], []),
    ]),
]

# Course-recap outro slugs get NO narration (.tts/audio) — they stay as pages but
# are silent. Every other section, including "Cleaning up", is narrated. (The old
# per-notebook "What's covered" intro was removed entirely — notebook + manifest.)
NO_AUDIO = {"what-to-practise", "course-end"}

presentations = []
for idx, (mid, title, stem, meta) in enumerate(MODULES, start=1):
    nb_headings = headings(os.path.join(NB, stem + ".ipynb"))
    assert len(nb_headings) == len(meta), (
        f"{stem}: notebook has {len(nb_headings)} headings, metadata has {len(meta)}"
    )
    nn = f"{idx:02d}"
    sections = []
    # Numbering starts at 2: section 01 was the old "What's covered" intro (now
    # removed), so the first real section keeps its original NN-02 audio slug —
    # preserving every existing tts/ + audio/ filename.
    for mm, (heading, (slug, spine, role, hl, focus)) in enumerate(zip(nb_headings, meta), start=2):
        sec = {"heading": heading, "scene": "kubernetes", "spine": spine}
        if role:
            sec["role"] = role
        if hl:
            sec["highlight"] = hl
        if focus:
            sec["focus"] = focus
        if slug not in NO_AUDIO:
            sec["audio"] = f"audio/{nn}-{mm:02d}-{slug}.wav"
        sections.append(sec)
    presentations.append({
        "id": mid,
        "title": title,
        "notebook": f"notebooks/{stem}.ipynb",
        "defaultScene": "kubernetes",
        "sections": sections,
    })

manifest = {
    "concept": "Kubernetes",
    "design": "DESIGN.md",
    "scenes": [
        {"id": "kubernetes", "title": "Kubernetes — the full platform", "status": "built"}
    ],
    "presentations": presentations,
}

out = os.path.join(ROOT, "manifest.json")
with open(out, "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")

total = sum(len(p["sections"]) for p in presentations)
print(f"wrote {out}: {len(presentations)} modules, {total} sections")
for p in presentations:
    print(f"  {p['id']:24s} {len(p['sections']):2d} sections")
