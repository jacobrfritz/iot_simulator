import argparse
import asyncio
import numpy as np

import redis.asyncio as aioredis

from .distributions import Exponential, LogNormal, Normal
from .event_emitters import GatewayEventEmitter
from .producer_factory import ProducerFactory
from .producers import IOTProducer
from .workers import GatewayWorker
from .worker_manager import WorkerManager

            

def get_redis(host: str = "localhost", port: int = 6379):
    pool = aioredis.BlockingConnectionPool(
        host=host,
        port=port,
        max_connections=100,
        timeout=30,
        decode_responses=True,
    )
    return  aioredis.Redis(connection_pool=pool)
        
               
async def run(args: argparse.Namespace) -> None:
    """Core application logic."""

    queue = asyncio.Queue()
    emitter = GatewayEventEmitter(queue)
    shared_rng = np.random.default_rng()
    worker_manager = WorkerManager()
    producer_factory = ProducerFactory()
    
    try:
        
        producers = producer_factory.make_producers(
            num_producers=args.num_clients,
            producer=IOTProducer,
            create_distribution=Exponential,
            delay_distribtuion=LogNormal,
            event_value_distribution=Normal,
            emitter=emitter,
            rng=shared_rng
        )
        workers = [worker_manager.create_worker(GatewayWorker, queue, get_redis(), GatewayEventEmitter, 100, worker) for worker in range(args.max_workers)]
        event_loops = [producer.event_loop() for producer in producers]
        await asyncio.gather(*event_loops, *workers)
    finally:
        ...
