import math

WIDTH, HEIGHT = 1000, 700
BG_COLOR = (10, 10, 20)

# Species params (tune these)
PREY_PARAMS = {
    "color": (120, 200, 255),
    "max_speed": 3,
    "max_force": 2,
    "vision": 80,
    "vision_angle": math.pi * 1.0,
    "sep_weight": 1.6,
    "align_weight": 1.5,
    "cohesion_weight": 2,
    "flee_weight": 2,
}

PREDATOR_PARAMS = {
    "color": (255, 100, 100),
    "max_speed": 3.0,
    "max_force": 0.09,
    "vision": 200,
    "vision_angle": math.pi,
    "sep_weight": 1.4,
    "chase_weight": 1.6,
    "wander_weight": 0.6,
}