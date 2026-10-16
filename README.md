Laboratory Work No. 4 — Computational Geometry
Methods for Determining the Position of a Point Relative to a Polygon

Author: Ayoub ELHARFA
Course: Computational Geometry
Laboratory Work: No. 4

1. Project Description

This project implements and compares two computational geometry algorithms used to determine the position of a point relative to a polygon.

The program classifies a point into one of three categories:

INSIDE — the point is inside the polygon.
OUTSIDE — the point is outside the polygon.
BOUNDARY — the point lies on an edge or vertex of the polygon.

The project also includes basic geometric operations, segment intersection tests, visualization, and performance measurements.

2. Algorithms Implemented
Ray Casting Method

The Ray Casting algorithm draws a horizontal ray from the test point and counts its intersections with the polygon boundary.

An odd number of intersections indicates that the point is inside.
An even number indicates that the point is outside.
Boundary points are detected separately.

This method works with simple convex and concave polygons.

Half-Plane Method

The half-plane method uses the cross product to determine the orientation of a point relative to each polygon edge.

For a convex polygon, consistent nonzero orientation signs indicate an interior point. If both positive and negative signs occur, the point is outside.

This method is intended for convex polygons.

3. Project Structure
File	Description
geometry.py	Point representation and basic geometric operations
algorithms.py	Ray Casting and half-plane algorithms
tests.py	Functional tests and performance experiments
visualization.py	Polygon and test-point visualization
README.md	Project documentation
4. Requirements
Python 3.8 or newer
Matplotlib
5. Installation

Clone the repository:

git clone https://github.com/YOUBY-25/computational-geometry-lab4.git
cd computational-geometry-lab4


Install Matplotlib:

python -m pip install matplotlib

6. How to Run

Run the geometric operations:

python geometry.py


Run the algorithm tests and performance experiment:

python tests.py


Display the visualizations:

python visualization.py

7. Testing

The project tests the following cases:

Intersecting segments
Segments touching at endpoints
Collinear overlapping segments
Parallel non-intersecting segments
Points inside and outside polygons
Points on polygon edges and vertices
Ray crossings at polygon vertex heights
Convexity requirements of the half-plane method
8. Performance Analysis

Both algorithms have O(n) time complexity per point query, where n is the number of polygon vertices.

Their additional working memory is O(1).

The performance experiment compares execution times for polygons with different numbers of vertices, using the same number of point queries for each size.

Actual measurements should be obtained by running tests.py.

9. Conclusion

This project demonstrates two approaches to the point-in-polygon problem.

Ray Casting is applicable to simple convex and concave polygons. The half-plane method is simpler but requires a convex polygon.

The laboratory work provides practical experience with geometric predicates, boundary handling, algorithm testing, visualization, and performance analysis in Python.

GitHub: YOUBY-25

Repository: computational-geometry-lab4
