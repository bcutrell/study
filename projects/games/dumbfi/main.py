import pyxel
import random
from collections import deque


class App:
    def __init__(self, width=160, height=120, fps=30, max_points=100):
        self.width = width
        self.height = height
        self.fps = fps
        self.max_points = max_points

        # Data points for the graph (using deque for efficient append/pop)
        self.data_points = deque(maxlen=max_points)

        # Colors
        self.bg_color = 0  # Black
        self.line_color = 11  # Yellow
        self.axis_color = 5  # Gray

        # Graph boundaries (leave some margin)
        self.margin = 10
        self.graph_x = self.margin
        self.graph_y = self.margin
        self.graph_width = self.width - 2 * self.margin
        self.graph_height = self.height - 2 * self.margin

        # Value range
        self.min_value = 0
        self.max_value = 100

        # Initialize Pyxel
        pyxel.init(self.width, self.height, title="dumbfi", fps=self.fps)

        # Start with some random data
        for _ in range(self.max_points // 2):
            self.add_data_point()

        # Start the app
        pyxel.run(self.update, self.draw)

    def add_data_point(self):
        # Generate a random value between min_value and max_value
        new_value = random.randint(self.min_value, self.max_value)
        self.data_points.append(new_value)

    def update(self):
        # Add a new random data point every frame
        self.add_data_point()

        # Exit on Q or ESC key
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def draw(self):
        # Clear the screen
        pyxel.cls(self.bg_color)

        # Draw axes
        pyxel.line(
            self.graph_x,
            self.graph_y + self.graph_height,
            self.graph_x + self.graph_width,
            self.graph_y + self.graph_height,
            self.axis_color,
        )  # X-axis
        pyxel.line(
            self.graph_x,
            self.graph_y,
            self.graph_x,
            self.graph_y + self.graph_height,
            self.axis_color,
        )  # Y-axis

        # Draw line graph
        if len(self.data_points) > 1:
            # Calculate x step based on number of points
            x_step = self.graph_width / (self.max_points - 1)

            # Draw lines connecting data points
            for i in range(len(self.data_points) - 1):
                # Calculate coordinates
                x1 = self.graph_x + i * x_step
                y1 = (
                    self.graph_y
                    + self.graph_height
                    - (self.data_points[i] / self.max_value * self.graph_height)
                )
                x2 = self.graph_x + (i + 1) * x_step
                y2 = (
                    self.graph_y
                    + self.graph_height
                    - (self.data_points[i + 1] / self.max_value * self.graph_height)
                )

                # Draw the line segment
                pyxel.line(x1, y1, x2, y2, self.line_color)


if __name__ == "__main__":
    App(width=240, height=180, fps=15)
