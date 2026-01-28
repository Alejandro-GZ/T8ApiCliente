from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


@staticmethod
def plot_xy(
        x: np.ndarray,
        y: np.ndarray,
        xlabel: str,
        ylabel: str,
        title: str,
        output_path: str | Path,
    ) -> None:
        """Create and save a 2D line plot.

        Generates a simple XY plot with the provided data and labels, then saves it
        to the specified output path. The plot includes a grid for better readability.

            x (np.ndarray): Array of x-axis values.
            y (np.ndarray): Array of y-axis values corresponding to x.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the plot.
            output_path (str | Path): File path where the plot image will be saved.
                Parent directories will be created if they don't exist.

        Returns:
            None

        Example:
            >>> import numpy as np
            >>> x = np.linspace(0, 10, 100)
            >>> y = np.sin(x)
            >>> plot_xy(x, y, "Time", "Amplitude", "Sine Wave", "output/plot.png")
        """
        output_path = Path(output_path)

        plt.figure()
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
