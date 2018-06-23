
import random

from mesa import Model
from mesa.space import MultiGrid
# from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from mesa_boxworld.agents import Walker, ClosedBox, blueItem, yellowItem, pinkItem, Obstacle
from mesa_boxworld.schedule import RandomActivationByType


class ThirdTestModel(Model):
    '''
    Third Test for the Boxworld Model
    '''

    height = 25
    width = 25

    initial_walkers = 1
    initial_boxes = 10
    # initial_items = initial_boxes//2  # -- currently divides int and results in a new int (as opposed to float)
    initial_total_items = 10
    # initial_yellow_items = 3
    # initial_green_items = 3
    # initial_blue_items = 4
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

    def __init__(self, height=25, width=25,
                 initial_walkers=1,
                 initial_boxes=10,
                 # initial_items=initial_boxes//2,
                 initial_yellow_items=3,
                 initial_blue_items=4,
                 initial_green_items=3,
                 initial_total_items=10,
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
        self.initial_total_items = initial_total_items
        self.initial_yellow_items = initial_yellow_items
        self.initial_blue_items = initial_blue_items
        self.initial_green_items = initial_green_items
        # self.initial_obstacles = initial_obstacles
        # self.obstacle_length = obstacle_length
        self.map_choice = map_choice

        self.empty_boxes = empty_boxes
        self.full_boxes = full_boxes
        self.all_boxes = all_boxes
        self.obstacles = obstacles

        # Grid
        self.grid_list = []
        for x in range(self.width):
            for y in range(self.height):
                self.grid_list.append((x, y))


        # Spawn Locations
        self.map_one_boxes = [(5, 7), (6, 20), (8, 5 ), (9, 10), (12, 12), (14, 17), (18, 12), (20, 4), (21, 12), (20, 21)]  # increased by 3
        self.map_one_obstacles = [(6, 19), (5, 19), (6, 19), (7, 19), (8, 19), (10, 14), (10, 13), (10, 12), (10, 11), (10, 10), (10, 9),
                             (15, 20), (15, 19), (15, 18), (15, 17), (15, 16), (15, 15), (15, 14), (19, 17),
                             (20, 17), (21, 17), (22, 17), (19, 6), (20, 6), (21, 6)]  # increased by 3

        self.map_two_boxes = [(4, 5), (5, 14), (7, 19), (11, 8), (11, 21), (3, 15), (16, 5), (18, 16), (20, 22), (21, 20)]  # increased by 3
        self.map_two_obstacles = [(4, 10), (5, 10), (6, 10), (9, 22), (9, 21), (9, 20), (9, 19), (9, 18), (9, 17),
                             (13, 10), (13, 9), (13, 8), (13, 7), (13, 6), (13, 5), (18, 18), (19, 18), (20, 18),
                             (21, 18)]  # increased by 3

        self.map_three_boxes = [(3, 5), (5, 18), (9, 18), (9, 21), (3, 13), (14, 16), (3, 18), (19, 20), (20, 18), (21, 7)]  # increased by 3
        self.map_three_obstacles = [(6, 20), (6, 19), (6, 18), (6, 17), (6, 16), (11, 21), (11, 20), (11, 19), (11, 18), (11, 17), (11, 16),
                               (11, 15), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (16, 5), (16, 4), (3, 16), (18, 13),
                               (19, 13), (20, 20), (19, 13), (20, 13)]  # increased by 3

        self.map_four_boxes = [(3, 14), (6, 13), (7, 17), (9, 19), (14, 22), (15, 4), (16, 7), (20, 11), (20, 21), (21, 15)]  # increased by 3
        self.map_four_obstacles = [(5, 18), (5, 17), (5, 16), (5, 15), (5, 14), (5, 13), (5, 12), (5, 11), (8, 19), (8, 18), (8, 17),
                              (8, 18), (11, 20), (11, 19), (11, 18), (11, 17), (18, 18), (19, 18), (20, 18), (21, 18),
                              (22, 18), (18, 8), (19, 8), (20, 8), (21, 8)]  # increased by 3

        self.map_five_boxes = [(4, 10), (6, 13), (7, 20), (11, 6), (14, 17), (15, 18), (18, 12), (19, 21), (3, 21), (21, 12)]  # increased by 3
        self.map_five_obstacles = [(5, 17), (6, 17), (7, 17), (8, 17), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (16, 20),
                              (16, 19), (16, 18), (16, 17), (16, 16), (16, 15), (16, 14), (18, 17), (19, 17), (20, 17), (21, 17),
                              (20, 6), (21, 6), (22, 6)]  # increased by 3

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
        print("Map ", self.map_choice)

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
        for j in range(self.initial_total_items):
            chosen_box = self.empty_boxes.pop(j)
            # print("Box Selected")
                    # chosen_box = self.empty_boxes.popitem()
                    # print("Box Selected")
                    # use the above to pop an arbitrary value from the empty boxes list
            types_available = ["yellow", "blue", "pink"]
            item_type = random.choice(types_available)
            if item_type == "yellow":
                item = yellowItem(chosen_box, self, True)
            elif item_type == "blue":
                item = blueItem(chosen_box, self, True)
            elif item_type == "pink":
                item = pinkItem(chosen_box, self, True)

            self.grid.place_agent(item, chosen_box)
            self.schedule.add(item)
            # print("Coloured Item Added")
            self.full_boxes[j] = chosen_box
            # print("Box Filled")

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