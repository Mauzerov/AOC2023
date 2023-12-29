import re
from abc import ABC
from math import lcm
from typing import Generator
from collections import deque

print(__file__)


modules = dict()
pulses = {
    'low': 0,
    'high': 0
}


class Module(ABC):
    name: str
    destinations: list[str]

    def __init__(self, _name: str, _destinations: list[str]):
        self.name = _name
        self.destinations = _destinations

    def receive(self, pulse: str, from_: str):
        ...


class FlipFlop(Module):
    on: bool = False

    def __init__(self, _name: str, _destinations: list[str]):
        super().__init__(_name, _destinations)

    def receive(self, pulse: str, from_: str) -> Generator[tuple[str, str, str], None, None]:
        super().receive(pulse, from_)
        if pulse == 'low':
            self.on = not self.on
            next_pulse = 'high' if self.on else 'low'

            for _destination in self.destinations:
                yield self.name, _destination, next_pulse


class Conjunction(Module):
    previous_pulses: dict[str, str]

    def __init__(self, _name: str, _destinations: list[str]):
        super().__init__(_name, _destinations)
        self.previous_pulses = dict()

    def receive(self, pulse: str, from_: str) -> Generator[callable, None, None]:
        super().receive(pulse, from_)
        self.previous_pulses[from_] = pulse
        all_high = all(pulse == 'high' for pulse in self.previous_pulses.values())
        next_pulse = 'low' if all_high else 'high'
        for _destination in self.destinations:
            yield self.name, _destination, next_pulse


start_destinations = None

with open('day20/input.txt') as f:
    for line in f.read().splitlines():
        if line.startswith('broadcaster'):
            destinations, = re.search(r'broadcaster -> ((?:[a-z]+(?:, )?)+)', line).groups()
            start_destinations = destinations.split(', ')
        else:
            module, name, destinations = re.search(r'([&%])([a-z]+) -> ((?:[a-z]+(?:, )?)+)', line).groups()
            destinations = destinations.split(', ')

            if module == '&':
                modules[name] = Conjunction(name, destinations)
            elif module == '%':
                modules[name] = FlipFlop(name, destinations)

    for module in modules.values():
        if isinstance(module, FlipFlop):
            for destination in module.destinations:
                destination_module = modules.get(destination)
                if isinstance(destination_module, Conjunction):
                    destination_module.previous_pulses[module.name] = 'low'

final_conjunction = next(module for module in modules.values() if 'rx' in module.destinations)
output_receivers = {
    module.name: 0
    for module in modules.values()
    if final_conjunction.name in module.destinations
}

button_presses = 0

while not all(output_receivers.values()) or button_presses < 1000:
    button_presses += 1
    stack: deque[callable] = deque()
    pulses['low'] += 1
    for destination in start_destinations:
        pulses['low'] += 1
        for current in modules[destination].receive('low', 'broadcaster'):
            stack.append(current)

    while stack:
        sender, receiver, pulse_ = stack.popleft()
        pulses[pulse_] += 1
        module = modules.get(receiver)

        if pulse_ == 'high' and sender in output_receivers and output_receivers[sender] == 0:
            output_receivers[sender] = button_presses
        if module is None:
            continue
        for current in module.receive(pulse_, sender):
            stack.append(current)

print(pulses['low'] * pulses['high'])
print(lcm(*output_receivers.values()))

