from helpers.vec2 import Vec2D
from config import HEIGHT, WIDTH

import random
import math
import pygame

class Entity:
    def __init__(self, pos: Vec2D, params:dict):
        self.pos = pos
        angle = random.random()* 2 * math.pi
        self.vel = Vec2D(math.cos(angle), math.sin(angle))
        self.vel = self.vel * (params.get('max_speed', 2) * 0.5)
        self.acc = Vec2D(0,0)  # acceleration
        self.params = params

    def update(self, dt, world):
        # integrate
        self.vel = (self.vel + self.acc).limit(self.params["max_speed"])
        if self.vel.mod() < 1e-3:
            angle = random.uniform(0, 2*math.pi)
            self.vel = Vec2D(math.cos(angle), math.sin(angle)) * 0.1
        self.pos = self.pos + self.vel * dt
        self.acc = Vec2D(0,0)
        self.wrap_position()

    def apply_force(self, force: Vec2D):
        self.acc = self.acc + force

    def wrap_position(self):
        # toroidal world (wrap-around)
        if self.pos.x < 0: self.pos.x += WIDTH
        if self.pos.x >= WIDTH: self.pos.x -= WIDTH
        if self.pos.y < 0: self.pos.y += HEIGHT
        if self.pos.y >= HEIGHT: self.pos.y -= HEIGHT

    def vec_to(self, other_pos: Vec2D) -> Vec2D:
        dx = other_pos.x - self.pos.x
        dy = other_pos.y - self.pos.y
        # handle wrap
        if dx > WIDTH/2: dx -= WIDTH
        if dx < -WIDTH/2: dx += WIDTH
        if dy > HEIGHT/2: dy -= HEIGHT
        if dy < -HEIGHT/2: dy += HEIGHT
        return Vec2D(dx, dy)

    def distance_to(self, other_pos: Vec2D) -> float:
        return self.vec_to(other_pos).mod()
    
    def visible_neighbors(self, world, species_type: type, radius=None, angle=None):
        if radius is None: radius = self.params["vision"]
        if angle is None: angle = self.params.get("vision_angle", math.pi)
        neighbors = []
        for e in world.entities:
            if not isinstance(e, species_type) or e is self:
                continue
            d = self.distance_to(e.pos)
            if d > radius: continue
            # check angle
            forward = self.vel.normalize()
            to_e = self.vec_to(e.pos).normalize()
            if forward.mod() == 0 or to_e.mod() == 0:
                neighbors.append((e, d))
            else:
                a = math.acos(max(-1, min(1, forward.x*to_e.x + forward.y*to_e.y)))
                if a <= angle/2:
                    neighbors.append((e, d))
        return neighbors
    
    def draw(self, screen):
        # default draw as circle
        pygame.draw.circle(screen, (255,255,255), (int(self.pos.x), int(self.pos.y)), 4)