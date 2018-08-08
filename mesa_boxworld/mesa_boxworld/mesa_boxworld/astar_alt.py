from queue import PriorityQueue
import math

# this is a test file to experiment with the A* solver algorithm and workable solutions

# def deliberative_nav():
#     .get_nodes()  # sets the global 'passable_nodes' to the list of non-obstacle map points
#     came_from, cost_so_far = astar_search(pos, goal)
#     reconstruct_path(came_from, pos, goal)
#
#     # generate a list of possible next steps (children) toward the goal from current pos
#     # store in ordered list (priority queue), based on distance to goal, closest first
#     # select closest child to the goal
#     # repeat until goal reached or no more children.
#     #  --- two important factors: how you measure distance to goal, and how to generate children

goal = (5,5)
start = (0,0)

passable_nodes = []

width = 6
height = 6

# convert grid to graph using nodes
def get_nodes():  # return nodes possible to navigate (not including obstacles)
    all_nodes = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                 (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
                 (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
                 (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
                 (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
                 (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),]

    passable_nodes = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                 (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
                 (0, 2), (1, 2), (3, 2), (4, 2), (5, 2),
                 (0, 3), (1, 3), (3, 3), (4, 3), (5, 3),
                 (0, 4), (1, 4), (3, 4), (4, 4), (5, 4),
                 (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),]

    return passable_nodes


def passable( id):
    passable_nodes = get_nodes()
    if id in passable_nodes:
        return True
    else:
        return False


def in_bounds(id):
    (x, y) = id
    return 0 <= x < width and 0 <= y < height


def get_neighbours(id):
    (x, y) = id
    results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
    print("Neighbours of", id, ": ", results)
    if (x + y) % 2 == 0: results.reverse()  # aesthetics
    passable_results = []

    for x in range(len(results)):
        value = results[x]
        print("Value:", value)
        if passable(value):
            print("Value is Passable")
            if in_bounds(value):
                print("Value is in Bounds")
                passable_results.append(value)
                print("Neighbour Added.")

    # results = filter(passable, results)  # need to find a way to check if the neighbours are passable or not
    print("Passable Neighbours: ", passable_results)
    return passable_results


# def get_neighbours( node):  # neighbours are other nodes connected by an edge to parent node
#     dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
#     result = []
#     for dir in dirs:
#         if passable([node[0] + dir[0], node[1] + dir[1]]):
#             result.append([node[0] + dir[0], node[1] + dir[1]])
#             print("Neighbours of", node, ": ", result)
#         if not passable([node[0] + dir[0], node[1] + dir[1]]):
#             print("That node can't be added as a neighbour")
#     print("Neighbours got!")
#     return result

def get_distance(current, target, euclid=False):
    dist = 0
    px, py = current
    qx, qy = target
    euclidean_distance = math.sqrt(math.pow((qx - px), 2) + (math.pow((qy - py), 2)))

    if current[0] <= target[0]:
        xs = range(current[0] + 1, target[0]) or [current[0]]
        ys = range(current[1] + 1, target[1]) or [current[1]]
        grid_sq_distance = [(x, y) for x in xs for y in ys]

    elif current[0] > target[0]:
        swapped_p1 = target
        swapped_p2 = current
        xs = range(swapped_p1[0] + 1, swapped_p2[0]) or [swapped_p1[0]]
        ys = range(swapped_p1[1] + 1, swapped_p2[1]) or [swapped_p1[1]]
        grid_sq_distance = [(x, y) for x in xs for y in ys]

    if euclid:
        return euclidean_distance
    elif not euclid:
        return len(grid_sq_distance)


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def get_cost(a, b):
    distance = get_distance(a, b, euclid=False)
    return 3 * abs(distance)


def astar_search(start,
                 goal):  # doesn't actually use node list as we check for passability in neighbour generator
    frontier = PriorityQueue()
    print("Established Frontier Q")
    frontier.put(start, 0)
    print("Put start location")
    came_from = {}
    print("Opened Came From")
    cost_so_far = {}
    print("Opened Cost So Far")
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        print("Frontier isn't empty")
        current = frontier.get()
        print("Current:", current)
        if current == goal:
            break

        for next in get_neighbours(current):
            print("Neighbours of current are:", get_neighbours(current))
            new_cost = cost_so_far[current] + get_cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    print("Came From List: ", came_from)
    print("Cost So Far: ", cost_so_far)
    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []

    while current != start:
        print("current in path reconstruction:", current)
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    print("Reconstructed Path: ", path)
    return path


get_nodes()
came_from, cost_so_far = astar_search(start, goal)
reconstruct_path(came_from, start, goal)

