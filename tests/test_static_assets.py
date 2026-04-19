import os
import urllib.request
from urllib.error import HTTPError, URLError


def test_modal_css_exists_on_disk() -> None:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, "src", "app", "static", "styles", "modal.css")
    assert os.path.exists(path), f"modal.css not found at {path}"


def test_modal_css_served_http() -> None:
    url = "http://127.0.0.1:8000/static/styles/modal.css"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            code = getattr(resp, 'status', None) or resp.getcode()
            assert code == 200
            content = resp.read()
            assert len(content) > 0
    except HTTPError as e:
        raise AssertionError(f"HTTP error when fetching {url}: {e.code}")
    except URLError as e:
        raise AssertionError(f"URL error when fetching {url}: {e.reason}")
