
"""Visualization for Laboratory Work No. 4."""

import matplotlib.pyplot as plt

from geometry import Point
from algorithms import (
    point_in_polygon_ray,
    point_in_convex_polygon,
)
from tests import RAY_POLYGON, CONVEX_POLYGON


def draw_polygon(polygon, point, title, method="ray"):
    """Draw a polygon, its test point, and the horizontal ray."""
    if method == "ray":
        result = point_in_polygon_ray(point, polygon)
    elif method == "half":
        result = point_in_convex_polygon(point, polygon)
    else:
        raise ValueError("Method must be 'ray' or 'half'.")

    x_values = [p.x for p in polygon] + [polygon[0].x]
    y_values = [p.y for p in polygon] + [polygon[0].y]

    colors = {
        "INSIDE": "green",
        "OUTSIDE": "red",
        "BOUNDARY": "orange",
    }

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.fill(
        x_values,
        y_values,
        color="lightblue",
        alpha=0.35,
        label="Polygon interior",
    )

    ax.plot(
        x_values,
        y_values,
        color="navy",
        marker="o",
        markersize=4,
        label="Polygon boundary",
    )

    ax.scatter(
        point.x,
        point.y,
        color=colors[result],
        s=100,
        zorder=5,
        label=f"Test point: {result}",
    )

    ax.annotate(
        f"{result} ({point.x}, {point.y})",
        (point.x, point.y),
        xytext=(8, 8),
        textcoords="offset points",
    )

    if method == "ray":
        min_x = min(p.x for p in polygon)
        max_x = max(p.x for p in polygon)
        ray_end = max_x + 0.15 * (max_x - min_x)

        ax.annotate(
            "",
            xy=(ray_end, point.y),
            xytext=(point.x, point.y),
            arrowprops={
                "arrowstyle": "->",
                "color": "darkorange",
                "linewidth": 2,
            },
        )

        ax.plot(
            [],
            [],
            color="darkorange",
            label="Horizontal ray",
        )

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_polygon(
        RAY_POLYGON,
        Point(0, 20),
        "Task 2: Ray Casting",
        method="ray",
    )

    draw_polygon(
        CONVEX_POLYGON,
        Point(0, 20),
        "Task 3: Half-plane method",
        method="half",
    )

    # Boundary example for Ray Casting.
    draw_polygon(
        RAY_POLYGON,
        Point(19, -53),
        "Boundary example: Ray Casting",
        method="ray",
    )
