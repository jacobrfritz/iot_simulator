import numpy as np

from iot_simulator.distributions import Exponential, LogNormal, Normal
from iot_simulator.event_emitters import PrintEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer


def test_make_producers() -> None:
    factory = ProducerFactory()
    emitter = PrintEventEmitter()
    rng = np.random.default_rng(42)

    producers = factory.make_producers(
        num_producers=3,
        producer=IOTProducer,
        create_distribution=Exponential,
        delay_distribtuion=LogNormal,
        event_value_distribution=Normal,
        emitter=emitter,
        rng=rng,
    )

    assert len(producers) == 3
    assert isinstance(producers[0].event_create_distribution, Exponential)
    assert isinstance(producers[0].event_delay_distribution, LogNormal)
    assert isinstance(producers[0].event_value_distribution, Normal)
