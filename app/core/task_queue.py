import asyncio
from app.core.config import settings

semaphore = asyncio.Semaphore(settings.max_concurrent_tasks)

async def enqueue_task(coro):
    async with semaphore:
        return await coro
