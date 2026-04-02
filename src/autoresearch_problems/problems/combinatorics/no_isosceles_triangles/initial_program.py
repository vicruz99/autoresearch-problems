"""Initial solution for No Isosceles Triangles: a small valid set."""


def solve() -> list:
    """Return a small set of grid points with no isosceles triangle."""
    # EVOLVE-BLOCK-START
    # Points (0,0), (1,0), (0,3): no isosceles triple
    # dist(0,0 -> 1,0)=1, dist(0,0 -> 0,3)=3, dist(1,0 -> 0,3)=sqrt(10)
    # Check ordered triples:
    #   (0,0),(1,0),(0,3): d(a,b)=1, d(b,c)=sqrt(10) -- ok
    #   (0,0),(0,3),(1,0): d(a,b)=3, d(b,c)=sqrt(10) -- ok
    #   (1,0),(0,0),(0,3): d(a,b)=1, d(b,c)=3 -- ok
    #   (1,0),(0,3),(0,0): d(a,b)=sqrt(10), d(b,c)=3 -- ok
    #   (0,3),(0,0),(1,0): d(a,b)=3, d(b,c)=1 -- ok
    #   (0,3),(1,0),(0,0): d(a,b)=sqrt(10), d(b,c)=1 -- ok
    return [(0, 0), (1, 0), (0, 3)]
    # EVOLVE-BLOCK-END
