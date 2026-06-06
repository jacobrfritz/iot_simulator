import argparse

from iot_simulator.distributions import Normal
from iot_simulator.event_emitters import PrintEventEmitter
from iot_simulator.main import clients_to_generate
from iot_simulator.producer_factory import ProducerFactory


def test_clients_to_generate():
    factory = ProducerFactory()
    emitter = PrintEventEmitter()

    args = argparse.Namespace(
        dist=[
            {
                "create_distribution": "normal",
                "delay_distribution": "normal",
                "event_value_distribution": "normal",
                "clients": 3,
            }
        ]
    )

    clients = clients_to_generate(factory, emitter, args)
    assert len(clients) == 3
    assert isinstance(clients[0].event_create_distribution, Normal)
