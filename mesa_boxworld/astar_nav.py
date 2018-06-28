import collections
import math
from mesa import Agent
from queue import PriorityQueue
# priotyQs (also: Heap Q's) are binary trees where every parent node has a value >= any of its children. It keeps track
# of the minimum value, helping retrieve that min value at all times

class State(object):
    def __init__(self, value, parent, start, goal):
        self.children = []  # list of all neighbouring possibilities - squares immediately around current pos
        self.parent = parent
        self.value = value  # value of the current child
        self.dist = 0  # placeholder for now, set in subclasses
        if parent:  # if parent has a value
            self.path = parent.path[:]  # copy the parent's path to our new path - [:] is very important!
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal

        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def GetDistance(self, current, target):
        pass

    def CreateChildren(self, point):
        pass

class State_String(State):  # subclass
    def __init__(self, value, parent, start, goal, grid, walls):
        super(State_String, self).__init__(value, parent, start, goal)  # initialise the base class
        self.dist = self.GetDistance()  # this function is for measuring distance to the goal
        self.grid = grid
        self.walls = walls

    def GetDistance(self, current, target, euclid=False):
        if self.value == self.goal:  # have we reached our goal?
            return 0
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
            return grid_sq_distance

    def CreateChildren(self, point):
        x, y = point

        if not self.children:
            for i in range(len(self.goal)):
                val = self.value
                val = [((x+1), y), ((x-1), y), (x, (y+1)), (x, (y-1))]
                print("val: ", val)
                child = State_String(val, self)
                self.children.append(child)


class AStar_Solver:
    def __init__(self, start, goal, grid, walls):
        self.path = []  # store solution path from start to goal state
        self.visitedQueue = []  # keep track of all children visited so we don't visit 2 twice
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.grid = grid
        self.walls = walls

    def Solve(self):
        startState = State_String(self.start, 0, self.start, self.goal, self.grid, self.walls)
        count = 0  # adding one every time we add a new child, id for child
        self.priorityQueue.put((0, count, startState))

        while(not self.path and self.priorityQueue.qsize()): # whilst the path is empty and the Q has a size
            closestChild = self.priorityQueue.get()[2]  # get startState from the first item in the priority Q
            closestChild.CreateChildren()
            self.visitedQueue.append((closestChild.value))
            for child in closestChild.children:
                if child.value not in self.visitedQueue:
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    



