from typing import Protocol
import asyncio

import redis.asyncio as aioredis

from iot_simulator.interfaces import Event


class EventEmitter(Protocol):
    async def emit(self, event: Event) -> None: ...


class PrintEventEmitter(EventEmitter):
    async def emit(self, event: Event) -> None:
        print(event.to_json())


class RedisEventEmitter(EventEmitter):
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.pool = aioredis.BlockingConnectionPool(
            host=host,
            port=port,
            max_connections=100,
            timeout=30,
            decode_responses=True,
        )
        self.r = aioredis.Redis(connection_pool=self.pool)

    async def emit(self, event: Event, stream_name: str = "iot_events") -> None:
        await self.r.xadd(
            stream_name, event.to_dict(), id="*", maxlen=50000, approximate=True
        )

    async def close(self) -> None:
        await self.r.aclose()
        await self.pool.disconnect()
        
class GatewayEventEmitter(EventEmitter):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        
    async def emit(self, event: Event):
        await self.queue.put(event)

