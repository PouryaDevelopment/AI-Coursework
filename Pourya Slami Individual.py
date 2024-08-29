import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
import matplotlib.cm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def get_next_to_node(node, setting_maze):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []
    for dx, dy in directions:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < setting_maze.shape[0] and 0 <= y < setting_maze.shape[1] and setting_maze[x, y]:
            neighbors.append((x, y))
    return neighbors


def frwrd_chaining_meth(setting_maze, startingpos, endingpos):
    opened_list = [startingpos]
    closed_list = set()
    par_map = {}
    attempt_list = []

    while opened_list:
        current_node = opened_list.pop(0)
        attempt_list.append(current_node)

        if current_node == endingpos:
            return remake_path(par_map, endingpos), attempt_list

        closed_list.add(current_node)
        for move in get_next_to_node(current_node, setting_maze):
            if move not in closed_list and move not in opened_list:
                par_map[move] = current_node
                opened_list.append(move)

    return None, attempt_list


def remake_path(par_map, endingpos):
    path = []
    current = endingpos
    while current in par_map:
        path.insert(0, current)
        current = par_map[current]
    path.insert(0, current)
    return path


def plot_maze(maze_configuration, start_node=None, end_node=None):
    cmap = ListedColormap(['lightsteelblue', 'red', 'yellow', 'green'])
    maze_plot = np.zeros_like(maze_configuration, dtype=int)
    maze_plot[maze_configuration == 0] = 1
    if start_node is not None:
        maze_plot[start_node] = 3
    if end_node is not None:
        maze_plot[end_node] = 2

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.05, right=0.75)
    ax.imshow(maze_plot, cmap=cmap)
    ax.grid(which='both', color='grey', linewidth=0.5)
    ax.set_xticks(range(maze_configuration.shape[1]))
    ax.set_yticks(range(maze_configuration.shape[0]))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='b', label='Start Node'),
        Patch(facecolor='lightsteelblue', edgecolor='b', label='Passable node'),
        Patch(facecolor='red', edgecolor='b', label='obstacle node'),
        Patch(facecolor='yellow', edgecolor='b', label='End Node'),
        Line2D([0], [0], color='black', lw=4, label='Path (line)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Attempts (small dots)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1))

    return fig, ax, maze_plot


def animate_search_attempt(animate_attempts, mazeani, start, end, path):
    fig, ax, maze_plot = plot_maze(mazeani, start, end)
    num_attempts = len(animate_attempts)

    # colour map for random colours for the attempt patches
    cmap = matplotlib.cm.get_cmap('tab20b')
    attempt_patches = []  # a list to store the attempt patches
    path_patches = []  # a list for the path line

    text = ax.text(0.5, -0.05, '', fontsize=12, ha='center', va='top', transform=ax.transAxes)

    def updatemaze(frame, axs, figure, maze_plots, attempt, paths):
        nonlocal attempt_patches, path_patches
        if frame < num_attempts:
            node = attempt[frame]
            x, y = node[1], node[0]
            color_index = frame % 20  # 20 colours in the colour map
            patch = axs.scatter(x, y, color=cmap(color_index), s=100, alpha=0.6,
                                edgecolors='black')  # small patches circle for attempts
            attempt_patches.append(patch)  # adds the patch to the list
            text.set_text(f'attempts: {frame + 1}')

        if frame == num_attempts:
            # this will clear the attempts and path from previous run
            for patch in attempt_patches:
                patch.remove()
            attempt_patches.clear()
            path_x = [node[1] for node in paths]
            path_y = [node[0] for node in paths]
            path_line, = axs.plot(path_x, path_y, 'black', lw=2, marker='o',
                                  markersize=8)  # Consistent line for the path
            path_patches.append(path_line)
            text.set_text('Successful path')  # change text to show successful path
        elif frame > num_attempts:
            for patch in path_patches:
                patch.remove()  # clears the path patches for next run
            path_patches.clear()

    ani = FuncAnimation(fig, updatemaze, frames=num_attempts + 2, fargs=(ax, fig, maze_plot, animate_attempts, path),
                        interval=500,
                        repeat=True, blit=False)
    plt.show()


maze = np.array([
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1]
], dtype=bool)
start_pos = (0, 0)
end_pos = (4, 5)

# Run forward chaining
found_path, attempts = frwrd_chaining_meth(maze, start_pos, end_pos)

if found_path:
    print("Path found:", found_path)
    print("Cost (number of steps):", len(found_path) - 1)
    animate_search_attempt(attempts, maze, start_pos, end_pos, found_path)
else:
    print("No path found")
