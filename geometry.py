
"""Basic geometric primitives and operations."""

from dataclasses import dataclass

EPS = 1e-9


@dataclass(frozen=True)
class Point:
    """Represent a point in two-dimensional space."""
    x: float
    y: float


def orientation(a: Point, b: Point, c: Point) -> float:
    """Return the cross product of AB and AC."""
    return (
        (b.x - a.x) * (c.y - a.y)
        - (b.y - a.y) * (c.x - a.x)
    )


def on_segment(a: Point, p: Point, b: Point) -> bool:
    """Return True if p lies on the closed segment AB."""
    if abs(orientation(a, b, p)) > EPS:
        return False

    return (
        min(a.x, b.x) - EPS <= p.x <= max(a.x, b.x) + EPS
        and min(a.y, b.y) - EPS <= p.y <= max(a.y, b.y) + EPS
    )


def segments_intersect(
    a: Point, b: Point, c: Point, d: Point
) -> bool:
    """Check whether closed segments AB and CD intersect."""
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    opposite1 = (
        (o1 > EPS and o2 < -EPS)
        or (o1 < -EPS and o2 > EPS)
    )
    opposite2 = (
        (o3 > EPS and o4 < -EPS)
        or (o3 < -EPS and o4 > EPS)
    )

    if opposite1 and opposite2:
        return True

    return (
        (abs(o1) <= EPS and on_segment(a, c, b))
        or (abs(o2) <= EPS and on_segment(a, d, b))
        or (abs(o3) <= EPS and on_segment(c, a, d))
        or (abs(o4) <= EPS and on_segment(c, b, d))
    )


def line_intersection(
    a: Point, b: Point, c: Point, d: Point
):
    """Return the intersection of lines AB and CD.

    Return None if the lines are parallel or coincident.
    The intersection need not lie on the finite segments.
    """
    dx1 = b.x - a.x
    dy1 = b.y - a.y
    dx2 = d.x - c.x
    dy2 = d.y - c.y

    denominator = dx1 * dy2 - dy1 * dx2

    if abs(denominator) <= EPS:
        return None

    t = (
        (c.x - a.x) * dy2 - (c.y - a.y) * dx2
    ) / denominator

    return Point(
        a.x + t * dx1,
        a.y + t * dy1
    )


if __name__ == "__main__":
    # Test 1: crossing segments
    a, b = Point(0, 0), Point(6, 6)
    c, d = Point(0, 6), Point(6, 0)

    print("Test 1:", segments_intersect(a, b, c, d))
    print("Intersection:", line_intersection(a, b, c, d))

    # Test 2: touching endpoints
    a, b = Point(0, 0), Point(4, 0)
    c, d = Point(4, 0), Point(7, 3)

    print("Test 2:", segments_intersect(a, b, c, d))

    # Test 3: collinear overlapping segments
    a, b = Point(0, 0), Point(5, 0)
    c, d = Point(2, 0), Point(7, 0)

    print("Test 3:", segments_intersect(a, b, c, d))

    # Test 4: parallel, separate segments
    a, b = Point(0, 0), Point(5, 0)
    c, d = Point(0, 2), Point(5, 2)

    print("Test 4:", segments_intersect(a, b, c, d))
