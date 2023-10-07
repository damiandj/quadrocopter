import math
import unittest

from parameterized import parameterized

from quadrocopter.model.utils import Point, Transmitter


class TestPoint(unittest.TestCase):
    @parameterized.expand([
        (1, 1, 1, 1, 0),
        (1, 1, 2, 2, math.sqrt(2)),
        (1, 1, 1, 2, 1)
    ])
    def test_distance_to(self, x1: int, y1: int, x2: int, y2: int, dist: float) -> None:
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)

        self.assertEqual(p1.distance_to(p2), p2.distance_to(p1))
        self.assertEqual(p1.distance_to(p2), dist)


class TestTransmitter(unittest.TestCase):
    @parameterized.expand([
        (1, 1, True),
        (2, 2, True),
        (2, 4, True),
        (2, 5, False),
    ])
    def test_is_point_in_range(self, px1: int, px2: int, result: bool) -> None:
        transmitter = Transmitter(Point(2, 2), 2)
        p = Point(px1, px2)
        self.assertEqual(transmitter.is_point_in_range(p), result)

    @parameterized.expand([
        (2, 2, 2, True),
        (1, 1, 1, True),
        (5, 5, 1, False),
        (5, 5, 0, False),
    ])
    def test_do_transmitters_intersect(self, x: int, y: int, power: int, result: bool) -> None:
        transmitter_1 = Transmitter(Point(2, 2), 2)
        transmitter_2 = Transmitter(Point(x, y), power)

        self.assertEqual(transmitter_1.do_transmitters_intersect(transmitter_2),
                         transmitter_2.do_transmitters_intersect(transmitter_1))
        self.assertEqual(transmitter_1.do_transmitters_intersect(transmitter_2), result)
