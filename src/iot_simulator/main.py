import argparse
import asyncio
import numpy as np

import redis.asyncio as aioredis

from iot_simulator.distributions import Distribution, Exponential, LogNormal, Normal
from iot_simulator.event_emitters import EventEmitter, GatewayEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer, Producer

async def redis_worker(worker_id: int, queue: asyncio.Queue, redis_client: Redis, batch_size: int = 200):
    """
    Workers continuously drain the queue and send data to Redis in batches
    using pipelines for maximum performance.
    """
    print(f"Worker {worker_id} started.")
    while True:
        batch = []
        
        # 1. Grab the first item (waits asynchronously if queue is empty)
        first_item = await queue.get()
        batch.append(first_item)
        queue.task_done()

        # 2. Opportunistically drain more items up to batch_size without waiting
        while len(batch) < batch_size and not queue.empty():
            item = queue.get_nowait()
            batch.append(item)
            queue.task_done()

        # 3. Flush the batch to Redis Streams using an atomic pipeline
        try:
            async with redis_client.pipeline(transaction=False) as pipe:
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
            print(f"Worker {worker_id} failed to flush to Redis: {e}")
            

def get_redis(host: str = "localhost", port: int = 6379):
    pool = aioredis.BlockingConnectionPool(
        host=host,
        port=port,
        max_connections=100,
        timeout=30,
        decode_responses=True,
    )
    return  aioredis.Redis(connection_pool=pool)
        
               
def clients_to_generate(
    factory: ProducerFactory, emitter: EventEmitter, args: argparse.Namespace, rng:np.random.Generator
) -> list[Producer]:
    all_clients = []
    for group in args.dist:
        create_distribution: Distribution
        delay_distribution: Distribution
        event_value_distribution: Distribution

        # if group["create_distribution"] == "normal":
        #     create_distribution = Normal()
        # elif group["create_distribution"] == "exponential":
        #     create_distribution = Exponential()
        # elif group["create_distribution"] == "lognormal":
        #     create_distribution = LogNormal()

        # if group["delay_distribution"] == "normal":
        #     delay_distribution = Normal()
        # elif group["delay_distribution"] == "exponential":
        #     delay_distribution = Exponential()
        # elif group["delay_distribution"] == "lognormal":
        #     delay_distribution = LogNormal()

        # if group["event_value_distribution"] == "normal":
        #     event_value_distribution = Normal()
        # elif group["event_value_distribution"] == "exponential":
        #     event_value_distribution = Exponential()
        # elif group["event_value_distribution"] == "lognormal":
        #     event_value_distribution = LogNormal()

        producers = factory.make_producers(
            num_producers=group["clients"],
            producer=IOTProducer,
            create_distribution=Exponential,
            delay_distribtuion=LogNormal,
            event_value_distribution=Normal,
            emitter=emitter,
            rng=rng
        )
        all_clients.extend(producers)
    return all_clients

def workers_to_generate(num_workers:int, queue:asyncio.Queue, redis_conn, batch_size):
    worker_tasks = []
    for i in range(num_workers):
        task = asyncio.create_task(redis_worker(i, queue, redis_conn, batch_size))
        worker_tasks.append(task)
    return worker_tasks
        
async def run(args: argparse.Namespace) -> None:
    """Core application logic."""

    queue = asyncio.Queue()
    emitter = GatewayEventEmitter(queue)
    shared_rng = np.random.default_rng()
    try:
        factory = ProducerFactory()
        producers = clients_to_generate(factory, emitter, args, shared_rng)
        workers = workers_to_generate(1, queue, get_redis(), 100)
        event_loops = [producer.event_loop() for producer in producers]
        await asyncio.gather(*event_loops, *workers)
    finally:
        ...
