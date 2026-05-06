import math

from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)


def to_xy(lat, lon):
    x, y = transformer.transform(lon, lat)
    return x, y

def circle_radius(p1, p2, p3):
    x1, y1 = to_xy(*p1)
    x2, y2 = to_xy(*p2)
    x3, y3 = to_xy(*p3)

    temp = x2**2 + y2**2
    bc = (x1**2 + y1**2 - temp) / 2
    cd = (temp - x3**2 - y3**2) / 2
    det = (x1 - x2)*(y2 - y3) - (x2 - x3)*(y1 - y2)

    if abs(det) < 1e-6:
        return float("inf")

    cx = (bc*(y2 - y3) - cd*(y1 - y2)) / det
    cy = ((x1 - x2)*cd - (x2 - x3)*bc) / det

    return math.sqrt((cx - x1)**2 + (cy - y1)**2)



def distance_m(p1, p2):
    x1, y1 = to_xy(p1[0], p1[1])
    x2, y2 = to_xy(p2[0], p2[1])
    return math.hypot(x2 - x1, y2 - y1)



def find_point_at_distance(route, start_index, target_dist_m, direction):
    dist = 0.0
    idx = start_index

    while 0 <= idx + direction < len(route):
        step = distance_m(route[idx], route[idx + direction])
        dist += step
        idx += direction

        if dist >= target_dist_m:
            return route[idx]

    return None


def turn_direction(p1, p2, p3):
    x1, y1 = to_xy(*p1)
    x2, y2 = to_xy(*p2)
    x3, y3 = to_xy(*p3)

    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    if cross > 0:
        return "left"
    elif cross < 0:
        return "right"
    else:
        return "straight"