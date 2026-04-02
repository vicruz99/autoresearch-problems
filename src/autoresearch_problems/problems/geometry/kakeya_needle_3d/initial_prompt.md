SETTING:
You are an expert in geometric measure theory and computational geometry, working on the 3D Kakeya needle problem.

PROBLEM CONTEXT:
The Kakeya needle problem asks: what is the minimum volume of a 3D set in which a unit needle (line segment of length 1) can be rotated to point in every direction?

In this discrete version, we work with n² tubes: for direction indices i,j in {0,...,n-1}, tube T_{ij} is a unit square cross-section prism connecting position (x_{i*n+j}, y_{i*n+j}) at z=0 to shifted position at z=1. The direction of tube T_{ij} is determined by (i/n, j/n) offsets.

Your task: find the n² positions (x_k, y_k) for k=0,...,n²-1 that minimise the total volume of the union of these tubes.

PERFORMANCE METRICS:
1. **volume**: Monte Carlo estimate of union volume (PRIMARY — minimise)
2. **score**: -(volume / reference_volume) — higher (less negative) is better

Your `solve(n)` function must return a numpy array of shape (n*n, 2) where each row is the (x, y) position of a tube.
