from geometry import circle_radius, distance_m, find_point_at_distance,turn_direction
from config import (
    TWIST_RADIUS_THRESHOLD,
    WINDOW_DIST_M,
    MIN_GROUP_LENGTH_M,
    MIN_SCORE_THRESHOLD,
    RHYTHM_MULTIPLIER
)

def classify_segments(route,gradients):
    segments = []

    for i in range(len(route)):
        p1 = route[i]

        p0 = find_point_at_distance(route, i, WINDOW_DIST_M, -1)
        p2 = find_point_at_distance(route, i, WINDOW_DIST_M, +1)

        if p0 is None or p2 is None:
            continue

        radius = circle_radius(p0, p1, p2)

        seg_type = "twisties" if radius < TWIST_RADIUS_THRESHOLD else "straight"

        direction = turn_direction(p0,p1,p2)

        segments.append({
            "p0": p0,
            "p1": p1,
            "p2": p2,
            "radius": radius,
            "type": seg_type,
            "direction":direction,
            "gradients": gradients[i] if i < len(gradients) else 0
        })
    return segments

def total_route_length(route):
    return sum(
        distance_m(route[i], route[i + 1])
        for i in range(len(route) - 1)
    )

def find_twisty_groups(segments):
    twisty_group = []
    current_group = []
    current_direction = []
    current_length = 0.0
    curvature_sum = 0.0
    prev_direction = None
    direction_changes = 0
    gradient_sum = 0.0

    for i in range(1, len(segments)):
        seg = segments[i]
        if seg["type"] == "twisties":
            if segments[i - 1]["type"] == "twisties":
                prev_point = segments[i - 1]["p1"]
                curr_point = segments[i]["p1"]
                current_length += distance_m(prev_point, curr_point)
            curvature_sum += 1 / seg["radius"]
            current_group.append(seg["p1"])
            direction = seg["direction"]
            gradient_sum += seg["gradients"]
            current_direction.append(direction)
            if prev_direction is not None and direction != prev_direction:
                direction_changes += 1
            prev_direction = direction


        else:
            if current_length >= MIN_GROUP_LENGTH_M:

                twist_score = curvature_sum * current_length
                rhythm_bonus = direction_changes * RHYTHM_MULTIPLIER
                avg_gradient = gradient_sum / len(current_group) if current_group else 0
                gradient_bonus = avg_gradient * 0.5  # tune this
                twist_score = twist_score + rhythm_bonus + gradient_bonus


                if twist_score >= MIN_SCORE_THRESHOLD:
                    twisty_group.append({
                        "points": current_group,
                        "score": twist_score,
                        "direction":current_direction,
                        "direction_changes":direction_changes
                    })

            current_group = []
            current_direction = []
            current_length = 0.0
            curvature_sum = 0.0
            prev_direction = None
            direction_changes = 0
            gradient_sum = 0.0

    # final group at the end of the loop
    if current_length >= MIN_GROUP_LENGTH_M:
        twist_score = curvature_sum * current_length
        rhythm_bonus = direction_changes * RHYTHM_MULTIPLIER
        avg_gradient = gradient_sum / len(current_group) if current_group else 0
        gradient_bonus = avg_gradient * 0.5  # tune this
        twist_score = twist_score + rhythm_bonus + gradient_bonus

        if twist_score >= MIN_SCORE_THRESHOLD:
            twisty_group.append({
                "points": current_group,
                "score": twist_score,
                "direction":current_direction,
                "direction_changes":direction_changes
            })

    return twisty_group

def find_rhythm_sections(twisty_group):

    if twisty_group["direction_changes"] >= 2:
        return twisty_group["points"]  # whole group is a rhythm section
    return []

def calculate_gradient(route,elevation):
    gradient = []
    for i in range(len(elevation)-1):

        elev1 = elevation[i]["elevation"]
        elev2 = elevation[i+1]["elevation"]
        dist = distance_m(route[i],route[i+1])
        if dist == 0:
            gradient.append(0)
            continue
        raw = (elev2 - elev1) / dist * 100
        gradient.append(max(-30, min(30, raw)))
    return gradient


