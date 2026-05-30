from typing import Protocol

from iot_simulator.interfaces import Event


class EventEmitter(Protocol):
    def emit(self, event: Event): ...
    
class PrintEventEmitter(EventEmitter):
    def emit(self, event: Event):
        print(event)