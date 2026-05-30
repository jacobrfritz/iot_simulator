import asyncio

from iot_simulator.distributions import Normal
from iot_simulator.event_emitters import PrintEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer


async def run() -> None:
    """Core application logic."""
    normal = Normal()
    emitter = PrintEventEmitter()
    factory = ProducerFactory()
    producers = factory.make_producers(
        num_producers=10, producer=IOTProducer, distribution=normal, emitter=emitter
    )

    event_loops = [producer.event_loop(mean=1.0, sd=0.1) for producer in producers]
    await asyncio.gather(*event_loops)
