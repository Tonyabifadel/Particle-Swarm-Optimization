import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math
from tqdm import tqdm

class Particle:
    def __init__(self, num_variables, bounds):
        self.position = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(num_variables)]
        self.velocity = [random.uniform(-1, 1) for _ in range(num_variables)]
        self.best_position = self.position[:]
        self.best_fitness = float('inf')

    def evaluate(self):
        x, y = self.position
        fitness = (x - 0.5)**2 + (y - 0.5)**2 # new fitness function 
        return fitness


class PSO:
    def __init__(self, num_particles, num_variables, bounds, max_iterations):
        self.inertia_weight = 0.3
        self.cognitive_weight = 1.2
        self.social_weight = 1.2
        self.num_particles = num_particles
        self.num_variables = num_variables
        self.bounds = bounds
        self.max_iterations = max_iterations
        self.global_best_position = [0.5] * num_variables
        self.global_best_fitness = float('inf')
        self.particles = [Particle(num_variables, bounds) for _ in range(num_particles)]
        self.positions = []  # store positions at each iteration

    def optimize(self):
        for _ in tqdm(range(self.max_iterations)):
            self.positions.append([[particle.position[0], particle.position[1]] for particle in self.particles])
            for particle in self.particles:
                fitness = particle.evaluate()
                if fitness < particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position[:]
                if fitness < self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best_position = particle.position[:]

            for particle in self.particles:
                for i in range(self.num_variables):
                    r1, r2 = random.random(), random.random()
                    particle.velocity[i] = (self.inertia_weight * particle.velocity[i] +
                                            self.cognitive_weight * r1 * (particle.best_position[i] - particle.position[i]) +
                                            self.social_weight * r2 * (self.global_best_position[i] - particle.position[i]))
                    particle.position[i] += particle.velocity[i]

    def animate(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        def update(frame):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            for particle in self.positions[frame]:
                ax.scatter(particle[0], particle[1], c='b')
            ax.scatter(self.global_best_position[0], self.global_best_position[1], c='r')

        ani = animation.FuncAnimation(fig, update, frames=self.max_iterations, interval=50)
        plt.show()


def main():
    num_particles = 50
    num_variables = 2
    bounds = [[0, 1]] * num_variables
    max_iterations = 1000

    optimizer = PSO(num_particles, num_variables, bounds, max_iterations)
    optimizer.optimize()
    optimizer.animate()

    print("Global best position: ", optimizer.global_best_position)
    print("Global best fitness: ", optimizer.global_best_fitness)


if __name__ == "__main__":
    main()