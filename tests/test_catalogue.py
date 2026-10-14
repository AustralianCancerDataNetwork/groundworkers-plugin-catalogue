from __future__ import annotations

import json

from scripts.validate_catalogue import (
    DIST,
    compatibility_matrix,
    load_source,
    projection,
    rendered_readme,
    validate,
)


def test_canonical_catalogue_validates() -> None:
    source = load_source()
    validate(source)


def test_generated_public_projection_matches_source() -> None:
    source = load_source()
    generated = json.loads((DIST / "public-index.json").read_text(encoding="utf-8"))

    assert generated == projection(source, "public")


def test_compatibility_matrix_only_includes_enabled_components_with_workflows() -> None:
    source = load_source()
    include = compatibility_matrix(source)["include"]

    assert include
    by_id = {plugin["id"]: plugin for plugin in source["plugins"]}
    for entry in include:
        compatibility = by_id[entry["id"]]["compatibility"]
        assert compatibility["matrix_enabled"]
        assert compatibility["workflow_file"]


def test_readme_contains_the_generated_status_table() -> None:
    source = load_source()
    readme = rendered_readme(source)

    assert "| Component | Visibility | Kind | Target version |" in readme
    assert "Groundcrew Prompt Packs" in readme
    assert "actions/workflows/compatibility.yml/badge.svg" in readme
