"""Flask application: a single-page form that runs an analysis and shows the report.

Local-only by construction: the app is meant to be served on 127.0.0.1 and performs no
network I/O. Folder paths are typed by the user (browsers cannot expose real paths).
"""

from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import Any

from flask import Flask, Response, abort, jsonify, render_template, request, session

from .. import __version__
from ..analyzer_bridge import AnalyzerError
from ..orchestrator import InvalidFolderError, analyze, analyze_dev
from ..report import build_tree_data, render_json, render_text

_LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})

# Remember the last folder/prefix across runs. Stored locally in the user's home; never
# leaves the machine. Best-effort: any I/O error degrades to "no memory", not a crash.
# CODEANALYZER_STATE overrides the location (used by tests to avoid touching real $HOME).
def _state_file() -> Path:
    override = os.environ.get("CODEANALYZER_STATE")
    return Path(override) if override else Path.home() / ".codeanalyzer" / "state.json"


def _load_state() -> dict[str, str]:
    try:
        data = json.loads(_state_file().read_text(encoding="utf-8"))
        return {"folder": str(data.get("folder", ""))}
    except (OSError, ValueError):
        return {"folder": ""}


def _save_state(folder: str) -> None:
    try:
        path = _state_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"folder": folder}), encoding="utf-8")
    except OSError:
        pass  # persistence is a convenience, never fatal


def _slug(value: str) -> str:
    """Turn an arbitrary string into a safe HTML id/anchor fragment."""
    return "".join(ch if ch.isalnum() else "-" for ch in value)


def create_app() -> Flask:
    app = Flask(__name__)
    app.add_template_filter(_slug, "slug")
    app.jinja_env.globals["app_version"] = __version__  # type: ignore

    # Local access control. On a shared machine another local user could otherwise reach
    # 127.0.0.1:<port>. We mint a one-time token (printed/opened by __main__); the first
    # GET carrying it is bound to a Strict-SameSite session cookie, so later requests and a
    # malicious cross-site page cannot drive the app. Also pin the Host header to localhost
    # to defeat DNS-rebinding. Set CODEANALYZER_NO_AUTH=1 to disable on a trusted single-
    # user box. Disabled automatically under tests (app.config['TESTING']).
    app.secret_key = secrets.token_hex(32)
    app.config["ACCESS_TOKEN"] = secrets.token_urlsafe(16)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Strict")
    auth_disabled = os.environ.get("CODEANALYZER_NO_AUTH") == "1"

    @app.before_request
    def _guard() -> None:
        if app.config.get("TESTING") or auth_disabled:
            return None
        host = (request.host or "").rsplit(":", 1)[0]
        if host not in _LOCAL_HOSTS:  # DNS-rebinding / non-local Host header
            abort(403)
        if session.get("authed"):
            return None
        if request.method == "GET" and request.args.get("t") == app.config["ACCESS_TOKEN"]:
            session["authed"] = True
            return None
        abort(403)

    @app.errorhandler(403)
    def _forbidden(_e: object) -> tuple[str, int]:
        return (
            "<h1>403 — access blocked</h1><p>codeAnalyzer is local-only. Open the "
            "tokenized URL printed in the terminal (<code>http://127.0.0.1:PORT/?t=…</code>). "
            "Each run uses a fresh token.</p>",
            403,
        )

    @app.after_request
    def _no_cache(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/")
    def index() -> str:
        state = _load_state()
        return render_template(
            "index.html",
            folder=state["folder"],
        )

    @app.get("/dev")
    def dev_index() -> str:
        state = _load_state()
        return render_template(
            "dev.html",
            folder=state["folder"],
        )

    @app.get("/pick-folder")
    def pick_folder() -> Any:
        """Open a native OS folder picker on this machine and return the chosen path.

        Runs entirely locally (a desktop dialog on the same box that serves the UI). If
        Tk is unavailable or the dialog fails, the UI falls back to manual path entry.
        """
        if app.config.get("TESTING"):
            return jsonify({"path": "", "available": False})  # no blocking GUI in tests
        try:
            import tkinter
            from tkinter import filedialog

            root = tkinter.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            chosen = filedialog.askdirectory(title="Select folder to analyze")
            root.destroy()
        except Exception:  # noqa: BLE001 - any GUI/Tk failure degrades gracefully
            return jsonify({"path": "", "available": False})
        return jsonify({"path": chosen or "", "available": True})

    @app.post("/dev_analyze")
    def run_dev_analysis() -> str:
        folder = (request.form.get("folder") or "").strip()
        if not folder:
            return render_template("dev.html", folder="", error="Please enter a folder path.")
        
        try:
            result = analyze_dev(Path(folder))
        except InvalidFolderError as err:
            return render_template("dev.html", folder=folder, error=str(err))
        except AnalyzerError as err:
            return render_template("dev.html", folder=folder, error=f"C# analyzer error: {err}")
            
        _save_state(folder)
        return render_template("dev_results.html", folder=folder, result=result)

    @app.post("/analyze")
    def run_analysis() -> str:
        folder = (request.form.get("folder") or "").strip()

        if not folder:
            return render_template(
                "index.html", folder="", error="Please enter a folder path."
            )

        try:
            result = analyze(Path(folder))
        except InvalidFolderError as err:
            return render_template("index.html", folder=folder, error=str(err))
        except AnalyzerError as err:
            return render_template(
                "index.html", folder=folder, error=f"C# analyzer error: {err}"
            )

        _save_state(folder)

        note = None
        if result.summary.file_count == 0:
            note = "No supported source files were found under that folder."

        # TCF methods are sent to the page as JSON so the browser can paginate/search them
        # client-side -- this keeps the DOM light even for codebases with thousands of
        # TCF methods. Everything stays local (no extra requests).
        tcf_sorted = sorted(result.tcf_methods, key=lambda m: (m.file, m.start_line))
        tcf_data = [
            {
                "id": "tcf-" + _slug(f"{m.file}::{m.name}"),
                "name": m.name,
                "file": m.file,
                "start": m.start_line,
                "end": m.end_line,
                "cx": m.cyclomatic_complexity,
                "tc": m.time_complexity,
                "tc_line": m.tc_line,
                "total": m.counts.total,
                "code": m.counts.code,
                "comment": m.counts.comment,
                "inline": m.counts.inline_comment,
                "blank": m.counts.blank,
                "ratio": round(m.counts.comment_ratio, 4),
                "helpers": [h.name for h in m.used_helpers],
            }
            for m in tcf_sorted
        ]

        # Helper usage is also sent as JSON and paginated client-side (a large codebase can
        # have thousands of helpers).
        helper_data = [
            {
                "name": u.helper.name,
                "file": u.helper.file,
                "callers": list(u.callers),
            }
            for u in result.helper_usage
        ]

        unused_method_data = [
            {
                "name": m.name,
                "file": m.file,
                "start": m.start_line,
                "end": m.end_line,
                "cx": m.cyclomatic_complexity,
            }
            for m in result.unused_methods
        ]

        unused_definition_data = [
            {
                "name": d.name,
                "type": d.type,
                "line": d.line,
                "file": d.file,
            }
            for d in result.unused_definitions
        ]

        return render_template(
            "results.html",
            folder=folder,
            result=result,
            tree=build_tree_data(result.files),
            tcf_data=tcf_data,
            helper_data=helper_data,
            unused_method_data=unused_method_data,
            unused_definition_data=unused_definition_data,
            report_text=render_text(result),
            report_json=render_json(result),
            note=note,
        )

    return app
