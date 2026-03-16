# Carbon‑Aware Workload Orchestrator

This repository demonstrates an orchestrator that dispatches compute
jobs to different regions or data centers based on real‑time carbon
intensity data.  The orchestrator queries an emissions API, compares
available regions, and selects the location with the lowest carbon
intensity at the time of job submission.

## Features

- Periodically fetches carbon intensity data from a public API.
- Maintains a registry of compute regions with their queue and
  capacity status.
- Routes incoming jobs to the region with the minimum carbon
  intensity while respecting capacity constraints.
- Provides a RESTful API for job submission and status checking.

## Usage

Install dependencies and run the orchestrator:

```bash
pip install -r requirements.txt
python orchestrator.py
```

Submit a job:

```bash
curl -X POST http://localhost:8000/jobs -H 'Content-Type: application/json' \
     -d '{"job_id": "abc123", "payload": "Hello, world!"}'
```

Check job status:

```bash
curl http://localhost:8000/jobs/abc123
```

## Extending

Integrate with real emissions data providers and real compute clusters.
Add authentication, persistent storage, and retry logic for a more
robust system.