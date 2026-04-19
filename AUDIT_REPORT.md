# Комплексний технічний аудит проєкту Gitara

Дата: 2026-04-19

Мета документа
--------------
Цей звіт допомагає зняти поточний стан коду, інфраструктури та робочого простору
проєкту Gitara, визначити ризики (зокрема «забруднення контексту»), і надати
поетапну стратегію рефакторингу для переходу до зрілої інженерної платформи.

Коротке резюме (Executive summary)
----------------------------------
- README був порожнім — відсутній майстер‑план (blocker).
- У робочому просторі знайдено сторонні артефакти (карти, SVG, медичні дані),
  що призводить до високого ризику data poisoning для SLM.
- Репозиторій має хорошу базову структуру (`src/`, `tests/`) і початкові інструменти
  CI/QA, але потребує формалізації: `mypy strict`, розширений `pre-commit`,
  чітка політика даних і адаптерна архітектура для LLM backend.

Ключові знахідки
---------------

1) Документація і майстер‑план
- README.md був семантично пустим; це створює «Blind Driven Development" —
  відсутність критеріїв приймання та архітектурних обмежень. Я додав початковий
  майстер‑план у [README.md](README.md).

2) «Забруднення контексту" (Context Pollution)
- Знайдені артефакти: `kharkiv_horse_clubs_map.html`, `data/terrain/route_1625m_40pts.svg`,
  та набори текстів ветеринарної тематики. Ці файли не відносяться до задачі Gitara
  і становлять критичну загрозу для якості моделей.
- Дія: створено `archives/` (ігнорується Git) і переміщено знайдені файли туди.

3) Модульність і інтерфейси ML
- Бачимо ідею SLM (Qwen3‑0.6B/4B) і квантування (llm-compressor → fp8). Відсутній
  строгий адаптер між бізнес‑логікою (diff→prompt) та бекендом інференсу.
- Рекомендація: впровадити патерн Adapter з інтерфейсом `LLMProvider`.

4) CI / QA / Static typing
- Є `.pre-commit-config.yaml` і коміти про `mypy`. Потрібно: `mypy` у `strict` режимі,
  додати `ruff`, `black`, `isort`, `detect-secrets`, `check-added-large-files`.
- CI (GitHub Actions) повинен містити статичні перевірки, тести та скан секретів.

5) Залежності і reproducibility
- На macOS/Python 3.14 деякі бінарні колесa (pydantic-core) збираються локально;
  рекомендовано таргетувати Python 3.11/3.12 у CI/контейнерах або забезпечити Rust toolchain
  в build stage.

Технічний аналіз архітектури ML та інференсу
-----------------------------------------

Парадигма
- Gitara — локальний LLM‑асистент для Git; основні вимоги: приватність даних,
  низька латентність (<2s), детермінованість відповідей для CI‑тестів.

Квантування та оптимізація
- Використання `llm-compressor` для квантування у `fp8` — виправданий вибір:
  значне зменшення пам'яті з прийнятним падінням якості (~10–15%).
- Для GPU: `vLLM` / Triton backend; для CPU/Apple Silicon: `llama.cpp` або `GGML`.

Архітектурні рекомендації
- Впровадити `LLMProvider` (Adapter) з мінімальною контрактною сигнатурою:

```py
from abc import ABC, abstractmethod
from typing import Optional, List, Dict

class LLMProvider(ABC):
    @abstractmethod
    def generate_commit_message(self, diff_text: str, examples: Optional[List[Dict]] = None) -> str:
        pass
```

- Реалізувати адаптери `LlamaCppProvider`, `VLLMProvider`, `HFTransformersProvider`.
- Інтерфейс повинен підтримувати timeouts, max_tokens, temperature і hooks для post-processing.

Аналіз «забруднення контексту" і ризиків
---------------------------------------

Чому це критично
- SLM мають обмежену ємність репрезентації; при fine‑tuning навіть невеликі
  некоректні корпуси швидко вбудовуються у модель, викликаючи неправильні
  відповіді (data poisoning).

Миттєві ризики та пом'якшення
- Витік PII/PHI → негайна ротація секретів, видалення із історії, ітерація на політиці.
- Нізька якість відповідей → чистка `data/`, додавання whitelist/blacklist тем.

Gap Analysis (стисло)
- Документація: CRITICAL -> потрібно README, DATA_POLICY, SECURITY.
- Data hygiene: CRITICAL -> архів / виняток у .gitignore.
- Inference pipeline: HIGH -> Adapter + packaging.
- QA: MEDIUM -> mypy strict + pre-commit + CI.

Детальна стратегія рефакторингу (по фазах)
-------------------------------------------

Фаза 1 — Радикальне санітарне очищення (0–3 дні)
- Ідентифікувати і перемістити всі нерелевантні файли в `archives/` або інший репо.
- Оновити `.gitignore` (включив `*.html`, `*.svg`, `*.geojson`, `*.gguf`, `*.safetensors`).
- Додати pre-commit hook `check-added-large-files` і `detect-secrets` (baseline).

Фаза 2 — Майстер‑план і політики (0–7 днів)
- Переписати `README.md` (зроблено).
- Додати `DATA_POLICY.md`, `SECURITY.md` (зроблено).
- Додати `CONTRIBUTING.md` та `DEPLOYMENT.md` з runbooks.

Фаза 3 — CI / QA укріплення (1–2 тижні)
- Налаштувати `mypy.ini` (strict):

```ini
[mypy]
strict = True
disallow_untyped_defs = True
disallow_any_generics = True
ignore_missing_imports = True
```

- Оновити `.pre-commit-config.yaml` з `ruff`, `black`, `isort`, `detect-secrets`.
- CI job: `ruff`, `black --check`, `mypy`, `pytest`, `detect-secrets scan`.

Фаза 4 — Adapter і Prompt Engine (2–6 тижнів)
- Ввести `LLMProvider` (реалізації для CPU/GPU) у `src/gitara/backends/`.
- Запровадити шаблони промптів у `data/templates/` (Jinja2) і тестову набірку few-shot.
- Як приклад, помістити `data/templates/commit_prompt.j2` і тестувати детерміновано.

Фаза 5 — Packaging, quantize pipeline, releases (2–8 тижнів)
- Скрипт `scripts/build_model.sh`:
```bash
# 1. validate license
# 2. run llm-compressor --quantize fp8 --input model.safetensors --output model.gguf
# 3. upload artifact to S3 or create GH Release
```
- У CI: build artifact only on release tags; не зберігати великі файли у git.

Фаза 6 — Production hardening та monitoring (1–3 міс.)
- VRAM / memory limits у адаптерах; idle tensor unloading; prometheus metrics for inference.
- Add error handling for OOM and graceful fallback to smaller models.

Тестування і валідація
----------------------
- Модульні тести для diff→prompt парсингу (mock subprocess.run для `git`).
- Інтеграційні тести з `LLMProvider` stub (`LlamaCppProvider` deterministic stub exists).
- E2E smoke: run local server, POST diff → expect Conventional Commit message format.

Контроль якості даних
---------------------
- Кожен файл у `data/` повинен мати `METADATA.md` з походженням, ліцензією, датою
  очищення і коротким переліком трансформацій (PII removal).

Операційні команди (швидкий набір)
---------------------------------
Архівація артефактів (приклад):
```bash
bash scripts/archive_artifacts.sh
```

Перевірка заборонених файлів у git:
```bash
git ls-files | egrep '\.(html|svg|geojson|shp|gguf|safetensors|pt|bin)$' || true
```

CI приклад (частини):
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: ruff check .
      - run: black --check .
      - run: mypy src/
      - run: pytest -q
      - run: detect-secrets scan --baseline .secrets.baseline.json
```

Ризики та пом'якшувальні заходи
--------------------------------
- Data poisoning: архівування та жорстке ігнорування, human review перед використанням у fine-tuning.
- Комміти секретів: `detect-secrets` + immediate rotation + git filter-repo if exposed.
- Build pain на нестандартних Python: pin CI to 3.11/3.12 or include Rust toolchain in builders.

Пріоритетні критерії приймання (Acceptance Criteria)
---------------------------------------------------
1. Присутні: `README.md`, `DATA_POLICY.md`, `SECURITY.md`, `CONTRIBUTING.md`.
2. Немає нерелевантних артефактів у `git ls-files`.
3. CI проходить: `mypy` (strict), `ruff`, `black --check`, `pytest` (базове покриття).
4. Існує `LLMProvider` інтерфейс і принаймні один детермінований stub adapter для тестів.

Дорожня карта (скорочено)
------------------------
- 0–3 дні: Фаза 1 (санітарія, .gitignore, pre-commit hooks).
- 3–10 днів: Фаза 2 (документи, policies, CONTRIBUTING).
- 1–3 тижні: Фаза 3 (CI/QA жорсткий режим).
- 2–6 тижнів: Фаза 4 (Adapter, prompts, unit tests).
- 2–8 тижнів: Фаза 5 (build pipeline, model packaging).
- 1–3 міс.: Фаза 6 (monitoring, production hardening).

Додатки
-------
- Файли, додані/оновлені під час першої ітерації:
  - [README.md](README.md)
  - [.gitignore](.gitignore)
  - [.pre-commit-config.yaml](.pre-commit-config.yaml)
  - [DATA_POLICY.md](DATA_POLICY.md)
  - [SECURITY.md](SECURITY.md)
  - `archives/` (локальна директорія для переміщених артефактів)

Заключні нотатки
-----------------
Gitara має усі інженерні передумови для того, щоб стати стабільним локальним
LLM‑асистентом для розробників. Пропонований план — практичний і поетапний;
важливо виконувати його дисципліновано, починаючи з санітарного прибирання і
закінчуючи формалізацією інтерфейсів та процесів упаковки моделей.
