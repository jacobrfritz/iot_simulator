from typing import Protocol

import redis.asyncio as aioredis

from iot_simulator.interfaces import Event


class EventEmitter(Protocol):
    async def emit(self, event: Event): ...


class PrintEventEmitter(EventEmitter):
    async def emit(self, event: Event):
        print(event.to_json())


class RedisEventEmitter(EventEmitter):
    async def emit(self, event: Event, stream_name: str = "iot_events"):
        r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
        entry_id = await r.xadd(
            stream_name, event.to_dict(), id="*", maxlen=50000, approximate=True
        )
