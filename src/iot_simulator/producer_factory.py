import numpy as np

"""
receives cmd line arguments to generate groups of producers
"""

from iot_simulator.distributions import Distribution
from iot_simulator.event_emitters import EventEmitter
from iot_simulator.producers import Producer


class ProducerFactory:
    def make_producers(
        self,
        num_producers: int,
        producer: type[Producer],
        create_distribution: type[Distribution],
        delay_distribtuion: type[Distribution],
        event_value_distribution: type[Distribution],
        emitter: EventEmitter,
        rng:np.random.Generator
    ) -> list[Producer]:
        producers = []
        for _ in range(num_producers):
            producers.append(
                producer(
                    event_create_distribution=create_distribution(rng),
                    event_delay_distribution=delay_distribtuion(rng),
                    event_value_distribution=event_value_distribution(rng),
                    event_emitter=emitter,
                )
            )
        return producers
