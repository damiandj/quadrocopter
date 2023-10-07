import math
import tkinter as tk
from tkinter import messagebox

from quadrocopter.model.path_finder import PathFinder
from quadrocopter.model.utils import Transmitter, Point

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20


class QuadrocopterApp:
    """
    A GUI application for Quadrocopter Path Finding.
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize the QuadrocopterApp.

        Args:
            root (tk.Tk): The tkinter root window.
        """

        self.root = root
        self.root.title("Quadrocopter Path Finder")

        self.transmitters = []
        self.start = None
        self.end = None

        self.path = None

        self.setting_start = False
        self.setting_end = False
        self.creating_transmitter = False
        self.current_transmitter = None

        self.create_widgets()
        self.setup_canvas_bindings()
        self.draw_environment()

    def create_widgets(self):
        """
        Create GUI widgets and buttons.
        """
        self.result_box = tk.Text(self.root, wrap=tk.WORD, width=40, height=2, state=tk.DISABLED, bg='white')
        self.result_box.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        self.create_button("Add Transmitter", self.add_transmitter)
        self.create_button("Set Start Point", self.set_start)
        self.create_button("Set End Point", self.set_end)
        self.create_button("Check Path", self.check_path)
        self.create_button("Reset Data", self.reset_data, bg='red')

    def create_button(self, text, command, bg='#007acc'):
        """
        Create and display a tkinter button.

        Args:
            text (str): The text to display on the button.
            command (callable): The function to call when the button is clicked.
            bg (str): Background color.
        """
        button = tk.Button(self.root, text=text, command=command, bg=bg, fg='white', font=("Arial", 12))
        button.pack(side=tk.LEFT, padx=10)

    def setup_canvas_bindings(self):
        """
        Setup mouse event bindings for the canvas.
        """
        self.canvas.bind("<Button-1>", self.canvas_left_click)
        self.canvas.bind("<B1-Motion>", self.canvas_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_left_release)

    def canvas_left_click(self, event):
        """
        Handle left mouse clicks on the canvas.

        Args:
            event (tk.Event): The mouse click event.
        """
        x, y = event.x, event.y
        x_grid, y_grid = x // GRID_SIZE, (WINDOW_HEIGHT - y) // GRID_SIZE

        if self.setting_start:
            self.start = Point(x_grid, y_grid)
        elif self.setting_end:
            self.end = Point(x_grid, y_grid)
        elif self.creating_transmitter:
            self.transmitters.append(Transmitter(Point(x_grid, y_grid), 0))
            self.current_transmitter = self.transmitters[-1]

        self.setting_start, self.setting_end = False, False
        self.reset_path()
        self.draw_environment()

    def canvas_left_drag(self, event):
        """
        Handle mouse drag events on the canvas.

        Args:
            event (tk.Event): The mouse drag event.
        """
        if self.creating_transmitter and self.current_transmitter:
            x, y = event.x, event.y
            x_grid, y_grid = x // GRID_SIZE, (WINDOW_HEIGHT - y) // GRID_SIZE
            self.current_transmitter.power = max(0, int(math.sqrt(
                (x_grid - self.current_transmitter.center.x) ** 2 + (y_grid - self.current_transmitter.center.y) ** 2)))
            self.draw_environment()

    def canvas_left_release(self, event):
        """
        Handle mouse button release events on the canvas.

        Args:
            event (tk.Event): The mouse release event.
        """
        if self.creating_transmitter:
            self.creating_transmitter = False
            self.reset_path()

    def reset_path(self):
        """
        Reset the path and result box to their initial state.
        """
        self.path = None
        self.result_box.config(state=tk.NORMAL, bg='white')
        self.result_box.delete(1.0, tk.END)
        self.result_box.config(state=tk.DISABLED)

    def draw_grid(self):
        """
        Draw a grid on the canvas with labels on the boundaries.
        """
        for i in range(0, WINDOW_HEIGHT, GRID_SIZE):
            self.canvas.create_line(0, i, WINDOW_WIDTH, i, fill="lightgray")

        for j in range(0, WINDOW_WIDTH, GRID_SIZE):
            self.canvas.create_line(j, 0, j, WINDOW_HEIGHT, fill="lightgray")

        for x in range(0, WINDOW_WIDTH, 2 * GRID_SIZE):
            label_x = x // GRID_SIZE
            self.canvas.create_text(x + GRID_SIZE // 2, WINDOW_HEIGHT - GRID_SIZE // 2, text=label_x, fill="black")

        for y in range(0, WINDOW_HEIGHT, 2 * GRID_SIZE):
            label_y = (WINDOW_HEIGHT - y) // GRID_SIZE
            self.canvas.create_text(GRID_SIZE // 2, y - GRID_SIZE // 2, text=f"{label_y}", fill="black")

    def reset_data(self):
        """
        Reset all data (transmitters, start, end, and path).
        """
        self.transmitters = []
        self.start = None
        self.end = None
        self.path = None
        self.result_box.config(state=tk.NORMAL, bg='white')
        self.result_box.delete(1.0, tk.END)
        self.result_box.config(state=tk.DISABLED)
        self.canvas.delete("all")
        self.draw_grid()

    def add_transmitter(self):
        """
        Set the flag for creating a transmitter.
        """
        self.creating_transmitter = True

    def set_start(self):
        """
        Set the flag for setting the start point.
        """
        self.setting_start = True

    def set_end(self):
        """
        Set the flag for setting the end point.
        """
        self.setting_end = True

    def check_path(self):
        """
        Check if a safe path is possible and update the result box and background color.
        """
        if not self.start or not self.end or not self.transmitters:
            messagebox.showerror("Error", "Please set start point, end point, and add transmitters.")
            return

        path_finder = PathFinder(start=self.start, end=self.end, transmitters=self.transmitters)
        result, self.path = path_finder.is_path_possible()
        bg_color = "lightgreen" if result else "red"

        self.result_box.config(state=tk.NORMAL, bg=bg_color)
        self.result_box.delete(1.0, tk.END)  # Clear previous results

        if result:
            self.result_box.insert(tk.END, "A safe flight path is possible.")

        else:
            self.result_box.insert(tk.END, "A safe flight path is not possible.")

        self.result_box.config(state=tk.DISABLED)
        self.draw_environment()

    def draw_environment(self):
        """
        Draw the environment on the canvas with transmitters, start, end, and path if available.
        """
        self.canvas.delete("all")
        self.draw_grid()

        if self.transmitters:
            for transmitter in self.transmitters:
                x, y = transmitter.center.x * GRID_SIZE, WINDOW_HEIGHT - transmitter.center.y * GRID_SIZE
                power = transmitter.power * GRID_SIZE
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
                self.canvas.create_oval(x - power, y - power, x + power, y + power, outline="black", width=2)
                self.canvas.create_line(x, y, x + power, y, fill="black", width=1)

        if self.start:
            x, y = self.start.x * GRID_SIZE, WINDOW_HEIGHT - self.start.y * GRID_SIZE
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                                    fill="green")

        if self.end:
            x, y = self.end.x * GRID_SIZE, WINDOW_HEIGHT - self.end.y * GRID_SIZE
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                                    fill="red")

        if self.path:
            x_start, y_start = self.start.x * GRID_SIZE, WINDOW_HEIGHT - self.start.y * GRID_SIZE
            x_path, y_path = self.path[0].center.x * GRID_SIZE, WINDOW_HEIGHT - self.path[0].center.y * GRID_SIZE
            self.canvas.create_line(x_start, y_start, x_path, y_path, fill="blue", width=2)

            x_end, y_end = self.end.x * GRID_SIZE, WINDOW_HEIGHT - self.end.y * GRID_SIZE
            x_path_end, y_path_end = self.path[-1].center.x * GRID_SIZE, WINDOW_HEIGHT - self.path[
                -1].center.y * GRID_SIZE
            self.canvas.create_line(x_end, y_end, x_path_end, y_path_end, fill="blue", width=2)

            for i in range(len(self.path) - 1):
                x1, y1 = self.path[i].center.x * GRID_SIZE, WINDOW_HEIGHT - self.path[i].center.y * GRID_SIZE
                x2, y2 = self.path[i + 1].center.x * GRID_SIZE, WINDOW_HEIGHT - self.path[i + 1].center.y * GRID_SIZE
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)


def main() -> None:
    root = tk.Tk()
    app = QuadrocopterApp(root)
    root.mainloop()
