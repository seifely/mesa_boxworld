
import random
import time

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from mesa_boxworld.mesa_boxworld.agents import Walker, ClosedBox, blueItem, yellowItem, pinkItem, Obstacle
from mesa_boxworld.mesa_boxworld.schedule import RandomActivationByType


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
    timed_mode = True

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
                 map_choice=[],
                 simple=3,
                 timed_mode=True):

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
        self.step_count = 0
        self.simple = simple

        self.start_timer = 0

        self.empty_boxes = empty_boxes
        self.full_boxes = full_boxes
        self.all_boxes = all_boxes
        self.obstacles = obstacles
        self.timed_mode = timed_mode

        if timed_mode:
            if self.simple == 1:
                self.time_limit = 10
            elif self.simple == 2:
                self.time_limit = 30
            elif self.simple == 3:
                self.time_limit = 90

        # Grid
        self.grid_list = []
        for x in range(self.width):
            for y in range(self.height):
                self.grid_list.append((x, y))

        # Spawn Locations - Simple
        # NOTE: Could move all of these to another function to save space and to reduce the size of the make boxes/
        # obstacles functions, but for now they live here

        self.map_one_boxes = [(4, 7), (5, 20), (7, 5 ), (8, 10), (11, 12), (13, 17), (17, 12), (19, 4), (20, 12), (19, 21)]  # increased by 3
        self.map_one_obstacles = [(5, 19), (4, 19), (6, 19), (7, 19), (9, 14), (9, 13), (9, 12), (9, 11), (9, 10), (9, 9),
                             (14, 20), (14, 19), (14, 18), (14, 17), (14, 16), (14, 15), (14, 14), (18, 17),
                             (19, 17), (20, 17), (21, 17), (18, 6), (19, 6), (20, 6)]  # increased by 3

        self.map_two_boxes = [(4, 5), (5, 14), (7, 19), (11, 8), (11, 19), (3, 15), (16, 5), (18, 16), (20, 22), (21, 20)]  # increased by 3
        self.map_two_obstacles = [(4, 10), (5, 10), (6, 10), (9, 21), (9, 20), (9, 19), (9, 18), (9, 17),
                             (13, 10), (13, 9), (13, 8), (13, 7), (13, 6), (13, 5), (18, 18), (19, 18), (20, 18),
                             (21, 18)]  # increased by 3

        self.map_three_boxes = [(3, 5), (5, 18), (9, 18), (9, 21), (3, 13), (14, 16), (3, 18), (19, 22), (20, 18), (21, 7)]  # increased by 3
        self.map_three_obstacles = [(6, 20), (6, 19), (6, 18), (6, 17), (6, 16), (11, 21), (11, 20), (11, 19), (11, 18), (11, 17), (11, 16),
                               (11, 15), (16, 6), (16, 5), (16, 7), (16, 8), (16, 4), (3, 16), (2, 16), (18, 13),
                               (19, 13), (20, 20), (19, 20), (18, 20), (19, 13), (20, 13)]  # increased by 3

        self.map_four_boxes = [(3, 14), (6, 13), (7, 17), (9, 19), (14, 22), (15, 4), (16, 7), (20, 11), (20, 21), (21, 15)]  # increased by 3
        self.map_four_obstacles = [(5, 18), (5, 17), (5, 16), (5, 15), (5, 14), (5, 13), (5, 12), (5, 11), (8, 19), (8, 18), (8, 17),
                              (8, 18), (11, 20), (11, 19), (11, 18), (11, 17), (18, 18), (19, 18), (20, 18), (21, 18),
                              (18, 8), (19, 8), (20, 8), (21, 8)]  # increased by 3

        self.map_five_boxes = [(4, 10), (6, 13), (7, 20), (11, 6), (14, 16), (15, 18), (18, 12), (19, 21), (3, 21), (21, 12)]  # increased by 3
        self.map_five_obstacles = [(5, 17), (6, 17), (7, 17), (8, 17), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (16, 20),
                              (16, 19), (16, 18), (16, 17), (16, 16), (16, 15), (16, 14), (18, 17), (19, 17), (20, 17), (21, 17),
                              (20, 6), (21, 6), (19, 6)]  # increased by 3

        # Spawn Locations - Complex
        self.map_six_boxes = [(2,14), (4,9),(6,7), (7,20), (11,9), (11,19), (17,5), (20,14), (21,10), (22,21)]
        self.map_six_obstacles = [(1,12), (2,12), (3,12), (4,12), (4,16), (4,15), (4,14), (4,13), (8,12), (8,11), (8,10), (8,9),
                                  (8,8), (8,7), (8,6), (8,5), (8,4), (8,18), (9,4),(9,12), (10,12), (11,12), (9,21), (9,20), (9,19), (9,18),
                                  (10, 4), (16,8), (17,8), (7,18), (18,8), (19,8), (19,7), (19,6), (19,5), (19,4), (19,21), (19,20),
                                  (19,19), (19,18), (20,18), (21,18)]

        self.map_seven_boxes = [(4,19), (1,11), (7,12), (6,0), (12,20), (14,15), (13,9), (16,3), (20,17), (21,5)]
        self.map_seven_obstacles = [(2,20), (2,19), (2,18), (2,17), (2,16), (3,16), (4,16), (5,16), (6,16), (6,20), (6,19),
                                    (6,18), (6,17), (3,13), (3,12), (3,11), (3,10), (3,9), (3,8), (2,8), (11,12), (11,11),
                                    (11,10), (11,9), (11,8), (11,7), (12,12), (13,12), (14,12), (15,12), (16,12), (16,17),
                                    (16,16), (16,15), (16,14), (16,13), (19,13), (20,12), (21,13), (22,12), (15,4), (16,4),
                                    (17,4), (17,3)]

        self.map_eight_boxes = [(2,22), (3,15), (8,19), (7,6), (11,12), (13,17), (17,1), (18,21), (20,12), (20,8)]
        self.map_eight_obstacles =[(2,19), (3,21), (3,20), (3,19), (4,21), (5,21), (6,18), (7,17), (7,16), (7,15), (8,15),
                                   (9,15), (10,15), (10,20), (10,19), (10,18), (10,17), (10,16), (12,14), (13,14), (14,14),
                                   (14,13), (14,12), (14,11), (14,10), (14,9), (14,8), (17,14), (17,13), (17,12), (17,11),
                                   (17,10), (18,17), (18,16), (18,15), (18,14), (19,17), (20,17), (16,3), (17,3), (18,3)]

        self.map_nine_boxes = [(1,8), (3,5), (6,17), (12,16), (13,7), (14,19), (17,13), (21,18), (23,11), (19,4)]
        self.map_nine_obstacles = [(2,11), (3,11), (4,11), (4,10), (4,9), (5,9), (5,8), (5,7), (5,6), (5,5), (6,15),
                                   (7,15), (8,15), (8,17), (8,16), (11,13), (12,13), (13,13), (14,13), (15,13), (15,20),
                                   (15,19), (15,18), (15,17), (15,16), (15,15), (15,14), (19,20), (19,19), (19,18),
                                   (19,17), (19,16), (19,15), (20,20), (21,20), (20,15), (21,15),
                                   (17,6), (17,5), (17,4), (17,3), (18,6), (19,6), (20,6), (21,6), (21,5), (21,4), (21,3)]

        self.map_ten_boxes = [(1,17), (6,19), (5,15), (3,2), (10,3), (13,18), (15,16), (20,22), (20,11), (15,4)]
        self.map_ten_obstacles = [(3,17), (3,16), (3,15), (3,14), (4,17), (5,17), (6,17), (7,17), (8,17), (8,20), (8,19),
                                  (8,18), (2,4), (3,4), (4,4), (5,4), (5,3), (11,20), (11,19), (11,18), (11,17), (11,16),
                                  (11,15), (12,15), (13,15), (14,15), (14,14), (15,14), (16,14), (16,18), (16,17), (16,16),
                                  (16,15), (9,4), (9,3), (10,4), (11,4), (18,13), (18,12), (18,11), (18,10), (18,9), (19,13),
                                  (20,13), (21,13), (22,13)]

        self.map_eleven_boxes = [(1,20), (5,16), (3,6), (10,10), (12,5), (14,16), (15,9), (17,20), (21,18), (20,5)]
        self.map_eleven_obstacles = [(1,18), (2,18), (3,21), (3,20), (3,19), (3,18), (3,17), (3,16), (3,15), (3,14),
                                     (3,13), (4,19), (5,19), (4,14), (5,14), (5,10), (5,9), (5,8), (5,7), (5,6), (5,5),
                                     (5,4), (6,7), (7,7), (8,7), (8,16), (8,15), (8,14), (8,13), (8,12), (8,11), (8,10),
                                     (8,9), (8,8), (9,13), (10,13), (11,19), (12,19), (13,19), (13,18), (13,17), (13,16),
                                     (13,15), (13,14), (13,13), (14,13), (15,13), (13,22), (14,22), (15,22), (15,21),
                                     (15,20), (15,19), (15,18), (15,17), (15,16), (15,15), (15,14), (16,17), (17,17),
                                     (18,17), (17,16), (17,15), (17,14), (17,13), (17,12), (17,11), (17,10), (17,9),
                                     (17,8), (20,10), (21,10), (22,10), (22,9), (22,8), (22,7), (22,6), (22,5), (22,4),
                                     (19, 4), (20, 4), (21, 4), (19,6), (19,5), (20,8), (20,7), (20,6)]

        self.map_twelve_boxes = [(4,15), (3,7), (7,4), (9,20), (13,17), (16,11), (17,22), (21,15), (22,6), (11,21)]
        self.map_twelve_obstacles = [(2,21), (3,21), (4,21), (5,21), (6,21), (7,21), (7,20), (7,19), (7,18), (7,17),
                                     (7,16), (7,15), (7,14), (7,13), (7,12), (7,11), (2,11), (3,11), (4,11), (5,11),
                                     (6,11), (2,18), (2,17), (2,16), (2,15), (2,14), (2,13), (3,18), (4,18), (5,18),
                                     (2,12), (5,17), (5,16), (5,15), (5,14), (9,13), (10,13), (11,13), (12,13), (9,9),
                                     (10,9), (11,9), (13,9), (14,9), (12,12), (12,11), (12,10), (12,9), (12,8), (12,7),
                                     (12,6), (13,6), (14,6), (15,6), (15,5), (15,4), (15,3), (13,19), (14,19),
                                     (15, 22), (15, 21), (15, 20), (15, 19), (15, 18), (15, 17), (15, 16), (16,19),
                                     (17,19), (18,13), (19,13), (20,20), (20,19), (20,18), (20,17), (20,16), (20,15),
                                     (20,14), (20,13), (20,12), (20,11), (20,10), (20,9), (20,8), (20,7), (20,6), (21,13),
                                     (22,13), (22,20), (22,19), (22,18), (22,17), (22,16), (22,15), (22,14)]

        self.map_thirteen_boxes = [(4,19), (5,15), (12,19), (13,11), (11,4), (15,18), (19,18), (20,13), (21,18), (21,5)]
        self.map_thirteen_obstacles = [(3,21), (4,21), (5,21), (6,21), (3,20), (3,19), (3,18), (3,17), (3,16), (4,17),
                                       (5,17), (5,18), (6,18), (7,18), (7,17), (7,16), (7,15), (7,14), (7,13), (4,13),
                                       (5,13), (6,13), (10,21), (11,21), (12,21), (13,21), (10,20), (10,19), (10,18),
                                       (13, 20), (13, 19), (12,18), (10,16), (10,15), (10,14), (11,14), (12,14), (13,14),
                                       (7, 3), (8, 3), (8,5), (8,4), (7,3), (8,3), (9,7), (9,6), (9,5), (10,7), (11,7),
                                       (12,7), (12,6), (12,5), (12,4), (12,3), (12,2), (13,2), (14,5), (14,4), (14,3),
                                       (17, 13), (18, 13), (18,18), (18,17), (18,16), (18,15), (18,14), (19,16), (20,16),
                                       (21,16), (22,16), (20,20), (20,19), (20,18), (20,17), (21,20), (22,20), (21,15),
                                       (21,14), (21,13), (21,12), (21,11), (20,11), (20,10), (20,9), (18,9), (19,9),
                                       (19, 8), (19, 7), (19, 6)]

        self.map_fourteen_boxes = [(8,18), (4,8), (4,3), (10,15), (10,5), (13,4), (15,11), (15,20), (21,18), (22,7)]
        self.map_fourteen_obstacles = [(3,17), (4,17), (3,20), (4,21), (5,22), (5,18), (6,22), (6,19), (7,21), (7,18),
                                       (8, 20), (9,19), (8,17), (8,16), (8,15), (8,14), (8,13), (9,13), (10,13), (11,13),
                                       (11, 16), (11, 15), (11, 14), (2,10), (3,10), (4,10), (5,9), (5,8), (5,7), (5,6),
                                       (5,5), (3,7), (4,7), (3,5), (4,5), (2,4), (2,3), (2,2), (9,7), (9,6), (10,7),
                                       (11,7), (11,6), (11,5), (11,4), (11,3), (12,3), (13,3), (14,3), (14,5), (14,4),
                                       (14, 20), (15,21), (16,21), (17,21), (14,18), (15,18), (15,17), (15,16), (17,18),
                                       (17,17), (17,16), (18,19), (18,18), (18,8), (18,7), (18,6), (20,6), (21,6), (22,6),
                                       (19, 8), (20, 8), (21, 8), (22, 8), (21,11), (21,10), (21,9), (22,10), (23,10),
                                       (23, 7)]

        self.map_fifteen_boxes = [(6,20), (7,16), (6,10), (4,10), (2,5), (12,6), (16,18), (17,3), (19,6), (21,12)]
        self.map_fifteen_obstacles = [(3,21), (3,20), (3,19), (3,18), (3,17), (3,16), (3,15), (3,14), (4,21), (5,21),
                                      (6,21), (7,21), (7,20), (7,19), (7,18), (5,18), (6,18), (5,17), (5,16), (5,15),
                                      (5,14), (2,12), (3,12), (4,12), (5,12), (6,12), (5,11), (5,10), (5,9), (5,8),
                                      (5,7), (6,9), (7,9), (8,9), (8,14), (8,13), (8,12), (8,11), (8,10), (12,13),
                                      (12, 10), (11,8), (11,7), (11,6), (11,5), (11,4), (11,3), (13,9), (13,8), (13,7),
                                      (13,6), (13,5), (13,4), (13,3), (12,3), (13,12), (14,12), (15,12), (16,12),
                                      (13, 11), (14, 11), (15, 11), (16, 11), (13,21), (14,21), (15,22), (16,22),
                                      (17, 21), (16,20), (14,19), (15,19), (16,19), (15,18), (15,17), (16,17), (17,17),
                                      (18,17), (18,19), (18,18), (20,16), (21,16), (22,20), (22,19), (22,18), (22,17),
                                      (22,16), (22,15), (22,14), (22,13), (19,13), (20,13), (21,13), (20,12), (20,10),
                                      (20,9), (21,9), (22,9), (23,9), (22,8), (22,7), (22,6), (18,9), (18,8), (18,7),
                                      (19, 7), (20, 7), (20,6), (20,5), (20,4)]

        self.map_complexity_data = [[5, 5, 1, 1], [5, 5, 1, 1], [6, 6, 1, 1], [5, 5, 1, 1], [5, 5, 1, 1],
                                    [5, 11, 2, 2.2], [5, 14, 3, 2.8], [5, 13, 3, 2.6], [5, 13, 3, 2.6], [5, 13, 2, 2.6],
                                    [4, 25, 6, 6.5], [4, 22, 5, 5.5], [5, 30, 7, 6], [8, 37, 3, 4.62], [8, 36, 5, 5.42]]

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

    def init_timer(self):
        self.start_timer = time.clock()

    def map_picker(self):
        if self.simple == 1:
            available_maps = ["one", "two", "three", "four", "five"]
            self.map_choice = random.choice(available_maps)
            # self.map_choice = "fifteen"
            print("Map ", self.map_choice)

        elif self.simple == 2:
            available_maps = ["six", "seven", "eight", "nine", "ten"]  # add eleven to fifteen here
            self.map_choice = random.choice(available_maps)
            # self.map_choice = "six"
            print("Map ", self.map_choice)

        elif self.simple == 3:
            available_maps = ["eleven", "twelve", "thirteen", "fourteen", "fifteen"]
            self.map_choice = random.choice(available_maps)
            # self.map_choice = "fifteen"
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

        elif self.map_choice == "six":
            for i in range(self.initial_boxes):
                x, y = self.map_six_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "seven":
            for i in range(self.initial_boxes):
                x, y = self.map_seven_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "eight":
            for i in range(self.initial_boxes):
                x, y = self.map_eight_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "nine":
            for i in range(self.initial_boxes):
                x, y = self.map_nine_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "ten":
            for i in range(self.initial_boxes):
                x, y = self.map_ten_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "eleven":
            for i in range(self.initial_boxes):
                x, y = self.map_eleven_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "twelve":
            for i in range(self.initial_boxes):
                x, y = self.map_twelve_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "thirteen":
            for i in range(self.initial_boxes):
                x, y = self.map_thirteen_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "fourteen":
            for i in range(self.initial_boxes):
                x, y = self.map_fourteen_boxes[i]
                closedBox = ClosedBox((x, y), self, True)
                self.grid.place_agent(closedBox, (x, y))
                self.schedule.add(closedBox)
                # --- append this box's xy to unordered list/dict keyed by the tuples of (x,y)
                self.empty_boxes[i] = (x, y)
                self.all_boxes[i] = (x, y)
                # print("Empty Box Created")

        elif self.map_choice == "fifteen":
            for i in range(self.initial_boxes):
                x, y = self.map_fifteen_boxes[i]
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
            print("Start Position: ", (x, y))
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

        elif self.map_choice == "six":
            for i in range(len(self.map_six_obstacles)):
                x, y = self.map_six_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "seven":
            for i in range(len(self.map_seven_obstacles)):
                x, y = self.map_seven_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "eight":
            for i in range(len(self.map_eight_obstacles)):
                x, y = self.map_eight_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "nine":
            for i in range(len(self.map_nine_obstacles)):
                x, y = self.map_nine_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "ten":
            for i in range(len(self.map_ten_obstacles)):
                x, y = self.map_ten_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "eleven":
            for i in range(len(self.map_eleven_obstacles)):
                x, y = self.map_eleven_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "twelve":
            for i in range(len(self.map_twelve_obstacles)):
                x, y = self.map_twelve_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "thirteen":
            for i in range(len(self.map_thirteen_obstacles)):
                x, y = self.map_thirteen_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "fourteen":
            for i in range(len(self.map_fourteen_obstacles)):
                x, y = self.map_fourteen_obstacles[i]
                obstacle = Obstacle((x, y), self)
                self.grid.place_agent(obstacle, (x, y))
                self.schedule.add(obstacle)
                self.obstacles.append((x, y))

        elif self.map_choice == "fifteen":
            for i in range(len(self.map_fifteen_obstacles)):
                x, y = self.map_fifteen_obstacles[i]
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
        self.step_count += 1

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