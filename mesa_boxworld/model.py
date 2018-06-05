

import random

from mesa import Model
from mesa.space import MultiGrid
# from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from mesa_boxworld.agents import Walker, ClosedBox, OpenedBox, Item, Obstacle
from mesa_boxworld.schedule import RandomActivationByType


class ThirdTestModel(Model):
    '''
    Third Test for the Boxworld Model
    '''

    height = 20
    width = 20

    initial_walkers = 1
    initial_boxes = 10
    # initial_items = initial_boxes//2  # -- currently divides int and results in a new int (as opposed to float)
    initial_items = 10
    initial_obstacles = 3
    obstacle_length = 7

    empty_boxes = {}
    full_boxes = {}
    known_items = {}
    all_boxes = {}
    obstacles = []

    verbose = False  # Print-monitoring

    description = 'A model for simulating wolf and sheep (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_walkers=1,
                 initial_boxes=10,
                 # initial_items=initial_boxes//2,
                 initial_items=10,
                 initial_obstacles=3,
                 obstacle_length=7,
                 empty_boxes={},
                 full_boxes={},
                 all_boxes={},
                 obstacles=[]):

        # Model Parameters Init
        self.height = height
        self.width = width
        self.initial_walkers = initial_walkers
        self.initial_boxes = initial_boxes
        self.initial_items = initial_items
        self.initial_obstacles = initial_obstacles
        self.obstacle_length = obstacle_length

        self.empty_boxes = empty_boxes
        self.full_boxes = full_boxes
        self.all_boxes = all_boxes
        self.obstacles = obstacles

        # Model Functions
        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"Closed Boxes": lambda m: m.schedule.get_type_count(ClosedBox)})

        # No clue why these are up here in particular - these are the actual parts of the model!
        self.make_walker_agents()
        self.make_boxes()
        self.make_items()
        self.make_obstacles()

        # create Boxes:

    def make_boxes(self):
        for i in range(self.initial_boxes):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            closedBox = ClosedBox((x, y), self, True)
            self.grid.place_agent(closedBox, (x, y))
            self.schedule.add(closedBox)
            # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
            self.empty_boxes[i] = (x, y)
            self.all_boxes[i] = (x, y)
            # print("Empty Box Created")

        # Create Walker:
    def make_walker_agents(self):
        for i in range(self.initial_walkers):
            x, y = self.grid.find_empty()
            # x = random.randrange(self.width)
            # y = random.randrange(self.height)
            walker = Walker((x, y), self, True)
            self.grid.place_agent(walker, (x, y))
            self.schedule.add(walker)

    def make_items(self):
        # this function takes the dictionary of empty boxes, selects one and puts an item in it
        for j in range(self.initial_items):
            chosen_box = self.empty_boxes.pop(j)
            # print("Box Selected")
                    # chosen_box = self.empty_boxes.popitem()
                    # print("Box Selected")
                    # use the above to pop an arbitrary value from the empty boxes list
            item = Item(chosen_box, self, True)
            self.grid.place_agent(item, chosen_box)
            self.schedule.add(item)
            # print("Item Added")
            self.full_boxes[j] = chosen_box
            # print("Box Filled")

        # if a random item placement is needed, uncomment below:
        # for i in range(self.initial_items):
        #     x = random.randrange(self.width)
        #     y = random.randrange(self.height)
        #     item = Item((x, y), self, True)
        #     self.grid.place_agent(item, (x, y))
        #     self.schedule.add(item)

        self.running = True
        self.datacollector.collect(self)

    def make_obstacles(self):
        for i in range(self.initial_obstacles):
            x, y = self.grid.find_empty()
            initial_obstacle = (x, y)
            obstacle = Obstacle((x, y), self)
            self.grid.place_agent(obstacle, initial_obstacle)
            self.schedule.add(obstacle)
            # print("Obstacle added!")

            self.obstacles.append(initial_obstacle)
            # need to think about how going to store obstacle information

            length = random.randrange(3, self.obstacle_length, 1)
            # print("Length is: ", length)
            neighbours = self.grid.get_neighborhood(initial_obstacle, False, False, 1)
            # print("Neighbours: ", neighbours)

            directions = ["north", "east", "south", "west"]
            random_direction = random.choice(directions)

            current_x = initial_obstacle[0]
            current_y = initial_obstacle[1]

            for j in range(length):
                if random_direction == "north":
                    new_obstacle = (current_x, (current_y + 1))

                    if self.grid.is_cell_empty(new_obstacle) == True:
                        self.grid.place_agent(obstacle, new_obstacle)
                        self.schedule.add(obstacle)
                        self.obstacles.append(new_obstacle)
                        current_y = current_y + 1
                        print("Obstacle extension added!")
                    else:
                        print("Obstacle couldn't be placed.")

                if random_direction == "east":
                    new_obstacle = ((current_x + 1), current_y)

                    if self.grid.is_cell_empty(new_obstacle) == True:
                        self.grid.place_agent(obstacle, new_obstacle)
                        self.schedule.add(obstacle)
                        self.obstacles.append(new_obstacle)
                        current_x = current_x + 1
                        print("Obstacle extension added!")
                    else:
                        print("Obstacle couldn't be placed.")

                if random_direction == "south":
                    new_obstacle = (current_x, (current_y - 1))

                    if self.grid.is_cell_empty(new_obstacle) == True:
                        self.grid.place_agent(obstacle, new_obstacle)
                        self.schedule.add(obstacle)
                        self.obstacles.append(new_obstacle)
                        current_y = current_y - 1
                        print("Obstacle extension added!")
                    else:
                        print("Obstacle couldn't be placed.")

                if random_direction == "west":
                    new_obstacle = ((current_x - 1), current_y)

                    if self.grid.is_cell_empty(new_obstacle) == True:
                        self.grid.place_agent(obstacle, new_obstacle)
                        self.schedule.add(obstacle)
                        self.obstacles.append(new_obstacle)
                        current_x = current_x - 1
                        print("Obstacle extension added!")
                    else:
                        print("Obstacle couldn't be placed.")

        # self.obstacles.sort()
        print("Obstacle list:", self.obstacles)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_type_count(ClosedBox)])

            # stopping agents having conflicting simultaneous actions

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number walkers: ',
                  self.schedule.get_type_count(Walker),
                  'Initial number closed boxes: ',
                  self.schedule.get_type_count(ClosedBox))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number walkers: ',
                  self.schedule.get_type_count(Walker),
                  'Final number closed boxes: ',
                  self.schedule.get_type_count(ClosedBox))
