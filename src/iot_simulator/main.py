import asyncio
import argparse

from iot_simulator.distributions import Normal, Exponential, LogNormal
from iot_simulator.event_emitters import RedisEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer


def clients_to_generate(factory: ProducerFactory, emitter, args: argparse.Namespace):
    all_clients = []
    for group in args.dist:
        if group["create_distribution"] == "normal":
            create_distribution = Normal()
        if group["delay_distribution"] == "normal":
            delay_distribution = Normal()
        if group["event_value_distribution"] == "normal":
            event_value_distribution = Normal()

        if group["create_distribution"] == "exponential":
            create_distribution = Exponential()
        if group["delay_distribution"] == "exponential":
            delay_distribution = Exponential()
        if group["event_value_distribution"] == "exponential":
            event_value_distribution = Exponential()

        if group["create_distribution"] == "lognormal":
            create_distribution = LogNormal()
        if group["delay_distribution"] == "lognormal":
            delay_distribution = LogNormal()
        if group["event_value_distribution"] == "lognormal":
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


async def run(args) -> None:
    """Core application logic."""

    emitter = RedisEventEmitter()
    factory = ProducerFactory()
    producers = clients_to_generate(factory, emitter, args)
    event_loops = [producer.event_loop() for producer in producers]
    await asyncio.gather(*event_loops)
