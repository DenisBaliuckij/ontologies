# -*- coding: utf-8 -*-
"""Validates every ontology document under files/ against its schema.

Schema choice is automatic: a document is treated as a language-specific
instance (language-ontology.schema.json) if its meta block has an
"iso_code" field or it has a top-level "Lexicon_Overview" section;
otherwise it is validated as a general ontology (base-ontology.schema.json).

Usage: python scripts/validate.py
Exit code is non-zero if any document fails validation.
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
FILES_DIR = ROOT / "files"

BASE_SCHEMA = "base-ontology.schema.json"
LANGUAGE_SCHEMA = "language-ontology.schema.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_registry(schemas: dict[str, dict]) -> Registry:
    resources = [
        (schema["$id"], Resource.from_contents(schema))
        for schema in schemas.values()
    ]
    return Registry().with_resources(resources)


def choose_schema_name(instance: dict) -> str:
    meta = instance.get("meta", {})
    if "iso_code" in meta or "Lexicon_Overview" in instance:
        return LANGUAGE_SCHEMA
    return BASE_SCHEMA


def main() -> int:
    schemas = {
        path.name: load_json(path) for path in sorted(SCHEMAS_DIR.glob("*.schema.json"))
    }
    if not schemas:
        print(f"No schemas found under {SCHEMAS_DIR}")
        return 1

    registry = build_registry(schemas)

    instance_paths = sorted(FILES_DIR.glob("*.json"))
    if not instance_paths:
        print(f"No ontology files found under {FILES_DIR}")
        return 1

    exit_code = 0
    for instance_path in instance_paths:
        instance = load_json(instance_path)
        schema_name = choose_schema_name(instance)
        schema = schemas[schema_name]
        validator = Draft202012Validator(schema, registry=registry)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))

        if errors:
            exit_code = 1
            print(f"FAIL {instance_path.name}  (against {schema_name})  {len(errors)} error(s)")
            for error in errors[:20]:
                location = "/".join(str(part) for part in error.path) or "<root>"
                print(f"  - {location}: {error.message}")
            if len(errors) > 20:
                print(f"  ... and {len(errors) - 20} more")
        else:
            print(f"OK   {instance_path.name}  (against {schema_name})")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
