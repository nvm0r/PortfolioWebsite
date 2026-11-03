# Local Docker verification — 2026-11-02

- Image: `ghost-shell-portfolio:v1` built successfully.
- Linux Python 3.12.14, Flask 3.1.3, Gunicorn 26.2.0.
- Non-root UID/GID 10001; two Gunicorn workers.
- Initial port 8080 binding failed because a host process was already listening there. Used 8081:8080 instead.
- Fixed the user's home directory so Gunicorn's control socket can initialize without a permission error.
- GET http://localhost:8081/ returned 200.
- GET /health returned `{"status":"healthy"}`.
- GET /api/version returned `{"commit":"uncommitted","environment":"local-docker","platform":"Docker","version":"v1.0.0"}`.
- Container name: `ghost-shell`. Left running for local review.

This verifies a local container only, not a cloud deployment or CI/CD pipeline.
