import math
import os
import random
import sys
from matplotlib import pyplot as plt

def load_script_arguments(args: list) -> (float, int):
    """
    :param args: read the arguments given when running script
    :return: arguments for radius and number of simulations if given, else default values
    """
    # define default values in case no arguments are given by user. R=1, Simulations=1 million
    try:
        radius = float(args[1])
    except:
        radius = 1
    try:
        simulation_counter = int(args[2])
    except:
        simulation_counter = int(1e6)
    return radius, simulation_counter

def count_circle_points(simulations: int, circle_radius: float) -> int:
    """
    :param simulations:
    :param circle_radius:
    :return:
    """
    circle_radius_squared = circle_radius ** 2
    in_circle_counter = 0  # counts how many points simulated are within the circle
    for simulation in range(simulations):
        # we sample (x,y) pairs only in the [0,1) x [0,1) quarter
        x = random.random()  # random number in [0, 1)
        y = random.random()
        if x ** 2 + y ** 2 <= circle_radius_squared:  # case where point (x,y) within the circle
            in_circle_counter += 1
    return in_circle_counter

def circle_surface_calc(simulations: int, circle_radius: float) -> (float, float):
    square_side = 2 * circle_radius
    circle_to_square_ratio = in_circle_counter / simulations
    square_surface = square_side ** 2
    calculated_circle_surface = square_surface * circle_to_square_ratio
    real_circle_surface = math.pi * (circle_radius ** 2)

    return calculated_circle_surface, real_circle_surface

if __name__ == "__main__":
    # we set the coordinate system's root (0,0) in the center of the circle.
    circle_radius, number_of_simulations = load_script_arguments(sys.argv)
    print(f'Monte Carlo estimation of the surface of circle\nradius\t\t\t\t=\t{circle_radius}\n'
          f'simulations\t\t\t=\t{number_of_simulations}')
    in_circle_counter = count_circle_points(simulations = number_of_simulations, circle_radius = circle_radius)
    calculated_circle_surface, real_circle_surface = circle_surface_calc(number_of_simulations, circle_radius)

    print(f'Calculated circle surface value\t=\t{calculated_circle_surface}')
    print(f'Real circle surface value\t=\t{real_circle_surface}')
    similarity = 1 - abs(real_circle_surface - calculated_circle_surface)/(real_circle_surface)
    similarity_ratio = round(100 * similarity, 2)
    print(f'Similarity level\t\t=\t{similarity_ratio} %')

    # ------------------------------------------------------------------------------------------
    # plot some figure with how the similarity increases by the number of simulations performed
    # ------------------------------------------------------------------------------------------

    # if 3rd argument is True then run the simulation
    try:
        full_simulation_flag = sys.argv[3]
    except:
        full_simulation_flag = False

    if  full_simulation_flag == "True":
        simulations_number_list = [10, 100, 1000, 10000, 100000, 1000000, 10000000]  # 10 to 10 million
        circle_surfaces = []
        for simulation in simulations_number_list:
            in_circle_counter = count_circle_points(simulations=simulation, circle_radius=circle_radius)
            calculated_circle_surface, real_circle_surface = circle_surface_calc(simulation, circle_radius)
            circle_surfaces.append(calculated_circle_surface)
        fig, ax = plt.subplots()
        ax.scatter(simulations_number_list, circle_surfaces, label='calculated')  # points of calculated surface value
        ax.axhline(y=math.pi * (circle_radius ** 2), color='r', linestyle='-', label='real')  # real surface value
        ax.set_xscale('log') # logarithmic scale for x axis
        ax.set_title(f'Monte carlo approximation of circle surface\nradius={circle_radius}')
        ax.set_xlabel('simulations')
        ax.set_ylabel('surface')
        ax.legend()
        figname = f'monte_carlo_circle_surface_simulations_radius={circle_radius}.png'
        print(f'Figure saved in {figname}')
        plt.savefig(figname)