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
        create_distribution: Distribution,
        delay_distribtuion: Distribution,
        event_value_distribution: Distribution,
        emitter: EventEmitter,
    ) -> list[Producer]:
        producers = []
        for _ in range(num_producers):
            producers.append(
                producer(
                    event_create_distribution=create_distribution,
                    event_delay_distribution=delay_distribtuion,
                    event_value_distribution=event_value_distribution,
                    event_emitter=emitter,
                )
            )
        return producers
