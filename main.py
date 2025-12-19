from pathlib import Path

import matplotlib.pyplot as plt


def read_even_lines(path: str) -> list[list[float]]:
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


def plot_overlay(ax: plt.Axes, series: list[list[float]], title: str) -> None:
    for values in series:
        x = range(len(values))
        ax.plot(x, values, color="tab:blue", alpha=0.15, linewidth=0.8)
    ax.set_title(title)
    ax.set_xlabel("Index")
    ax.set_ylabel("8-bit brightness")
    ax.grid(True, alpha=0.2)


def main() -> None:
    data1 = read_even_lines("data1.csv")
    data2 = read_even_lines("data2.csv")

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
    plot_overlay(axes[0], data1, "data1.csv")
    plot_overlay(axes[1], data2, "data2.csv")

    fig.tight_layout()
    plt.savefig("overlay_plots.png", dpi=300)


if __name__ == "__main__":
    main()
