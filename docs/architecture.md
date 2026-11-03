# Architecture — current local milestone

```text
Browser
  ├─ GET /                 Flask → Jinja template + approved content
  ├─ GET /static/...       local CSS, JS, favicon (and CV when provided)
  ├─ GET /health           {status: healthy}
  └─ GET /api/version      environment-based version / commit / platform
```

The server has no external runtime dependencies, database, login, or user-submitted data. All assets are same-origin. Typography uses system fallbacks if Space Grotesk or IBM Plex Mono is not installed. The hooded ghost is original text artwork, not a licensed character asset.

The status panel requests both endpoints with a six-second timeout and no cache. Failed HTTP responses, invalid metadata, invalid JSON, or network failures clear stale fields and show UNAVAILABLE. A non-healthy status in a successful response shows DEGRADED. Refresh requests cannot overlap through the disabled button. Text is assigned using `textContent`.

The Flask factory reads non-secret runtime configuration once at startup. The HTML and version API share `APP_VERSION`. API responses specify `Cache-Control: no-store`. The same-origin content security policy excludes inline scripts, external resources, embedded objects, and framing.

## Intended later pipeline (not implemented/deployed)

```text
GitHub PR       → tests → container build validation
GitHub main push → tests → Docker build → SHA-tagged ECR image
                                        → explicit service image update
                                        → wait for rollout
                                        → health + exact SHA verification
```

No credentials or deployment configuration are included at this visual checkpoint. AWS App Runner is the proposed target from the brief, subject to current availability, costs, and account eligibility. Confirm those before choosing or provisioning a deployment target.
