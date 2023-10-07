from __future__ import annotations

from collections import deque
from typing import List, Tuple

from matplotlib import pyplot as plt

from quadrocopter.model.utils import Point, Transmitter


class PathFinder:
    """
    A class for finding paths between points in the presence of transmitters.

    Attributes:
        start (Point): The starting point of the path.
        end (Point): The ending point of the path.
        transmitters (List[Transmitter]): A list of transmitters in the environment.
    """

    def __init__(self, start: Point, end: Point, transmitters: List[Transmitter]) -> None:
        """
        Initialize a PathFinder object.

        Args:
            start (Point): The starting point of the path.
            end (Point): The ending point of the path.
            transmitters (List[Transmitter]): A list of transmitters in the environment.
        """
        self.start = start
        self.end = end
        self.transmitters = transmitters

    def is_path_possible(self) -> Tuple[bool, List[Transmitter]]:
        """
        Check if a path between the start and end points is possible in the presence of transmitters.

        Returns:
            Tuple[bool, List[Transmitter]]: A tuple where the first element is a boolean indicating
            if a path is possible, and the second element is a list of transmitters representing
            the path if found.
        """
        visited = set()
        queue = deque(
            [(transmitter,) for transmitter in self.transmitters if transmitter.is_point_in_range(self.start)])

        while queue:
            path = queue.popleft()
            current_transmitter = path[-1]

            if current_transmitter.is_point_in_range(self.end):
                return True, list(path)  # Return both True and the path

            neighbors = [
                neighbor for neighbor in self.transmitters
                if (neighbor != current_transmitter
                    and current_transmitter.do_transmitters_intersect(neighbor)
                    and neighbor not in path
                    and neighbor not in visited)
            ]

            queue.extend([(path + (neighbor,)) for neighbor in neighbors])
            visited.update(neighbors)

        return False, []  # Return both False and an empty path

    def draw_environment(self, path: List[Transmitter] = None):
        """
        Draw the environment including transmitters, start and end points, and the shortest path if provided.

        Args:
            path (List[Transmitter]): The list of transmitters representing the path (optional).
        """
        plt.figure(figsize=(8, 8))

        for transmitter in self.transmitters:
            circle = plt.Circle((transmitter.center.x, transmitter.center.y), transmitter.power, color='black',
                                fill=False)
            plt.gca().add_patch(circle)

        plt.scatter([self.start.x], [self.start.y], color='green', marker='+', label='Start', s=100)
        plt.scatter([self.end.x], [self.end.y], color='red', marker='+', label='End', s=100)

        if path:
            path_x = [self.start.x] + [transmitter.center.x for transmitter in path] + [self.end.x]
            path_y = [self.start.y] + [transmitter.center.y for transmitter in path] + [self.end.y]
            plt.plot(path_x, path_y, linestyle='--', marker='o', markersize=0, color='blue', label='Path')

        plt.xlim(0, 5 + max(t.center.x + t.power for t in self.transmitters))
        plt.ylim(0, 5 + max(t.center.y + t.power for t in self.transmitters))
        plt.gca().set_aspect('equal', adjustable='box')
        plt.legend()
        plt.grid(True)
        plt.title('Polygon with Transmitters and Path')
        plt.show()
