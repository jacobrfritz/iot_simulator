import asyncio

import redis.asyncio as aioredis

from .workers import Worker
from .event_emitters import EventEmitter

class WorkerManager:
    def create_worker(self, worker:type[Worker],  queue:asyncio.Queue, redis_conn:aioredis.Redis, emiter:EventEmitter, batch_size:int, worker_id:int):
        w = worker(worker_id, queue, redis_conn, emiter)
        task = asyncio.create_task(w.loop(batch_size))
        return task

    def worker_offline(self, worker:type[Worker]):
        """
        Worker stops emitting events to simulate going offline
        """
        ...
        
    def worker_online(self, worker:type[Worker]):
        """
        Worker start emitting events to simulate going coming back online
        """
        ...