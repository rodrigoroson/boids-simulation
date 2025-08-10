from entity import Entity
from config import PREDATOR_PARAMS
from helpers.vec2 import Vec2D

import random
import pygame

class Predator(Entity):
    def __init__(self, pos):
        super().__init__(pos, PREDATOR_PARAMS)
        self.color = PREDATOR_PARAMS["color"]

    def update(self, dt, world):
        # chase nearest in vision
        from species.prey import Prey
        prey_seen = [(e, self.distance_to(e.pos)) for e in world.entities if isinstance(e, Prey)]
        target = None
        min_d = 1e8
        for e, d in prey_seen:
            if d < min_d and d <= self.params["vision"]:
                min_d = d; target = e

        if target:
            chase = self.vec_to(target.pos).normalize() * self.params["max_speed"] - self.vel
            chase = chase.limit(self.params["max_force"]) * self.params["chase_weight"]
            self.apply_force(chase)
        else:
            # wander: small random steer
            wander = Vec2D(random.uniform(-1,1), random.uniform(-1,1)).normalize() * self.params["max_speed"] - self.vel
            wander = wander.limit(self.params["max_force"]) * self.params["wander_weight"]
            self.apply_force(wander)

        # separation from other predators
        sep = Vec2D(0,0); cnt = 0
        for e in world.entities:
            if isinstance(e, Predator) and e is not self:
                d = self.distance_to(e.pos)
                if d < 30 and d>0:
                    sep = sep + (self.vec_to(e.pos) * -1) / (d*d)
                    cnt += 1
        if cnt>0:
            sep = (sep / cnt).normalize() * self.params["max_speed"] - self.vel
            sep = (sep * self.params["sep_weight"]).limit(self.params["max_force"])
            self.apply_force(sep)

        super().update(dt, world)

    def draw(self, screen):
        r = 7
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), r)