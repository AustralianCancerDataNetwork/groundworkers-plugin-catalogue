# Groundworkers Plugin Catalogue

The Groundworkers Plugin Catalogue is the release and compatibility index for the Groundworkers ecosystem. It describes the Groundworkers host, installable runtime plugins, prompt-pack distributions, and site-owned filesystem packs.

The catalogue is public by design. It lists public and private components so readers can see what exists; private records contain non-sensitive summaries and compatibility metadata. Access to a private component and its release is by request.

The canonical source is [`catalogue/plugins.yaml`](catalogue/plugins.yaml). The validator generates the indexes under `dist/`, and the refresh workflow maintains the status table below. `dist/public-index.json` contains public records only. `dist/private-index.json` contains every record, including private components, and is intentionally public; it is not an access-controlled index.

## Find a component

The table below is generated from the canonical catalogue. A GitHub Actions badge appears when a component declares a `compatibility.yml` workflow; badges are live and may change without this README being regenerated. A dash means no workflow is declared, not that compatibility has passed.

<!-- BEGIN GENERATED PLUGIN STATUS -->
| Component | Visibility | Kind | Target version | Groundworkers compatibility | CI status |
| --- | --- | --- | --- | --- | --- |
| Groundworkers | public | host | `0.10.0` | `host` | — |
| Groundskeeping | public | host | `0.9.1` | `host` | — |
| Groundstore | public | host | `0.5.0` | `host` | — |
| OHDSI Prompt Registry | public | runtime-plugin | `0.5.0` | `>=0.7.1,<1.0` | [![compatibility](https://github.com/AustralianCancerDataNetwork/ohdsi-prompt-registry/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/ohdsi-prompt-registry/actions) |
| Circe Cohort Definition Check | private | runtime-plugin | `0.1.0` | `>=0.7,<1` | — |
| OMOP Concept Grounding | public | prompt-pack | `0.3.1` | `>=0.7.1,<1.0` | [![compatibility](https://github.com/AustralianCancerDataNetwork/omop-concept-grounding/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/omop-concept-grounding/actions) |
| Cohort Shape Guide | private | prompt-pack | `0.1.0` | `>=0.7,<1` | — |
| Groundworkers Imaging Extension | private | runtime-plugin | `0.1.0` | `>=0.7.1,<1.0` | — |
| Knowledge Base Prompt Packs | private | filesystem-pack | `Git revision` | `>=0.7.1,<1.0` | — |
| Comparator Recommender | public | runtime-plugin | `0.1.1` | `>=0.7.1,<1.0` | [![compatibility](https://github.com/AustralianCancerDataNetwork/comparator-recommender/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/comparator-recommender/actions) |
| CQI Workers | private | runtime-plugin | `0.1.0` | `>=0.7.1,<1.0` | [![compatibility](https://github.com/AustralianCancerDataNetwork/cqi-workers/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/cqi-workers/actions) |
| PBS Mapper | private | runtime-plugin | `0.1.0` | `>=0.7.1,<1.0` | [![compatibility](https://github.com/AustralianCancerDataNetwork/pbs-mapper/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/pbs-mapper/actions) |
| eviQ Mapper | private | runtime-plugin | `0.1.0` | `>=0.7.1,<1.0` | — |
| OHDSI Onto-Bridge | private | runtime-plugin | `0.2.1` | `>=0.7.1,<1.0` | — |
| OHDSI UMLS Bridge | private | runtime-plugin | `0.1.0` | `>=0.7.1,<1.0` | [![compatibility](https://github.com/AustralianCancerDataNetwork/ohdsi-umls-bridge/actions/workflows/compatibility.yml/badge.svg?branch=main)](https://github.com/AustralianCancerDataNetwork/ohdsi-umls-bridge/actions) |
<!-- END GENERATED PLUGIN STATUS -->

The catalogue uses these component kinds:

| Kind | Meaning | User action |
| --- | --- | --- |
| `host` | The Groundworkers MCP host itself. | Install and configure Groundworkers. |
| `runtime-plugin` | An installed Python package discovered through the `groundworkers.plugins` entry-point group. | Install the package into the Groundworkers environment and configure it if required. |
| `prompt-pack` | A versioned Python distribution that contributes workflows to the OHDSI Prompt Registry. | Install the distribution alongside the registry. |
| `filesystem-pack` | A directory of prompt-pack content loaded from a configured filesystem path. | Obtain repository access, configure the pack root, and restart Groundworkers. |

### Install a public component

Use the installation command shown in the component's catalogue record. Public components install from PyPI:

```bash
uv add groundworkers==0.10.0
uv add ohdsi-prompt-registry==0.5.0
```

### Get access to a private component

Private components are not on the public installation path. Their catalogue records use `Access on request` instead of a private SSH install command. Contact the maintainers to request repository and release access.

Install the host and any desired components into the same environment. Catalogue dependencies include workflow prerequisites as well as Python packages; each component's package metadata defines its Python dependencies. After installation, configure the component according to its own README, start Groundworkers, and use `groundworkers --describe` to confirm that the package was discovered and whether it is active.

### Understand compatibility status

The declared Groundworkers range describes intended support. A live workflow badge links to current test evidence; the catalogue does not cache a pass/fail result. Check the workflow for the exact component version, Groundworkers version, Python version, commit, and test result before adopting a component.

The catalogue describes what can be installed. Groundworkers entry-point discovery describes what is installed in one environment, and `groundworkers --describe` describes what is active and configured in that environment. The catalogue never downloads or executes a package automatically.

## Publish or maintain a component

Add one record to [`catalogue/plugins.yaml`](catalogue/plugins.yaml) for each published component. Keep the record focused on information a user or compatibility job needs:

- Use a stable, lower-case `id` that will not change when the display title changes.
- Set `visibility` to match the source repository. Private entries are public catalogue metadata, so keep their summaries and capabilities informative without including sensitive details.
- Classify the component as `runtime-plugin`, `prompt-pack`, or `filesystem-pack`. Use `host` only for Groundworkers itself.
- Record the source repository, distribution channel, released version, install command, capabilities, dependencies, and declared Groundworkers/Python ranges.
- Use `distribution.channel: pypi` for public components and `git` for private distributions. Private `install` fields say `Access on request`; the catalogue does not publish private SSH commands.
- Set `status: released` only when the stated version is available on PyPI or through a GitHub Release on that tag. Keep unreleased work as `planned`.
- Mark compatibility as passed only after the required workflow matrix has passed.

Every released runtime plugin or prompt-pack distribution should provide a `compatibility.yml` workflow that accepts the `groundworkers-compatibility` repository-dispatch event. The workflow contract and release gates are documented in [`docs/compatibility.md`](docs/compatibility.md).

The catalogue's compatibility workflow dispatches requests to released components. The component repository owns the detailed test matrix and publishes the result through its normal GitHub Actions checks. First-party release automation should not publish a component until its required matrix is green.

For a public component, add the repository and package metadata to the canonical catalogue, add its compatibility workflow, enable its matrix, and regenerate the projections and README. For a private component, use an access-on-request install field and remove sensitive details from its public metadata.

The [public Groundworkers plugin template](https://github.com/AustralianCancerDataNetwork/gw-plugin-template) is a starting point for new runtime plugins, rather than a component to install, so it is linked here instead of listed in the catalogue. The private [gw-prompt-builder](https://github.com/AustralianCancerDataNetwork/gw-prompt-builder) is a Claude Code skill authoring toolkit; it does not run as a Groundworkers or Prompt Registry component and is out of scope for this catalogue.

## Current release set

The records target Groundworkers `0.10.0` and Python `3.12`/`3.13`. `planned` means the listed version is not yet available as a PyPI release or a published GitHub Release. A declared range is not compatibility evidence; follow a live workflow badge for test results.

### Planned cohort workflow components

`circe-cohort-check` is a private runtime plugin for Circe definition checks, rendering, SQL text generation, and structural shape classification. `cohort-shape-guide` provides guidance for cohort shape and logic decisions through the OHDSI Prompt Registry. It combines Groundworkers concept grounding with structural checks on a draft Circe definition.

The guide requires registry **0.5.0 or newer**, the OMOP Concept Grounding pack, and the `circe_cohort_check_validate`, `circe_cohort_check_render`, and `circe_cohort_check_shape` tools. The concept-grounding pack and Circe Cohort Definition Check are workflow prerequisites rather than Python dependencies of the guide. Applications such as Study Agent can incorporate the guide while retaining their own review sessions, approval process, artifact generation, and execution.

Both entries target an initial `0.1.0` release. Their private source repositories are `AustralianCancerDataNetwork/circe-cohort-check` and `AustralianCancerDataNetwork/cohort-shape-guide`; access is by request. Compatibility dispatch remains disabled for both until their repositories provide the required workflow.

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
  private-index.json        # generated all-record projection, intentionally public
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
