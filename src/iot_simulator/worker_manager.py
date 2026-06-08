import asyncio

import redis.asyncio as aioredis

from iot_simulator.interfaces import Event

from .event_emitters import EventEmitter
from .workers import Worker


class WorkerManager:
    def create_worker(
        self,
        worker: type[Worker],
        queue: asyncio.Queue[Event],
        redis_conn: aioredis.Redis,
        emiter: EventEmitter,
        batch_size: int,
        worker_id: int,
    ) -> asyncio.Task[None]:
        w = worker(worker_id, queue, redis_conn, emiter)
        task = asyncio.create_task(w.loop(batch_size))
        return task

    def worker_offline(self, worker: type[Worker]) -> None:
        """
        Worker stops emitting events to simulate going offline
        """
        ...

    def worker_online(self, worker: type[Worker]) -> None:
        """
        Worker start emitting events to simulate going coming back online
        """
        ...
