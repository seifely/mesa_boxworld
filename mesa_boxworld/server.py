from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from mesa_boxworld.agents import Walker, ClosedBox, OpenedBox, Item, Obstacle
from mesa_boxworld.model import ThirdTestModel


def third_test_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # define the portrayal features such as layers, shapes, colours etc.
    # can make this dependent on agent values, such as energy variable etc.
    if type(agent) is Walker:
        portrayal = {"Shape": "circle",
                     "scale": 1,
                     "Color": "red",
                     "Filled": "true",
                     "Layer": 1,
                     "r": 0.5,
                     "text": "ᕕ( ՞ ᗜ ՞ )ᕗ",
                     "text_color": "black",
                     "scale": 1
                     }
        # if step is odd, one arms, if even, other arms, then he'll look animated :P

    elif type(agent) is ClosedBox:
            portrayal = {"Shape": "rect",
                     "scale": 1,
                     "Color": "brown",
                     "Filled": "true",
                     "Layer": 2,
                     "w": 1,
                     "h": 1
                     }

    elif type(agent) is OpenedBox:
            portrayal = {"Shape": "rect",
                     "scale": 1,
                     "Color": "black",
                     "Filled": "false",
                     "Layer": 0,
                     "w": 1,
                     "h": 1
                     }


    elif type(agent) is Item:
        # if agent.consumed:
        portrayal = {"Shape": "circle",
                     "scale": 1,
                     "Color": "yellow",
                     "Filled": "true",
                     "Layer": 1,
                     "r": 0.5,
                     "text": "✿",
                     "text_color": "black",
                     "scale": 0.7
                     }

    elif type(agent) is Obstacle:
            portrayal = {"Shape": "rect",
                     "scale": 1,
                     "Color": "gray",
                     "Filled": "true",
                     "Layer": 1,
                     "w": 1,
                     "h": 1
                     }

    return portrayal


canvas_element = CanvasGrid(third_test_portrayal, 25, 25, 500, 500)
chart_element = ChartModule([{"Label": "Walkers", "Color": "#AA0000"},
                             {"Label": "Closed Boxes", "Color": "#666666"}])


#model_params = {"initial_items": UserSettableParameter('slider', 'Initial Item Number', 10, 1, 15, 1)}
# the above should be used when there are user settable sliders

model_params = {#"height": UserSettableParameter('slider', 'Height', 20, 10, 50, 10),
                #"width": UserSettableParameter('slider', 'Width', 20, 10, 50, 10),
                # "initial_walkers": UserSettableParameter('slider', 'Initial Walker Population', 1, 1, 10, 1),
                # "initial_boxes": UserSettableParameter('slider', 'Initial Box Number', 10, 1, 20, 1),
                "initial_items": UserSettableParameter('slider', 'Initial Item Number', 10, 1, 20, 1),
                # "initial_obstacles": UserSettableParameter('slider', 'Initial Whole Obstacle Number', 3, 1, 10, 1),
                # "obstacle_length": UserSettableParameter('slider', 'Maximum Obstacle Length', 5, 1, 12, 1),
                }

#model_params = {"height": 20, "width": 20, "initial_walkers": 1, "initial_boxes": 10, "initial_items": 10}

# "item_timeout": UserSettableParameter('slider', 'Item Decay Rate', 0.05, 0.01, 1.0, 0.01)

server = ModularServer(ThirdTestModel, [canvas_element, chart_element], "Boxworld Model", model_params)
server.port = 8521

