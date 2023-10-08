import random
import time

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from quadrocopter.model.path_finder import PathFinder
from quadrocopter.model.utils import Transmitter, Point

MAX_TRANSMITTERS = 2000
ITERATIONS = 100
STEP = 50
TIMES = []


def run_path_finding(transmitters_count: int) -> float:
    """
    Run path finding with random transmitters.

    Args:
        transmitters_count (int): The number of transmitters to use.

    Returns:
        float: The elapsed time in seconds for path finding.
    """
    max_range = transmitters_count
    max_power = max(int(transmitters_count / 14), 1)

    # Generate random transmitters
    transmitters = [
        Transmitter(Point(random.randint(0, max_range), random.randint(0, max_range)),
                    random.randint(1, max_power))
        for _ in range(transmitters_count)
    ]

    # Select random start and end points
    start_point = random.sample(transmitters, k=1)[0].center
    end_point = random.sample(transmitters, k=1)[0].center

    # Create a PathFinder instance
    path_finder = PathFinder(start=start_point, end=end_point, transmitters=transmitters)

    # Measure the time for path finding
    start_time = time.time()
    path_finder.is_path_possible()
    elapsed_time = time.time() - start_time

    return elapsed_time


def main() -> None:
    transmitter_counts = range(10, MAX_TRANSMITTERS + 1, STEP)
    average_times = []

    for transmitters_count in tqdm(transmitter_counts):
        iteration_times = []
        for _ in range(ITERATIONS):
            elapsed_time = run_path_finding(transmitters_count)
            iteration_times.append(elapsed_time)
        average_time = np.average(iteration_times)
        average_times.append(average_time)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(transmitter_counts, average_times, marker='o', linestyle='-')
    plt.title('Average Path Finding Time vs. Number of Transmitters')
    plt.xlabel('Number of Transmitters')
    plt.ylabel('Average Time (seconds)')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
