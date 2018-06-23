import math
import collections
from mesa import Agent

class Queue:
    def __init__(self):
        self.elements = collections.deque()  # deque is a faster list datatype

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):  # a function for adding items to the queue
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()  # popleft pops the leftmost deque element, or raises an error if non present

class AgentGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, position):
        (x, y) = position
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, position):
        return position not in self.walls

    def neighbours(self, position):
        (x, y) = position
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


