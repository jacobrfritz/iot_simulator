import asyncio
import argparse

from iot_simulator.distributions import Normal, Poisson, LogNormal 
from iot_simulator.event_emitters import PrintEventEmitter
from iot_simulator.producer_factory import ProducerFactory
from iot_simulator.producers import IOTProducer

def clients_to_generate(factory: ProducerFactory, emitter, args:argparse.Namespace):
    all_clients = []
    for group in args.dist:
        if group['create_distribution'] == 'normal':
            create_distribution = Normal()
        if group['delay_distribution'] == 'normal':
            delay_distribution = Normal()
        if group['event_value_distribution'] == 'normal':
            event_value_distribution = Normal()
        
        if group['create_distribution'] == 'poisson':
            create_distribution = Poisson()
        if group['delay_distribution'] == 'poisson':
            delay_distribution = Poisson()
        if group['event_value_distribution'] == 'poisson':
            event_value_distribution = Poisson()
            
        if group['create_distribution'] == 'lognormal':
            create_distribution = LogNormal()
        if group['delay_distribution'] == 'lognormal':
            delay_distribution = LogNormal()
        if group['event_value_distribution'] == 'lognormal':
            event_value_distribution = LogNormal()
            
        producers = factory.make_producers(
        num_producers=group['clients'], producer=IOTProducer, create_distribution=create_distribution, delay_distribtuion=delay_distribution, event_value_distribution=event_value_distribution, emitter=emitter
        )
        all_clients.extend(producers)
    return producers

async def run(args) -> None:
    """Core application logic."""
    
    emitter = PrintEventEmitter()
    factory = ProducerFactory()
    producers = clients_to_generate(factory, emitter, args)
    event_loops = [producer.event_loop() for producer in producers]
    await asyncio.gather(*event_loops)
