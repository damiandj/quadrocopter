import random
import time

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from quadrocopter.model.path_finder import PathFinder
from quadrocopter.model.utils import Transmitter, Point

# Constants
MAX_TRANSMITTERS = 1000
ITERATIONS = 100
TIMES = []


# Function to run path finding with random transmitters
def run_path_finding(transmitters_count: int) -> float:
    max_range = transmitters_count
    max_power = max(int(transmitters_count / 14), 1)
    _transmitters = [
        Transmitter(Point(random.randint(0, max_range), random.randint(0, max_range)), random.randint(1, max_power)) for
        _ in
        range(transmitters_count)]
    _start = random.sample(_transmitters, k=1)[0].center
    _end = random.sample(_transmitters, k=1)[0].center
    tp = PathFinder(start=_start, end=_end, transmitters=_transmitters)
    start_time = time.time()
    _, path = tp.is_path_possible()
    elapsed_time = time.time() - start_time
    return elapsed_time


# Create data for different transmitter counts
transmitter_counts = range(10, MAX_TRANSMITTERS + 1, 10)
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
