#!/usr/bin/env python3
# Validate basic structure and uniqueness of canonical dictionary entries.

from pathlib import Path
import sys
import yaml

REQUIRED = {"id", "name", "version", "protobuf_type", "definition", "owner", "status"}

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    dictionary_dir = repo_root / "dictionary"
    files = sorted(dictionary_dir.glob("*.yaml"))
    if not files:
        print("ERROR: no dictionary YAML files found", file=sys.stderr)
        return 1

    seen = {}
    errors = []

    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            errors.append(f"{path.relative_to(repo_root)}: YAML parse error: {exc}")
            continue

        concepts = data.get("concepts", [])
        if not isinstance(concepts, list):
            errors.append(f"{path.relative_to(repo_root)}: 'concepts' must be a list")
            continue

        for index, concept in enumerate(concepts, start=1):
            if not isinstance(concept, dict):
                errors.append(f"{path.name}: concept #{index} must be a mapping")
                continue
            missing = REQUIRED - set(concept)
            if missing:
                errors.append(
                    f"{path.name}: concept #{index} missing fields: {', '.join(sorted(missing))}"
                )
            concept_id = concept.get("id")
            if not isinstance(concept_id, str) or not concept_id.strip():
                errors.append(f"{path.name}: concept #{index} has invalid or missing id")
                continue
            if concept_id in seen:
                errors.append(
                    f"duplicate canonical ID {concept_id!r}: "
                    f"{seen[concept_id]} and {path.name}#{index}"
                )
            else:
                seen[concept_id] = f"{path.name}#{index}"

            if concept.get("protobuf_type") == "TYPE_MESSAGE" and not concept.get("protobuf_message_type"):
                errors.append(
                    f"{path.name}: {concept_id} uses TYPE_MESSAGE but lacks protobuf_message_type"
                )

    if errors:
        print("Canonical dictionary validation FAILED:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Canonical dictionary validation passed ({len(seen)} concepts).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
