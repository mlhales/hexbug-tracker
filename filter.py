__author__ = 'mlh'

import numpy as np
from bug import *


class ParticleFilter():
    """
    ParticleFilter implements the particle filter algorithm
    """

    def __init__(self, bounds, size, count=1000):
        self.count = count
        self.particles = []
        for i in range(count):
            # todo instantiate the bugs based on the bounds
            self.particles.append(Bug(x, y, size))

    def sense(self, x, y):
        probability = []
        for particle in self.particles:
            particle.predict()
            probability.append(particle.measurement_prob(x, y))

        new_population = []
        index = int(random.random() * self.count)
        beta = 0.0
        max_prob = max(probability)
        for i in range(self.count):
            beta += random.random() * 2.0 * max_prob
            while beta > max_prob[index]:
                beta -= max_prob[index]
                index = (index + 1) % self.count
            new_population.append(self.population[index].copy())
        self.particles = new_population

    def best(self):
        # todo actually find the best particle.
        return self.particles[0]