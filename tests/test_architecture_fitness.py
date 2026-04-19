import os
from pathlib import Path


def test_services_do_not_import_main():
    """Fitness function: service modules must not import the HTTP controller (`app.main`).

    This enforces separation of concerns: services are application/business logic
    and should not depend on controller layer.
    """
    repo_root = Path(__file__).resolve().parents[1]
    services_dir = repo_root / "src" / "app" / "services"
    assert services_dir.exists(), "services directory missing"

    offenders = []
    for py in services_dir.rglob("*.py"):
        txt = py.read_text(encoding="utf8")
        if "import app.main" in txt or "from app.main" in txt:
            offenders.append(str(py.relative_to(repo_root)))

    assert not offenders, f"Service modules should not import app.main: {offenders}"


def test_integrations_facade_present():
    """Fitness function: integrations facade should exist to protect variations.
    """
    try:
        from app.integrations.facade import IntegrationsFacade  # noqa: F401
    except Exception as exc:  # pragma: no cover - test signalling
        raise AssertionError("IntegrationsFacade not importable") from exc
