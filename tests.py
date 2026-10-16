
"""Tests and performance experiment for Laboratory Work No. 4."""

import math
import random
import time

from geometry import (
    Point,
    orientation,
    on_segment,
    segments_intersect,
    line_intersection,
)
from algorithms import (
    is_convex,
    point_in_polygon_ray,
    point_in_convex_polygon,
)


# Source polygon for Task 2: Ray Casting.
RAY_POLYGON = [
    Point(19, -53),
    Point(54, -78),
    Point(82, -94),
    Point(95, -25),
    Point(61, 19),
    Point(69, 75),
    Point(26, 59),
    Point(-90, 89),
    Point(-26, 15),
    Point(-77, 33),
    Point(-66, -45),
]


# Source polygon for Task 3: half-plane method.
CONVEX_POLYGON = [
    Point(19, -105),
    Point(54, -101),
    Point(82, -94),
    Point(95, -25),
    Point(95, 19),
    Point(69, 75),
    Point(26, 95),
    Point(-90, 89),
    Point(-90, 50),
    Point(-85, 33),
    Point(-66, -45),
]


def test_geometry():
    """Test the four required segment configurations."""
    print("\n=== TASK 1: GEOMETRIC OPERATIONS ===")

    cases = [
        (
            "Crossing",
            Point(0, 0), Point(6, 6),
            Point(0, 6), Point(6, 0),
            True,
        ),
        (
            "Touching",
            Point(0, 0), Point(4, 0),
            Point(4, 0), Point(7, 3),
            True,
        ),
        (
            "Collinear overlap",
            Point(0, 0), Point(5, 0),
            Point(2, 0), Point(7, 0),
            True,
        ),
        (
            "Parallel separate",
            Point(0, 0), Point(5, 0),
            Point(0, 2), Point(5, 2),
            False,
        ),
    ]

    for name, a, b, c, d, expected in cases:
        actual = segments_intersect(a, b, c, d)
        status = "PASS" if actual == expected else "FAIL"
        print(f"{name:20} {actual!s:6} {status}")

        if name == "Crossing":
            print("Intersection:", line_intersection(a, b, c, d))

    print("Point on segment:", on_segment(
        Point(0, 0), Point(2, 0), Point(5, 0)
    ))
    print("Orientation:", orientation(
        Point(0, 0), Point(4, 0), Point(2, 2)
    ))


def test_ray_casting():
    """Test at least 10 points on the Ray Casting polygon."""
    print("\n=== TASK 2: RAY CASTING ===")

    cases = [
        ("Vertex", Point(19, -53), "BOUNDARY"),
        ("Edge midpoint", Point(36.5, -65.5), "BOUNDARY"),
        ("Far right", Point(200, 200), "OUTSIDE"),
        ("Far left", Point(-200, 0), "OUTSIDE"),
        ("Above polygon", Point(0, 120), "OUTSIDE"),
        ("Below polygon", Point(0, -120), "OUTSIDE"),
        ("Vertex y = 89", Point(0, 89), None),
        ("Vertex y = 59", Point(0, 59), None),
        ("Vertex y = 19", Point(0, 19), None),
        ("Candidate point", Point(0, 20), None),
        ("Candidate point", Point(0, 0), None),
        ("Candidate point", Point(50, 0), None),
    ]

    for name, point, expected in cases:
        actual = point_in_polygon_ray(point, RAY_POLYGON)

        if expected is None:
            status = "RECORDED"
        else:
            status = "PASS" if actual == expected else "FAIL"

        print(
            f"{name:18} point={point!r:28} "
            f"result={actual:8} {status}"
        )


def print_orientation_signs(point, polygon):
    """Print orientation signs for every polygon edge."""
    signs = []

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]
        value = orientation(a, b, point)

        if value > 1e-9:
            signs.append("+")
        elif value < -1e-9:
            signs.append("-")
        else:
            signs.append("0")

    print("Point:", point)
    print("Signs:", " ".join(signs))


def test_half_plane():
    """Test the convex polygon and print orientation signs."""
    print("\n=== TASK 3: HALF-PLANE METHOD ===")
    print("Is source polygon convex:", is_convex(CONVEX_POLYGON))

    cases = [
        ("Vertex", Point(19, -105)),
        ("Edge midpoint", Point(36.5, -103)),
        ("Far outside", Point(200, 200)),
        ("Far left", Point(-200, 0)),
        ("Above polygon", Point(0, 120)),
        ("Candidate point", Point(0, 20)),
    ]

    for name, point in cases:
        result = point_in_convex_polygon(point, CONVEX_POLYGON)

        print(f"\n{name}: {point} -> {result}")
        print_orientation_signs(point, CONVEX_POLYGON)


def test_concave_polygon():
    """Show why the half-plane method requires convexity."""
    print("\n=== CONCAVE POLYGON TEST ===")

    concave = [
        Point(0, 0),
        Point(4, 0),
        Point(4, 4),
        Point(3, 4),
        Point(3, 1),
        Point(1, 1),
        Point(1, 4),
        Point(0, 4),
    ]

    point = Point(2, 3)

    print("Is convex:", is_convex(concave))
    print("Ray Casting:", point_in_polygon_ray(point, concave))

    try:
        result = point_in_convex_polygon(point, concave)
        print("Half-plane:", result)
    except ValueError as error:
        print("Half-plane rejected:", error)


def generate_convex_polygon(n, radius=100.0):
    """Generate a convex polygon using equally spaced circle angles."""
    return [
        Point(
            radius * math.cos(2 * math.pi * i / n),
            radius * math.sin(2 * math.pi * i / n),
        )
        for i in range(n)
    ]


def run_experiment():
    """Measure the runtime of both methods on convex polygons."""
    print("\n=== TASK 4: PERFORMANCE EXPERIMENT ===")

    random.seed(42)
    query_count = 10_000

    print(
        f"{'Vertices':>8} {'Queries':>8} "
        f"{'Ray (s)':>12} {'Half-plane (s)':>16} "
        f"{'Matches':>12}"
    )

    for n in [10, 100, 1000]:
        polygon = generate_convex_polygon(n)

        points = [
            Point(
                random.uniform(-120, 120),
                random.uniform(-120, 120),
            )
            for _ in range(query_count)
        ]

        start = time.perf_counter()
        ray_results = [
            point_in_polygon_ray(point, polygon)
            for point in points
        ]
        ray_time = time.perf_counter() - start

        start = time.perf_counter()
        half_results = [
            point_in_convex_polygon(point, polygon)
            for point in points
        ]
        half_time = time.perf_counter() - start

        matches = sum(
            a == b for a, b in zip(ray_results, half_results)
        )

        print(
            f"{n:8d} {query_count:8d} "
            f"{ray_time:12.4f} {half_time:16.4f} "
            f"{matches:8d}/{query_count}"
        )


if __name__ == "__main__":
    test_geometry()
    test_ray_casting()
    test_half_plane()
    test_concave_polygon()
    run_experiment()
