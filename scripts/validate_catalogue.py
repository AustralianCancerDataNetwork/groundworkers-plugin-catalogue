#!/usr/bin/env python3
"""Validate the canonical catalogue and generate deterministic projections."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalogue" / "plugins.yaml"
SCHEMA = ROOT / "catalogue" / "schema" / "plugin.schema.json"
DIST = ROOT / "dist"
README = ROOT / "README.md"
README_START = "<!-- BEGIN GENERATED PLUGIN STATUS -->"
README_END = "<!-- END GENERATED PLUGIN STATUS -->"

STATUS_SYMBOLS = {
    "verified": "✅",
    "failed": "❌",
    "stale": "⚠️",
    "unverified": "⏳",
    "unknown": "❔",
}


def load_source() -> dict[str, Any]:
    with SOURCE.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("catalogue/plugins.yaml must contain an object")
    return value


def validate(source: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(source), key=str)
    if errors:
        details = "\n".join(f"- {error.json_path}: {error.message}" for error in errors)
        raise ValueError(f"catalogue schema validation failed:\n{details}")

    plugins = source["plugins"]
    ids = [plugin["id"] for plugin in plugins]
    if len(ids) != len(set(ids)):
        raise ValueError("plugin ids must be unique")

    for plugin in plugins:
        private = plugin["visibility"] == "private"
        if private != (plugin["repository"]["access"] == "private"):
            raise ValueError(
                f"{plugin['id']}: visibility and repository access must agree"
            )

        if plugin["kind"] == "filesystem-pack" and plugin["distribution"] is not None:
            raise ValueError(f"{plugin['id']}: filesystem packs must not have a distribution")
        if plugin["kind"] != "filesystem-pack" and plugin["distribution"] is None:
            raise ValueError(f"{plugin['id']}: non-filesystem components need a distribution")
        if plugin["status"] != "released" and plugin["verification"]["status"] == "verified":
            raise ValueError(f"{plugin['id']}: an unreleased component cannot be verified")
        if plugin["compatibility"]["matrix_enabled"] and plugin["status"] != "released":
            raise ValueError(f"{plugin['id']}: matrix testing requires a released component")


def projection(source: dict[str, Any], visibility: str) -> dict[str, Any]:
    return {
        "schema_version": source["schema_version"],
        "catalogue": source["catalogue"],
        "plugins": [
            p for p in source["plugins"] if visibility == "all" or p["visibility"] == visibility
        ],
    }


def compatibility_matrix(source: dict[str, Any]) -> dict[str, Any]:
    include = []
    for plugin in source["plugins"]:
        compatibility = plugin["compatibility"]
        if not compatibility["matrix_enabled"]:
            continue
        include.append(
            {
                "id": plugin["id"],
                "repository": plugin["repository"]["slug"],
                "kind": plugin["kind"],
                "test_profile": compatibility["test_profile"],
                "groundworkers": compatibility["groundworkers"],
                "python": compatibility["python"],
                "python_versions": source["catalogue"]["target_python"],
            }
        )
    return {
        "schema_version": source["schema_version"],
        "groundworkers": source["catalogue"]["target_groundworkers"],
        "python": source["catalogue"]["target_python"],
        "include": include,
    }


def readme_status(plugin: dict[str, Any]) -> str:
    verification = plugin["verification"]
    symbol = STATUS_SYMBOLS[verification["status"]]
    status = f"{symbol} {verification['status']}"

    workflow_file = verification["workflow_file"]
    workflow = verification["workflow"]
    if workflow_file and workflow:
        slug = plugin["repository"]["slug"]
        badge = (
            f"https://github.com/{slug}/actions/workflows/"
            f"{workflow_file}/badge.svg?branch=main"
        )
        badge_link = f"[![compatibility]({badge})]({workflow})"
        status = f"{status} {badge_link}"
    elif workflow:
        status = f"[{status}]({workflow})"
    return status


def render_status_table(source: dict[str, Any]) -> str:
    rows = [
        "| Component | Visibility | Kind | Target version | Groundworkers compatibility | CI status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for plugin in source["plugins"]:
        distribution = plugin["distribution"]
        version = distribution["version"] if distribution else "Git revision"
        compatibility = plugin["compatibility"]["groundworkers"] or "host"
        rows.append(
            f"| {plugin['title']} | {plugin['visibility']} | {plugin['kind']} | "
            f"`{version}` | `{compatibility}` | {readme_status(plugin)} |"
        )
    return "\n".join(rows)


def rendered_readme(source: dict[str, Any]) -> str:
    original = README.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"{re.escape(README_START)}.*?{re.escape(README_END)}",
        flags=re.DOTALL,
    )
    replacement = f"{README_START}\n{render_status_table(source)}\n{README_END}"
    rendered, count = pattern.subn(replacement, original, count=1)
    if count != 1:
        raise ValueError("README must contain exactly one generated status marker pair")
    return rendered


def write_readme(source: dict[str, Any]) -> None:
    README.write_text(rendered_readme(source), encoding="utf-8")


def check_readme(source: dict[str, Any]) -> None:
    expected = rendered_readme(source)
    actual = README.read_text(encoding="utf-8")
    if actual != expected:
        raise ValueError("README generated status table is out of date; run with --write-readme")


def encoded(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def write_outputs(source: dict[str, Any]) -> None:
    DIST.mkdir(exist_ok=True)
    outputs = {
        "public-index.json": projection(source, "public"),
        "private-index.json": projection(source, "all"),
        "compatibility-matrix.json": compatibility_matrix(source),
    }
    for name, value in outputs.items():
        (DIST / name).write_text(encoded(value), encoding="utf-8")


def check_outputs(source: dict[str, Any]) -> None:
    expected = {
        "public-index.json": projection(source, "public"),
        "private-index.json": projection(source, "all"),
        "compatibility-matrix.json": compatibility_matrix(source),
    }
    errors = []
    for name, value in expected.items():
        path = DIST / name
        if not path.exists():
            errors.append(f"missing generated file: {path.relative_to(ROOT)}")
            continue
        if path.read_text(encoding="utf-8") != encoded(value):
            errors.append(f"out-of-date generated file: {path.relative_to(ROOT)}")
    if errors:
        raise ValueError("\n".join(errors) + "\nRun scripts/validate_catalogue.py to regenerate them.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-generated", action="store_true")
    parser.add_argument("--check-readme", action="store_true")
    parser.add_argument("--write-readme", action="store_true")
    parser.add_argument(
        "--matrix",
        action="store_true",
        help="print the GitHub Actions matrix JSON after validation",
    )
    args = parser.parse_args()
    try:
        source = load_source()
        validate(source)
        if args.check_generated:
            check_outputs(source)
        if args.check_readme:
            check_readme(source)
        if args.write_readme:
            write_readme(source)
        if not args.check_generated and not args.check_readme and not args.write_readme and not args.matrix:
            write_outputs(source)
        if args.matrix:
            print(json.dumps(compatibility_matrix(source)["include"], separators=(",", ":")))
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
