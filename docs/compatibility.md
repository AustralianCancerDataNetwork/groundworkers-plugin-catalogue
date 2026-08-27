# Compatibility CI contract

This document explains how component developers publish compatibility evidence and how component users should interpret it. The catalogue records declared support and recent verification, but the component repositories own the tests and the Groundworkers repository owns the reverse-install checks.

## What users should look for

The `compatibility` section in a catalogue record is a declaration of intended support. The `verification` section is evidence produced by CI. A component is ready for normal use when its stated release is available, its required matrix has passed, and its verification is recent enough for the project's policy.

The status values have these meanings:

| Status | Meaning |
| --- | --- |
| `unverified` | No release-compatible result has been recorded. |
| `verified` | The declared required matrix passed recently. |
| `stale` | A previous success exists, but it is older than the policy window. |
| `failed` | The most recent required compatibility run failed. |
| `unknown` | CI could not determine a reliable result. |

The README status symbol is generated from `verification.status`. A GitHub Actions badge is generated when `verification.workflow_file` is set; it is a live view of the named workflow in the component repository. The badge and the catalogue symbol may differ briefly, so users should follow the workflow link for the detailed result.

## Component workflow

Every released runtime plugin and prompt-pack distribution should expose a workflow named `compatibility.yml`. It must accept a `repository_dispatch` event with type `groundworkers-compatibility`.

The catalogue sends a payload like this:

```json
{
  "groundworkers_version": "0.5.0",
  "python_versions": ["3.12", "3.13"],
  "catalogue_id": "comparator-recommender",
  "test_profile": "runtime-discovery",
  "requested_by": "groundworkers-plugin-catalogue"
}
```

The component workflow should test the released package or release candidate, not an editable checkout, against the requested Groundworkers version. It should verify package installation and dependency resolution, entry-point discovery, configuration discovery when applicable, MCP registration, one representative capability operation, and the component's normal unit and static checks.

Prompt-pack workflows should additionally install the relevant registry version, discover the declared pack, validate its manifest and schemas, and exercise the published prompt or resource surface. Filesystem-pack workflows should check out the pack source and validate that it loads through the installed prompt registry.

The workflow should publish a result containing the component version, Groundworkers version, Python version, tested commit SHA, overall status, and workflow URL. A result should be considered a pass only when the complete required matrix passes.

## Matrix policy

The component repository owns its detailed matrix. The catalogue owns the list of curated components and dispatches reverse compatibility requests when Groundworkers releases.

| Event | Matrix | Release impact |
| --- | --- | --- |
| Component pull request | Minimum supported Groundworkers, latest stable, and Groundworkers main. | Required for first-party components. |
| Component release | Every supported Groundworkers and Python combination. | Must pass before publication. |
| Groundworkers release | Reverse-install every released curated component. | Required for first-party components. |
| Nightly | Groundworkers main and upcoming Python versions. | Report failures; normally do not block a released package. |

Do not run the full Cartesian matrix on every pull request unless the component is small enough to make that practical. A minimum/latest/main smoke matrix on pull requests and the complete matrix on release candidates gives fast feedback without weakening the release gate.

The initial catalogue targets Groundworkers `0.5.0` and Python `3.12`/`3.13`. The listed records keep `matrix_enabled: false` because these are planned releases. Set it to `true` only after the package is published and its component workflow is ready to receive dispatch events.

## Reverse validation

Groundworkers release CI should install each released catalogue component into a clean environment and verify that the host can discover and register it. Runtime-plugin checks should cover the `groundworkers.plugins` entry point, configuration entry points when present, plugin build behavior, and MCP tool registration. Prompt-pack checks should cover the registry entry point, pack discovery, manifest loading, and schema/resource publication.

Private components may use an internal token and private package source for reverse validation. They should remain visible in the internal catalogue and should be advisory for a public Groundworkers release unless the release explicitly depends on them.

## README and generated views

The catalogue README contains a generated table between the `BEGIN GENERATED PLUGIN STATUS` and `END GENERATED PLUGIN STATUS` markers. The refresh workflow rewrites that table and the generated indexes whenever the canonical catalogue changes.

For a component with `verification.workflow_file`, the table includes a live badge at `https://github.com/{repository}/actions/workflows/{workflow_file}/badge.svg?branch=main`. The standard workflow filename is `compatibility.yml`. Components without a reachable workflow still receive a generated status symbol from `verification.status`.

The badge is live, but the symbol is a catalogue assertion. A compatibility workflow should update `verification.status` through the agreed result-publication path only after the complete required matrix has passed. This prevents stale green evidence from being mistaken for current cross-version support.

## Release checklist

Before marking a component `released`:

1. Publish the package or make the private Git revision available.
2. Confirm that the package depends on a released Groundworkers version rather than a development branch.
3. Run the complete component compatibility matrix.
4. Run the reverse-install check from Groundworkers CI.
5. Record the result details and workflow URL in the catalogue verification data.
6. Set `status: released`, enable the matrix, regenerate `dist/`, and refresh the README.

