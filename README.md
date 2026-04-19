# Gitara — локальний Git-асистент (Master Plan)

Коротко: **Gitara** — це локальний інструмент‑асистент для роботи з Git, що використовує компактні дистильовані мовні моделі (SLM) для генерації повідомлень комітів, підказок до рев'ю та допоміжних CLI‑операцій, при цьому повністю працює локально (без викликів зовнішніх API), щоб гарантувати приватність коду.

## Vision
- Захист конфіденційності — нічого з вихідного коду не відправляється в хмару.
- Мінімальна латентність — відповіді < 2s на споживчому обладнанні.
- Модульність — заміна backend'ів LLM без змін бізнес‑логіки.

## Архітектура (високий рівень)
- `src/gitara/` — ядро бізнес‑логіки: парсинг `git diff`, формування контексту, правила постобробки.
- `src/gitara/backends/` — адаптери LLM (інтерфейс `LLMProvider`). Приклади: `LlamaCppProvider`, `VLLMProvider`.
- `data/` — дозволені інструкції/шаблони промптів (`data/instructions/`, `data/templates/`). Інші дані — поза цим репо.
- `tests/` — модульні та інтеграційні тести (з моками subprocess для `git`).

## Політика даних
- Жодні неочищені зовнішні датасети (геодані, медичні тексти, карти тощо) не повинні зберігатися в цьому репозиторії.
- Якщо потрібно зберегти сторонні артефакти — створити окремий репозиторій (наприклад `polinas-maps`) або використовувати зовнішнє сховище (S3/MinIO) та DVC.

## Модельна політика і інференс
- Підтримуються SLM (наприклад Qwen3‑0.6B або 4B) з форматом квантування `fp8` через `llm-compressor`.
- Інтерфейс `LLMProvider` повинен бути абстрактним і детермінованим — бізнес‑логіка викликає тільки цей інтерфейс.
- Пакування ваг: великі файли (\*.gguf, \*.safetensors, \*.pt) не комітяться; використовувати релізи/артефакти або реєстр артефактів.

## Quickstart (локально)
1. Створити віртуальне середовище і встановити deps:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
2. Запустити сервер (dev):
```bash
export PYTHONPATH=src
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
3. Запуски для inference (CPU fallback): налаштування через `src/gitara/backends/`.

## Розробка і QA
- `mypy` — строгий режим (`mypy.ini` / `pyproject.toml`): `strict = True`.
- `pre-commit` хуки: `ruff`, `black`, `isort`, `detect-secrets`, `check-added-large-files`.
- Запустити тести:
```bash
pytest -q
```

## Data/Prompt Engineering
- Зберігайте шаблони промптів у `data/templates/` як Jinja2‑шаблони.
- Тренуйте few‑shot приклади у `data/instructions/` (тільки очищені від PII/PHI).

## CI / Security
- CI має виконувати: `ruff`, `black --check`, `mypy`, `pytest`, `detect-secrets scan --baseline .secrets.baseline.json`.
- Заборонити коміти великих ваг моделей через pre‑commit.

## Roadmap / Acceptance Criteria
- README + DATA_POLICY + SECURITY.md присутні.
- Немає нерелевантних артефактів у головному репо.
- CI зелений: `mypy strict`, `ruff`, `pytest` (базове покриття).

## Контакти та внесок
- Див. `CONTRIBUTING.md` для правил внеску та політик огляду коду.

---
Документ: початковий майстер‑план; подальші деталі та операційні runbooks будуть додані в окремі документи (`DATA_POLICY.md`, `SECURITY.md`, `DEPLOYMENT.md`).