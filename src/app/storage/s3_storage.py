import os
import shutil
from typing import Any

# boto3 is an optional dependency; avoid import-time failures in lightweight
# developer environments by making it optional and falling back to local storage.
try:
    import boto3
except Exception:
    boto3 = None

try:
    from botocore.client import Config
    from botocore.exceptions import EndpointConnectionError
except Exception:
    # botocore may not be installed in lightweight developer environments;
    # provide fallbacks so import-time does not fail.
    class _EndpointConnectionError(Exception):
        pass
    EndpointConnectionError = _EndpointConnectionError
    Config = None
from app.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET


class S3Storage:
    """S3/MinIO storage wrapper that tolerates missing MinIO by falling
    back to a local filesystem storage. Initialization is non-fatal so the
    application can start in developer environments without MinIO.
    """
    def __init__(self) -> None:
        self.bucket: str = MINIO_BUCKET
        self.endpoint: str = MINIO_ENDPOINT
        self._use_minio: bool = False
        self.client: Any = None
        # Defer network calls until an upload is attempted to avoid long
        # import-time delays when MinIO is not available in the environment.
        # Only attempt to initialize a boto3 client if the library is present
        if boto3 is not None:
            try:
                kwargs = dict(
                    service_name='s3',
                    endpoint_url=f'http://{MINIO_ENDPOINT}',
                    aws_access_key_id=MINIO_ACCESS_KEY,
                    aws_secret_access_key=MINIO_SECRET_KEY,
                    region_name='us-east-1'
                )
                if Config is not None:
                    kwargs['config'] = Config(signature_version='s3v4')
                # note: boto3 may raise if network unreachable; catch broadly
                self.client = boto3.client(**kwargs)
            except Exception:
                self.client = None
        else:
            self.client = None
        # We'll optimistically assume MinIO is not in use until a call succeeds
        self._use_minio = False

        # Local fallback directory
        self._local_dir: str = os.path.join(os.getcwd(), 'data', 'local_storage')
        os.makedirs(self._local_dir, exist_ok=True)

    def upload_file(self, local_path: str, object_name: str) -> str:
        # Try using MinIO if a client is configured; wrap network calls so
        # failures do not prevent the app from functioning.
        if self.client is not None:
            try:
                # Ensure bucket exists (non-fatal)
                try:
                    self.client.head_bucket(Bucket=self.bucket)
                except Exception:
                    try:
                        self.client.create_bucket(Bucket=self.bucket)
                    except Exception:
                        pass

                self.client.upload_file(local_path, self.bucket, object_name)
                self._use_minio = True
                return f"http://{self.endpoint}/{self.bucket}/{object_name}"
            except Exception:
                # If any network/endpoint error occurs, fall back to local copy
                self._use_minio = False
                pass

        # Fallback: copy to a local storage dir and return a file:// URL
        dest = os.path.join(self._local_dir, object_name.replace('/', os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(local_path, dest)
        return f"file://{dest}"

    def generate_presigned_url(self, object_name: str, expires: int = 3600) -> str:
        if self._use_minio:
            try:
                return str(self.client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket, 'Key': object_name},
                    ExpiresIn=expires
                ))
            except Exception:
                pass
        # For local fallback return a file URL if exists
        local_path = os.path.join(self._local_dir, object_name.replace('/', os.sep))
        if os.path.exists(local_path):
            return f"file://{local_path}"
        raise FileNotFoundError(object_name)
