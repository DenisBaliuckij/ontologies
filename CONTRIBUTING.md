# Contributing

*[Русская версия ниже](#вклад-в-проект)*

Thank you for contributing a language ontology to this repository. This document explains the schema that every ontology file must follow, and how to add a new one.

## Repository layout

```
ontologies/
├── files/                             # the ontology documents
│   ├── OntoLing.json                  # general/theoretical linguistics ontology (the base)
│   └── OntoKon.json                   # a language-specific instance (Konabère)
├── schemas/
│   ├── base-ontology.schema.json      # shared envelope + recursive concept-node shape
│   └── language-ontology.schema.json  # extends the base for a single-language instance
└── scripts/
    └── validate.py                    # validates every file in files/ against its schema
```

## The schema, in plain terms

Every ontology document has two parts:

1. **A fixed envelope.** A `meta` block (title, version, description, sources, ...) and seven top-level GOLD modules: `Core_Foundations`, `Phonetics_and_Phonology`, `Morphology`, `Syntax`, `Semantics`, `Interfaces_and_Integration`, `Relations_and_Properties`. This part is the same shape in every document, and the schema enforces it strictly — these keys must exist, spelled exactly this way.

2. **A free-form concept tree inside each module.** Inside `Morphology`, `Syntax`, etc., the actual linguistic content is a nested tree of concepts — the specific concept names, how deep the nesting goes, and which fields appear vary by language and by how much has been documented. The schema does **not** try to enumerate this vocabulary. Instead it enforces a general shape: at any point in the tree, a value must be one of:
   - a string (a definition, a note, free text),
   - a list of strings or of structured records (e.g. a list of dialect names, or a list of `{name, location, notes}` records),
   - a nested object (another sub-tree of concepts).

   Anything else — a bare number, a boolean, `null`, an empty object — is rejected. This is deliberately loose on vocabulary and strict on shape: it catches real mistakes (wrong data type, a stray typo'd structure) without forcing every language's ontology to use the same set of concept names.

Two schema files implement this:

- **`schemas/base-ontology.schema.json`** — the envelope plus the recursive concept-tree definition (`OntologyNode` / `OntologyValue`). This is what a general/theoretical ontology like `OntoLing.json` validates against directly, and what a language instance extends.
- **`schemas/language-ontology.schema.json`** — extends the base for a single-language instance. It adds required `meta` fields that identify the language (`language_name`, `iso_code`, `classification`, `location`) and a required top-level `Lexicon_Overview` section, and it closes the document (`unevaluatedProperties: false`) so a language file cannot contain any top-level section outside this list — meta, the seven base modules, and `Lexicon_Overview`.

## Adding a new language ontology

1. Copy the structure of `files/OntoKon.json` as your starting point — same seven modules, same `Lexicon_Overview` section, same `meta` shape.
2. Fill in `meta`:
   - `title`, `version` (e.g. `"1.0"`), `description`, `sources` (a non-empty list of citations), `gold_base_uri`.
   - `language_name` (human-readable), `iso_code` (**ISO 639-3**, three lowercase letters, e.g. `"bbo"`), `classification` (the genetic classification path), `location`.
   - `speaker_population`, `dialects`, `standard_dialect` are optional but encouraged when known.
3. Populate the seven modules and `Lexicon_Overview` with whatever level of detail your sources support. You do not need to fill in every GOLD concept — an incomplete but structurally valid document is fine; a structurally invalid one is not.
4. Save the file as `files/<Name>.json` (match the existing `OntoXxx.json` naming style).
5. Validate locally before opening a merge/pull request (see below).

## Validating locally

```bash
pip install -r requirements.txt
python scripts/validate.py
```

The script checks every file in `files/` and automatically picks the right schema: a file is validated as a language instance if its `meta.iso_code` or a top-level `Lexicon_Overview` is present, otherwise as the general/base ontology. It prints `OK`/`FAIL` per file, and for failures the exact location and reason (e.g. `meta/iso_code: 'BBO' does not match '^[a-z]{3}$'`).

## Common validation errors

| Error | Cause | Fix |
|---|---|---|
| `'Lexicon_Overview' is a required property` | Missing that section in a language instance | Add a `Lexicon_Overview` object at the top level |
| `'iso_code' is a required property` | Language `meta` is missing `iso_code` | Add the ISO 639-3 code |
| `... does not match '^[a-z]{3}$'` | `iso_code` isn't three lowercase letters | Use lowercase, e.g. `"bbo"` not `"BBO"` |
| `Additional properties are not allowed ('X' was unexpected)` | An unexpected top-level key, or a stray key alongside `allOf`/`oneOf` composition | Move the content into one of the seven modules or `Lexicon_Overview`, or check for a typo in a section name |
| `12345 is not of type 'string'` / `... 'array'` / `... 'object'` | A concept-tree leaf holds a number, boolean, or `null` | Express it as text, e.g. `"speaker_population": "60000"` (a string), not a bare number |

## Continuous integration

Every push and pull request runs `scripts/validate.py` over every file in `files/` (see `.github/workflows/validate.yml`). A file that doesn't conform to its schema fails the build — this is enforced automatically, not left to reviewers to catch by eye.

---

# Вклад в проект

*[English version above](#contributing)*

Спасибо за вклад в языковые онтологии этого репозитория. В этом документе описана схема, которой должен соответствовать каждый файл онтологии, и порядок добавления нового языка.

## Структура репозитория

```
ontologies/
├── files/                             # документы онтологий
│   ├── OntoLing.json                  # общая/теоретическая лингвистическая онтология (базовая)
│   └── OntoKon.json                   # экземпляр для конкретного языка (конкабере)
├── schemas/
│   ├── base-ontology.schema.json      # общий каркас + рекурсивная форма узла понятий
│   └── language-ontology.schema.json  # расширяет базовую схему для языкового экземпляра
└── scripts/
    └── validate.py                    # проверяет каждый файл в files/ по его схеме
```

## Схема простыми словами

Каждый документ онтологии состоит из двух частей:

1. **Фиксированный каркас.** Блок `meta` (название, версия, описание, источники и т.д.) и семь разделов верхнего уровня по системе GOLD: `Core_Foundations`, `Phonetics_and_Phonology`, `Morphology`, `Syntax`, `Semantics`, `Interfaces_and_Integration`, `Relations_and_Properties`. Эта часть имеет одинаковую форму во всех документах, и схема строго это проверяет — эти ключи обязаны присутствовать и называться именно так.

2. **Свободная структура понятий внутри каждого раздела.** Внутри `Morphology`, `Syntax` и других разделов реальное лингвистическое содержание — это вложенное дерево понятий: конкретные названия понятий, глубина вложенности и набор полей различаются от языка к языку и зависят от того, насколько подробно язык описан. Схема **не** пытается перечислить этот словарь понятий. Вместо этого она проверяет общую форму: в любой точке дерева значение может быть:
   - строкой (определение, примечание, свободный текст),
   - списком строк или структурированных записей (например, список названий диалектов или список записей вида `{name, location, notes}`),
   - вложенным объектом (ещё одно поддерево понятий).

   Всё остальное — голое число, булево значение, `null`, пустой объект — отклоняется. Это намеренно: схема не ограничивает используемый словарь понятий, но строго проверяет форму данных — это позволяет находить реальные ошибки (неверный тип данных, случайно испорченная структура), не заставляя онтологии разных языков использовать один и тот же набор понятий.

Схема реализована в двух файлах:

- **`schemas/base-ontology.schema.json`** — каркас плюс рекурсивное определение дерева понятий (`OntologyNode` / `OntologyValue`). По этой схеме напрямую проверяется общая/теоретическая онтология, например `OntoLing.json`, и её же расширяет схема языкового экземпляра.
- **`schemas/language-ontology.schema.json`** — расширяет базовую схему для экземпляра одного языка. Добавляет обязательные поля в `meta`, идентифицирующие язык (`language_name`, `iso_code`, `classification`, `location`), и обязательный раздел `Lexicon_Overview` верхнего уровня, а также закрывает документ (`unevaluatedProperties: false`), так что языковой файл не может содержать ничего, кроме `meta`, семи базовых разделов и `Lexicon_Overview`.

## Добавление новой языковой онтологии

1. Возьмите за основу структуру `files/OntoKon.json` — те же семь разделов, тот же раздел `Lexicon_Overview`, та же форма `meta`.
2. Заполните `meta`:
   - `title`, `version` (например, `"1.0"`), `description`, `sources` (непустой список источников), `gold_base_uri`.
   - `language_name` (человекочитаемое название), `iso_code` (**ISO 639-3**, три строчные латинские буквы, например `"bbo"`), `classification` (путь генетической классификации), `location`.
   - `speaker_population`, `dialects`, `standard_dialect` — необязательны, но желательны, если данные известны.
3. Заполните семь разделов и `Lexicon_Overview` с той степенью детализации, которую позволяют ваши источники. Не обязательно заполнять каждое понятие GOLD — неполный, но структурно корректный документ допустим; структурно некорректный — нет.
4. Сохраните файл как `files/<Название>.json` (придерживайтесь стиля именования `OntoXxx.json`, как в существующих файлах).
5. Проверьте файл локально перед созданием merge/pull request (см. ниже).

## Локальная проверка

```bash
pip install -r requirements.txt
python scripts/validate.py
```

Скрипт проверяет каждый файл в `files/` и автоматически выбирает нужную схему: файл проверяется как языковой экземпляр, если в `meta` присутствует `iso_code` или на верхнем уровне есть раздел `Lexicon_Overview`, иначе — как общая/базовая онтология. Для каждого файла выводится `OK`/`FAIL`, а при ошибке — точное место и причина (например, `meta/iso_code: 'BBO' does not match '^[a-z]{3}$'`).

## Частые ошибки проверки

| Ошибка | Причина | Исправление |
|---|---|---|
| `'Lexicon_Overview' is a required property` | В языковом экземпляре отсутствует этот раздел | Добавьте объект `Lexicon_Overview` на верхнем уровне |
| `'iso_code' is a required property` | В `meta` языка отсутствует `iso_code` | Добавьте код ISO 639-3 |
| `... does not match '^[a-z]{3}$'` | `iso_code` состоит не из трёх строчных букв | Используйте строчные буквы, например `"bbo"`, а не `"BBO"` |
| `Additional properties are not allowed ('X' was unexpected)` | Неожиданный ключ верхнего уровня или опечатка в названии раздела | Перенесите содержимое в один из семи разделов или в `Lexicon_Overview`, либо проверьте название раздела на опечатку |
| `12345 is not of type 'string'` / `... 'array'` / `... 'object'` | Лист дерева понятий содержит число, булево значение или `null` | Выразите значение текстом, например `"speaker_population": "60000"` (строка), а не голым числом |

## Непрерывная интеграция

При каждом push и pull request автоматически запускается `scripts/validate.py` по всем файлам в `files/` (см. `.github/workflows/validate.yml`). Файл, не соответствующий своей схеме, останавливает сборку — это проверяется автоматически, а не полагается на внимательность рецензента.
