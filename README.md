# Gitara — локальний Git-ассистент (polinas)

Коротко: Gitara — приватний, локальний інструмент‑помічник для системи контролю версій Git, який використовує компактні мовні моделі (SLM) для автоматизації рутинних дій (згенерувати commit message, скласти опис PR, підготувати changelog тощо) без передачі коду в хмару.

Цей документ — робочий мастер‑план репозиторію. Він містить візію, архітектурні рішення, політику роботи з даними та інструкції для розробника. Якщо ви потрапили сюди як новий учасник — почніть з розділу "Developer quickstart".

---

## Vision

- Забезпечити приватний та детермінований інструмент для перетворення змін у коді (diff) на якісні, стандартизовані commit‑повідомлення та інші текстові артефакти.
- Виконання локально, із можливістю використовувати різні бекенди інференсу (CPU, Apple Silicon, GPU) через стандартизований адаптер.
- Зберегти контроль над даними: жодні PII/PHI чи нерелевантні доменні артефакти не повинні проникати в датасети або пайплайн моделі.

---

## Поточний статус (важливі зауваги)

- README був порожнім — перезаписано цим мастер‑планом.
- В робочому просторі було виявлено семантично нерелевантні файли (карти, SVG, ветеринарні нотатки). Вони винесені в ігнорований архів `archives/polinas_artifacts/` та зафіксовані у `ARCHIVE_MANIFEST.md`.
- Додано базові правила ігнорування (`.gitignore`) та хук `check-added-large-files` у `.pre-commit-config.yaml` для запобігання випадкових комітів великих артефактів.

---

## Архітектура репозиторію

- `src/gitara/` — основна бізнес‑логіка: парсинг `git diff`, формування контексту, трансформація у prompt для LLM.
- `src/gitara/backends/` — адаптери бекендів інференсу (абстракція `LLMProvider`).
- `data/` — лише curated instruction templates та few‑shot examples (тільки те, що пройшло валідацію та очищення).
- `tests/` — unit/integration tests (mocking subprocess/git invocations).
- `.github/workflows/` — CI (mypy/ruff/black/pytest/detect-secrets).

---

## Модель та інференс — технічні вимоги

- Рекомендовані початкові SLM: Qwen3-0.6B (ефективність), Qwen3-4B (точність). Усі моделі повинні супроводжуватись ліцензійною перевіркою.
- Політика квантування: використовувати `llm-compressor` для конвертації в fp8 (за потреби) та збереження артефактів у згортаному форматі (`.gguf`, `.safetensors`).
- Абстракція інференсу: реалізувати `LLMProvider` (adapter pattern) із методом `generate_commit_message(diff_text: str, **opts) -> str`.
- Підтримувані рантайми: `vLLM` (GPU), `llama.cpp` (CPU/Apple Silicon), HuggingFace Transformers (для досліджень).

---

## Політика даних і гігієна робочого простору

- Забороняється зберігати у `data/` нерелевантні артефакти: `*.html`, `*.svg`, `*.geojson`, медичні чи персональні тексти тощо.
- Всі великі файли моделей та ваг повинні бути в `.gitignore` і зберігатись у зовнішньому реєстрі (S3/MinIO або release artifacts). Не використовувати Git LFS для постійних ваг без чіткої політики.
- У випадку виявлення сторонніх артефактів: перемістити їх в окремий приватний репозиторій/архів і зафіксувати в `ARCHIVE_MANIFEST.md`.

---

## CI / QA (обов'язкові налаштування)

- `mypy` у strict режимі (mypy.ini / pyproject.toml): `strict = True`, `disallow_untyped_defs = True`, `disallow_any_generics = True`, `ignore_missing_imports = True`.
- Pre-commit hooks: `ruff`, `black`, `isort`, `detect-secrets`, `check-added-large-files`.
- GitHub Actions: збірка з Python 3.11/3.12, виконання `mypy`, `ruff`, `black --check`, `pytest`, `detect-secrets scan --baseline .secrets.baseline.json`.

---

## Developer quickstart

1. Створити середовище та встановити залежності:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Встановити pre-commit та запустити перевірки:

```bash
pre-commit install
pre-commit run --all-files
```

3. Запустити тести та локальний сервер (dev):

```bash
pytest -q
export PYTHONPATH=src
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Acceptance criteria (мінімальні)

- README + DATA_POLICY + SECURITY.md присутні і актуальні.
- Жодних нерелевантних `.html`/`.svg`/геофайлів у `git ls-files` для `data/` або `src/`.
- CI проходить для головних перевірок: `mypy(strict)`, `ruff`, `black`, `pytest`.
- Існує `LLMProvider` інтерфейс і як мінімум один адаптер для CPU (llama.cpp) у `src/gitara/backends/`.

---

## Roadmap (коротко)

1. (0–3d) Санітарне очищення: архівувати сторонні файли, оновити `.gitignore`, baseline detect-secrets.
2. (3–10d) Документація: завершити README, DATA_POLICY, SECURITY, CONTRIBUTING.
3. (1–3w) QA: mypy strict, pre-commit, CI розширити для автоматичного сканування моделей і валідації data/.
4. (2–6w) Рефакторинг: Adapter pattern для LLM, шаблони промптів (Jinja2), coverage tests for diff→prompt pipeline.
5. (1–3mo) Production polish: model packaging, monitoring, memory/VRAM management and model fallback strategies.

---

Якщо погоджуєтесь, я можу одразу:

- перемістити в `src/gitara/` шаблон інтерфейсу `LLMProvider` і створити простий CPU адаптер (llama.cpp stub), або
- підготувати пул‑реквест (PR) з цими змінами та відкликанням архівних шаблонів.

Оберіть наступний крок або скажіть «роби сам» — я продовжу з реалізацією адаптера `LLMProvider`.
