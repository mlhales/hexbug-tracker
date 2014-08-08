__author__ = 'mlh'

import numpy as np
from bug import *


class ParticleFilter():
    """
    ParticleFilter implements the particle filter algorithm
    """

    def __init__(self, world_properties, count=1000):
        x, y = world_properties["centroid"][0]
        bug_size = world_properties["size"]
        self.count = count
        self.particles = []
        Bug.speed_mu = 9.8
        Bug.speed_var = 5
        Bug.speed_max = 15
        Bug.turn_mu = 0.1
        Bug.turn_var = 0.5
        Bug.turn_max = math.pi / 2
        for i in range(count):
            self.particles.append(Bug(x, y, bug_size))

    def sense(self, x, y):
        if x > 0 and y > 0:
            probability = []
            p1 = []
            for particle in self.particles:
                prob, new_particle = particle.measurement_prob(x, y)
                p1.append(new_particle)
                probability.append(prob)

            p2 = []
            index = int(random.random() * self.count)
            beta = 0.0
            max_prob = max(probability)
            for i in range(self.count):
                beta += random.random() * 2.0 * max_prob
                while beta > probability[index]:
                    beta -= probability[index]
                    index = (index + 1) % self.count
                p2.append(p1[index].clone())
            self.particles = p2
        else:
            p1 = []
            for particle in self.particles:
                p1.append(particle.random_move())
            self.particles = p1

    def best(self):
        return max(self.particles)