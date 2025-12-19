from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class HU:
    @classmethod
    def read_even_lines(cls, path: str) -> list[list[float]]:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        series: list[list[float]] = []
        for line_index, line in enumerate(lines, start=1):
            if line_index % 2 != 0:
                continue
            line = line.strip()
            if not line:
                continue
            values = [float(value) for value in line.split(",") if value.strip()]
            if values:
                series.append(values)
        return series

    @classmethod
    def plot_overlay(cls, ax: plt.Axes, series: list[list[float]], title: str) -> None:
        for values in series:
            x = range(len(values))
            ax.plot(x, values, color="tab:blue", alpha=0.15, linewidth=1)
        ax.set_title(title)
        ax.set_xlabel("Index")
        ax.set_ylabel("8-bit brightness")
        ax.grid(True, alpha=0.2)

    @classmethod
    def plot_polyfit_overlay(
        cls,
        ax: plt.Axes,
        series: list[list[float]],
        title: str,
        degree: int = 4,
    ) -> None:
        for values in series:
            if len(values) <= degree:
                continue
            x = np.arange(len(values))
            coeffs = np.polyfit(x, values, degree)
            y_fit = np.polyval(coeffs, x)
            ax.plot(x, y_fit, color="tab:orange", alpha=0.35, linewidth=1)
        ax.set_title(title)
        ax.set_xlabel("Index")
        ax.set_ylabel("8-bit brightness (polyfit)")
        ax.grid(True, alpha=0.2)

    @classmethod
    def _polyfit_extrema_x(
        cls,
        coeffs: np.ndarray,
        x_min: float,
        x_max: float,
        tol: float = 1e-6,
    ) -> tuple[np.ndarray, np.ndarray]:
        deriv = np.polyder(coeffs)
        roots = np.roots(deriv)
        real_mask = np.isclose(roots.imag, 0.0, atol=1e-7)
        real_roots = roots[real_mask].real
        real_roots = real_roots[(real_roots >= x_min) & (real_roots <= x_max)]
        if real_roots.size == 0:
            return np.array([]), np.array([])
        real_roots.sort()
        second = np.polyder(deriv)
        maxima = []
        minima = []
        for root in real_roots:
            curvature = np.polyval(second, root)
            if abs(curvature) <= tol:
                continue
            if curvature < 0:
                maxima.append(root)
            else:
                minima.append(root)
        return np.array(maxima), np.array(minima)

    @classmethod
    def plot_polyfit_extrema_overlay(
        cls,
        ax: plt.Axes,
        series: list[list[float]],
        title: str,
        degree: int = 4,
    ) -> None:
        for values in series:
            if len(values) <= degree:
                continue
            x = np.arange(len(values))
            coeffs = np.polyfit(x, values, degree)
            y_fit = np.polyval(coeffs, x)
            ax.plot(x, y_fit, color="tab:orange", alpha=0.35, linewidth=1)
            x_maxima, x_minima = cls._polyfit_extrema_x(coeffs, 0, len(values) - 1)
            if x_maxima.size:
                y_maxima = np.polyval(coeffs, x_maxima)
                ax.scatter(x_maxima, y_maxima, color="red", s=20, alpha=0.85, zorder=3)
            if x_minima.size:
                y_minima = np.polyval(coeffs, x_minima)
                ax.scatter(x_minima, y_minima, color="blue", s=20, alpha=0.85, zorder=3)
        ax.set_title(title)
        ax.set_xlabel("Index")
        ax.set_ylabel("8-bit brightness (polyfit)")
        ax.grid(True, alpha=0.2)

    @classmethod
    def run(
        cls,
        data_paths: tuple[str, ...] = ("data1.csv", "data2.csv"),
        output_path: str = "overlay_plots.png",
    ) -> None:
        series_list = [cls.read_even_lines(path) for path in data_paths]
        fig_height = 4 * len(data_paths)
        fig, axes = plt.subplots(nrows=len(data_paths), ncols=1, figsize=(10, fig_height))
        if len(data_paths) == 1:
            axes = [axes]
        for ax, series, title in zip(axes, series_list, data_paths):
            cls.plot_overlay(ax, series, title)
        fig.tight_layout()
        plt.savefig(output_path, dpi=300)

    @classmethod
    def run_polyfit_overlay(
        cls,
        data_paths: tuple[str, ...] = ("data1.csv", "data2.csv"),
        output_path: str = "overlay_polyfit.png",
        degree: int = 4,
    ) -> None:
        series_list = [cls.read_even_lines(path) for path in data_paths]
        fig_height = 4 * len(data_paths)
        fig, axes = plt.subplots(nrows=len(data_paths), ncols=1, figsize=(10, fig_height))
        if len(data_paths) == 1:
            axes = [axes]
        for ax, series, title in zip(axes, series_list, data_paths):
            plot_title = f"{title} (poly{degree})"
            cls.plot_polyfit_overlay(ax, series, plot_title, degree=degree)
        fig.tight_layout()
        plt.savefig(output_path, dpi=300)

    @classmethod
    def run_polyfit_extrema_overlay(
        cls,
        data_paths: tuple[str, ...] = ("data1.csv", "data2.csv"),
        output_path: str = "overlay_polyfit_extrema.png",
        degree: int = 4,
    ) -> None:
        series_list = [cls.read_even_lines(path) for path in data_paths]
        fig_height = 4 * len(data_paths)
        fig, axes = plt.subplots(nrows=len(data_paths), ncols=1, figsize=(10, fig_height))
        if len(data_paths) == 1:
            axes = [axes]
        for ax, series, title in zip(axes, series_list, data_paths):
            plot_title = f"{title} (poly{degree} extrema)"
            cls.plot_polyfit_extrema_overlay(ax, series, plot_title, degree=degree)
        fig.tight_layout()
        plt.savefig(output_path, dpi=300)


def main() -> None:
    HU.run()
    HU.run_polyfit_overlay(degree=4)
    HU.run_polyfit_extrema_overlay(degree=4)


if __name__ == "__main__":
    main()
