"""
receives cmd line arguments to generate groups of producers
"""

from iot_simulator.producers import Producer
from iot_simulator.distributions import Distribution
from iot_simulator.event_emitters import EventEmitter


class ProducerFactory:
    def make_producers(
        self,
        num_producers: int,
        producer: type[Producer],
        distribution: Distribution,
        emitter: EventEmitter,
    ) -> list[Producer]:
        producers = []
        for _ in range(num_producers):
            producers.append(
                producer(
                    event_create_distribution=distribution,
                    event_delay_distribution=distribution,
                    event_value_distribution=distribution,
                    event_emitter=emitter,
                )
            )
        return producers
