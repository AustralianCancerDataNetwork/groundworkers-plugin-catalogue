# Groundworkers Plugin Catalogue

The Groundworkers Plugin Catalogue is the release and compatibility index for the Groundworkers ecosystem. It describes the Groundworkers host, installable runtime plugins, prompt-pack distributions, and site-owned filesystem packs.

The canonical source is [`catalogue/plugins.yaml`](catalogue/plugins.yaml). The validation tool generates filtered indexes under `dist/`, and the refresh workflow maintains the status table in this README. This repository must remain private while its canonical source contains private plugin metadata.

## Find a component

The table below is generated from the canonical catalogue. The status symbol is the latest recorded catalogue verification state. A GitHub Actions badge is included when the component declares a `compatibility.yml` workflow; badges are live and may change without this README being regenerated.

<!-- BEGIN GENERATED PLUGIN STATUS -->
| Component | Visibility | Kind | Target version | Groundworkers compatibility | CI status |
| --- | --- | --- | --- | --- | --- |
| Groundworkers | public | host | `0.5.0` | `host` | ⏳ unverified |
| OHDSI Prompt Registry | public | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified [![compatibility](https://github.com/AustralianCancerDataNetwork/ohdsi-prompt-registry/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/ohdsi-prompt-registry/actions) |
| OMOP Concept Grounding | public | prompt-pack | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified [![compatibility](https://github.com/AustralianCancerDataNetwork/omop-concept-grounding/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/omop-concept-grounding/actions) |
| Comparator Recommender | public | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified [![compatibility](https://github.com/AustralianCancerDataNetwork/comparator-recommender/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/comparator-recommender/actions) |
| CQI Workers | private | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified |
| PBS Mapper | private | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified |
| eviQ Mapper | private | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified |
| Groundcrew Prompt Packs | private | filesystem-pack | `Git revision` | `>=0.5,<0.6` | ⏳ unverified [![compatibility](https://github.com/AustralianCancerDataNetwork/groundcrew-prompts/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/groundcrew-prompts/actions) |
| OHDSI Onto-Bridge | private | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified [![compatibility](https://github.com/AustralianCancerDataNetwork/ohdsi-onto-bridge/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/ohdsi-onto-bridge/actions) |
| OHDSI UMLS Bridge | private | runtime-plugin | `0.1.0` | `>=0.5,<0.6` | ⏳ unverified |
<!-- END GENERATED PLUGIN STATUS -->

The catalogue uses these component kinds:

| Kind | Meaning | User action |
| --- | --- | --- |
| `host` | The Groundworkers MCP host itself. | Install and configure Groundworkers. |
| `runtime-plugin` | An installed Python package discovered through the `groundworkers.plugins` entry-point group. | Install the package into the Groundworkers environment and configure it if required. |
| `prompt-pack` | A versioned Python distribution that contributes workflows to the OHDSI Prompt Registry. | Install the distribution alongside the registry. |
| `filesystem-pack` | A directory of prompt-pack content loaded from a configured filesystem path. | Obtain repository access, configure the pack root, and restart Groundworkers. |

### Install a public component

Use the installation command shown in the component's catalogue record. For the planned public Python distributions, the normal form is:

```bash
uv add groundworkers==0.5.0
uv add ohdsi-prompt-registry==0.1.0
uv add omop-concept-grounding==0.1.0
uv add comparator-recommender==0.1.0
uv add pbs-mapper==0.1.0
uv add eviq-mapper==0.1.0
```

Install the host and any desired components into the same environment. After installation, configure the component according to its own README, start Groundworkers, and use `groundworkers --describe` to confirm that the package was discovered and whether it is active.

Private components are not part of the public installation path. Their catalogue records are visible only to people with access to this repository and the corresponding source repository.

### Understand compatibility status

The declared Groundworkers range describes what the component claims to support. The status symbol and workflow badge provide evidence about what has actually been tested. `unverified` means that no release-compatible result has been recorded; it does not mean that the component is known to be broken. Check the linked workflow for the exact component version, Groundworkers version, Python version, commit, and test result before adopting a planned or private component.

The catalogue describes what can be installed. Groundworkers entry-point discovery describes what is installed in one environment, and `groundworkers --describe` describes what is active and configured in that environment. The catalogue never downloads or executes a package automatically.

## Publish or maintain a component

Add one record to [`catalogue/plugins.yaml`](catalogue/plugins.yaml) for each published component. Keep the record focused on information a user or compatibility job needs:

- Use a stable, lower-case `id` that will not change when the display title changes.
- Set `visibility` to `public` only when the source and installation path can be disclosed to public users; use `private` for internal components.
- Classify the component as `runtime-plugin`, `prompt-pack`, or `filesystem-pack`. Use `host` only for Groundworkers itself.
- Record the source repository, distribution channel, released version, install command, capabilities, dependencies, and declared Groundworkers/Python ranges.
- Set `status: released` only when users can obtain the stated version. Keep future work as `planned`.
- Leave `verification.status` as `unverified` until the required compatibility matrix has passed.

Every released runtime plugin or prompt-pack distribution should provide a `compatibility.yml` workflow that accepts the `groundworkers-compatibility` repository-dispatch event. The workflow contract and release gates are documented in [`docs/compatibility.md`](docs/compatibility.md).

The catalogue's compatibility workflow dispatches requests to released components. The component repository owns the detailed test matrix and publishes the result through its normal GitHub Actions checks. First-party release automation should not publish a component until its required matrix is green.

For a public component, add the repository and package metadata to the canonical catalogue, add its compatibility workflow, enable its matrix, and regenerate the projections and README. For a private component, keep the source URL, installation details, and status in this private repository; the generated public index will exclude the record.

## Current release set

The initial records target Groundworkers `0.5.0` and Python `3.12`/`3.13`.

## Repository layout

```text
catalogue/
  plugins.yaml              # canonical records, including private records
  schema/plugin.schema.json # versioned record contract
docs/
  compatibility.md          # developer and CI contract
scripts/
  validate_catalogue.py     # validate and generate filtered indexes
dist/
  public-index.json         # generated public projection
  private-index.json        # generated internal projection
  compatibility-matrix.json # generated CI dispatch matrix
.github/workflows/
  validate.yml              # validate source and generated files
  refresh-readme.yml        # regenerate and commit README/index changes
  compatibility-dispatch.yml# request component compatibility runs
```

## Local development

```bash
uv sync --dev
uv run python scripts/validate_catalogue.py
uv run python scripts/validate_catalogue.py --write-readme
uv run python scripts/validate_catalogue.py --check-generated
uv run python scripts/validate_catalogue.py --check-readme
uv run python -m pytest -q -p no:cacheprovider
```

The generated files are deterministic. The validation workflow fails when a change leaves `README.md` or `dist/` out of date, while the refresh workflow can regenerate and commit those views on `main`.
