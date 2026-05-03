# Action Plan

This file is only for the initial execution plan. The actual backlog must be managed in GitHub Projects using issues, labels, cycles, modules, and Kanban cards.

## Initial Setup Tasks

1. Create the repository folder structure defined in `resumo_executivo.md`.
2. Create `requirements.txt` for the Streamlit Cloud deployment workflow.
3. Create the initial pt-BR `README.md` with setup, local run, CSV schema, and deployment notes.
4. Create the first Streamlit app shell with CSV upload, provider selection, and API key input behavior.
5. Create the CSV schema and validation modules.
6. Create the analysis pipeline interfaces without mock fallback data.
7. Create the first dashboard metrics and filtered CSV export flow.
8. Create the GitHub Actions CI workflow.
9. Configure the GitHub Project board.

## GitHub Project Structure

Create a GitHub Project in Kanban style with these columns:

- Backlog
- Ready
- In Progress
- Review
- Done

Create cycles or milestones:

- Cycle 1: Project foundation and CSV validation
- Cycle 2: Analysis pipeline and provider configuration
- Cycle 3: Streamlit dashboard and exports
- Cycle 4: Tests, CI/CD, documentation, and Streamlit Cloud deployment

Create modules:

- Data ingestion
- Schema validation
- Provider configuration
- LLM provider clients
- Analysis pipeline
- Metrics and dashboard
- CSV export
- Tests
- CI/CD
- Documentation
- Deployment

Create labels:

- `priority: high`
- `priority: medium`
- `priority: low`
- `type: feature`
- `type: bug`
- `type: test`
- `type: documentation`
- `type: ci-cd`
- `module: ingestion`
- `module: validation`
- `module: providers`
- `module: pipeline`
- `module: dashboard`
- `module: export`
- `module: tests`
- `module: deployment`

## First GitHub Project Cards

Create issues/cards for:

1. Bootstrap repository structure.
2. Add pt-BR README with local and Streamlit Cloud instructions.
3. Define CSV schema validation.
4. Implement open and closed ticket date handling.
5. Add provider selector and API key resolution.
6. Implement analysis output schema.
7. Build first dashboard KPIs.
8. Add dashboard filters.
9. Add full and filtered CSV export.
10. Add CI workflow with lint, format, and tests.
