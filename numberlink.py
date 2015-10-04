'''NAMES OF THE AUTHOR(S): Alexandre Hauet & Tanguy Vaessen'''
import time
import sys
from os import listdir, system
from search import *
from enum import IntEnum


#################
# Problem class #
#################^

class NumberLink(Problem):
    def __init__(self, grid):
        self.endPointsPath = constructEndPointsPathDictionnary(grid)
        self.copyEndPointsPath = self.endPointsPath
        firstPoint = getNextPoints(self.endPointsPath)
        initialState = State(grid, firstPoint.letter, [firstPoint.start], firstPoint.start)
        super().__init__(initialState)

    def goal_test(self, state):
        for line in state.grid:
            for letter in line:
                if letter == '.':
                    return False
        return True

    def successor(self, state):
        extensions = ([0, -1], [0, 1], [1, 0], [-1, 0])  # Left, Right, Up, Down
        for extension in extensions:
            newPosition = [ state.position[0] + extension[0],
                            state.position[1] + extension[1]]
            newGrid = state.grid.copy()
            try: # need a try catch because the newPosition can be out of bound!
                if newGrid[newPosition[0]][newPosition[1]] != '.':
                    # this position is already used
                    pass
                else:
                    newGrid[newPosition[0]][newPosition[1]] = state.letter
                    print(state.letter)

            except Exception:
                # Out of grid
                pass
            else:
                # TODO should check if this is a correct successor by calling PathExist
                if noDeadEnd(grid, self.copyEndPointsPath):
                    newPath = state.path.copy()
                    newPath.append(newPosition)
                    yield (extension, State(newGrid, state.letter, newPath, newPosition))



###############
# State class #
###############

class State:
    """The state class represent a state of the problem.
        It contains a grid, the current path and the last extension
    """
    def __init__(self, grid: list, currentLetter, currentPath: list, lastPosition: list):
        self.grid = grid
        self.letter = currentLetter
        self.path = currentPath
        self.position = lastPosition

class Pair:
    def __init__(self, letter, start, end):
        self.letter = letter
        self.start = start
        self.end = end

######################
# Auxiliary function #
######################

directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def noDeadEnd(grid, points):
    """
    Check if it exist paths between all the pairs of points
    """
    for value in list(points.values()):
        if pathExists(grid,value[0],value[1]) == False:
            return False
    return True



def pathExists(grid, start, end):
    visited = [[0 for j in range(0, len(grid[0]))] for i in range(0, len(grid))]
    ok = pathExistsDFS(grid, start, end, visited)
    return ok


def pathExistsDFS(grid, start, end, visited):
    for d in directions:
        i = start[0] + d[0]
        j = start[1] + d[1]
        next = [i, j]
        if i == end[0] and j == end[1]:
            return True
        if inBounds(grid, next) and grid[i][j] == '.' and not visited[i][j]:
            visited[i][j] = 1
            exists = pathExistsDFS(grid, next, end, visited)
            if exists:
                return True
    return False


def inBounds(grid, pos):
    return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])


def constructGrid(problemFileName):
    """
    Open and interpret a file as a grid
    :rtype : a matrix representing the problem's grid
    """
    grid = []
    try:
        file = open(problemFileName)
        for line in file.readlines():
            tmp = []
            for character in line:
                if character != '\n':
                    tmp.append(character)
            grid.append(tmp)
    except IOError:
        print("File " + problemFileName + " can not be found or open")
        exit(1)
    else:
        grid.reverse()  # need to reverse it to get the (0,0) at the bottom left
        return grid


def constructEndPointsPathDictionnary(grid):
    """Consruct a dictionnary that associate a letter to an array of 2 points"""
    dictionnary = {}
    i = 0
    j = 0
    for line in grid:
        for letter in line:
            if letter != '.':
                if dictionnary.get(letter) is None:
                    # add the letter to the dic
                    dictionnary[letter] = [[i, j]]
                else:
                    # add the coordinates to the dictionnary
                    dictionnary.get(letter).append([i, j])
            j += 1
        i += 1
        j = 0
    return dictionnary

def getNextPoints(dico) :
    keys = list(dico.keys())
    i = 0
    result = Pair(keys[i], dico.__getitem__(keys[i])[0], dico.__getitem__(keys[i])[1])
    i = i + 1
    while i < len(keys):
        tmp = Pair(keys[i], dico.__getitem__(keys[i])[0], dico.__getitem__(keys[i])[1])
        if abs(result.start[0] - result.end[0]) + abs(result.start[1] - result.end[1]) < abs(tmp.start[0] - tmp.end[0]) + abs(tmp.start[1] - tmp.end[1]):
            result = tmp
        i = i + 1
    del dico[result.letter]
    return result

def abs(n):
    return (n,-n)[n<0]

#####################
# Launch the search #
#####################

grid = constructGrid(sys.argv[1])
problem = NumberLink(grid)

#for i in problem.successor(problem.initial):
#    print(i[1].grid, i[1].letter, i[1].path, i[1].position)

# example of bfs search
node = depth_first_tree_search(problem)
# example of print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format
