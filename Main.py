from random import shuffle
import pygame
import sys
import MQTT
import datetime, json
from Cell import Cell

width = 50
height = 50
cell_width = 10
mqttclient = MQTT.mqtt()
grid = [[Cell() for j in range(height)] for i in range(width)]

# starts mqtt listener
def start_mqtt_listener():
    mqttclient.connect()
    mqttclient.add_listener_func(message_callback)
# gets called when a mqtt message arrives
def message_callback(msg):
    #strip the b''
    msg = msg[2:-1]
    for row in grid:
        for cell in row:
            res = {"timestamp": datetime.datetime.now().isoformat(),
                   "value": -1,
                   "username": "simulator"}
            if cell.getPreferences()[1] == msg:
                res["value"] = 1
            mqttclient.publish("alex",json.dumps(res))
    print(msg)



def visualize():
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((width * cell_width, height * cell_width))
    pygame.display.set_caption("IOT simulator")
    while 1:
        for i in range(width):
            for j in range(height):
                dirs = [[-1,0],[0,1],[0,-1],[1,0]]
                #shuffles dir to counter bias
                shuffle(dirs)
                this_cell = grid[i][j]
                for _dir in dirs:
                    # calculate neighbours
                    try:
                        # -1 in python means last element
                        if i + _dir[0] == -1:
                            raise IndexError("")
                        if j + _dir[1] == -1:
                            raise IndexError("")

                        neighbour = grid[i + _dir[0]][j + _dir[1]]
                        result = neighbour.getInfluenceFactor()
                        if result[1] == "rock":
                            this_cell.rock = 0.5 * this_cell.rock + result[0]
                            this_cell.techno =  this_cell.techno - result[0] * 0.5
                            this_cell.pop = this_cell.pop - result[0] * 0.5
                        elif result[1] == "pop":
                            this_cell.pop = 0.5 * this_cell.pop + result[0]
                            this_cell.techno = this_cell.techno -  result[0] * 0.5
                            this_cell.rock = this_cell.rock - result[0] * 0.5
                        elif result[1] == "techno":
                            this_cell.techno = 0.5 * this_cell.techno + result[0]
                            this_cell.pop = this_cell.pop - result[0] * 0.5
                            this_cell.rock = this_cell.rock - result[0] * 0.5

                        if this_cell.techno < 0:
                            this_cell.techno = 0
                        if this_cell.pop < 0:
                            this_cell.pop = 0
                        if this_cell.rock < 0:
                            this_cell.rock = 0
                    except IndexError:
                        pass

                rect = pygame.Rect(i * cell_width, j * cell_width, cell_width, cell_width)
                pygame.draw.rect(screen, grid[i][j].getPreferences()[0], rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

if __name__ == '__main__':

    start_mqtt_listener()
    visualize()

