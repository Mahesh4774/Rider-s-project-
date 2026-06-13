from road_conditions import get_road_conditions

# Munnar route - a few points you know well
test_route = [
    (10.0889, 77.0595),
    (10.0950, 77.0650),
    (10.1020, 77.0700),
    (10.1100, 77.0750),
    (10.1200, 77.0800),
]

score = get_road_conditions(test_route)
print(f"Road condition score: {score}")