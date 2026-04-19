import pytest

from app.integrations.facade import IntegrationsFacade


def test_upload_files_no_storage_raises():
    f = IntegrationsFacade()
    with pytest.raises(RuntimeError):
        f.upload_files([("/tmp/x", "k")])
