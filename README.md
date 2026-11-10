# Carbon-aware workload orchestrator

A local FastAPI simulation that chooses the region with the lowest sampled
carbon intensity. Three regions receive illustrative random values at startup.
Submitted work is simulated with a short asynchronous delay. Job status now
tracks the background task, including the period before its queue starts.

## Run the example

```bash
python -m pip install -r requirements.txt
python -m uvicorn orchestrator:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
curl -X POST http://127.0.0.1:8000/jobs -H "Content-Type: application/json" -d '{"job_id":"demo-1","payload":"synthetic workload"}'
curl http://127.0.0.1:8000/jobs/demo-1
```

Submission returns the selected region. Status progresses from `queued` to
`completed`, with `failed` for a cancelled or failed task. A duplicate ID
returns HTTP 400. Jobs and task records remain in memory for the process
lifetime. Real emissions feeds, capacity limits, and cluster execution would
be additional integrations.

## Verify

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
