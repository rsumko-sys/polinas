import os
from dotenv import load_dotenv

# Load .env early so env lookups pick up local values during development
load_dotenv()

# Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_SESSIONS_DB_ID = os.getenv("NOTION_SESSIONS_DB_ID")
NOTION_ISSUES_DB_ID = os.getenv("NOTION_ISSUES_DB_ID")
NOTION_DRILLS_DB_ID = os.getenv("NOTION_DRILLS_DB_ID")
NOTION_ANALYSIS_DB_ID = os.getenv("NOTION_ANALYSIS_DB_ID")
NOTION_PLAN_DB_ID = os.getenv("NOTION_PLAN_DB_ID")
NOTION_HORSE_CONTEXT_DB_ID = os.getenv("NOTION_HORSE_CONTEXT_DB_ID")
NOTION_OSINT_CASES_DB_ID = os.getenv("NOTION_OSINT_CASES_DB_ID")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# MinIO / S3
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "horse-data")

# PostgreSQL (для метаданих, якщо використовуємо не тільки Notion)
POSTGRES_DSN = os.getenv("POSTGRES_DSN", "postgresql://user:pass@db:5432/horse_db")

# Redis (черги)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Neo4j (граф OSINT)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "pass")

# Інше
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
