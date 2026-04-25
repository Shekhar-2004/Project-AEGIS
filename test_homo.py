import numpy as np

H = np.array([
    [ 9.45427428e-02 , 7.55234019e-02 ,-4.35775569e+01],
    [-2.45049372e-03 ,-1.09632958e-01 , 6.27198541e+01],
    [ 4.17822571e-04 , 2.63988402e-02 , 1.00000000e+00],
])

def project(point):
    x, y = point
    p = np.array([x, y, 1.0])
    p_t = H @ p
    p_t /= p_t[2]
    return p_t[:2]

# test points
points = [
    (1000, 1500),  # near
    (1500, 1000),  # mid
    (2000, 500)    # far
]

for p in points:
    print(p, "→", project(p))