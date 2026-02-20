import sys
import numpy as np

x_vec = [1, 2, 3, 4, 5]
y_vec = [10, 11, 12]
z_vec = [20, 30]

axes_order = ['x', 'y', 'z']
move_pattern = 'snake'

axes_vectors = {
    'x': x_vec.copy(),
    'y': y_vec.copy(),
    'z': z_vec.copy(),
}

num_of_points_per_layer = len(axes_vectors[axes_order[0]]) * len(axes_vectors[axes_order[1]])
num_of_layers = len(axes_vectors[axes_order[2]])
total_num_of_points = num_of_points_per_layer * num_of_layers

layer_count = 0
point_in_layer_count = 0
total_point_count = 0

if move_pattern == 'snake':
    # Initialize vector copies to realize snake-like movement
    axes_vectors[axes_order[0]] = np.flip(axes_vectors[axes_order[0]])
    axes_vectors[axes_order[1]] = np.flip(axes_vectors[axes_order[1]])

for a2 in axes_vectors[axes_order[2]]:
    layer_count += 1
    if move_pattern == 'snake':
        axes_vectors[axes_order[1]] = np.flip(axes_vectors[axes_order[1]])  # snake movement in ax1-direction
    # measure one layer
    for a1 in axes_vectors[axes_order[1]]:
        if move_pattern == 'snake':
            axes_vectors[axes_order[0]] = np.flip(axes_vectors[axes_order[0]])  # snake movement in ax0-direction
        for a0 in axes_vectors[axes_order[0]]:
            point_in_layer_count += 1
            total_point_count += 1
            # Re-Map coordinates to x,y,z
            cur_coordinate = {
                axes_order[0]: a0,
                axes_order[1]: a1,
                axes_order[2]: a2,
            }
            x_coor = cur_coordinate['x']
            y_coor = cur_coordinate['y']
            z_coor = cur_coordinate['z']

            total_point_count += 1
            print(f"Move to {total_point_count}. Point: {x_coor}, {y_coor}, {z_coor} | Layer: {layer_count}")