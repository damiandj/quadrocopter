from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Point:
    """
    Represents a 2D point with x and y coordinates.

    Attributes:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
    """

    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x, self.y}"

    def __repr__(self) -> str:
        return self.__str__()

    def distance_to(self, other: Point) -> float:
        """
        Calculate the Euclidean distance between this point and another point.

        Args:
            other (Point): The other point to calculate the distance to.

        Returns:
            float: The Euclidean distance between this point and the other point.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass(unsafe_hash=True)
class Transmitter:
    """
    Represents a transmitter with a center point and power range.

    Attributes:
        center (Point): The center point of the transmitter.
        power (int): The power range of the transmitter.
    """

    center: Point
    power: int

    def __str__(self) -> str:
        return f"{self.center, self.power}"

    def __repr__(self) -> str:
        return self.__str__()

    def is_point_in_range(self, point: Point) -> bool:
        """
        Check if a given point is within the range of this transmitter.

        Args:
            point (Point): The point to check.

        Returns:
            bool: True if the point is within the range of the transmitter, False otherwise.
        """
        return self.center.distance_to(point) <= self.power

    def do_transmitters_intersect(self, other_transmitter: Transmitter) -> bool:
        """
        Check if this transmitter intersects with another transmitter.

        Args:
            other_transmitter (Transmitter): The other transmitter to check for intersection.

        Returns:
            bool: True if the transmitters intersect, False otherwise.
        """
        distance_between_centers_transmitters = self.center.distance_to(other_transmitter.center)
        return distance_between_centers_transmitters <= (self.power + other_transmitter.power)
