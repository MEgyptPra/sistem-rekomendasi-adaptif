# Backend: model loading and collab-loader

This document explains how to safely load large model artifacts (especially the ~6GB collaborative model) and how to run the `collab-loader` worker.

Recommendations

- Do NOT load the collaborative model on normal backend startup — it may OOM the container.
- Use the `collab-loader` service or run the loader in a separate container with an explicit memory cap.
- Protect model-loading endpoints with an admin token.

Set ADMIN token (example)

- Create an `.env` file at repository root with:

```env
ADMIN_LOAD_TOKEN=replace-with-strong-secret
```

or export it in your shell before running `docker-compose`.

Update and rebuild image

```powershell
# from repo root
docker-compose -f pariwisata-recommender\docker-compose.yml build backend
```

Run the loader in an isolated container with a memory cap (recommended)

```powershell
# Build image (if not built already)
docker build -t pariwisata-backend ./pariwisata-recommender/backend

# Run the loader with 12GB memory limit (adjust to your host)
docker run --rm --name collab-loader --memory=12g `
  -v ${PWD}/pariwisata-recommender/backend/data/models:/app/data/models `
  -e ADMIN_LOAD_TOKEN='your-secret-token' `
  pariwisata-backend python /app/scripts/load_collab_worker.py /app/data/models/collaborative_model.pkl
```

Or use `docker-compose run` (no memory cap via compose):

```powershell
docker-compose -f pariwisata-recommender\docker-compose.yml run --rm collab-loader
```

Using the protected HTTP endpoints

- Load `content_based` or `hybrid` via:

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/ml/load?model=content_based' -Headers @{ 'X-ADMIN-TOKEN' = 'your-secret-token' }
```

- Trigger the worker endpoint (this will spawn a process inside the backend container):

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/ml/load/collaborative-worker' -Headers @{ 'X-ADMIN-TOKEN' = 'your-secret-token' }
```

Notes

- The loader script attempts to use `joblib` with `mmap_mode='r'` to reduce peak memory. The worker will check available memory with `psutil` (if installed).
- For production, prefer running the loader in a separate container with an explicit `--memory` cap or on a host with more RAM.
- The backend image installs dependencies from `requirements.txt` — `joblib` and `psutil` were added there.
