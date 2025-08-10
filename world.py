from typing import List
import random
import pygame

from helpers.vec2 import Vec2D
from entity import Entity
from config import WIDTH, HEIGHT
from species.predator import Predator
from species.prey import Prey

class World:
    def __init__(self):
        self.entities: List[Entity] = []

    def populate(self, n_prey=60, n_pred=6):
        for _ in range(n_prey):
            p = Prey(Vec2D(random.uniform(0, WIDTH),
                           random.uniform(0, HEIGHT)))
            self.entities.append(p)
        for _ in range(n_pred):
            p = Predator(Vec2D(random.uniform(0, WIDTH),
                               random.uniform(0, HEIGHT)))
            self.entities.append(p)

    def update(self, dt):
        # update entities
        for e in self.entities:
            e.update(dt, self)

    def draw(self, screen):
        # draw entities
        for e in self.entities:
            e.draw(screen)
