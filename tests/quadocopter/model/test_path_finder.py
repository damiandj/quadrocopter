import unittest

from quadrocopter.model.path_finder import PathFinder
from quadrocopter.model.utils import Transmitter, Point


class TestPathFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.transmitters = [
            Transmitter(Point(6, 11), 4),
            Transmitter(Point(8, 17), 3),
            Transmitter(Point(19, 19), 2),
            Transmitter(Point(19, 11), 4),
            Transmitter(Point(15, 7), 6),
            Transmitter(Point(12, 19), 4)
        ]

        self.circular_transmitters = [
            Transmitter(Point(2, 2), 2),
            Transmitter(Point(6, 2), 2),
            Transmitter(Point(2, 6), 2),
            Transmitter(Point(6, 6), 2),
            Transmitter(Point(10, 6), 2),
            Transmitter(Point(9, 2), 1)
        ]

    def test_is_path_possible(self) -> None:
        start = Point(10, 19)
        end = Point(19, 14)
        pf = PathFinder(start, end, self.transmitters)
        possible, _ = pf.is_path_possible()
        self.assertTrue(possible)

    def test_is_path_not_possible(self) -> None:
        start = Point(0, 0)
        end = Point(100, 100)
        pf = PathFinder(start, end, self.transmitters)
        possible, _ = pf.is_path_possible()
        self.assertFalse(possible)

    def test_is_circular_path_possible(self) -> None:
        start = Point(11, 6)
        end = Point(10, 2)
        pf = PathFinder(start, end, self.circular_transmitters)
        possible, _ = pf.is_path_possible()
        self.assertTrue(possible)

    def test_is_circular_path_not_possible(self) -> None:
        start = Point(11, 6)
        end = Point(12, 2)
        pf = PathFinder(start, end, self.circular_transmitters)
        possible, _ = pf.is_path_possible()
        self.assertFalse(possible)
