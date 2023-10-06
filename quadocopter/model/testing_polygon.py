from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import List

import networkx as nx


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

    def distance_to(self, other: Point) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass(unsafe_hash=True)
class Transmitter:
    center: Point
    power: int

    def is_point_in_range(self, point: Point) -> bool:
        return self.center.distance_to(point) <= self.power

    def do_transmitters_intersect(self, other_transmitter: Transmitter) -> bool:
        distance_between_centers_transmitters = self.center.distance_to(other_transmitter.center)
        return distance_between_centers_transmitters <= (self.power + other_transmitter.power)


class TestingPolygon:
    def __init__(self, start: Point, end: Point, transmitters: List[Transmitter]) -> None:
        self.start = start
        self.end = end
        self.transmitters = transmitters

    def _build_graph(self) -> nx.Graph:
        graph = nx.Graph()
        for transmitter in self.transmitters:
            graph.add_node(transmitter)
        for t1, t2 in itertools.combinations(self.transmitters, 2):
            if t1.do_transmitters_intersect(t2):
                graph.add_edge(t1, t2)

        return graph

    def is_path_possible_graph(self) -> bool:
        transmitters_in_the_start_point_neighborhood = [
            transmitter for transmitter in self.transmitters if
            transmitter.is_point_in_range(point=self.start)
        ]

        transmitters_in_the_end_point_neighborhood = [
            transmitter for transmitter in self.transmitters if
            transmitter.is_point_in_range(point=self.end)
        ]

        if not transmitters_in_the_start_point_neighborhood or not transmitters_in_the_end_point_neighborhood:
            return False

        graph = self._build_graph()

        return nx.has_path(graph, transmitters_in_the_start_point_neighborhood[0],
                           transmitters_in_the_end_point_neighborhood[0])

    def is_path_possible(self) -> bool:
        _history = []

        def step(current_transmitter: Transmitter) -> bool:
            if current_transmitter.is_point_in_range(point=self.end):
                return True
            transmitters_in_neighborhood = [
                transmitter for transmitter in self.transmitters if current_transmitter.do_transmitters_intersect(
                    other_transmitter=transmitter) and current_transmitter != transmitter
            ]

            for transmitter in transmitters_in_neighborhood:
                if not {current_transmitter, transmitter} in _history:
                    _history.append({current_transmitter, transmitter})
                    return step(transmitter)
            return False

        transmitters_in_the_start_point_neighborhood = [
            transmitter for transmitter in self.transmitters if
            transmitter.is_point_in_range(point=self.start)
        ]
        if not transmitters_in_the_start_point_neighborhood:
            return False
        return step(transmitters_in_the_start_point_neighborhood[0])


_transmitters = [
    Transmitter(Point(6, 11), 4),
    Transmitter(Point(8, 17), 3),
    Transmitter(Point(19, 19), 2),
    Transmitter(Point(19, 11), 4),
    Transmitter(Point(15, 7), 6),
    Transmitter(Point(12, 19), 4)
]

_start = Point(10, 19)
_end = Point(19, 14)

tp = TestingPolygon(start=_start, end=_end, transmitters=_transmitters)

print(tp.is_path_possible_graph())
print(tp.is_path_possible())
