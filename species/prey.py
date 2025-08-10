from entity import Entity
from config import PREY_PARAMS
from helpers.vec2 import Vec2D

import math
import pygame

class Prey(Entity):
    def __init__(self, pos):
        super().__init__(pos, PREY_PARAMS)
        self.color = PREY_PARAMS['color']

    def update(self, dt, world):
        # compute boid rules
        sep = Vec2D(0,0)
        align = Vec2D(0,0)
        coh = Vec2D(0,0)
        total = 0
        neighbors = self.visible_neighbors(world, Prey)

        for (other, d) in neighbors:
            diff = self.vec_to(other.pos) * -1
            if d > 0.01:
                sep = sep + (diff / (d*d))  # weighted
            align = align + other.vel
            coh = coh + other.pos
            total += 1
            
        if total > 0:
            # separation
            sep_dir = (sep / total).safe_normalize()
            if sep_dir.mod() > 0:
                sep = sep_dir * self.params["max_speed"] - self.vel
                sep = sep.limit(self.params["max_force"]) * self.params["sep_weight"]
            else:
                sep = Vec2D(0, 0)
            # alignment
            align_dir = (align / total).safe_normalize()
            if align_dir.mod() > 0:
                align = align_dir * self.params["max_speed"] - self.vel
                align = align.limit(self.params["max_force"]) * self.params["sep_weight"]
            else:
                align = Vec2D(0, 0)
            # cohesion
            coh_dir = (coh / total).safe_normalize()
            if coh_dir.mod() > 0:
                coh = coh_dir * self.params["max_speed"] - self.vel
                coh = coh.limit(self.params["max_force"]) * self.params["sep_weight"]
            else:
                coh = Vec2D(0, 0)





            """"
            sep = (sep / total).normalize() * self.params["max_speed"] - self.vel
            sep = (sep * self.params["sep_weight"]).limit(self.params["max_force"])
            # alignment
            align = (align / total).normalize() * self.params["max_speed"] - self.vel
            align = align.limit(self.params["max_force"]) * self.params["align_weight"]
            # cohesion
            coh = (coh / total)
            to_center = self.vec_to(coh).normalize() * self.params["max_speed"] - self.vel
            coh = to_center.limit(self.params["max_force"]) * self.params["cohesion_weight"]"""
        else:
            sep = Vec2D(0,0); align = Vec2D(0,0); coh = Vec2D(0,0)

        # flee from nearby predators
        from species.predator import Predator
        flee = Vec2D(0,0)
        for (pred, d) in self.visible_neighbors(world, Predator, radius=PREY_PARAMS["vision"]*1.5):
            away = self.vec_to(pred.pos) * -1
            if d > 0:
                flee = flee + (away / (d*d))
        if flee.mod() > 0:
            flee = flee.normalize() * self.params["max_speed"] - self.vel
            flee = flee.limit(self.params["max_force"]) * self.params["flee_weight"]

        # combine forces (tweak weights above)
        total_force = sep + align + coh + flee
        total_force = total_force.limit(self.params["max_force"])
        self.apply_force(total_force)

        super().update(dt, world)

    def draw(self, screen):
        # triangle pointing in direction of velocity
        dir_norm = self.vel.normalize()
        angle = math.atan2(dir_norm.y, dir_norm.x)
        p1 = (self.pos.x + math.cos(angle)*8, self.pos.y + math.sin(angle)*8)
        p2 = (self.pos.x + math.cos(angle+2.5)*6, self.pos.y + math.sin(angle+2.5)*6)
        p3 = (self.pos.x + math.cos(angle-2.5)*6, self.pos.y + math.sin(angle-2.5)*6)
        pygame.draw.polygon(screen, self.color, [p1,p2,p3])