"""
Pytest configuration for DUNK.ai tests.

Adds the `backend` directory to `sys.path` so the package can be imported
without installing it in editable mode.
"""

import sys
from pathlib import Path


def pytest_sessionstart(session):  # pragma: no cover - pytest hook
    """Ensure `backend` directory is importable before tests run."""
    project_root = Path(__file__).resolve().parents[1]
    backend_path = project_root / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

