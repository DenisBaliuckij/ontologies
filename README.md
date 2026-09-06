# ontologies

Language ontologies following the [GOLD](http://purl.org/linguistics/gold/) (General Ontology for Linguistic Description) structure, plus a common JSON Schema contract for them.

## Layout

```
ontologies/
├── files/                             # the ontology documents
│   ├── OntoLing.json                  # general/theoretical linguistics ontology (the base)
│   └── OntoKon.json                   # a language-specific instance (Konabère, ISO 639-3: bbo)
├── schemas/
│   ├── base-ontology.schema.json      # shared envelope + recursive concept-node shape
│   └── language-ontology.schema.json  # extends the base for a single-language instance
└── scripts/
    └── validate.py                    # validates every file in files/ against its schema
```

## The two documents

- **`OntoLing.json`** is the general, theoretical linguistics ontology: definitions and structure for phonetics/phonology, morphology, syntax, semantics, their interfaces, and the GOLD relations/properties vocabulary. It carries no language-specific data.
- **`OntoKon.json`** is a single-language instance built on that same structure, populated with data for one language (Konabère). Every future language ontology added to `files/` is expected to follow this same shape.

## Schema design

The ontology content itself is a recursive **concept tree** — a node's value can be free text, a list, or another nested node — and the specific concept names inside each module (`Core_Foundations`, `Morphology`, `Syntax`, ...) legitimately vary and grow per language and per revision of linguistic theory. Pinning down that vocabulary in a schema would be both huge and constantly out of date.

So the schema is strict where the structure is genuinely fixed, and permissive where it's genuinely open-ended:

- **`base-ontology.schema.json`** requires the document envelope: a `meta` block with `title`/`version`/`description`/`sources`/`gold_base_uri`, and the seven core GOLD module sections (`Core_Foundations`, `Phonetics_and_Phonology`, `Morphology`, `Syntax`, `Semantics`, `Interfaces_and_Integration`, `Relations_and_Properties`). Inside each module, content must follow the recursive `OntologyNode`/`OntologyValue` shape (string, array of strings/records, or nested node) — this catches real mistakes (wrong types, empty objects) without constraining *which* concepts appear.
- **`language-ontology.schema.json`** extends the base (via `allOf` + `$ref`) for a single-language instance: it requires the extra `meta` fields that identify the language (`language_name`, `iso_code` — validated as an ISO 639-3 code, `classification`, `location`) and a top-level `Lexicon_Overview` section, and closes the document (`unevaluatedProperties: false`) so a language file can only contain `meta`, the seven base sections, and `Lexicon_Overview`.

## Validating

```bash
pip install -r requirements.txt
python scripts/validate.py
```

`validate.py` picks the schema automatically per file: a document is validated as a language instance if its `meta.iso_code` or a top-level `Lexicon_Overview` is present, otherwise as the general/base ontology. Adding a new language ontology to `files/` (e.g. `OntoXyz.json`) picks up validation automatically — no script changes needed.
