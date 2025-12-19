from pathlib import Path

import matplotlib.pyplot as plt


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
            ax.plot(x, values, color="tab:blue", alpha=0.15, linewidth=0.8)
        ax.set_title(title)
        ax.set_xlabel("Index")
        ax.set_ylabel("8-bit brightness")
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


def main() -> None:
    HU.run()


if __name__ == "__main__":
    main()
