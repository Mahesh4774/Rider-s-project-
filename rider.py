from geocoding import geocode, get_midpoint_routes, get_elevation

from analysis import classify_segments, find_twisty_groups, total_route_length, find_rhythm_sections, calculate_gradient

from mapping import draw_map

from road_conditions import fetch_road_elements
from road_conditions import score_section

def analyze_route(current_location, destination):
    cur_loc_send = current_location + ",kerala"
    des_send = destination + ",kerala"

    start_location = geocode(cur_loc_send)
    end_location = geocode(des_send)
    route = get_midpoint_routes(start_location, end_location)

    elevation = get_elevation(route)
    gradients = calculate_gradient(route, elevation)

    segments = classify_segments(route, gradients)

    elements = fetch_road_elements(route)  # one API call

    print(f"Elements fetched: {len(elements)}")
    twisty_group = find_twisty_groups(segments,elements)

    rhythm_points = []
    for group in twisty_group:
        rhythm_points.extend(find_rhythm_sections(group))

    total_length_m = total_route_length(route)
    total_route_km = total_length_m / 1000


    draw_map(route, twisty_group, rhythm_points)

    return {
        "route": route,
        "twisty_groups": twisty_group,
        "rhythm_points": rhythm_points,
        "total_km": total_route_km,
    }
if __name__ == "__main__":
    current_location = input("Enter your current location... ")
    destination = input("Enter the destination that you want to travel to...")
    result = analyze_route(current_location, destination)
    print(f"\nTotal distance = {result['total_km']:.2f} km")
    print(f"Twisty groups found: {len(result['twisty_groups'])}")
    from road_conditions import score_section, fetch_road_elements

    elements = fetch_road_elements(result['route'])
    for i, group in enumerate(result['twisty_groups']):
        print(f"Group {i + 1}: score={group['score']:.2f}, road_condition={group.get('road_conditions')}")


# Work with real or longer routes
#
# Instead of 4 points, take a real GPS route (e.g., 50–100 points).
#
# Calculate all segments and classify them as twisty/straight.
#
# Store them in your segments list (JSON-like structure).
#
# ✅ Goal: Your code should work for any number of points automatically.