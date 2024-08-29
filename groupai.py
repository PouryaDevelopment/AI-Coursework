from queue import PriorityQueue

def a_star_search(maze, start, end):
    def get_neighbors(node):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        result = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if (0 <= neighbor[0] < len(maze)) and (0 <= neighbor[1] < len(maze[0])) and maze[neighbor[0]][neighbor[1]]:
                result.append(neighbor)
        return result

    def heuristic(node, end):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])

    priority_queue = PriorityQueue()
    priority_queue.put((0 + heuristic(start, end), 0, start, [start]))
    visited = set()

    while not priority_queue.empty():
        _, cost, current_node, path = priority_queue.get()
        
        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end:
            return path

        for neighbor in get_neighbors(current_node):
            if neighbor not in visited:
                priority_queue.put((cost + 1 + heuristic(neighbor, end), cost + 1, neighbor, path + [neighbor]))

    return None

# Maze configuration (True for open path, False for obstacle)
maze = [
    [True, True, True, True, True, True],
    [True, True, True, False, True, True],
    [True, False, True, False, True, True],
    [True, True, True, True, True, True],
    [True, True, True, True, True, True]
]

start_node = (0, 0)
end_node = (4, 5)

path = a_star_search(maze, start_node, end_node)
print("Path found:", path)