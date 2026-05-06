import folium

from config import LOW_SCORE_THRESHOLD, HIGH_SCORE_THRESHOLD


def draw_map(route, twisty_groups, rhythm_points, output_path="route_map2.html"):
    starting_point = route[0]
    m = folium.Map(location=starting_point, zoom_start=14, tiles="CartoDB positron")

    # Full route in green
    folium.PolyLine(route, color="green", weight=5, opacity=0.6).add_to(m)

    # Twisty groups colored by score
    for twist in twisty_groups:
        points = twist["points"]
        score = twist["score"]

        if len(points) >= 2:
                if score >= HIGH_SCORE_THRESHOLD:
                    color = "darkred"
                elif score >= LOW_SCORE_THRESHOLD:
                    color = "red"
                else:
                    color = "orange"

                folium.PolyLine(points, color=color, weight=6).add_to(m)


    for p in rhythm_points:
        folium.CircleMarker(location=p,radius=6,color="blue",fill=True,popup="RhythmSection!!").add_to(m)


    folium.Marker(route[0], popup="Start").add_to(m)
    folium.Marker(route[-1], popup="End").add_to(m)

    m.save(output_path)