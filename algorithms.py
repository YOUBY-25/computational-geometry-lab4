
"""Point-in-polygon algorithms."""

from geometry import Point, EPS, orientation, on_segment


def validate_polygon(polygon):
    """Check polygon size and reject zero-length edges."""
    if len(polygon) < 3:
        raise ValueError("A polygon needs at least 3 vertices.")

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]

        if (
            abs(a.x - b.x) <= EPS
            and abs(a.y - b.y) <= EPS
        ):
            raise ValueError("Polygon has a zero-length edge.")


def is_convex(polygon):
    """Return True if a polygon has consistent nonzero turns."""
    if len(polygon) < 3:
        return False

    signs = []

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]
        c = polygon[(i + 2) % len(polygon)]

        value = orientation(a, b, c)

        if value > EPS:
            signs.append(1)
        elif value < -EPS:
            signs.append(-1)

    return bool(signs) and all(
        sign == signs[0] for sign in signs
    )


def point_in_polygon_ray(point, polygon):
    """Classify a point using horizontal Ray Casting."""
    validate_polygon(polygon)

    inside = False
    n = len(polygon)

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        # Check the boundary before counting intersections.
        if on_segment(a, point, b):
            return "BOUNDARY"

        # The half-open rule avoids double-counting vertices.
        if (a.y > point.y) != (b.y > point.y):
            x_cross = (
                a.x
                + (point.y - a.y)
                * (b.x - a.x)
                / (b.y - a.y)
            )

            if x_cross > point.x:
                inside = not inside

    return "INSIDE" if inside else "OUTSIDE"


def point_in_convex_polygon(point, polygon):
    """Classify a point using the half-plane method.

    The polygon must be convex.
    """
    validate_polygon(polygon)

    if not is_convex(polygon):
        raise ValueError(
            "The half-plane method requires a convex polygon."
        )

    has_positive = False
    has_negative = False

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]

        value = orientation(a, b, point)

        if abs(value) <= EPS and on_segment(a, point, b):
            return "BOUNDARY"

        if value > EPS:
            has_positive = True
        elif value < -EPS:
            has_negative = True

        if has_positive and has_negative:
            return "OUTSIDE"

    return "INSIDE"


if __name__ == "__main__":
    triangle = [
        Point(0, 0),
        Point(4, 0),
        Point(2, 3),
    ]

    print("Triangle convex:", is_convex(triangle))
    print(
        "Ray Casting:",
        point_in_polygon_ray(Point(2, 1), triangle)
    )
    print(
        "Half-plane:",
        point_in_convex_polygon(Point(2, 1), triangle)
    )
