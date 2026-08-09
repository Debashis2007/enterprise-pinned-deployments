# Design: Enterprise Pinned Deployments

**Project:** `enterprise-pinned-deployments`  
**Parent system design:** `09-multi-model-routing-api-platform.md`

## 1. What this POC demonstrates

Org-level pins with history and one-click rollback; no floating aliases.

## 2. Architecture (POC)

```text
GET/POST /orgs/{org}/pin → history
POST /rollback → prior revision
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Org pin map | Change control for B2B. | `pins[org]`. |
| Pin history | Rollback needs prior digest. | `history` list. |
| No floating aliases | Surprise swaps forbidden. | API speaks revisions only. |

## 4. Key endpoints

`GET /health`, `GET/POST /orgs/{org}/pin`, `POST /orgs/{org}/rollback`

## 5. Tradeoffs / POC limits

No maintenance-window workflow UI.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

