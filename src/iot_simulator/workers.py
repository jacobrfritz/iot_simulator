from typing import Protocol
import asyncio

from redis import Redis

from .event_emitters import EventEmitter

class Worker(Protocol):
    async def loop(self, worker_id: int, queue: asyncio.Queue, redis_client: Redis, emiter: EventEmitter):
        ...

class GatewayWorker(Worker):
    """
    Reads Items from the queue and emits
    """
    def __init__(self,
        worker_id: int, 
        queue: asyncio.Queue, 
        redis_client: Redis, 
        emiter: EventEmitter):
        self.worker_id = worker_id
        self.queue = queue
        self.redis_client = redis_client
        self.emiter = emiter
        
    async def loop(self, batch_size:int ):
        """
        Workers continuously drain the queue and send data to Redis in batches
        using pipelines for maximum performance.
        """
        print(f"Worker {self.worker_id} started.")
        
        while True:
            batch = []
            
            # 1. Grab the first item (waits asynchronously if queue is empty)
            first_item = await self.queue.get()
            batch.append(first_item)
            self.queue.task_done()

            # 2. Opportunistically drain more items up to batch_size without waiting
            while len(batch) < batch_size and not self.queue.empty():
                item = self.queue.get_nowait()
                batch.append(item)
                self.queue.task_done()

            # 3. Flush the batch to Redis Streams using an atomic pipeline
            try:
                async with self.redis_client.pipeline(transaction=False) as pipe:
                    for event in batch:
                        # Revert to event.to_dict() so Redis gets its required dictionary format
                        pipe.xadd(
                            "iot_events",           # Using your original stream name from before
                            event.to_dict(),        # Crucial fix here!
                            id="*", 
                            maxlen=50000, 
                            approximate=True
                        )
                    
                    # Executes all XADDs in a single network round-trip
                    await pipe.execute()
                    
            except Exception as e:
                print(f"Worker {self.worker_id} failed to flush to Redis: {e}")