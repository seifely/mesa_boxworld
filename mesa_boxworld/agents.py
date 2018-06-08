import random
import math

from mesa import Agent

###########################################################################################################
class Walker(Agent):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
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
    avoidance_check = []
    able_to_move = True  # not currently used
    steps_memory = []  # not currently used
    obstacle_present = False

    # for debugging
    distance_verbose = False
    box_open_verbose = False
    quick_verbose = False

    def __init__(self, pos, model, moore, stepCount=0, goal=[], closed_box_list={}, open_box_list={}, next_move=[],
                 able_to_move=True, steps_memory=[], obstacle_present=False, avoidance_goal=[], avoidance_check=[]):
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

        self.closed_box_list = closed_box_list
        self.closed_box_list = self.model.all_boxes  # this used to be set to the full box list, but now agent = blind
        self.open_box_list = open_box_list

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

    def simple_move_goal(self):
        '''
        Step one cell in any allowable direction towards the closest box.
        '''

        if self.able_to_move:
            goal = self.goal


        elif not self.able_to_move:
            print("I can't move right now.")






        # if self.able_to_move:
        #     goal = self.goal
        #     current_x, current_y = self.pos
        #     goal_x, goal_y = goal
        #
        #     if self.pos != goal:
        #         if current_x > goal_x:
        #             self.next_move = ((current_x - 1), current_y)
        #             self.check_for_obstacles(self.next_move)
        #             if self.obstacle_present == True:
        #                 self.avoid_obstacle()
        #             elif self.obstacle_present == False:
        #                 self.model.grid.move_agent(self, self.next_move)
        #
        #         elif current_x < goal_x:
        #             self.next_move = ((current_x + 1), current_y)
        #             self.check_for_obstacles(self.next_move)
        #             if self.obstacle_present == True:
        #                 self.avoid_obstacle()
        #             elif self.obstacle_present == False:
        #                 self.model.grid.move_agent(self, self.next_move)
        #
        #         if current_y > goal_y:
        #             self.next_move = (current_x, (current_y - 1))
        #             self.check_for_obstacles(self.next_move)
        #             if self.obstacle_present == True:
        #                 self.avoid_obstacle()
        #
        #                 # IS THIS BIR=T --------------------------------------------------------------------
        #                 new_current_x, new_current_y = self.pos
        #                 self.next_move = (new_current_x, (new_current_y - 1))
        #                 self.model.grid.move_agent(self, self.next_move)
        #
        #             elif self.obstacle_present == False:
        #                 self.model.grid.move_agent(self, self.next_move)
        #
        #         elif current_y < goal_y:
        #             self.next_move = (current_x, (current_y + 1))
        #             self.check_for_obstacles(self.next_move)
        #             if self.obstacle_present == True:
        #                 self.avoid_obstacle()
        #             elif self.obstacle_present == False:
        #                 self.model.grid.move_agent(self, self.next_move)
        #
        #     else:
        #         self.goal_reached = True
        #         return "Goal Reached!"

        elif not self.able_to_move:
            print("I'm not allowed to move right now.")

    def check_for_obstacles(self, cell):  # no longer used, generic obstacle checking
        next_cell = self.model.grid.get_cell_list_contents([cell])
        potential_obstacle = [obj for obj in next_cell
                              if isinstance(obj, Obstacle)]
        if len(potential_obstacle) > 0:
            print("Generic Obstacle Detected!")
            # self.able_to_move = False
            self.obstacle_present = True
        elif len(potential_obstacle) == 0:
            self.obstacle_present = False

    def check_for_freedom(self):
        current_x, current_y = self.pos
        goal_x, goal_y = self.goal

        # for n cells in list (of cells between here and the goal)
        # check each one for Obstacle agent
        # obstacle count + 1 for each that returns true
        # if obstacle count == 0
            # return True
        # if obstacle count == 1
            # return False
            # initiate immediacy of obstacle check? How is the obstacle 1 step away or many?
            # if obstacle is more than one step away (dist_x =< 1, dist_y =< 1)
                # return True

    def follow_wall(self):
        print("Following wall")
        current_x, current_y = self.pos

    def blocked_north(self):
        current_x, current_y = self.pos

        if self.next_move == (current_x, (current_y + 1)):
            next_cell = self.model.grid.get_cell_list_contents([self.next_move])
            potential_obstacle = [obj for obj in next_cell
                                  if isinstance(obj, Obstacle)]
            if len(potential_obstacle) > 0:
                print("Obstacle Detected North!")
                # self.able_to_move = False
                self.obstacle_present = True
            elif len(potential_obstacle) == 0:
                self.obstacle_present = False

    def blocked_east(self):
        current_x, current_y = self.pos

        if self.next_move == ((current_x + 1), current_y):
            next_cell = self.model.grid.get_cell_list_contents([self.next_move])
            potential_obstacle = [obj for obj in next_cell
                                  if isinstance(obj, Obstacle)]
            if len(potential_obstacle) > 0:
                print("Obstacle Detected East!")
                # self.able_to_move = False
                self.obstacle_present = True
            elif len(potential_obstacle) == 0:
                self.obstacle_present = False

    def blocked_south(self):
        current_x, current_y = self.pos

        if self.next_move == (current_x, (current_y - 1)):
            next_cell = self.model.grid.get_cell_list_contents([self.next_move])
            potential_obstacle = [obj for obj in next_cell
                                  if isinstance(obj, Obstacle)]
            if len(potential_obstacle) > 0:
                print("Obstacle Detected South!")
                # self.able_to_move = False
                self.obstacle_present = True
            elif len(potential_obstacle) == 0:
                self.obstacle_present = False

    def blocked_west(self):
        current_x, current_y = self.pos

        if self.next_move == ((current_x - 1), current_y):
            next_cell = self.model.grid.get_cell_list_contents([self.next_move])
            potential_obstacle = [obj for obj in next_cell
                                  if isinstance(obj, Obstacle)]
            if len(potential_obstacle) > 0:
                print("Obstacle Detected West!")
                # self.able_to_move = False
                self.obstacle_present = True
            elif len(potential_obstacle) == 0:
                self.obstacle_present = False

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
            if self.goal_reached == False :
                self.simple_move_goal()
                # self.check_for_obstacles()
                self.open_box()
                print("Next Move is: ", self.next_move)
                # if self.check_for_obstacles():
                #     self.avoid_obstacle()

            if self.goal_reached == True :
                self.calculate_box_distances_from_current_pos()
                self.set_goal()
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






