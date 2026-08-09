# Use Case: Enterprise Pinned Deployments

**YouTube walkthrough:** [Enterprise Pinned Deployments — System Design #Shorts](https://youtu.be/SzhDROyjGAE)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [09 — Multi-Model Routing / API Platform](../09-multi-model-routing-api-platform.md)

## Users & problem

Enterprises forbid surprise model changes. They pin revisions, schedule upgrades, and require change tickets.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Pin | Exact revision, not `latest` |
| Upgrade | Explicit promote with window |
| Notify | Changelog + webhook |
| Rollback | One-click prior pin |

## Design (from parent)

```
Org policy: deny floating aliases
  → pin map in router
  → maintenance window promote
  → canary inside org optional
  → keep prior revision warm
```

## Specializations

| Concern | Pin choice |
|---------|------------|
| Contracts | SLA on notice period |
| Testing | Customer sandbox gets candidate first |
| Registry | Pins reference immutable digests |
| Support | “What am I on?” API |

## Failure modes

- Alias flip affects enterprise → router enforces pin override.
- Pin points to deleted artifact → GC tombstones; forbid delete of pinned.
- Emergency security fix → out-of-band forced promote with notice.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Enterprise Pinned Deployments — System Design #Shorts](https://youtu.be/SzhDROyjGAE)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd enterprise-pinned-deployments
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/orgs/acme/pin -H 'Content-Type: application/json' -d '{"revision":"chat-r2026.01.01"}' | jq
