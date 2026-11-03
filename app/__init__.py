import os
import secrets
from pathlib import Path

from flask import Flask, jsonify, render_template

from .content import PROFILE, SKILLS
from .ascii_art import generate_gallery


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        APP_VERSION=os.getenv("APP_VERSION", "v0.1.0-dev"),
        APP_ENV=os.getenv("APP_ENV", "local"),
        GIT_SHA=os.getenv("GIT_SHA", "uncommitted"),
        APP_PLATFORM=os.getenv("APP_PLATFORM", "Local Python / Flask"),
    )
    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        cv_available = (Path(app.static_folder) / "docs" / "cv.pdf").is_file()
        gallery = generate_gallery()
        artwork = secrets.choice(gallery)
        return render_template("index.html", profile=PROFILE, skills=SKILLS,
                               cv_available=cv_available, version=app.config["APP_VERSION"],
                               gallery=gallery, artwork=artwork)

    @app.get("/health")
    def health():
        return jsonify(status="healthy")

    @app.get("/api/version")
    def version():
        return jsonify(version=app.config["APP_VERSION"], environment=app.config["APP_ENV"],
                       commit=app.config["GIT_SHA"], platform=app.config["APP_PLATFORM"])

    @app.after_request
    def headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "base-uri 'self'; frame-ancestors 'none'"
        )
        if response.is_json or response.mimetype == "text/html":
            response.headers["Cache-Control"] = "no-store"
        return response

    return app
