import pytest

from app import create_app
from app.ascii_art import generate_ghost, generate_gallery


@pytest.fixture
def app():
    return create_app({"TESTING": True})


def test_portfolio_identity_sections_and_links(app):
    response = app.test_client().get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    for value in ["Zhivko Petkov", "Cybersecurity student", "https://github.com/nvm0r",
                  "mailto:zhivkop3@gmail.com", 'id="about"', 'id="projects"',
                  'id="status"', 'id="contact"']:
        assert value in html


def test_health_is_deterministic(app):
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}
    assert response.headers["Cache-Control"] == "no-store"


def test_metadata_uses_environment(monkeypatch):
    values = {"APP_VERSION": "v2.3.4", "APP_ENV": "test", "GIT_SHA": "a" * 40,
              "APP_PLATFORM": "Test container"}
    for name, value in values.items():
        monkeypatch.setenv(name, value)
    client = create_app({"TESTING": True}).test_client()
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json == {"version": "v2.3.4", "environment": "test",
                             "commit": "a" * 40, "platform": "Test container"}
    assert "v2.3.4" in client.get("/").get_data(as_text=True)


def test_metadata_defaults_are_local(monkeypatch):
    for key in ("APP_VERSION", "APP_ENV", "GIT_SHA", "APP_PLATFORM"):
        monkeypatch.delenv(key, raising=False)
    data = create_app({"TESTING": True}).test_client().get("/api/version").json
    assert data["environment"] == "local"
    assert data["commit"] == "uncommitted"
    assert data["version"] == "v0.1.0-dev"


def test_missing_cv_has_no_dead_download_link(app, tmp_path):
    app.static_folder = str(tmp_path)
    html = app.test_client().get("/").get_data(as_text=True)
    assert "CV coming soon" in html
    assert "docs/cv.pdf" not in html


def test_supplied_cv_can_be_downloaded(app, tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    pdf = b"%PDF-1.4\n% Test fixture only\n"
    (docs / "cv.pdf").write_bytes(pdf)
    app.static_folder = str(tmp_path)
    client = app.test_client()
    html = client.get("/").get_data(as_text=True)
    assert '/static/docs/cv.pdf' in html
    assert "Download CV" in html
    assert client.get("/static/docs/cv.pdf").data == pdf


@pytest.mark.parametrize("asset,mimetype", [
    ("css/style.css", "text/css"), ("js/main.js", "javascript"),
    ("images/favicon.svg", "image/svg+xml"),
])
def test_static_assets(app, asset, mimetype):
    response = app.test_client().get(f"/static/{asset}")
    assert response.status_code == 200
    assert mimetype in response.content_type


def test_security_headers(app):
    response = app.test_client().get("/")
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_unknown_route_is_not_a_false_success(app):
    assert app.test_client().get("/does-not-exist").status_code == 404


def test_generated_art_fits_hero_and_changes_between_requests(app):
    for _ in range(100):
        art, render_id = generate_ghost()
        assert len(art.splitlines()) == 20
        assert all(len(row) == 35 for row in art.splitlines())
        assert len(render_id) == 8
    client = app.test_client()
    first = client.get("/")
    second = client.get("/")
    assert first.data != second.data
    assert first.headers["Cache-Control"] == "no-store"
    assert b"Randomly generated ASCII" in first.data


def test_gallery_has_distinct_subjects_in_the_same_frame():
    gallery = generate_gallery()
    assert {item["id"] for item in gallery} == {
        "ghost", "robot", "skull", "cat", "satellite", "moth", "portal"
    }
    assert len({item["art"] for item in gallery}) == 7
    for item in gallery:
        assert len(item["art"].splitlines()) == 20
        assert all(len(row) == 35 for row in item["art"].splitlines())
