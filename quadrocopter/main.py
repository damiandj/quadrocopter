from quadrocopter.model.path_finder import PathFinder
from quadrocopter.model.utils import Transmitter, Point


def main() -> None:
    num_transmitters = int(input("Podaj liczbę nadajników: "))

    transmitters = []
    for _ in range(num_transmitters):
        x, y, power = map(int, input("Podaj współrzędne (x y) i moc nadajnika: ").split())
        transmitters.append(Transmitter(Point(x, y), power))

    x, y = map(int, input("Podaj współrzędne punktu początkowego (x y): ").split())
    start = Point(x=x, y=y)

    x, y = map(int, input("Podaj współrzędne punktu końcowego (x y): ").split())
    end = Point(x=x, y=y)

    path_finder = PathFinder(start=start, end=end, transmitters=transmitters)
    result, path = path_finder.is_path_possible()
    if result:
        print("Bezpieczny przelot jest możliwy")
        path_finder.draw_environment(path)
    else:
        print("Bezpieczny przelot nie jest możliwy")
