from __future__ import annotations

from typing import Protocol
import uuid
from datetime import datetime
import asyncio

from iot_simulator.event_emitters import EventEmitter
from iot_simulator.distributions import Distribution
from iot_simulator.interfaces import Event


class Producer(Protocol):
    """
    creates and emits events
    """

    id: uuid.UUID
    event_create_distribution: Distribution
    event_delay_distribution: Distribution
    event_emitter: EventEmitter

    def __init__(
        self,
        event_create_distribution: Distribution,
        event_delay_distribution: Distribution,
        event_value_distribution: Distribution,
        event_emitter: EventEmitter,
    ) -> None: ...

    def generate_event(self) -> Event: ...

    async def event_loop(self): ...


class IOTProducer(Producer):
    def __init__(
        self,
        event_create_distribution: Distribution,
        event_delay_distribution: Distribution,
        event_value_distribution: Distribution,
        event_emitter: EventEmitter,
    ):
        self.id = uuid.uuid4()
        self.event_create_distribution = event_create_distribution
        self.event_delay_distribution = event_delay_distribution
        self.event_value_distribution = event_value_distribution
        self.event_emitter = event_emitter

    def generate_event(self) -> tuple[float, float, float]:
        event_inter_arrival_time = self.event_create_distribution.sample()
        event_delay_time = self.event_delay_distribution.sample()
        event_value = self.event_value_distribution.sample()
        return event_inter_arrival_time, event_delay_time, event_value

    async def event_loop(self):
        async def delay_and_emit(event_delay_time: float, event: Event) -> None:
            await asyncio.sleep(event_delay_time)
            await self.event_emitter.emit(event)

        while True:
            event_inter_arrival_time, event_delay_time, event_value = (
                self.generate_event()
            )
            await asyncio.sleep(event_inter_arrival_time)
            event_start_time = datetime.now()
            event = Event(
                producer_id=self.id, event_time=event_start_time, payload=event_value
            )
            asyncio.create_task(delay_and_emit(event_delay_time, event))
