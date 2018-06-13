

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
    # initial_obstacles = 3
    # obstacle_length = 7

    empty_boxes = {}
    full_boxes = {}
    known_items = {}
    all_boxes = {}
    obstacles = []
    map_choice = []

    verbose = False  # Print-monitoring

    description = 'A model for simulating wolf and sheep (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_walkers=1,
                 initial_boxes=10,
                 # initial_items=initial_boxes//2,
                 initial_items=10,
                 # initial_obstacles=3,
                 # obstacle_length=7,
                 empty_boxes={},
                 full_boxes={},
                 all_boxes={},
                 obstacles=[],
                 map_choice=[]):

        # Model Parameters Init
        self.height = height
        self.width = width
        self.initial_walkers = initial_walkers
        self.initial_boxes = initial_boxes
        self.initial_items = initial_items
        # self.initial_obstacles = initial_obstacles
        # self.obstacle_length = obstacle_length
        self.map_choice = map_choice

        self.empty_boxes = empty_boxes
        self.full_boxes = full_boxes
        self.all_boxes = all_boxes
        self.obstacles = obstacles

        # Spawn Locations
        self.map_one_boxes = [(2, 4), (3, 17), (5, 2), (6, 7), (9, 9), (11, 14), (15, 9), (17, 1), (17, 10), (17, 18)]
        self.map_one_obstacles = [(1,14), (2,14), (3,14), (4,14), (5,14), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7), (7, 6),
                             (13, 17), (13, 16), (13, 15), (13, 14), (13, 13), (13, 12), (13, 11), (15, 14), (16, 14),
                             (17, 14), (18, 14), (19, 14), (16, 3), (17, 3), (18, 3)]
        self.map_two_boxes = [(0, 2), (2, 11), (4, 16), (8, 5), (8, 18), (0, 12), (13, 2), (15, 13), (17, 19), (18, 17)]
        self.map_two_obstacles = [(0, 7), (1, 7), (2, 7), (3, 7), (6, 19), (6, 18), (6, 17), (6, 16), (6, 15), (6, 14),
                             (10, 7), (10, 6), (10, 5), (10, 4), (10, 3), (10, 2), (15, 15), (16, 15), (17, 15),
                             (18, 15), (19, 15)]

        self.map_three_boxes = [(0, 2), (2, 15), (6, 15), (6, 18), (0, 10), (11, 13), (0, 15), (16, 17), (17, 15), (18, 4)]
        self.map_three_obstacles = [(3,17), (3,16), (3,15), (3,14), (3,13), (8,18), (8,17), (8,16), (8,15), (8,14), (8,13),
                               (8,12), (8,3), (9,3), (10,3), (11,3), (12,3), (13,3), (13,2), (13,1), (0,13), (15,10),
                               (16,10), (17,10), (18,10), (16,10)]

        self.map_four_boxes = [(0,11), (3,10), (4,14), (6,16), (11,19), (12,1), (13,3), (17,8), (17,18), (18,12)]
        self.map_four_obstacles = [(2,15), (2,14), (2,13), (2,12), (2,11), (2,10), (2,9), (2,8), (5,16), (5,15), (5,14),
                              (5,13), (8,18), (8,17), (8,16), (8,15), (8,14), (15,15), (16,15), (17,15), (18,15),
                              (19,15), (15,5), (16,5), (17,5), (18,5)]

        self.map_five_boxes = [(1,7), (3,10), (4,17), (8,3), (11,13), (12,15), (15,9), (16,18), (0,18), (18,9)]
        self.map_five_obstacles = [(2,14), (3,14), (4,14), (5,14), (5,10), (5,9), (5,8), (5,7), (5,6), (5,5), (13,17),
                              (13,16), (13,15), (13,14), (13,13), (13,12), (13,11), (15,14), (16,14), (17,14), (18,14),
                              (17,3), (18,3), (19,3)]

        # Model Functions
        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"Closed Boxes": lambda m: m.schedule.get_type_count(ClosedBox)})

        # No clue why these are up here in particular - these are the actual parts of the model!
        self.map_picker()
        self.make_boxes()
        self.make_items()
        self.make_obstacles()
        self.make_walker_agents()

        # pick a map
    def map_picker(self):
        available_maps = ["one", "two", "three", "four", "five"]
        self.map_choice = random.choice(available_maps)

        # create Boxes:
    def make_boxes(self):
        if self.map_choice == "one":
            for i in range(self.initial_boxes):
                x, y = self.map_one_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "two":
            for i in range(self.initial_boxes):
                x, y = self.map_two_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "three":
            for i in range(self.initial_boxes):
                x, y = self.map_three_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "four":
            for i in range(self.initial_boxes):
                x, y = self.map_four_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "five":
            for i in range(self.initial_boxes):
                x, y = self.map_five_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        # --------------------- BELOW: RANDOM BOX GENERATION -------------------------
        # for i in range(self.initial_boxes):
        #     x = random.randrange(self.width)
        #     y = random.randrange(self.height)
        #     closedBox = ClosedBox((x, y), self, True)
        #     self.grid.place_agent(closedBox, (x, y))
        #     self.schedule.add(closedBox)
        #     # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
        #     self.empty_boxes[i] = (x, y)
        #     self.all_boxes[i] = (x, y)
        #     # print("Empty Box Created")

        # Create Walker:

    def make_walker_agents(self):
        for i in range(self.initial_walkers):
            x, y = self.grid.find_empty()
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
        if self.map_choice == "one":
            for i in range(len(self.map_one_obstacles)):
                x, y = self.map_one_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "two":
            for i in range(len(self.map_two_obstacles)):
                x, y = self.map_two_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "three":
            for i in range(len(self.map_three_obstacles)):
                x, y = self.map_three_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "four":
            for i in range(len(self.map_four_obstacles)):
                x, y = self.map_four_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "five":
            for i in range(len(self.map_five_obstacles)):
                x, y = self.map_five_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

    # ------------------------------ BELOW: RANDOM OBSTACLE GENERATION ------------------------------------
    # def make_obstacles(self):
    #     for i in range(self.initial_obstacles):
    #         x, y = self.grid.find_empty()
    #         initial_obstacle = (x, y)
    #         obstacle = Obstacle((x, y), self)
    #         self.grid.place_agent(obstacle, initial_obstacle)
    #         self.schedule.add(obstacle)
    #         # print("Obstacle added!")
    #
    #         self.obstacles.append(initial_obstacle)
    #         # need to think about how going to store obstacle information
    #
    #         length = random.randrange(3, self.obstacle_length, 1)
    #         # print("Length is: ", length)
    #         neighbours = self.grid.get_neighborhood(initial_obstacle, False, False, 1)
    #         # print("Neighbours: ", neighbours)
    #
    #         directions = ["north", "east", "south", "west"]
    #         random_direction = random.choice(directions)
    #
    #         current_x = initial_obstacle[0]
    #         current_y = initial_obstacle[1]
    #
    #         for j in range(length):
    #             if random_direction == "north":
    #                 new_obstacle = (current_x, (current_y + 1))
    #
    #                 if self.grid.is_cell_empty(new_obstacle) == True:
    #                     self.grid.place_agent(obstacle, new_obstacle)
    #                     self.schedule.add(obstacle)
    #                     self.obstacles.append(new_obstacle)
    #                     current_y = current_y + 1
    #                     print("Obstacle extension added!")
    #                 else:
    #                     print("Obstacle couldn't be placed.")
    #                     return
    #
    #             if random_direction == "east":
    #                 new_obstacle = ((current_x + 1), current_y)
    #
    #                 if self.grid.is_cell_empty(new_obstacle) == True:
    #                     self.grid.place_agent(obstacle, new_obstacle)
    #                     self.schedule.add(obstacle)
    #                     self.obstacles.append(new_obstacle)
    #                     current_x = current_x + 1
    #                     print("Obstacle extension added!")
    #                 else:
    #                     print("Obstacle couldn't be placed.")
    #                     return
    #
    #             if random_direction == "south":
    #                 new_obstacle = (current_x, (current_y - 1))
    #
    #                 if self.grid.is_cell_empty(new_obstacle) == True:
    #                     self.grid.place_agent(obstacle, new_obstacle)
    #                     self.schedule.add(obstacle)
    #                     self.obstacles.append(new_obstacle)
    #                     current_y = current_y - 1
    #                     print("Obstacle extension added!")
    #                 else:
    #                     print("Obstacle couldn't be placed.")
    #                     return
    #
    #             if random_direction == "west":
    #                 new_obstacle = ((current_x - 1), current_y)
    #
    #                 if self.grid.is_cell_empty(new_obstacle) == True:
    #                     self.grid.place_agent(obstacle, new_obstacle)
    #                     self.schedule.add(obstacle)
    #                     self.obstacles.append(new_obstacle)
    #                     current_x = current_x - 1
    #                     print("Obstacle extension added!")
    #                 else:
    #                     print("Obstacle couldn't be placed.")
    #                     return
    #
    #     # self.obstacles.sort()
    #     print("Obstacle list:", self.obstacles)

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
