import asyncio
import argparse

from iot_simulator.distributions import Normal
from iot_simulator.event_emitters import PrintEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer

def clients_to_generate(factory: ProducerFactory, emitter, args:argparse.Namespace):
    all_clients = []
    for group in args.dist:
        if group['type'] == 'normal':
            producers = factory.make_producers(
            num_producers=group['clients'], producer=IOTProducer, distribution=Normal(), emitter=emitter
        )
        all_clients.extend(producers)
    return producers

async def run(args) -> None:
    """Core application logic."""
    
    emitter = PrintEventEmitter()
    factory = ProducerFactory()
    producers = clients_to_generate(factory, emitter, args)
    event_loops = [producer.event_loop(mean=1.0, sd=0.1) for producer in producers]
    await asyncio.gather(*event_loops)
