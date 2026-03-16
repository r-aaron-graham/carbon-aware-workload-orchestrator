"""Carbon‑aware workload orchestrator.

This script implements a minimal server that assigns jobs to regions
based on carbon intensity.  It simulates regional queues and returns
job status.  Real implementations would integrate with emissions
data providers and compute infrastructure.
"""

from __future__ import annotations

import asyncio
import random
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Job(BaseModel):
    job_id: str
    payload: str


class Region:
    def __init__(self, name: str) -> None:
        self.name = name
        self.queue: Dict[str, Job] = {}
        self.carbon_intensity = random.uniform(100, 400)  # gCO2eq/kWh

    async def add_job(self, job: Job) -> None:
        # Simulate asynchronous job processing
        self.queue[job.job_id] = job
        await asyncio.sleep(random.uniform(0.1, 0.5))
        # In a real system, job completion would be signaled separately
        del self.queue[job.job_id]


class Orchestrator:
    def __init__(self) -> None:
        # Pretend we have three regions.  In reality you would query
        # carbon intensity and capacity from external services.
        self.regions: Dict[str, Region] = {
            "us-east": Region("us-east"),
            "eu-west": Region("eu-west"),
            "asia-south": Region("asia-south"),
        }
        # Track submitted jobs
        self.jobs: Dict[str, str] = {}

    def select_region(self) -> Region:
        # Choose region with lowest carbon intensity
        return min(self.regions.values(), key=lambda r: r.carbon_intensity)

    async def submit_job(self, job: Job) -> str:
        if job.job_id in self.jobs:
            raise ValueError("Job ID already exists")
        region = self.select_region()
        self.jobs[job.job_id] = region.name
        # Fire off job processing asynchronously
        asyncio.create_task(region.add_job(job))
        return region.name

    def get_status(self, job_id: str) -> Optional[str]:
        region_name = self.jobs.get(job_id)
        if region_name is None:
            return None
        region = self.regions[region_name]
        return "queued" if job_id in region.queue else "completed"


app = FastAPI(title="Carbon‑Aware Orchestrator", version="0.1.0")
orch = Orchestrator()


@app.post("/jobs")
async def submit_job(job: Job) -> Dict[str, str]:
    try:
        region_name = await orch.submit_job(job)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"job_id": job.job_id, "region": region_name}


@app.get("/jobs/{job_id}")
def job_status(job_id: str) -> Dict[str, str]:
    status = orch.get_status(job_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)