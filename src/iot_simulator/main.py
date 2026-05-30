from iot_simulator.distributions import Normal
from iot_simulator.event_emitters import PrintEventEmitter
from iot_simulator.producers import IOTProducer

async def run() -> None:
    """Core application logic."""
    normal = Normal()
    emitter = PrintEventEmitter()
    producer = IOTProducer(
        event_create_distribution=normal,
        event_delay_distribution=normal,
        event_value_distribution=normal,
        event_emitter=emitter
    )
    await producer.event_loop(mean = 1.0, sd = 0.1)

