import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import queue as q



def loadMap(file="./solomon-100/c101-obstacle.txt"):
    # Load map txt as matrix.
    # 0: path, 1: obstacle, 2: start point, 3: end point
    f = open(file)
    lines = f.readlines()
    numOfLines = 50
    returnMap = np.zeros((numOfLines, 50))
    A_row = 0
    for line in lines[0:51]:
        list = line.strip().split(' ')
        returnMap[A_row:] = list[0:50]
        A_row += 1
    print(np.shape(returnMap))
    return returnMap


map = loadMap()

def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])   # using the manhattan distance as the heuristic
    # value for the A* algorithm


def getNeighbor(file, pos):
    neighbor = []
    # map = loadMap(file)
    # the point above
    if pos[0]>=1 and map[pos[0]-1, pos[1]]!=1:
        neighbor.append((pos[0]-1, pos[1]))
    # the point on the right
    if pos[1]<=len(map[0])-2 and map[pos[0], pos[1]+1]!=1:
        neighbor.append((pos[0], pos[1]+1))
    # the point below
    if pos[0]<=len(map)-2 and map[pos[0]+1, pos[1]]!=1:
        neighbor.append((pos[0]+1, pos[1]))
    # the point on the left
    if pos[1]>=1 and map[pos[0], pos[1]-1]!=1:
        neighbor.append((pos[0], pos[1]-1))
    return neighbor


def Astar(mapfile, rowNum, colNum, node_a, node_b):
    start = (int(node_a.x), int(node_a.y))
    goal = (int(node_b.x), int(node_b.y))
    frontier = q.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    # came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in getNeighbor(mapfile, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    # self.drawPath(came_from)

    # get the length of the path
    length = 0
    path = [goal]
    while goal != start:
        goal = came_from[goal]
        path.append(goal)
        length += 1
    # print(path[1][1])
    return length, path
