# CloudMesh Sentinel

**AI-assisted multi-cloud network observability and security.**

CloudMesh Sentinel is an open-source platform for discovering, monitoring and assessing network infrastructure across cloud environments. Initial API is intentionally small and testable.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
ruff check .
pytest -q
uvicorn cloudmesh_sentinel.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` or `/health`.

## Autonomous development

The scheduled workflow is **disabled by default** and currently **dry-run only**. It does not generate or push code. See [agent policy](docs/AGENT_POLICY.md) and [roadmap](docs/ROADMAP.md). AI contributions will be disclosed, tested and reviewed according to risk.

## Scope
AWS discovery first; Azure, Kubernetes and observability follow in later phases.

## License
No license has been selected yet; choose one before accepting external contributions.
