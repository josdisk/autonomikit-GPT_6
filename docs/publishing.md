# Publishing

## Publish the Python package to TestPyPI / PyPI

We ship a workflow that builds and publishes the package:

1. Push your code to `main`.
2. Go to **Actions → Publish to (Test)PyPI**.
3. Choose `testpypi` or `pypi` and **Run workflow**.

The action uses **trusted publishing** (OIDC). For PyPI:
- Create the project on PyPI (`autonomi-kit`).
- Enable trusted publishing and grant your repo permission.
- Alternatively, add a **PYPI_API_TOKEN** repository secret and the action will still work.

## Draft a GitHub Release

1. Tag your repo (example):  
   ```bash
   git tag -a v0.1.0 -m "first release"
   git push origin v0.1.0
   ```
2. Run **Actions → Draft GitHub Release**, provide the tag (e.g., `v0.1.0`).  
   The release body will use `.github/RELEASE_NOTES.md`.

## GHCR Images

Upon pushing a tag like `v0.1.0`, the `Release (GHCR)` workflow builds and pushes:
- `ghcr.io/josdisk/autonomikit-api:<tags>`
- `ghcr.io/josdisk/autonomikit-web:<tags>`
