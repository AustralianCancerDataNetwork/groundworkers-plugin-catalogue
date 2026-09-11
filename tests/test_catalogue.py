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


def test_initial_compatibility_matrix_is_not_enabled_before_release() -> None:
    source = load_source()

    assert compatibility_matrix(source)["include"] == []


def test_readme_contains_the_generated_status_table() -> None:
    source = load_source()
    readme = rendered_readme(source)

    assert "| Component | Visibility | Kind | Target version |" in readme
    assert "Groundcrew Prompt Packs" in readme
    assert "actions/workflows/compatibility.yml/badge.svg" in readme
