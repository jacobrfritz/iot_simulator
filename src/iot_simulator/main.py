import argparse
import asyncio

from iot_simulator.distributions import Distribution, Exponential, LogNormal, Normal
from iot_simulator.event_emitters import EventEmitter, RedisEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer, Producer


def clients_to_generate(
    factory: ProducerFactory, emitter: EventEmitter, args: argparse.Namespace
) -> list[Producer]:
    all_clients = []
    for group in args.dist:
        create_distribution: Distribution
        delay_distribution: Distribution
        event_value_distribution: Distribution

        if group["create_distribution"] == "normal":
            create_distribution = Normal()
        elif group["create_distribution"] == "exponential":
            create_distribution = Exponential()
        elif group["create_distribution"] == "lognormal":
            create_distribution = LogNormal()

        if group["delay_distribution"] == "normal":
            delay_distribution = Normal()
        elif group["delay_distribution"] == "exponential":
            delay_distribution = Exponential()
        elif group["delay_distribution"] == "lognormal":
            delay_distribution = LogNormal()

        if group["event_value_distribution"] == "normal":
            event_value_distribution = Normal()
        elif group["event_value_distribution"] == "exponential":
            event_value_distribution = Exponential()
        elif group["event_value_distribution"] == "lognormal":
            event_value_distribution = LogNormal()

        producers = factory.make_producers(
            num_producers=group["clients"],
            producer=IOTProducer,
            create_distribution=create_distribution,
            delay_distribtuion=delay_distribution,
            event_value_distribution=event_value_distribution,
            emitter=emitter,
        )
        all_clients.extend(producers)
    return all_clients


async def run(args: argparse.Namespace) -> None:
    """Core application logic."""

    emitter = RedisEventEmitter()
    try:
        factory = ProducerFactory()
        producers = clients_to_generate(factory, emitter, args)
        event_loops = [producer.event_loop() for producer in producers]
        await asyncio.gather(*event_loops)
    finally:
        await emitter.close()
