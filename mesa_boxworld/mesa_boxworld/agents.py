import random
import math
import csv
import time
import sys


from mesa import Agent
from queue import PriorityQueue
import pickle
from scipy.spatial import distance
import numpy as np
import scipy.stats

# priotyQs (also: Heap Q's) are binary trees where every parent node has a value >= any of its children. It keeps
# track # of the minimum value, helping retrieve that min value at all times

###########################################################################################################


class Walker(Agent):
    '''
    '''

    moore = True
    grid = None
    x = None
    y = None
    stepCount = 0
    goal = []
    closed_box_list = {}
    open_box_list = {}
    goal_reached = False
    next_move = []
    able_to_move = True  # not currently used
    steps_memory = []  # not currently used
    obstacle_present = False
    normal_navigation = True
    navigation_mode = 1
    score = 0
    items_picked_up = 0
    inventory = {}

    # for debugging
    distance_verbose = False
    box_open_verbose = False
    quick_verbose = False

    def __init__(self, pos, model, moore, stepCount=0, goal=[], closed_box_list={}, open_box_list={}, next_move=[],
                 able_to_move=True, steps_memory=[], obstacle_present=False, normal_navigation=True,
                 score=0, inventory={}, items_picked_up=0): # navigation_mode=2
        super().__init__(pos, model)

        # AGENT NOTE: IT ALWAYS TRAVELS ALONG ITS Y AXIS BEFORE ITS X AXIS

        # Bug Notes:
        # Sidestepping has been reduced to +1, doesn't seem to cause an issue for now
        # A* needs some work, as it zooms about too much at the moment

        # randomly select a nav mode to start in: 1 is Reactive, 2 is Deliberative
        # navigation_mode = random.choice([1, 2])
        navigation_mode = 2

        self.moore = moore
        random_n = str(random.randint(1,1001))
        nav_type = str(navigation_mode)
        self.filename = "nav" + nav_type + "_map" + self.model.map_choice + "_" + random_n
        self.next_move = next_move
        self.able_to_move = able_to_move
        self.steps_memory = steps_memory
        self.obstacle_present = obstacle_present
        self.normal_navigation = normal_navigation
        self.navigation_mode = navigation_mode

        self.delib_verbose = False
        self.completed = False
        self.plan_acquired = False

        self.pos = pos
        self.stepCount = stepCount
        self.inter_goal_stepCount = 0
        self.goal = goal
        self.score = score
        self.inventory = inventory
        self.items_picked_up = items_picked_up

        self.closed_box_list = closed_box_list
        self.closed_box_list = self.model.all_boxes  # this used to be set to the full box list, but now agent = blind
        self.open_box_list = open_box_list

        # --------------------------- Metacognitive Inputs: General ----------------------------
        self.planned_path = []
        self.planned_path_cost = []
        self.current_step_time = 0
        self.tt_step = 0
        self.planning_steps_taken = 0
        self.stuck = 0
        self.loop = 0
        self.stress = 0
        self.step_time_memory = []
        self.planning_step_memory = []
        self.average_step_time = 0
        self.goal_distance = 0
        self.switch_cost = 0

        # things we want to track are:
        # program run time - is it going on too long? What are the average completion times for the current map?
        # step length (time) - how long is each step taking? Too long?
        # how much printing is being done - if performance is poor, are we explaining ourselves enough?
        # distance to set goal - does this increase at any point? Do we have to move further away to get closer?
        # is goal blocked
        # amount of memory being used - particularly important if we make large-scale calculations for deliberation
        # where have we been? - step memory that is restricted to a limited size

        # -------------------------- Metacognitive Transformed Outputs -------------------------

        # time performance - each step as a function of total program time (can't be a fraction as this will get
        # infinitely small?)
        # fault monitoring - are we stuck?
        # number of steps as a ratio to distance to goal (smaller is better)
        # current score (next version applications!)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # MAP NODES & STRAT CHOICE - UTILITY PURPOSES

    def use_q(self, n_obstacles, n_branches, mean_branches):
        # get current map complexity data across 3 axes - find closest combination in the training data
        # initialise a k value (make this a global so later functions can change it)
        # for i to len of training data ( there are 30 q value pairs total )
        # want closest k across 3 dimensions, so cloest on x y and z axis
        # set calculated distances in ascending order based on distance

        # import the q_data - we /could/ import this data from the pickle files, but for simplicity we can document it
        # for viewing below. Headings are (n of obstacles, n of total branches, average branch per obst., q-value
        # for strategy 1, q value for strategy 2):
        training_data = ([[5, 5, 1, 10.0, 4.75],
                          [5, 5, 1, 10.0, 2.687],
                          [6, 6, 1, 8.0, 4.125],
                          [5, 5, 1, 10.0, 2.50],
                          [5, 5, 1, 10.0, 3.625],
                          [5, 11, 2.2, 4.5, 7.812],
                          [5, 14, 2.8, 3.375, 7.0],
                          [5, 13, 2.6, 5.062, 8.0],
                          [5, 13, 2.6, 7.125, 5.8125],
                          [5, 13, 2.6, 1.25, 7.562],
                          [4, 25, 6.5, 1.5, 9.937],
                          [4, 22, 5.5, 0.625, 10],
                          [5, 30, 6, 0.625, 9.937],
                          [8, 37, 4.625, 1.937, 9.937],
                          [8, 36, 5.42, 0.25, 9.937]])

        # the above data can be imported from the pickle file 'training_data', plus appended to with future training,
        # using the pickle functions as seen in self.update_q()
        training_spatials = []
        # extract the spatial data for inter-map comparison
        for i in range(len(training_data)):
            x, y, z = training_data[i][0], training_data[i][1], training_data[i][2]
            training_spatials.append([x, y, z])

        # now that we have the 3 dimensions we need to compare, we import our new data
        new_map = [n_obstacles, n_branches, mean_branches]
        training_spatials.append(new_map)
        D = distance.squareform(distance.pdist(training_spatials))  # this gets the euclidean distance between each row
        # and each other row in n-dimensional space
        comparative_row = training_spatials[len(training_spatials)]
        closest = np.argsort(comparative_row, axis=1)  # this gives our new map's row with a list of the row indices
        # that are closest

        # initialise k
        k = 3
        k_nearest_neighbours = (closest[:, 1:k+1])

        # then we select the rows of training_data that are those neighbours
        classifications = []
        for n in k_nearest_neighbours:
            row_n = k_nearest_neighbours[n]
            first_q, second_q = training_data[row_n]
            if first_q > second_q:
                classifications.append(1)
            if first_q < second_q:
                classifications.append(2)

        if scipy.stats.mode(classifications) == 1:
            return 1
        elif scipy.stats.mode(classifications) == 2:
            return 2

    def get_nodes(self):  # the more reliable version!
        all_nodes = self.model.grid_list
        passable_nodes = []
        map_choice = self.model.map_choice

        for item in range(len(all_nodes)):
            value = all_nodes[item]
            if map_choice == "one":
                forbidden_nodes = self.model.map_one_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "two":
                forbidden_nodes = self.model.map_two_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "three":
                forbidden_nodes = self.model.map_three_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "four":
                forbidden_nodes = self.model.map_four_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "five":
                forbidden_nodes = self.model.map_five_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "six":
                forbidden_nodes = self.model.map_six_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "seven":
                forbidden_nodes = self.model.map_seven_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "eight":
                forbidden_nodes = self.model.map_eight_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "nine":
                forbidden_nodes = self.model.map_nine_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "ten":
                forbidden_nodes = self.model.map_ten_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "eleven":
                forbidden_nodes = self.model.map_eleven_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "twelve":
                forbidden_nodes = self.model.map_twelve_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "thirteen":
                forbidden_nodes = self.model.map_thirteen_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "fourteen":
                forbidden_nodes = self.model.map_fourteen_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)
            elif map_choice == "fifteen":
                forbidden_nodes = self.model.map_fifteen_obstacles
                if value not in forbidden_nodes:
                    passable_nodes.append(value)

        return passable_nodes

    def passable(self, id):
        passable_nodes = self.get_nodes()
        if id in passable_nodes:
            return True
        else:
            return False

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.model.width and 0 <= y < self.model.height

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # REACTIVE NAVIGATION - VARIATION ON BUG0 ALGORITHM

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
        self.steps_memory.insert(0, next_move)

    def calculate_box_distances_from_current_pos(self):
        '''
        Calculate the distances to the boxes on the map from the current position.
        '''
        distances_to_boxes = {}
        box_list = self.model.all_boxes
        if self.distance_verbose == True:
            print("Box list is: ", box_list)

        for ii in self.model.all_boxes:
            px, py = self.pos
            qx, qy = box_list[ii]
            # # calculate the euclidean distance to the next box in the list
            distance_to_box = math.sqrt(math.pow((qx - px), 2) + (math.pow((qy - py), 2)))
            if self.distance_verbose == True:
                print("Distance to box is ", distance_to_box)
            distances_to_boxes[ii] = distance_to_box
            if self.distance_verbose == True:
                print("Distance Added")

        if self.distance_verbose == True:
            print("Box Distance Matrix: ", distances_to_boxes)
        return distances_to_boxes

    def set_goal(self):

        distances = self.calculate_box_distances_from_current_pos()
        # furthest_box = max(distances.keys(), key=(lambda k: distances[k]))
        if self.closed_box_list:
            # print("min function arg:", distances.keys())
            closest_box = min(distances.keys(), key=(lambda k: distances[k]))
            if len(self.closed_box_list) == 0:
                closest_box = self.closed_box_list[0]
            # if self.distance_verbose == True:
            # print("Closest Box is: ", closest_box)

            box_goal = closest_box
            # if self.distance_verbose == True:
            print("Goal Box is: ", box_goal)

            goal_coords = self.model.all_boxes[box_goal]
            # if self.distance_verbose == True:
            print("Goal coordinates are:", goal_coords)

            self.goal = goal_coords  # sets the global variable 'goal' to the result of boxgoal
            self.goal_reached = False
            # if self.distance_verbose == True:
            # print("Goal is: ", self.goal)
        if not self.closed_box_list:
            self.goal = self.goal
            print("There's nowhere left to go! I win!")

            # q_val = self.update_q(len(self.open_box_list), 0, 0, 0, 0)
            # self.output_learned_data(q_val)
            sys.exit()

    def reactive_nav(self):

        if self.normal_navigation:
            self.simple_move_goal()
            self.check_for_obstacles(self.next_move)
            print("Bug_nav checked for next move obstacles")
            if self.obstacle_present:
                self.blocked_direction = self.directional_blockage_checker()
                self.normal_navigation = False
                print("Normal navigation turned off.")
            # if not self.obstacle_present:
            #     print("Bug_nav found no obstacle.")
        elif not self.normal_navigation:
            self.bug_navigation(self.blocked_direction)

        elif not self.able_to_move:
            print("I can't move right now.")

    def simple_move_goal(self):
        '''
        Step one cell in any allowable direction towards the closest box.
        '''

        goal = self.goal
        current_x, current_y = self.pos
        goal_x, goal_y = goal

        if self.normal_navigation:
            if self.pos != goal:
                if current_x > goal_x:
                    self.next_move = ((current_x - 1), current_y)
                    self.check_for_obstacles(self.next_move)
                    if self.obstacle_present:
                        self.next_move = ((current_x - 1), current_y)
                        return
                    else:
                        self.model.grid.move_agent(self, self.next_move)
                        self.steps_memory.insert(0, self.next_move)

                elif current_x < goal_x:
                    self.next_move = ((current_x + 1), current_y)
                    self.check_for_obstacles(self.next_move)
                    if self.obstacle_present:
                        self.next_move = ((current_x + 1), current_y)
                        return
                    else:
                        self.model.grid.move_agent(self, self.next_move)
                        self.steps_memory.insert(0, self.next_move)

                if current_y > goal_y:
                    self.next_move = (current_x, (current_y - 1))
                    self.check_for_obstacles(self.next_move)
                    if self.obstacle_present:
                        self.next_move = (current_x, (current_y - 1))
                        return
                    else:
                        self.model.grid.move_agent(self, self.next_move)
                        self.steps_memory.insert(0, self.next_move)

                elif current_y < goal_y:
                    self.next_move = (current_x, (current_y + 1))
                    self.check_for_obstacles(self.next_move)
                    if self.obstacle_present:
                        self.next_move = (current_x, (current_y + 1))
                        return
                    else:
                        self.model.grid.move_agent(self, self.next_move)
                        self.steps_memory.insert(0, self.next_move)

            elif self.pos == self.goal:
                self.goal_reached = True
                print("Goal Reached!")

        elif not self.normal_navigation:
            print("I'm trying to use simple_move_goal but I'm not allowed to.")

    def check_for_freedom(self, goal, current_location):
        obstacle_count = 0
        cells_between = self.points_between(goal, current_location)
        print("Cells between here and my goal are: ", cells_between)

        for each in range(len(cells_between)):
            # print("Cell Observed: ", each)
            # print("obstacle_count: ", obstacle_count)
            if self.check_for_obstacles(cells_between[each]):
                # print("Obstacle in LOS found.")
                obstacle_count = obstacle_count + 1

        if obstacle_count == 0:
            print("Line of Sight to Goal is Not Blocked")
            self.normal_navigation = True
            return True
        if obstacle_count > 0:
            print("Line of Sight to Goal is Blocked")
            return False

            # initiate immediacy of obstacle check? How is the obstacle 1 step away or many?
            # if obstacle is more than one step away (dist_x =< 1, dist_y =< 1)
            # return True

    def check_obj_direction(self, position, target):
        x, y = position
        p, q = target

        if p > x:
            if q == y:
                return "east"
            if q > y:
                return "northeast"
            if q < y:
                return "southeast"
        elif p < x:
            if q == y:
                return "west"
            if q > y:
                return "northwest"
            if q < y:
                return "southwest"

    def follow_wall(self, blocked_direction):
        print("Following wall, blocked direction: ", blocked_direction)
        current_x, current_y = self.pos

        if blocked_direction == "north":
            null_goal = ((current_x - 6), (current_y + 2))
            if self.generic_movement(null_goal):
                self.normal_navigation = True
            return

        elif blocked_direction == "east":
            null_goal = ((current_x + 2), (current_y + 6))
            if self.generic_movement(null_goal):
                self.normal_navigation = True
            return

        elif blocked_direction == "south":
            null_goal = ((current_x + 6), (current_y - 2))
            if self.generic_movement(null_goal):
                self.normal_navigation = True
            return

        elif blocked_direction == "west":
            null_goal = (current_x - 2), (current_y - 6)
            if self.generic_movement(null_goal):
                self.normal_navigation = True
            return

    # def follow_wall(self, blocked_direction):
    #     print("Following wall")
    #     current_x, current_y = self.pos
    #     avoidance_steps = 0
    #     obstacle_width = 2  # this might need to be 2
    #     # get the neighbourhood around self.pos
    #
    #     if blocked_direction == "north":
    #         print("Current XY: ", current_x, current_y)
    #         while self.blocked_north():
    #             print("while self.blocked_north():")
    #             avoidance_move = ((current_x - 1), current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #             avoidance_steps = avoidance_steps + 1
    #             print("     Avoidance Step Value: ", avoidance_steps)
    #
    #         for m in range(obstacle_width):
    #             print("for m in range(obstacle_width):")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = (current_x, (current_y + 1))
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         for n in range(avoidance_steps):
    #             print("n in range(avoidance_steps)")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = ((current_x + 1), current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         self.check_for_freedom()
    #         if self.check_for_freedom():
    #             print("I moved around it!")
    #             self.normal_navigation = True
    #         if not self.check_for_freedom():
    #             print("I fucked up!")
    #             # some kind of recursion
    #
    #     elif blocked_direction == "east":
    #         print("Current XY: ", current_x, current_y)
    #         while self.blocked_east():
    #             print("while self.blocked_east():")
    #             avoidance_move = (current_x, (current_y + 1))
    #             print("     Current XY: ", current_x, current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #             avoidance_steps = avoidance_steps + 1
    #             print("     Avoidance Step Value: ", avoidance_steps)
    #
    #         for m in range(obstacle_width):
    #             print("for m in range(obstacle_width):")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = ((current_x + 1), current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         for n in range(avoidance_steps):
    #             print("n in range(avoidance_steps)")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = (current_x, (current_y - 1))
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         self.check_for_freedom()
    #         if self.check_for_freedom():
    #             print("I moved around it!")
    #             self.normal_navigation = True
    #         if not self.check_for_freedom():
    #             print("I fucked up!")
    #             # some kind of recursion
    #
    #     elif blocked_direction == "south":
    #         print("Current XY: ", current_x, current_y)
    #         while self.blocked_south():
    #             print("while self.blocked_south():")
    #             avoidance_move = ((current_x + 1), current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #             avoidance_steps = avoidance_steps + 1
    #             print("     Avoidance Step Value: ", avoidance_steps)
    #
    #         for m in range(obstacle_width):
    #             print("for m in range(obstacle_width):")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = (current_x, (current_y - 1))
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         for n in range(avoidance_steps):
    #             print("n in range(avoidance_steps)")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = ((current_x - 1), current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         self.check_for_freedom()
    #         if self.check_for_freedom():
    #             print("I moved around it!")
    #             self.normal_navigation = True
    #         if not self.check_for_freedom():
    #             print("I fucked up!")
    #             # some kind of recursion
    #
    #     elif blocked_direction == "west":
    #         print("Current XY: ", current_x, current_y)
    #         while self.blocked_west():
    #             print("while self.blocked_west():")
    #             avoidance_move = (current_x, (current_y - 1))
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #             avoidance_steps = avoidance_steps + 1
    #             print("     Avoidance Step Value: ", avoidance_steps)
    #
    #         for m in range(obstacle_width):
    #             print("for m in range(obstacle_width):")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = ((current_x - 1), current_y)
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         for n in range(avoidance_steps):
    #             print("n in range(avoidance_steps)")
    #             current_x, current_y = self.pos
    #             print("     Current XY: ", current_x, current_y)
    #             avoidance_move = (current_x, (current_y + 1))
    #             print("     Avoidance move coords: ", avoidance_move)
    #             self.model.grid.move_agent(self, avoidance_move)
    #
    #         self.check_for_freedom()
    #         if self.check_for_freedom():
    #             print("I moved around it!")
    #             self.normal_navigation = True
    #         if not self.check_for_freedom():
    #             print("I fucked up!")
    #             # some kind of recursion

    # def blocked_north(self):
    #     current_x, current_y = self.pos
    #
    #     if self.next_move == (current_x, (current_y + 1)):
    #         next_cell = self.model.grid.get_cell_list_contents([self.next_move])
    #         potential_obstacle = [obj for obj in next_cell
    #                               if isinstance(obj, Obstacle)]
    #         if len(potential_obstacle) > 0:
    #             print("Obstacle Detected North!")
    #             # self.able_to_move = False
    #             return True
    #         elif len(potential_obstacle) == 0:
    #             return False
    #
    # def blocked_east(self):
    #     current_x, current_y = self.pos
    #
    #     if self.next_move == ((current_x + 1), current_y):
    #         next_cell = self.model.grid.get_cell_list_contents([self.next_move])
    #         potential_obstacle = [obj for obj in next_cell
    #                               if isinstance(obj, Obstacle)]
    #         if len(potential_obstacle) > 0:
    #             print("Obstacle Detected East!")
    #             # self.able_to_move = False
    #             return True
    #         elif len(potential_obstacle) == 0:
    #             return False
    #
    # def blocked_south(self):
    #     current_x, current_y = self.pos
    #
    #     if self.next_move == (current_x, (current_y - 1)):
    #         next_cell = self.model.grid.get_cell_list_contents([self.next_move])
    #         potential_obstacle = [obj for obj in next_cell
    #                               if isinstance(obj, Obstacle)]
    #         if len(potential_obstacle) > 0:
    #             print("Obstacle Detected South!")
    #             # self.able_to_move = False
    #             return True
    #         elif len(potential_obstacle) == 0:
    #             return False
    #
    # def blocked_west(self):
    #     current_x, current_y = self.pos
    #
    #     if self.next_move == ((current_x - 1), current_y):
    #         next_cell = self.model.grid.get_cell_list_contents([self.next_move])
    #         potential_obstacle = [obj for obj in next_cell
    #                               if isinstance(obj, Obstacle)]
    #         if len(potential_obstacle) > 0:
    #             print("Obstacle Detected West!")
    #             # self.able_to_move = False
    #             return True
    #         elif len(potential_obstacle) == 0:
    #             return False

    def bug_navigation(self, blocked_direction):
        print("Bug Navigation ACTIVATED")
        # blocked_direction = blocked_direction
        # self.follow_wall(blocked_direction)

        # ----------------- FOLLOWING 4 LINES WORK TO GUIDE TO GOAL THEN BREAK BACK TO NORMAL ---------------------
        # null_goal = (0, 0)
        # if self.generic_movement(null_goal):
        #     self.normal_navigation = True
        # return

        if blocked_direction == "north":
            null_goal = self.avoidance_goal_calculator("north", self.pos)

            if self.passable(null_goal) and self.in_bounds(null_goal):
                # null_goal = ((9), (9))
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "east":
            null_goal = self.avoidance_goal_calculator("east", self.pos)
            # null_goal = ((9), (9))

            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "south":
            null_goal = self.avoidance_goal_calculator("south", self.pos)
            # null_goal = ((9), (9))
            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "west":
            null_goal = self.avoidance_goal_calculator("west", self.pos)
            # null_goal = (9), (9)

            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "north_west":
            null_goal = self.avoidance_goal_calculator("north_west", self.pos)
            # null_goal = (9), (9)

            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "north_east":
            null_goal = self.avoidance_goal_calculator("north_east", self.pos)
            # null_goal = (9), (9)

            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "south_east":
            null_goal = self.avoidance_goal_calculator("south_east", self.pos)
            # null_goal = (9), (9)

            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):
                        if self.directional_blockage_checker() == "local_free":
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

        elif blocked_direction == "south_west":
            null_goal = self.avoidance_goal_calculator("south_west", self.pos)
            # null_goal = (9), (9)

            if self.passable(null_goal) and self.in_bounds(null_goal):
                if self.generic_movement(null_goal):
                    if self.check_for_freedom(self.goal, self.pos):
                        if self.left_right_sidestep(blocked_direction, self.pos):
                            print("Normal Navigation turned on.")
                            self.normal_navigation = True
                    elif not self.check_for_freedom(self.goal, self.pos):  # if there is blockage between here and goal
                        if self.directional_blockage_checker() == "local_free":  # but my local area is free
                            if self.left_right_sidestep(blocked_direction, self.pos):
                                print("But, my local area is free of obstacles! I'll turn on Normal Nav")
                                self.normal_navigation = True  # maybe turn this off, have some more checking before that??????????????????????
                                # if self.directional_blockage_checker() == "local_free":
                            else:
                                print("I can't sidestep!")
                                self.stuck += 1
                        else:
                            print("My local area is not free.")
                            return
                    return
            else:
                print("My reactive avoidance goal is impassable. I'm stuck.")
                self.stuck += 1
                return

    # def bug_navigation(self, blocked_direction):
    #     print("Bug Navigation ACTIVATED")
    #     null_goal = self.avoidance_goal_calculator(blocked_direction, self.pos)
    #     self.generic_movement(null_goal)
    #
    #     if self.check_for_freedom():
    #         if self.left_right_sidestep(blocked_direction, self.pos):
    #             print("Turning Normal Navigation on.")
    #             self.normal_navigation = True
    #     elif not self.check_for_freedom():
    #         if self.directional_blockage_checker() == "local_free":
    #
    #             goal_direction = self.check_obj_direction(self.pos, self.goal)
    #             print("Direction of my Goal is: ", goal_direction)
    #             second_null_goal = self.avoidance_goal_calculator(goal_direction, self.pos)
    #             print("Second Null Goal: ", second_null_goal)
    #             self.generic_movement(second_null_goal)
    #             if self.check_for_freedom():
    #                 if self.directional_blockage_checker() == "local_free":
    #                     print("I tried to navigate around a little, now resuming Normal Navigation")
    #                     self.normal_navigation = True
    #                     return
    #                 if self.directional_blockage_checker() != "local_free":
    #                     print("I tried to move around a little and I'm still stuck.")
    #
    #             # for i in range(4):
    #             #     self.random_move()

    def left_right_sidestep(self, blocked_direction, current_position):  # Does this need fixing?
        current_x, current_y = current_position

        if blocked_direction == "north":
            sidestep = (current_x, (current_y + 1))
            if self.passable(sidestep) and self.in_bounds(sidestep):
            # if not self.check_for_obstacles(sidestep):
                print("Sidestepping")
                self.model.grid.move_agent(self, sidestep)
                self.steps_memory.insert(0, sidestep)
                return True
            else:
                print("I can't sidestep, I'm stuck.")
                return False # need some kind of alternative clause

        elif blocked_direction == "east":
            sidestep = ((current_x + 1), current_y)
            if self.passable(sidestep) and self.in_bounds(sidestep):
            # if not self.check_for_obstacles(sidestep):
                print("Sidestepping")
                self.model.grid.move_agent(self, sidestep)
                self.steps_memory.insert(0, sidestep)
                return True
            else:
                print("I can't sidestep, I'm stuck.")
                return False

        elif blocked_direction == "south":
            sidestep = (current_x, (current_y - 1))
            if self.passable(sidestep) and self.in_bounds(sidestep):
            # if not self.check_for_obstacles(sidestep):
                print("Sidestepping")
                self.model.grid.move_agent(self, sidestep)
                self.steps_memory.insert(0, sidestep)
                return True
            else:
                print("I can't sidestep, I'm stuck.")
                return False

        elif blocked_direction == "west":
            sidestep = ((current_x - 1), current_y)
            if self.passable(sidestep) and self.in_bounds(sidestep):
            # if not self.check_for_obstacles(sidestep):
                print("Sidestepping")
                self.model.grid.move_agent(self, sidestep)
                self.steps_memory.insert(0, sidestep)
                return True
            else:
                print("I can't sidestep, I'm stuck.")
                return False

    def avoidance_goal_calculator(self, blocked_direction, current_position):

        current_x, current_y = current_position

        if blocked_direction == "north":
            avoidance_goal = ((current_x - 1), (current_y))
            print("Avoidance Goal Set: ", avoidance_goal)
            # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            return avoidance_goal
            # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "east":
            avoidance_goal = ((current_x), (current_y + 1))
            print("Avoidance Goal Set: ", avoidance_goal)
            # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            return avoidance_goal
            # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "south":
            avoidance_goal = ((current_x + 1), (current_y))
            print("Avoidance Goal Set: ", avoidance_goal)
            # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            return avoidance_goal
            # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "west":
            avoidance_goal = ((current_x), (current_y + 1))
            print("Avoidance Goal Set: ", avoidance_goal)
            # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            return avoidance_goal
            # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
            #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "north_west":
            n = random.choice(range(1))
            if n == 1:
                avoidance_goal = ((current_x - 1), (current_y))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")
            elif n == 0:
                avoidance_goal = ((current_x), (current_y + 1))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "north_east":
            n = random.choice(range(1))
            if n == 1:
                avoidance_goal = ((current_x + 1), (current_y))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")
            elif n == 0:
                avoidance_goal = ((current_x), (current_y + 1))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "south_east":
            n = random.choice(range(1))
            if n == 1:
                avoidance_goal = ((current_x + 1), (current_y))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")
            elif n == 0:
                avoidance_goal = ((current_x), (current_y - 1))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")

        elif blocked_direction == "south_west":
            n = random.choice(range(1))
            if n == 1:
                avoidance_goal = ((current_x - 1), (current_y))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")
            elif n == 0:
                avoidance_goal = ((current_x), (current_y - 1))
                print("Avoidance Goal Set: ", avoidance_goal)
                # if self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                return avoidance_goal
                # elif not self.passable(avoidance_goal) and self.in_bounds(avoidance_goal):
                #     print("That avoidance goal is impassable. I'm stuck.")


    def SYSTEM_ALPHA(self):
        # start = time.clock()

        if self.stepCount == 0:  # this should be done once at the start, then again when a box is opened
            self.calculate_box_distances_from_current_pos()
            self.set_goal()
            self.stepCount += 1
            self.goal_distance = self.get_distance(self.pos, self.goal, False)
            # EACH STEP SHOULD RECORD THE AGENT'S POSITION AND USE POP FOR MEMORY LIMIT?
        else:
            self.stepCount += 1  # This is not needed as the agent can access the step number through other means??
            # print("Goal Reached?", self.goal_reached)
            if self.goal == 0 or []:  # this is a catcher for if the goal has been wiped
                self.calculate_box_distances_from_current_pos()
                self.set_goal()

            self.inter_goal_stepCount += 1
            if not self.goal_reached:
                time_start = time.clock()
                self.reactive_nav()
                time_elapsed = (time.clock() - time_start)
                self.current_step_time = time_elapsed
                print("Reactive Time: ", self.current_step_time)
                self.open_box()
                self.pickup_item()
                print("Current Step:", self.pos)
                print("Next Step: ", self.next_move)
                print("Current Goal:", self.goal)

            if self.goal_reached:
                self.calculate_box_distances_from_current_pos()
                self.set_goal()
                self.goal_distance = self.get_distance(self.pos, self.goal, False)
                print("Current Inventory: ", self.inventory)
                print("Current Score: ", self.score)
                print("Step Count: ", self.stepCount)
                # print("Setting new goal.")
                self.goal_reached = False
                self.inter_goal_stepCount = 0
                if self.box_open_verbose:
                    print("Full Box List: ", self.model.full_boxes)

            # step_time = time.clock() - start
            # print("Step Time: ", step_time)
            # self.step_time_memory.append(step_time)

        # self.output_data()

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # UTILITY FUNCTIONS - GENERAL

    def open_box(self):
        # If there is a Box available at the current location, open it.
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        current_box = [obj for obj in this_cell
                       if isinstance(obj, ClosedBox)]  # object in this cell, if it is an agent of type ClosedBox
        current_box_coords = self.pos

        if len(current_box) > 0:  # if there is a box here
            box_to_consume = random.choice(current_box)  # redundant line, pick a random box to consume

            # if we want the box to be removed altogether
            self.model.grid._remove_agent(self.pos, box_to_consume)
            self.model.schedule.remove(box_to_consume)

            openedBox = OpenedBox(self.pos, self.model)
            self.model.grid.place_agent(openedBox, self.pos)

            current_box_in_list = (
                list(self.model.all_boxes.keys())[list(self.model.all_boxes.values()).index(current_box_coords)])
            # current_full_box_in_list = (
            # list(self.model.full_boxes.keys())[list(self.model.full_boxes.values()).index(current_box_coords)])
            if self.box_open_verbose == True:
                print("Current box in the list is: ", current_box_in_list)
            # this gets the key - for example, the box number

            del self.closed_box_list[current_box_in_list]
            if self.box_open_verbose == True:
                print("Box removed from Closed Box List")
            self.open_box_list[current_box_in_list] = (x, y)
            if self.box_open_verbose == True:
                print("Box added to Open Box List")
                print("Open Box List: ", self.open_box_list)

            # delete that key/value pair from the full boxes list  -  THIS IS ONLY NEEDED WHEN THE ITEMS ARE CONSUMED
            del self.model.full_boxes[current_box_in_list]  # possible bug here

    def pickup_item(self):
        x, y = self.pos

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        pink_item = [obj for obj in this_cell
                     if isinstance(obj, pinkItem)]  # object in this cell, if it is an agent of type xItem
        blue_item = [obj for obj in this_cell
                     if isinstance(obj, blueItem)]
        yellow_item = [obj for obj in this_cell
                       if isinstance(obj, yellowItem)]

        if len(pink_item) > 0:  # if there is a box here
            item_to_consume = random.choice(pink_item)
            item_colour = "pink"
            # print("Item to consume: ", item_to_consume)
            self.model.grid._remove_agent(self.pos, item_to_consume)
            self.score += 2
            self.items_picked_up += 1
            self.inventory[self.items_picked_up] = item_colour

        elif len(yellow_item) > 0:  # if there is a box here
            item_to_consume = random.choice(yellow_item)
            item_colour = "yellow"
            # print("Item to consume: ", item_to_consume)
            self.model.grid._remove_agent(self.pos, item_to_consume)
            self.score -= 1
            self.stress += 10
            self.items_picked_up += 1
            self.inventory[self.items_picked_up] = item_colour

        elif len(blue_item) > 0:
            item_to_consume = random.choice(blue_item)
            item_colour = "blue"
            # print("Item to consume: ", item_to_consume)
            self.model.grid._remove_agent(self.pos, item_to_consume)
            self.score += 1
            self.items_picked_up += 1
            self.inventory[self.items_picked_up] = item_colour

    def directional_blockage_checker(self):
        current_x, current_y = self.pos
        north_cell = (current_x, (current_y + 1))
        north_east_cell = ((current_x + 1), (current_y + 1))
        east_cell = ((current_x + 1), current_y)
        south_east_cell = ((current_x + 1), (current_y - 1))
        south_cell = (current_x, (current_y - 1))
        south_west_cell = ((current_x - 1), (current_y - 1))
        west_cell = ((current_x - 1), current_y)
        north_west_cell = ((current_x - 1), (current_y + 1))

        if self.check_for_obstacles(north_cell):
            print("North blocked.")
            return "north"
        if self.check_for_obstacles(north_east_cell):
            if not self.check_for_obstacles(north_cell):
                if not self.check_for_obstacles(north_west_cell):
                    if not self.check_for_obstacles(west_cell):
                        print("North East blocked.")
                        return "north_east"
        if self.check_for_obstacles(east_cell):
            print("East blocked.")
            return "east"
        if self.check_for_obstacles(south_east_cell):
            if not self.check_for_obstacles(south_cell):
                if not self.check_for_obstacles(south_west_cell):
                    if not self.check_for_obstacles(east_cell):
                        print("South East blocked.")
                        return "south_east"
        if self.check_for_obstacles(south_cell):
            print("South blocked.")
            return "south"
        if self.check_for_obstacles(south_west_cell):
            if not self.check_for_obstacles(south_cell):
                if not self.check_for_obstacles(south_east_cell):
                    if not self.check_for_obstacles(west_cell):
                        print("South West blocked.")
                        return "south_east"
        if self.check_for_obstacles(west_cell):
            print("West blocked.")
            return "west"
        if self.check_for_obstacles(north_west_cell):
            if not self.check_for_obstacles(north_cell):
                if not self.check_for_obstacles(north_east_cell):
                    if not self.check_for_obstacles(east_cell):
                        print("North West blocked.")
                        return "north_west"

        else:
            if not self.check_for_obstacles(north_cell):
                if not self.check_for_obstacles(north_east_cell):
                    if not self.check_for_obstacles(north_west_cell):
                        if not self.check_for_obstacles(south_cell):
                            if not self.check_for_obstacles(south_east_cell):
                                if not self.check_for_obstacles(south_west_cell):
                                    if not self.check_for_obstacles(west_cell):
                                        if not self.check_for_obstacles(east_cell):
                                            return "local_free"

    def points_between(self, p1, p2):
        if p1[0] <= p2[0]:
            xs = range(p1[0] + 1, p2[0]) or [p1[0]]
            ys = range(p1[1] + 1, p2[1]) or [p1[1]]
            return [(x, y) for x in xs for y in ys]
        elif p1[0] > p2[0]:
            swapped_p1 = p2
            swapped_p2 = p1
            xs = range(swapped_p1[0] + 1, swapped_p2[0]) or [swapped_p1[0]]
            ys = range(swapped_p1[1] + 1, swapped_p2[1]) or [swapped_p1[1]]
            return [(x, y) for x in xs for y in ys]  # be aware these will be in reverse order from the point to current

    def generic_movement(self, target):
        # print("Generic Goal Set!")
        goal = target
        current_x, current_y = self.pos
        goal_x, goal_y = goal

        if self.pos != goal:
            if current_x > goal_x:
                # print("goal is:", goal)
                self.next_move = ((current_x - 1), current_y)
                self.check_for_obstacles(self.next_move)
                self.model.grid.move_agent(self, self.next_move)
                self.steps_memory.insert(0, self.next_move)

            elif current_x < goal_x:
                # print("goal is:", goal)
                self.next_move = ((current_x + 1), current_y)
                self.model.grid.move_agent(self, self.next_move)
                self.steps_memory.insert(0, self.next_move)

            if current_y > goal_y:
                # print("goal is:", goal)
                self.next_move = (current_x, (current_y - 1))
                self.check_for_obstacles(self.next_move)
                self.model.grid.move_agent(self, self.next_move)
                self.steps_memory.insert(0, self.next_move)

            elif current_y < goal_y:
                # print("goal is:", goal)
                self.next_move = (current_x, (current_y + 1))
                self.check_for_obstacles(self.next_move)
                self.model.grid.move_agent(self, self.next_move)
                self.steps_memory.insert(0, self.next_move)

        if self.pos == goal:
            # print("Generic Goal Reached!")
            return True  # not quite sure how to use this yet

    def check_for_obstacles(self, cell):
        next_cell = self.model.grid.get_cell_list_contents([cell])
        potential_obstacle = [obj for obj in next_cell
                              if isinstance(obj, Obstacle)]
        if len(potential_obstacle) > 0:
            print("Check for Obstacles = True!")
            self.obstacle_present = True
            return True
        elif len(potential_obstacle) == 0:
            self.obstacle_present = False
            return False

    def output_data(self, total_time, crowdedness, map_complexity, branch_complexity):

        if self.navigation_mode == 1:

            # open the csv file
            # ofile = open('%d.csv' % (self.filename), "a")
            with open('{}.csv'.format(self.filename), 'a', newline='') as csvfile:
                fieldnames = ['mode', 'total_stepcount', 'number_closed_box', 'total_time', 'average_steptime', 'score', 'goal_dist',
                              'crowdedness', 'branch_complex', 'map_complex']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                distance_to_goal = self.get_distance(self.pos, self.goal, False)
                box_numbers = len(self.closed_box_list)

                if self.stepCount == 1:
                    writer.writeheader()
                writer.writerow({'mode': self.navigation_mode, 'total_stepcount': self.stepCount, 'number_closed_box': box_numbers,
                                 'total_time': total_time, 'average_steptime': self.average_step_time, 'score': self.score,
                                 'goal_dist': distance_to_goal, 'crowdedness': crowdedness,
                                 'branch_complex': branch_complexity, 'map_complex': map_complexity})


        elif self.navigation_mode == 2:

            with open('{}.csv'.format(self.filename), 'a', newline='') as csvfile:
                fieldnames = ['mode', 'total_stepcount', 'number_closed_box', 'total_time', 'average_steptime', 'score', 'goal_dist', 'planning_steps',
                              'path_cost', 'crowdedness', 'branch_complex', 'map_complex']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                distance_to_goal = self.get_distance(self.pos, self.goal, False)
                box_numbers = len(self.closed_box_list)

                if self.stepCount == 1:
                    writer.writeheader()
                writer.writerow({'mode': self.navigation_mode, 'total_stepcount': self.stepCount, 'total_time': total_time,'number_closed_box': box_numbers,
                                 'average_steptime': self.average_step_time, 'score': self.score, 'goal_dist': distance_to_goal,
                                 'planning_steps': self.planning_steps_taken, 'path_cost': self.planned_path_cost,
                                 'crowdedness': crowdedness, 'branch_complex': branch_complexity, 'map_complex': map_complexity})




            # TO ADD: Some kind of pause function? We want to stop the agent moving if there is a problem
            # want to stop the agent turning on normal navigation under ALPHA when it encounters difficulties

    def output_learned_data(self, q_value):
        box_score = len(self.open_box_list)
        n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches = self.complexity_judge()

        # save it to our numpy file
        # trial_data = np.matrix([n_obstacles, total_branches, mean_branch_per_obs, self.navigation_mode,
        #                           box_score])
        # f = open('learned.csv', 'a')
        # for iind in range(0):
        #     a = trial_data
        #     np.savetxt(f, a)
        # f.close()

        # state 1 state 2 state 3 action result
        # save it to an excel file too

        with open('{}-training.csv'.format(self.filename), 'a', newline='') as csvfile:
            fieldnames = ['N of Obstacles', 'N of Branches', 'Mean Branches Per Obstacle', 'Action', 'Result', 'Overall Q']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            box_score = len(self.open_box_list)

            if self.stepCount == 1:
                writer.writeheader()

            writer.writerow({'N of Obstacles': n_obstacles, 'N of Branches': total_branches, 'Mean Branches Per Obstacle': mean_branch_per_obs,
                             'Action': self.navigation_mode, 'Result': box_score, 'Overall Q': q_value})

    def pause(self):  # !! This should be employed to clear self.next_move, stop it from going on a mission off the map
        return

    def crowdedness(self, radius):
        x, y = self.pos
        crowdedness = 0

        if radius == 1:
            check_space = [(x, (y +1)), ((x+1), (y+1)), ((x+1), y), ((x+1), (y-1)), (x, (y-1)), ((x-1), (y-1)), ((x-1), y),
                           ((x - 1), (y + 1))]

            for x in range(len(check_space)):
                if not self.passable(check_space[x]):
                    crowdedness += 1

            return crowdedness

        if radius == 2:
            check_space = [(x, (y +1)), ((x+1), (y+1)), ((x+1), y), ((x+1), (y-1)), (x, (y-1)), ((x-1), (y-1)), ((x-1), y),
                           ((x - 1), (y + 1)), (x, (y+2)), ((x+1), (y+2)), ((x+2), (y+2)), ((x+2), (y+1)), ((x+1), y),
                           ((x + 2), (y - 1)), ((x+2), (y-2)), ((x+1), (y-2)), (x, (y-2)), ((x-1), (y-2)), ((x-2), (y-2)),
                           ((x - 2), (y - 1)), ((x-2), y), ((x-1),(y+1)), ((x-2), (y+2)), ((x-1), (y+2))]

            for x in range(len(check_space)):
                if not self.passable(check_space[x]):
                    crowdedness += 1

            return crowdedness

        if radius == 3:
            check_space = [(x, (y +1)), ((x+1), (y+1)), ((x+1), y), ((x+1), (y-1)), (x, (y-1)), ((x-1), (y-1)), ((x-1), y),
                           ((x - 1), (y + 1)), (x, (y+2)), ((x+1), (y+2)), ((x+2), (y+2)), ((x+2), (y+1)), ((x+1), y),
                           ((x + 2), (y - 1)), ((x+2), (y-2)), ((x+1), (y-2)), (x, (y-2)), ((x-1), (y-2)), ((x-2), (y-2)),
                           ((x - 2), (y - 1)), ((x-2), y), ((x-1),(y+1)), ((x-2), (y+2)), ((x-1), (y+2)), (x, (y+3)),
                           ((x + 1), (y + 3)), ((x+2), (y+3)), ((x+2), (y+3)), ((x+3), (y+2)), ((x+3), (y+1)),
                           ((x + 3), y), ((x+3), (y-1)), ((x+3), (y-2)), ((x+3), (y-3)), ((x+2), (y-3)), ((x+1), (y-3)),
                           ((x), (y - 3)), ((x-1), (y-3)), ((x-2), (y-3)), ((x-3), (y-3)), ((x-3), (y-2)), ((x-3), (y-1)),
                           ((x - 3), (y)), ((x-3), (y+1)), ((x-3), (y+2)), ((x-3), (y+3)), ((x-2), (y+3)), ((x-1), (y+3))]

            for x in range(len(check_space)):
                if not self.passable(check_space[x]):
                    crowdedness += 1

            return crowdedness

        elif radius != 1 or 2 or 3:
            print("Radius input error")
            return

    def complexity_judge(self):
        # number of branches are going to be represented by the number of duplicate x or y's in the obstacle array?
        # i could provide this as a flat number for each map (easier), number of branches
        # OR I could provide it with the PERCENTAGE OF MAP COVERED BY OBSTACLE but that doesn't represent complexity
        complexity_value = 0

        if self.model.map_choice == "one":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[0]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "two":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[1]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "three":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[2]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "four":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[3]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "five":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[4]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "six":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[5]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "seven":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[6]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "eight":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[7]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "nine":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[8]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "ten":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[9]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "eleven":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[10]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "twelve":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[11]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "thirteen":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[12]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "fourteen":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[13]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

        elif self.model.map_choice == "fifteen":
            n_obstacles, total_branches, modal_branch_per_obs, mean_branch_per_obs = self.model.map_complexity_data[14]
            return n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # DELIBERATIVE NAVIGATION - A* ALGORITHM

    def deliberative_nav(self):
        starter = time.clock()
        # self.get_nodes()  # sets the global 'self.passable_nodes' to the list of non-obstacle map points
        came_from, cost_so_far, planning_step = self.astar_search(self.pos, self.goal)
        path, path_cost = self.reconstruct_path(came_from, self.pos, self.goal)
        print("Planning steps taken: ", planning_step)
        # now we need a navigation system to take this path and use it
        # we also need to time this process so that we can have feedback on it

        plan_time = time.clock() - starter
        print("Planning Time Taken: ", plan_time)

        return path, path_cost, planning_step

        # generate a list of possible next steps (children) toward the goal from current pos
        # store in ordered list (priority queue), based on distance to goal, closest first
        # select closest child to the goal
        # repeat until goal reached or no more children.
        #  --- two important factors: how you measure distance to goal, and how to generate children

    def get_neighbours(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if self.delib_verbose:
            print("Neighbours of", id, ": ", results)
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        passable_results =[]

        for x in range(len(results)):
            value = results[x]
            # if self.delib_verbose:
            #     print("Value:", value)
            if self.passable(value):
                # if self.delib_verbose:
                    # print("Value is Passable")
                if self.in_bounds(value):
                    # if self.delib_verbose:
                    #     print("Value is in Bounds")
                    passable_results.append(value)
                    if self.delib_verbose:
                        print("Neighbour Added.")

        # results = filter(self.passable, results)  # need to find a way to check if the neighbours are passable or not
        if self.delib_verbose:
            print("Passable Neighbours: ", passable_results)
        return passable_results

    def get_distance(self, current, target, euclid=False):
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

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def get_cost(self, a, b):
        distance = self.get_distance(a, b, euclid=False)
        return 3*abs(distance)

    def astar_search(self, start, goal):  # doesn't actually use node list as we check for passability in neighbours
        frontier = PriorityQueue()
        if self.delib_verbose:
            print("Established Frontier Q")
        frontier.put(start, 0)
        if self.delib_verbose:
            print("Put start location")
        came_from = {}
        if self.delib_verbose:
            print("Opened Came From")
        cost_so_far = {}
        if self.delib_verbose:
            print("Opened Cost So Far")
        came_from[start] = None
        cost_so_far[start] = 0
        planning_step = 0

        while not frontier.empty():
            planning_step += 1
            if self.delib_verbose:
                print("Frontier isn't empty")
            current = frontier.get()
            if self.delib_verbose:
                print("Current:", current)
            if current == goal:
                break

            for next in self.get_neighbours(current):
                if self.delib_verbose:
                    print("Neighbours of current are:", self.get_neighbours(current))
                new_cost = cost_so_far[current] + self.get_cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far [next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        if self.delib_verbose:
            print("Came From List: ", came_from)
            print("Cost So Far: ", cost_so_far)
        return came_from, cost_so_far, planning_step

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []

        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional
        print("Start Point:", self.pos, "Goal Point: ", self.goal)
        print("Path Length: ", len(path)) # "Reconstructed Path: ", path,
        path_cost = 0
        for each in range(len(path)):
            coord_cost = self.get_cost(path[each], self.goal)
            path_cost = path_cost + coord_cost
        print("Successful Path Cost: ", path_cost)
        return path, path_cost

    def SYSTEM_BETA(self):
        # start = time.clock()
        if self.stepCount == 0:
            self.calculate_box_distances_from_current_pos()
            self.set_goal()
            self.stepCount += 1
            self.goal_distance = self.get_distance(self.pos, self.goal, False)

        else:
            self.stepCount += 1
            self.inter_goal_stepCount += 1
            if self.goal == 0 or []:  # this is a catcher for if the goal has been wiped
                self.calculate_box_distances_from_current_pos()
                self.set_goal()

            if not self.goal_reached:
                if not self.plan_acquired:
                    path, path_cost, planning_step = self.deliberative_nav()
                    self.planned_path = path
                    self.planned_path_cost = path_cost
                    self.planning_steps_taken = planning_step
                    # self.current_step_time = time_elapsed
                    # print("Planning Time Elapsed: ", time_elapsed)
                    self.plan_acquired = True

                if self.plan_acquired:
                    next_step = self.planned_path.pop(0)
                    # self.model.grid.move_agent(self, next_step)
                    # self.steps_memory.insert(0, next_step)
                    # print("Took my next step...")
                    self.generic_movement(next_step)

                    self.open_box()
                    self.pickup_item()
                    if self.pos == self.goal:
                        self.goal_reached = True

            if self.goal_reached:
                self.calculate_box_distances_from_current_pos()
                self.set_goal()
                self.goal_distance = self.get_distance(self.pos, self.goal, False)
                print("Current Inventory: ", self.inventory)
                self.inter_goal_stepCount = 0
                # print("Setting new goal.")
                self.goal_reached = False
                self.plan_acquired = False

            # self.output_data()
            # step_time = time.clock() - start
            # self.current_step_time = step_time
            # self.step_time_memory.append(step_time)
            print("Current Score: ", self.score, "Step Count: ", self.stepCount)
            # print("Step Time:", step_time)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # META COGNITION A

    def loop_monitor(self, step_memory):
        if len(step_memory) >= 3:
            if step_memory[0] == step_memory[2]:
                self.loop += 0.125  # this value is set cautiously to prevent unnecessary switching whilst in A*
                print("I may be looping. Loop Value now at: ", self.loop)
        if len(step_memory) >= 4:
            if step_memory[0] == step_memory[3]:
                self.loop += 0.125
                print("I may be looping. Loop Value now at: ", self.loop)
        if len(step_memory) >= 5:
            if step_memory[0] == step_memory[4]:
                # this will do for now, as long as the agent retraces steps in lines rather than going in CIRCLES
                # a circular catcher is harder as we have no idea the size of circle
                self.loop += 0.125
                print("I may be looping. Loop Value now at: ", self.loop)

        if len(step_memory) >= 7:
            if step_memory[0] == step_memory[6]:
                self.loop += 0.125  # this should catch circular loops (I think?)
                print("I may be looping. Loop Value now at: ", self.loop)
        if len(step_memory) >= 9:
            if step_memory[0] == step_memory[8]:
                self.loop += 0.125  # this should catch circular loops (I think?)
                print("I may be looping. Loop Value now at: ", self.loop)


    def meta_monitoring(self, path_length, path_cost, running_time, step_memory, score, steps_since_last_goal,
                        distance_to_goal, ):
        crowdedness = self.crowdedness(3)
        n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches = self.complexity_judge()

        if len(self.step_time_memory) > 0:
            self.average_step_time = sum(self.step_time_memory)/len(self.step_time_memory)
        # need to store these to a new list, check the list for increasing values or decreases from the previous step?
        total_time = sum(self.step_time_memory)
        print("Average Step Time:", self.average_step_time, "Total Step Time: ", total_time)

        # loop checking is for checking if we have gotten stuck in a movement loop thanks to reactive behaviour.
        # ideally, it checks for if any value comes up twice in a short space - the shortest check we can do is if
        # x o x has occurred as a movement (e.g. (2,3) -> (2,4) -> (2,3))
        #   this may happen reasonably as a part of inefficient progress, so increment the stuck value slowly, as we
        #   need to employ caution.

        # steps left, time left

        if steps_since_last_goal != 0 and distance_to_goal != 0:
            progress_ratio = steps_since_last_goal/distance_to_goal

            print("Progress Ratio: ", progress_ratio)
            progress_queue = []
            if len(progress_queue) < 2:
                progress_queue.append(progress_ratio)

            elif len(progress_queue) >= 2:
                progress_queue.pop(0)
                progress_queue.append(progress_ratio)

            if len(progress_queue) >= 2:
                if progress_queue.index(0) < progress_queue.index(1):  # if the previous step's ratio is lower than our current ratio, doing better
                    print("Progress Queue: ", progress_queue)
                    return

                elif progress_queue.index(0) > progress_queue.index(1):  # if the previous step's ratio is higher than ours, doing worse
                    print("Progress Queue: ", progress_queue)
                    return

        # NEED AN 'IF PERFORMANCE DROPS, CHANGE AN X VALUE IN THE SYSTEM TO IMPROVE PERFORMANCE'


        self.loop_monitor(step_memory)
        return self.average_step_time, total_time, crowdedness, n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches
        # return

    # should there be some kind of third function that makes the decision on what the best course of action is?

    def meta_actor(self, time_performance, planning_performance, stuck_level, loop_check,):  # this needs to be done better
        switch_threshold = 0

        if stuck_level >= 1:  # NEED TO IMPLEMENT AN INCREASE IN STUCK LEVEL WHEN IT IS STUCK FOR THIS TO ACTUALLY WORK
            switch_threshold += 1

        # if loop_check >= 1:
        #     switch_threshold += 1

        # if switch_threshold >= 1:
        #     sys.exit()
            # self.switch()
            # self.switch_cost += 50

        # can change threshold values? So if switching is occurring VERY OFTEN, make the loop and stuck checkers more cautious
        # need to implement a cost for switching

    def switch(self):
        if self.navigation_mode == 1:
            print("Switching ALPHA to BETA")
            self.navigation_mode = 2
            self.stuck = 0
            self.loop = 0
            self.steps_memory = []
            self.steps_memory.insert(0, self.pos)
        elif self.navigation_mode == 2:
            print("Switching BETA to ALPHA")
            self.navigation_mode = 1
            self.stuck = 0
            self.loop = 0
            self.steps_memory = []
            self.steps_memory.insert(0, self.pos)

    def update_q(self, score, strategy, state, learning_rate, gamma):

        initial_run = False

        # have a numpy matrix stored that we can access and update
        # matrix iteration goes mat[i][j], where i is row and j is column

        # if there is no pickle for that map, create one - a zero 2D matrix
        # if there is a pickle for that map, load it - THIS IS OUR Q TABLE

        file_name = "map15_q_values"

        if initial_run:
            new_q = [0, 0]
            new_file = open(file_name, 'wb')
            pickle.dump(new_q, new_file)
            new_file.close()

            # then load this value, and alter the correct one based on strategy used]#
            fileRead = open(file_name, 'rb')
            imported_q = pickle.load(fileRead)
            fileWrite = open(file_name, 'wb')

            if self.navigation_mode == 1:
                if initial_run:
                    imported_q[0] = score

                    new_q = imported_q
                    pickle.dump(new_q, fileWrite)
                    fileWrite.close()
                    return new_q

                elif not initial_run:
                    if imported_q[0] == 0:
                        imported_q[0] = score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

                    else:
                        imported_q[0] = (imported_q[0] + score) / 2  # if averaging over the trials
                        # imported_q[0] = (imported_q[0] + learning_rate) * score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

            if self.navigation_mode == 2:
                if initial_run:
                    imported_q[1] = score

                    new_q = imported_q
                    pickle.dump(new_q, fileWrite)
                    fileWrite.close()
                    return new_q

                elif not initial_run:
                    if imported_q[1] == 0:
                        imported_q[1] = score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

                    else:
                        imported_q[1] = (imported_q[1] + score) / 2  # if averaging over the trials
                        # imported_q[1] = (imported_q[1] + learning_rate) * score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

        elif not initial_run:
            fileRead = open(file_name, 'rb')
            imported_q = pickle.load(fileRead)
            fileWrite = open(file_name, 'wb')

            if self.navigation_mode == 1:
                if initial_run:
                    imported_q[0] = score

                    new_q = imported_q
                    pickle.dump(new_q, fileWrite)
                    fileWrite.close()
                    return new_q

                elif not initial_run:
                    if imported_q[0] == 0:
                        imported_q[0] = score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

                    else:
                        imported_q[0] = (imported_q[0] + score) / 2  # if averaging over the trials
                        # imported_q[0] = (imported_q[0] + learning_rate) * score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

            if self.navigation_mode == 2:
                if initial_run:
                    imported_q[1] = score

                    new_q = imported_q
                    pickle.dump(new_q, fileWrite)
                    fileWrite.close()
                    return new_q

                elif not initial_run:
                    if imported_q[1] == 0:
                        imported_q[1] = score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q

                    else:
                        imported_q[1] = (imported_q[1] + score) / 2  # if averaging over the trials
                        # imported_q[1] = (imported_q[1] + learning_rate) * score

                        new_q = imported_q
                        pickle.dump(new_q, fileWrite)
                        fileWrite.close()
                        return new_q


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # META COGNITION B

    def update_performance_memory(self):
        return

    def check_performance_memory(self):
        return

    def judge_choice(self):
        return

    # this needs to be a system that checks the reliability of the other system
    # type 1 falls down when we train on a subset and then fail to generalise
    # bayesian trustworthiness based on some kind of memory?

    # can override the meta actors in META A if it does not trust the response based on a lookup table
    # calculate some kind of distance from current (new) scenario to learned scenarios, and the greater the distance
    # the less trustworthy the response should be?


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    def step(self):
        '''
        A model step. Depending on the Nav Mode being used, either use reactive navigation to reach the closest
        unopened box, or use A* navigation to traverse the map.
        '''

        if self.stepCount == 0:
            self.use_q()

        start = time.clock()
        print("obl: ", len(self.open_box_list))
        if self.stepCount != 0:
            # print("Inter goal step:", self.inter_goal_stepCount)
            # print("Goal distance: ", self.goal_distance)
            av_step, tt_step, crowdedness, n_obstacles, modal_branch_per_obs, mean_branch_per_obs, total_branches = self.meta_monitoring(0, 0, 0, self.steps_memory,
                                                                        self.score, self.inter_goal_stepCount,
                                                                        self.goal_distance)
            # print("Average and Total Step Time:", av_step, tt_step)
            self.meta_actor(0, 0, self.stuck, self.loop)  # this could take in 'time remaining' -
            # e.g. if we are in last ten seconds and there are still boxes, switch to reactive
            self.tt_step = tt_step
            # self.output_data(tt_step, crowdedness, map_complex, branch_complex)

        # print("Step Memory:", self.steps_memory)

        # Navigation Systems
        if self.navigation_mode == 1:
            self.SYSTEM_ALPHA()

        elif self.navigation_mode == 2:
            self.SYSTEM_BETA()

        step_time = time.clock() - start
        time_remaining = self.model.time_limit - self.tt_step  # could use this as
        self.step_time_memory.append(step_time)  # this results in step time memory being step t-1?
        if self.tt_step > self.model.time_limit:
            print("Time's up!")

            # do I record the run data here as an internal variable?
            # q_val = self.update_q(len(self.open_box_list),0,0,0,0)
            # self.output_learned_data(q_val)
            sys.exit()

        # depending on what stress levels are, set resources available: how far we can check back (for looping),
        # change switching costs/thresholds (so we under or overvalue switching), less access to information such as
        #


    ############################################################################################################


class ClosedBox(Agent):
    ''' Want this to spawn a random box at locations around the map, on layer 2, can be removed '''

    def __init__(self, pos, model, opened=False, closed=True, countup=0):
        super().__init__(pos, model)
        self.opened = opened
        self.countup = countup
        self.closed = closed

    def step(self):
        if not self.opened:
            self.countup += 1
            print(self.countup)


class OpenedBox(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)


#########################################################################################################

class blueItem(Agent):
    ''' Want this to spawn a random item at locations under boxes, on layer 2, can be removed '''

    def __init__(self, pos, model, decay=15, colour="blue", itemValue=1):
        super().__init__(pos, model)
        self.decay = decay
        self.colour = colour
        self.itemValue = itemValue

    def step(self):
            self.decay -= 1
            print(self.decay)


class yellowItem(Agent):
    ''' Want this to spawn a random item at locations under boxes, on layer 2, can be removed '''

    def __init__(self, pos, model, decay=15, colour="yellow", itemValue=-1):
        super().__init__(pos, model)
        self.decay = decay
        self.colour = colour
        self.itemValue = itemValue

    def step(self):
            self.decay -= 1
            print(self.decay)


class pinkItem(Agent):
    ''' Want this to spawn a random item at locations under boxes, on layer 2, can be removed '''

    def __init__(self, pos, model, decay=15, colour="green", itemValue=2):
        super().__init__(pos, model)
        self.decay = decay
        self.colour = colour
        self.itemValue = itemValue

    def step(self):
            self.decay -= 1
            print(self.decay)



#########################################################################################################


class Obstacle(Agent):
    ''' Grey agents that are impassable, that Walker agents must navigate around. Cannot spawn over boxes. '''

    def __init__(self, pos, model):
        super().__init__(pos, model)

    def step(self):
        return

