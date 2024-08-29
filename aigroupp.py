import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from queue import PriorityQueue


def searchmethodAstar(setting_maze, startingpos, endingpos):
    def get_next_to_node(node):
        next_node = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        result = []
        for nn in next_node:
            nodes_around = (node[0] + nn[0], node[1] + nn[1])
            if 0 <= nodes_around[0] < setting_maze.shape[0] and 0 <= nodes_around[1] < setting_maze.shape[1] and setting_maze[nodes_around[0], nodes_around[1]]:
                result.append(nodes_around)
        return result

        # the heuristic function, it uses manhattan distance
    def h_cost(node, end):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])

        # the cost function basing on the length of the path

    def g_cost(path):
        return len(path) - 1

    priority_queue = PriorityQueue()
    priority_queue.put((g_cost([startingpos]) + h_cost(startingpos, endingpos), [startingpos]))  # the priority path
    visited = set()

    while not priority_queue.empty():
        current_priority, current_path = priority_queue.get()
        current_node = current_path[-1]

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == endingpos:
            return current_path

        for neighbor in get_next_to_node(current_node):
            if neighbor not in visited:
                new_path = current_path + [neighbor]
                new_priority = g_cost(new_path) + h_cost(neighbor, endingpos)
                priority_queue.put((new_priority, new_path))

    return None


# the maze configuration for figure 1 , here we can change the maze choosing which block is passable and which is an
# obstacle, it uses a numpy array to store this type of data set.
maze_configuration = np.array([   # 1= passable
    [1, 0, 1, 1, 1, 1],                 # 0= obstacle
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1]
], dtype=bool)

starting_position = (0, 0)
ending_position = (4, 5)

# this finds the path using the A* star method, by using the maze config with the starting and ending positions:
path_to_ending_pos = searchmethodAstar(maze_configuration, starting_position, ending_position)

print("Cost (number of steps):", len(path_to_ending_pos) - 1 if path_to_ending_pos else "No path found")


# the plotting function for the maze and the path
def maze_plot(maze_configuration, path=None, start_node=None, end_node=None):
    colour_map = ListedColormap(['lightsteelblue', 'red', 'black'])
    plotmaze = np.zeros_like(maze_configuration, dtype=int)
    plotmaze[maze_configuration == 0] = 1  # maze plots are lightsteel blue, obstacles are red to match the maze given

    if path is not None:
        for node in path:
            plotmaze[node] = 3  # Path is black

    plt.figure(figsize=(10, 8))
    plt.imshow(plotmaze, cmap=colour_map)
    plt.grid(which='both', color='grey', linewidth=0.5)
    plt.xticks(range(maze_configuration.shape[1]), [])
    plt.yticks(range(maze_configuration.shape[0]), [])
    # displays the number of steps on the plot
    if path:
        plt.text(2.5, -1.0, f'Number of steps: {len(path) - 1}', fontsize=12, ha='center', va='center', color='black')
    plt.show()


# runs the plotting function to visualize the maze and the path
maze_plot(maze_configuration, path_to_ending_pos, starting_position, ending_position)
