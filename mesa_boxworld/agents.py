import random
import math
import operator

from mesa import Agent

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
    goal_reached = False  # not currently used
    next_move = []
    avoidance_goal = []  # not currently used
    avoidance_check = [] # used???
    able_to_move = True  # not currently used
    steps_memory = []  # not currently used
    obstacle_present = False
    normal_navigation = True

    # for debugging
    distance_verbose = False
    box_open_verbose = False
    quick_verbose = False

    def __init__(self, pos, model, moore, stepCount=0, goal=[], closed_box_list={}, open_box_list={}, next_move=[],
                 able_to_move=True, steps_memory=[], obstacle_present=False, avoidance_goal=[], avoidance_check=[],
                 normal_navigation=True):
        super().__init__(pos, model)
        self.moore = moore
        self.pos = pos
        self.stepCount = stepCount
        self.goal = goal
        self.next_move = next_move
        self.avoidance_goal = avoidance_goal
        self.avoidance_check = avoidance_check
        self.able_to_move = able_to_move
        self.steps_memory = steps_memory
        self.obstacle_present = obstacle_present
        self.normal_navigation = normal_navigation

        self.closed_box_list = closed_box_list
        self.closed_box_list = self.model.all_boxes  # this used to be set to the full box list, but now agent = blind
        self.open_box_list = open_box_list

        # AGENT NOTE: IT ALWAYS TRAVELS ALONG ITS Y AXIS BEFORE ITS X AXIS?

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

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
            distance_to_box = math.sqrt(math.pow((qx-px), 2) + (math.pow((qy-py), 2)))
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
        furthest_box = max(distances.keys(), key=(lambda k: distances[k]))
        closest_box = min(distances.keys(), key=(lambda k: distances[k]))
        if self.distance_verbose == True:
            print("Closest Box is: ", closest_box)

        box_goal = closest_box
        if self.distance_verbose == True:
            print("Goal Box is: ", box_goal)

        goal_coords = self.model.all_boxes[box_goal]
        if self.distance_verbose == True:
            print("Goal coordinates are:", goal_coords)

        self.goal = goal_coords  # sets the global variable 'goal' to the result of boxgoal
        self.goal_reached = False
        if self.distance_verbose == True:
            print("Goal is: ", self.goal)

    def bug0_nav(self):

        if self.normal_navigation:
            self.simple_move_goal()
            self.check_for_obstacles(self.next_move)
            print("Bug_nav checked for next move obstacles")
            if self.obstacle_present:
                self.normal_navigation = False
                print("Normal navigation turned off.")
            # if not self.obstacle_present:
            #     print("Bug_nav found no obstacle.")
        elif not self.normal_navigation:
            self.bug_navigation()

        elif not self.able_to_move:
            print("I can't move right now.")

    def simple_move_goal(self):
        '''
        Step one cell in any allowable direction towards the closest box.
        '''

        goal = self.goal
        current_x, current_y = self.pos
        goal_x, goal_y = goal

        if self.pos != goal:
            if current_x > goal_x:
                self.next_move = ((current_x - 1), current_y)
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = ((current_x - 1), current_y)
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

            elif current_x < goal_x:
                self.next_move = ((current_x + 1), current_y)
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = ((current_x + 1), current_y)
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

            if current_y > goal_y:
                self.next_move = (current_x, (current_y - 1))
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = (current_x, (current_y - 1))
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

            elif current_y < goal_y:
                self.next_move = (current_x, (current_y + 1))
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = (current_x, (current_y + 1))
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

        elif self.pos == self.goal:
            self.goal_reached = True
            print("Goal Reached!")

    def generic_movement(self, target):

        goal = target
        current_x, current_y = self.pos
        goal_x, goal_y = goal

        if self.pos != goal:
            if current_x > goal_x:
                self.next_move = ((current_x - 1), current_y)
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = ((current_x - 1), current_y)
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

            elif current_x < goal_x:
                self.next_move = ((current_x + 1), current_y)
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = ((current_x + 1), current_y)
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

            if current_y > goal_y:
                self.next_move = (current_x, (current_y - 1))
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = (current_x, (current_y - 1))
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

            elif current_y < goal_y:
                self.next_move = (current_x, (current_y + 1))
                self.check_for_obstacles(self.next_move)
                if self.obstacle_present:
                    self.next_move = (current_x, (current_y + 1))
                    return
                else:
                    self.model.grid.move_agent(self, self.next_move)

        elif self.pos == self.goal:
            return True  # not quite sure how to use this yet

    def check_for_obstacles(self, cell):  # no longer used, generic obstacle checking
        next_cell = self.model.grid.get_cell_list_contents([cell])
        potential_obstacle = [obj for obj in next_cell
                              if isinstance(obj, Obstacle)]
        if len(potential_obstacle) > 0:
            print("Generic Obstacle Detected!")
            self.obstacle_present = True
            return True
        elif len(potential_obstacle) == 0:
            self.obstacle_present = False
            return False

    def check_neighbourhood(self):
        return

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

    def check_for_freedom(self):
        obstacle_count = 0
        goal = self.goal
        current_location = self.pos
        cells_between = self.points_between(goal, current_location)
        print("Cells between here and my goal are: ", cells_between)

        for each in range(len(cells_between)):
            print("Cell Observed: ", each)
            print("obstacle_count: ", obstacle_count)
            if self.check_for_obstacles(cells_between[each]):
                print("Obstacle in LOS found.")
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

    def follow_wall(self, blocked_direction):
        print("Following wall")
        current_x, current_y = self.pos
        avoidance_steps = 0
        obstacle_width = 2  # this might need to be 2
        # get the neighbourhood around self.pos

        if blocked_direction == "north":
            print("Current XY: ", current_x, current_y)
            move_left = ((current_x - 4), current_y)
            self.generic_movement(move_left)
            clear_obstacle = (current_x, (current_y + 2))
            self.generic_movement(clear_obstacle)
            move_right = ((current_x + 4), current_y)
            self.generic_movement(move_right)

        elif blocked_direction == "east":
            print("Current XY: ", current_x, current_y)
            move_left = (current_x, (current_y + 4))
            self.generic_movement(move_left)
            clear_obstacle = ((current_x + 2), current_y)
            self.generic_movement(clear_obstacle)
            move_right = (current_x, (current_y - 4))
            self.generic_movement(move_right)

        elif blocked_direction == "south":
            print("Current XY: ", current_x, current_y)
            move_left = ((current_x + 4), current_y)
            self.generic_movement(move_left)
            clear_obstacle = (current_x, (current_y - 2))
            self.generic_movement(clear_obstacle)
            move_right = ((current_x - 4), current_y)
            self.generic_movement(move_right)

        elif blocked_direction == "west":
            print("Current XY: ", current_x, current_y)
            move_left = (current_x, (current_y - 4))
            self.generic_movement(move_left)
            clear_obstacle = ((current_x - 2), current_y)
            self.generic_movement(clear_obstacle)
            move_right = (current_x, (current_y + 4))
            self.generic_movement(move_right)

        self.check_for_freedom()
        if self.check_for_freedom():
            print("I moved around it!")
            self.normal_navigation = True
        if not self.check_for_freedom():
            print("I fucked up!")
            # some kind of recursion

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

    def directional_blockage_checker(self):
        current_x, current_y = self.pos
        north_cell = (current_x, (current_y + 1))
        east_cell = ((current_x + 1), current_y)
        south_cell = (current_x, (current_y - 1))
        west_cell = ((current_x - 1), current_y)

        if self.check_for_obstacles(north_cell):
            print("North blocked.")
            return "north"
        if self.check_for_obstacles(east_cell):
            print("East blocked.")
            return "east"
        if self.check_for_obstacles(south_cell):
            print("South blocked.")
            return "south"
        if self.check_for_obstacles(west_cell):
            print("West blocked.")
            return "west"

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

    def bug_navigation(self):
        print("Bug Navigation ACTIVATED")

        self.follow_wall(self.directional_blockage_checker())


        # self.check_for_freedom()
        # if self.check_for_freedom():
        #     self.normal_navigation = True

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
            if self. box_open_verbose == True:
                print("Box removed from Closed Box List")
            self.open_box_list[current_box_in_list] = (x, y)
            if self.box_open_verbose == True:
                print("Box added to Open Box List")
                print("Open Box List: ", self.open_box_list)

            # delete that key/value pair from the full boxes list  -  THIS IS ONLY NEEDED WHEN THE ITEMS ARE CONSUMED
            # del self.model.full_boxes[current_full_box_in_list]

    def step(self):
        '''
        A model step. Move, open box if possible.
        '''
        if self.stepCount == 0: # this should be done once at the start, then again when a box is opened
            self.calculate_box_distances_from_current_pos()
            self.set_goal()
            self.stepCount += 1
            # EACH STEP SHOULD RECORD THE AGENT'S POSITION AND USE POP FOR MEMORY LIMIT
        else:
            self.stepCount += 1  # This is not needed as the agent can access the step number through other means??
            # print("Goal Reached?", self.goal_reached)
            if self.goal_reached == False :
                self.bug0_nav()
                self.open_box()
                print("Current Step:", self.pos)
                print("Next Step: ", self.next_move)
                print("Current Goal:", self.goal)

            if self.goal_reached == True :
                self.calculate_box_distances_from_current_pos()
                self.set_goal()
                # print("Setting new goal.")
                self.goal_reached = False
                if self.box_open_verbose == True:
                    print("Full Box List: ", self.model.full_boxes)


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

class Item(Agent):
    ''' Want this to spawn a random item at locations under boxes, on layer 2, can be removed '''

    def __init__(self, pos, model, consumed=False, decay=15):
        super().__init__(pos, model)
        self.consumed = consumed
        self.decay = decay

    def step(self):
        if not self.consumed:
            self.decay -= 1
            print(self.decay)

#########################################################################################################


class Obstacle(Agent):
    ''' Grey agents that are impassable, that Walker agents must navigate around. Cannot spawn over boxes. '''

    def __init__(self, pos, model):
        super().__init__(pos, model)

    def step(self):
        return






