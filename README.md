# Streamlit Dashboard Template

A reusable Streamlit dashboard template with a fake-data generator, reusable components, example plots, and tests. Use this repo as a starting point for demos, prototypes, or internal dashboards.

Features
- Generate reproducible fake datasets (names, timestamps, categories, numeric metrics).
- Sidebar controls: date range, category multi-select, numeric sliders, text search.
- Interactive charts (Plotly and Altair examples).
- Data table with optional AgGrid integration (if `st-aggrid` is installed).
- CSV download of the currently filtered dataset.
- Cached data loading for fast UI interactions.
- Unit tests (pytest) for data generation and helper functions.

Quickstart (PowerShell)

1. Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run tests:

```powershell
pytest -q
```

3. Run the app locally:

```powershell
streamlit run app.py
```

If PowerShell blocks activation due to execution policy, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\.venv\Scripts\Activate.ps1
```

Files of interest
- `app.py` — example Streamlit app demonstrating layout, filters, charts, and downloads
- `data/fake_data.py` — fake data generator (reproducible via seed)
- `components/ui.py` — reusable UI helpers, CSV export, filtering and optional AgGrid display
- `components/plots.py` — helper functions for Plotly and Altair charts
- `tests/` — pytest tests for generator and helpers

Notes & next steps
- `st-aggrid` is optional; the app uses it if available. To enable advanced grid features, install `st-aggrid` (uncomment in `requirements.txt` and re-run `pip install -r requirements.txt`).
- For production authentication, consider an SSO solution or `streamlit-authenticator` (do not store secrets in repo).
- To deploy: Streamlit Cloud, a Docker container, or other hosting; see `readme_deployment.md` for notes.

License
- This template contains example/demo code; adapt as needed for your use case.
