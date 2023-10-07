import random
import time

import matplotlib.pyplot as plt
import numpy as np

from quadrocopter.model.path_finder import PathFinder
from quadrocopter.model.utils import Transmitter, Point

# Constants
MAX_TRANSMITTERS = 10000
ITERATIONS = 100
TIMES = []


# Function to run path finding with random transmitters
def run_path_finding(transmitters_count: int) -> float:
    _transmitters = [
        Transmitter(Point(random.randint(0, 100), random.randint(0, 100)), random.randint(0, 100)) for _ in
        range(transmitters_count)]
    _start = Point(random.randint(0, 100), random.randint(0, 100))
    _end = Point(random.randint(0, 100), random.randint(0, 100))
    tp = PathFinder(start=_start, end=_end, transmitters=_transmitters)
    start_time = time.time()
    tp.is_path_possible()
    elapsed_time = time.time() - start_time
    return elapsed_time


# Create data for different transmitter counts
transmitter_counts = range(1, MAX_TRANSMITTERS + 1, 10)
average_times = []

for transmitters_count in transmitter_counts:
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
