import os
import tempfile
import shutil
import sys
import importlib

def test_s3storage_local_fallback(tmp_path):
    # Patch sys.modules to simulate missing boto3
    sys.modules['boto3'] = None
    sys.modules['botocore'] = None
    sys.modules['botocore.client'] = None
    sys.modules['botocore.exceptions'] = None
    import app.storage.s3_storage as s3mod
    importlib.reload(s3mod)
    S3Storage = s3mod.S3Storage
    storage = S3Storage()
    # Create a temp file to upload
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"testdata123")
        src = f.name
    dest_name = "testdir/testfile.txt"
    url = storage.upload_file(src, dest_name)
    assert url.startswith("file://"), f"Expected file:// url, got {url}"
    # Check file exists in fallback dir
    local_dir = os.path.join(os.getcwd(), 'data', 'local_storage', 'testdir')
    local_file = os.path.join(local_dir, 'testfile.txt')
    assert os.path.exists(local_file), f"Expected file at {local_file}"
    with open(local_file, 'rb') as f:
        assert f.read() == b"testdata123"
    # Cleanup
    os.unlink(src)
    shutil.rmtree(os.path.join(os.getcwd(), 'data'), ignore_errors=True)