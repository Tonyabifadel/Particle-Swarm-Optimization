import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math
from tqdm import tqdm

def initialize_swarm(num_particles, bounds):
    swarm = []
    for _ in range(num_particles):
        position = [random.uniform(bounds[0], bounds[1]) for _ in range(2)]
        velocity = [random.uniform(-1, 1) for _ in range(2)]
        best_position = position[:]
        best_fitness = float('inf')
        fitness = float('inf')
        swarm.append({'position': position, 'velocity': velocity, 'best_position': best_position, 'best_fitness': best_fitness, 'fitness': fitness})
    return swarm

def evaluate_fitness(position):
    x, y = position
    fitness = (x - 0.5)**2 + (y - 0.5)**2
    return fitness

def optimize(swarm, num_particles, bounds, max_iterations):
    inertia_weight = 0.3
    cognitive_weight = 1.2
    social_weight = 1.2
    global_best_position = [0.5, 0.5]
    global_best_fitness = float('inf')
    positions = []

    for _ in tqdm(range(max_iterations)):
        positions.append([particle['position'][:] for particle in swarm])
        for i in range(num_particles):
            fitness = evaluate_fitness(swarm[i]['position'])
            if fitness < swarm[i]['best_fitness']:
                swarm[i]['best_fitness'] = fitness
                swarm[i]['best_position'] = swarm[i]['position'][:]
            if fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_position = swarm[i]['position'][:]

        for i in range(num_particles):
            for j in range(2):
                r1, r2 = random.random(), random.random()
                swarm[i]['velocity'][j] = (inertia_weight * swarm[i]['velocity'][j] +
                                           cognitive_weight * r1 * (swarm[i]['best_position'][j] - swarm[i]['position'][j]) +
                                           social_weight * r2 * (global_best_position[j] - swarm[i]['position'][j]))
                swarm[i]['position'][j] += swarm[i]['velocity'][j]
                swarm[i]['position'][j] = min(max(swarm[i]['position'][j], bounds[0]), bounds[1])

    return swarm, positions, global_best_position, global_best_fitness

def animate(positions, global_best_position):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    def update(frame):
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        for particle in positions[frame]:
            ax.scatter(particle[0], particle[1], c='b')
        ax.scatter(global_best_position[0], global_best_position[1], c='r')

    ani = animation.FuncAnimation(fig, update, frames=len(positions), interval=50)
    plt.show()

def main():
    num_particles = 50
    bounds = [0, 1]
    max_iterations = 1000

    swarm = initialize_swarm(num_particles, bounds)
    swarm, positions, global_best_position, global_best_fitness = optimize(swarm, num_particles, bounds, max_iterations)
    animate(positions, global_best_position)

    print("Global best position: ", global_best_position)
    print("Global best fitness: ", global_best_fitness)

if __name__ == "__main__":
    main()