"""Local-only Flask web UI for the analyzer."""

from .server import create_app

__all__ = ["create_app"]
