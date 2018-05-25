

import random

from mesa import Model
from mesa.space import MultiGrid
# from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from mesa_boxworld.agents import Walker, ClosedBox, OpenedBox, Item
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

    empty_boxes = {}
    full_boxes = {}
    known_items = {}
    all_boxes = {}

    verbose = False  # Print-monitoring

    description = 'A model for simulating wolf and sheep (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_walkers=1,
                 initial_boxes=10,
                 # initial_items=initial_boxes//2,
                 initial_items=10,
                 empty_boxes={},
                 full_boxes={},
                 all_boxes={}):

        # Model Parameters Init
        self.height = height
        self.width = width
        self.initial_walkers = initial_walkers
        self.initial_boxes = initial_boxes
        self.initial_items = initial_items

        self.empty_boxes = empty_boxes
        self.full_boxes = full_boxes
        self.all_boxes = all_boxes

        # Model Functions
        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"Walkers": lambda m: m.schedule.get_type_count(Walker)})

        self.make_walker_agents()
        self.make_boxes()
        self.make_items()

        # Create Walker:
    def make_walker_agents(self):
        for i in range(self.initial_walkers):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            walker = Walker((x, y), self, True)
            self.grid.place_agent(walker, (x, y))
            self.schedule.add(walker)

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
            print("Empty Box Created")

    def make_items(self):
        # this function takes the dictionary of empty boxes, selects one and puts an item in it
        for j in range(self.initial_items):
            chosen_box = self.empty_boxes.pop(j)
            print("Box Selected")
            # chosen_box = self.empty_boxes.popitem()
            # print("Box Selected")
            # use the above to pop an arbitrary value from the empty boxes list
            item = Item(chosen_box, self, True)
            self.grid.place_agent(item, chosen_box)
            self.schedule.add(item)
            print("Item Added")
            self.full_boxes[j] = chosen_box
            print("Box Filled")

        # if a random item placement is needed, uncomment below:
        # for i in range(self.initial_items):
        #     x = random.randrange(self.width)
        #     y = random.randrange(self.height)
        #     item = Item((x, y), self, True)
        #     self.grid.place_agent(item, (x, y))
        #     self.schedule.add(item)

        self.running = True
        self.datacollector.collect(self)

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
                  self.schedule.get_type_count(Walker))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number walkers: ',
                  self.schedule.get_type_count(Walker))

