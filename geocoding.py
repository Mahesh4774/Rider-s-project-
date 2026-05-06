import requests
import polyline

from config import API_KEY

def geocode(address):
    url = f"https://api.openrouteservice.org/geocode/search?api_key={API_KEY}&text={address}"
    response = requests.get(url)
    data = response.json()
    coords = data['features'][0]['geometry']['coordinates'] # this cords is in long, lat format
    return coords[1],coords[0]

def get_midpoint_routes(start_location,end_location):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization" : API_KEY,"Content-type" : "application/json"}
    body = {"coordinates" : [
                             [start_location[1],start_location[0]],
                             [end_location[1],end_location[0]]
                            ]
        ,"geometry_simplify" : False
           }
    response = requests.post(url, json=body,headers=headers)
    data = response.json()
    # print(data) terminal log
    encoded_routes = data["routes"][0]["geometry"]
    decoded_routes  = polyline.decode(encoded_routes)
    return decoded_routes


def get_elevation(route):
    url = "https://api.open-elevation.com/api/v1/lookup"
    locations = []
    for points in route:
        locations.append({"latitude":points[0],"longitude":points[1]})
    body = {"locations":locations}
    response = requests.post(url, json=body)
    data = response.json()
    return data["results"]
