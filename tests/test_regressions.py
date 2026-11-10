import asyncio
import unittest
from orchestrator import Job, Orchestrator

class JobStatusTests(unittest.IsolatedAsyncioTestCase):
    async def test_status_tracks_task_lifecycle(self):
        orch = Orchestrator()
        job = Job(job_id="synthetic-job", payload="fixture")
        await orch.submit_job(job)
        self.assertEqual(orch.get_status(job.job_id), "queued")
        await orch.tasks[job.job_id]
        self.assertEqual(orch.get_status(job.job_id), "completed")
        with self.assertRaises(ValueError):
            await orch.submit_job(job)

    async def test_cancelled_work_is_failed(self):
        orch = Orchestrator()
        await orch.submit_job(Job(job_id="cancelled", payload="fixture"))
        task = orch.tasks["cancelled"]
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(orch.get_status("cancelled"), "failed")
