import re
from abc import ABC
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

with open('input.txt') as f:
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

prev = 0

for i in range(1000):
    stack: deque[callable] = deque()
    pulses['low'] += 1
    for destination in start_destinations:
        pulses['low'] += 1
        for current in modules[destination].receive('low', 'broadcaster'):
            stack.append(current)

    while stack:
        sender, receiver, pulse_ = stack.popleft()
        pulses[pulse_] += 1

        try:
            for current in modules[receiver].receive(pulse_, sender):
                stack.append(current)
        except KeyError:
            pass

    flipflops_on = [not m.on for m in modules.values() if isinstance(m, FlipFlop)]

    if all(flipflops_on):
        print(i, prev - i)
        prev = i

print(pulses['low'] * pulses['high'])


with open('graph.dot', 'w') as graph:
    graph.write("digraph {\n")
    for module in modules.values():
        color = 'red' if isinstance(module, FlipFlop) else 'blue'
        graph.write(f"\t{module.name} [color={color}]\n")
        for connection in module.destinations:
            graph.write(f"\t{module.name} -> {connection}\n")

    for start in start_destinations:
        graph.write(f"\tbroadcaster -> {start}\n")
    graph.write("}\n")


