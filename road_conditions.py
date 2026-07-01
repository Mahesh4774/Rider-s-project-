import requests
from geometry import distance_m
from rtree import index

SURFACE_SCORES = {
    "asphalt": 1.0,
    "paved": 0.7,
    "concrete": 0.55,
    "gravel": 0.3,
    "dirt": 0.1,
    "unpaved": 0.1,
}

SMOOTHNESS_SCORES = {
    "excellent": 1.0,
    "good": 0.8,
    "intermediate": 0.6,
    "bad": 0.3,
    "horrible": 0.1,
}

def get_bounding_box(route):
    lats = [p[0] for p in route]
    lons = [p[1] for p in route]
    return min(lats), min(lons), max(lats), max(lons)

def query_overpass_bbox(south, west, north, east):
    query = f"""
    [out:json][timeout:25];
    way["highway"]["surface"]({south},{west},{north},{east});
    out tags geom;
    """
    headers = {"User-Agent": "MischiefApp/1.0"}
    servers = [
        "https://overpass-api.de/api/interpreter",
        "https://lz4.overpass-api.de/api/interpreter",
        "https://z.overpass-api.de/api/interpreter",
    ]
    for server in servers:
        try:
            response = requests.get(server, params={"data": query}, headers=headers, timeout=25)
            if response.status_code == 200:
                return response.json()
            print(f"{response.status_code} from {server}, trying next...")
        except requests.exceptions.Timeout:
            print(f"Timeout on {server}, trying next...")
        except Exception as e:
            print(f"Error: {e}, trying next...")
    return {"elements": []}

def fetch_road_elements(route):
    south, west, north, east = get_bounding_box(route)
    data = query_overpass_bbox(south, west, north, east)
    return data.get("elements", [])

def build_spatial_index(elements):
    idx = index.Index()
    node_map = {}
    i = 0
    for element in elements:
        for node in element.get("geometry", []):
            idx.insert(i, (node["lat"], node["lon"], node["lat"], node["lon"]))
            node_map[i] = element
            i += 1
    return idx, node_map

def find_closest_element(route_point, idx, node_map):
    nearest = list(idx.nearest((route_point[0], route_point[1], route_point[0], route_point[1]), 1))
    if not nearest:
        return None, float("inf")
    closest_element = node_map[nearest[0]]
    # calculate actual distance
    geom = closest_element.get("geometry", [])
    best_dist = float("inf")
    for node in geom:
        d = distance_m(route_point, (node["lat"], node["lon"]))
        if d < best_dist:
            best_dist = d
    return closest_element, best_dist

def score_tags(tags):
    scores = []
    if "surface" in tags:
        s = SURFACE_SCORES.get(tags["surface"])
        if s is not None:
            scores.append(s)
    if "smoothness" in tags:
        s = SMOOTHNESS_SCORES.get(tags["smoothness"])
        if s is not None:
            scores.append(s)
    return sum(scores) / len(scores) if scores else None

def score_section(idx, node_map, section_points, max_snap_dist=50):
    scores = []
    for point in section_points:
        closest, dist = find_closest_element(point, idx, node_map)
        if closest and dist <= max_snap_dist:
            score = score_tags(closest.get("tags", {}))
            if score is not None:
                scores.append(score)
    return sum(scores) / len(scores) if scores else None