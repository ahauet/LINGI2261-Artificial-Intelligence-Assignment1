'''NAMES OF THE AUTHOR(S): Alexandre Hauet & Tanguy Vaessen'''
import time
from search import *
import copy


#################
# Problem class #
#################^

class NumberLink(Problem):
    """This class herits from Problem. It is used to solve a problem that is represent as a grid"""
    def __init__(self, grid):
        """Initialize the solver.
        - grid : the initial grid reprensenting the problem to solve
        """
        self.endPointsPath = constructEndPointsPathDictionnary(grid)
        self.copyEndPointsPath = copy.deepcopy(self.endPointsPath)
        firstPoint = getNextPoints(self.endPointsPath)
        initialState = State(grid, firstPoint.letter, [firstPoint.start], firstPoint.end, copy.copy(self.endPointsPath))
        super().__init__(initialState)

        self.dico = {}

    def goal_test(self, state):
        """A problem is solved if there are no more points in the grid"""
        for line in state.grid:
            for letter in line:
                if letter == '.':
                    return False
        return True
        # return len(state.endPoints) == 0

    def successor(self, state):
        """ Return a generator that gives some pairs of direction ([-1,0] for example) associated with a state.
        Before returning a successor, the method checks
        - if the position is in the bounds of the grid
        - if the position is not already used
        - if the path is not doing a 2*2 squarre with the same letter
        - if every non-solved path can still be solved
        - if the path is not isolating a lonely point"""
        pathCompleted = False
        for direction in directions:
            if not pathCompleted:
                newPosition = [state.path[-1][0] + direction[0],
                               state.path[-1][1] + direction[1]]
                if inBounds(grid, newPosition):
                    if state.grid[newPosition[0]][newPosition[1]] == '.':  # if this is not a '.', the position is already used
                        if hasTwoNeighboorMax(state.grid, state.letter, newPosition):
                            newGrid = [row[:] for row in state.grid] #code from https://stackoverflow.com/questions/6532881/how-to-make-a-copy-of-a-2d-array-in-python#answer-6533065
                            newGrid[newPosition[0]][newPosition[1]] = state.letter
                            newPath = copy.copy(state.path)
                            newPath.append(newPosition)
                            newState = State(newGrid, state.letter, newPath, state.endPoint, copy.copy(state.endPoints))
                            if noDeadEndWithState(newGrid, state.endPoints, newState)and hasNoLonelyPoint(newGrid, state.letter, state.endPoints):
                                # if not str(newPosition) in self.dico: self.dico[str(newPosition)] = 1
                                # else : self.dico[str(newPosition)] = self.dico[str(newPosition)] + 1
                                # if self.dico[str(newPosition)] <= 100:
                                    #print(newState)
                                    if isPathCompleted(newState):
                                        pathCompleted = True
                                        self.dico = {}
                                        yield (direction, self.startNewPath(newState))
                                    else:
                                        yield (direction, newState)
                                # else: not a good solution
                            # else: position already used
                        # else : out of bound

    def startNewPath(self, state):
        newEndPoints = copy.copy(state.endPoints)
        del newEndPoints[state.letter]
        nextPoint = getNextPoints(newEndPoints)
        if not nextPoint: state.endPoints = newEndPoints; return state
        return State(state.grid, nextPoint.letter, [nextPoint.start], nextPoint.end, newEndPoints)

###############
# State class #
###############

class State:
    """The state class represent a state of the problem.
        - grid is a copy of the grid representing the current state of the problem
        - currentLetter is the path trying to complete
        - currentPath is a list of points representing the path
        - endPoint is the goal point fot the current path
        - endPoints is a dictionnary associating a letter to the endPoints of the path for the not-solved path
    """

    def __init__(self, grid: list, currentLetter, currentPath: list, endPoint, endPoints):
        self.grid = grid
        self.letter = currentLetter
        self.path = currentPath
        self.endPoint = endPoint
        self.endPoints = endPoints

    def __str__(self):
        output = ""
        for line in self.grid:
            for letter in line:
                output += letter
            output += '\n'
        return output


class Pair:
    def __init__(self, letter, start, end):
        self.letter = letter
        self.start = start
        self.end = end


######################
# Auxiliary function #
######################

directions = ([0, -1], [0, 1], [1, 0], [-1, 0])  # Left, Right, Up, Down
#directions = ([-1, 0], [1, 0], [0, -1], [0, 1])  # Down, Up, Left, Right
directions8 = ([0, -1], [0, 1], [1, 0], [-1, 0], [1, -1], [1, 1], [-1,-1], [-1, 1])


def hasNoLonelyPoint(grid, ltr, dico):
    """Check if there is a lonely point in the grid
    If there is a lonely point but that it is the last point in the grid, return True
    If there is a lonely point but that it is the last point between a path's head and the path's goal, return True
    """
    noLonelyPoints = True
    i = 0
    nbrPoints = 0
    for line in grid:
        j = 0
        for letter in line:
            if letter == '.': #we look for each '.' in the grid
                nbrPoints += 1
                lonelyPoint = True
                point = [i, j]
                for direction in directions8: #check if the dot is alone
                    newPosition = [point[0] + direction[0],
                                    point[1] + direction[1]]
                    if inBounds(grid, newPosition) and grid[newPosition[0]][newPosition[1]] == '.':
                        lonelyPoint = False
                        break
                if lonelyPoint: #a dot can be alone if it is the last dot between the goal's path and the path's head
                    for direction in directions:
                        posToCheck = [point[0] + direction[0],
                                       point[1] + direction[1]]
                        if inBounds(grid, posToCheck):
                            for value in dico[ltr]:
                                if posToCheck[0] == value[0] and posToCheck[1] == value[1]:
                                    lonelyPoint = False
                noLonelyPoints = noLonelyPoints and not lonelyPoint
                if not noLonelyPoints: break
            j += 1
        i += 1
    if not noLonelyPoints and nbrPoints == 1:
        return True
    else: return noLonelyPoints



def hasTwoNeighboorMax(grid, letter, position):
    """Check if position in grid will be next to more than 2 same letters.
    for example:
    A A A
    B B A
    B . A
    in this small grid, if position is at the '.' coordinates and letter is 'B', the function will return False because there are more than 2 neighboors with the same letter
    """
    subSquarre1 = ([0, -1], [-1, 0], [-1,-1])  # Left, Down, Both
    subSquarre2 = ([0,  1], [-1, 0], [-1, 1])  # Right, Down, Both
    subSquarre3 = ([0, -1], [1 , 0], [1, -1])  # Left, Up, Both
    subSquarre4 = ([0,  1], [1 , 0], [1,  1])  # Right, Up, Both

    subSquarres = [subSquarre1, subSquarre2, subSquarre3, subSquarre4]

    result = True

    numberOfLetter = 0
    for direction in directions8: #test the number of same letter in a 3*3 squarre
        newPosition = [position[0] + direction[0],
                       position[1] + direction[1]]
        if inBounds(grid, newPosition):
            if grid[newPosition[0]][newPosition[1]] == letter:
                numberOfLetter += 1
    result = numberOfLetter <= 3 #dans le "grand" carré de 3*3, on autorise 3 voisins avec la même lettre

    for subSquarre in subSquarres: #test the number of same letter in the 4 differents 2*2 squarres
        numberOfLetter = 0
        for direction in subSquarre:
            newPosition = [position[0] + direction[0],
                           position[1] + direction[1]]
            if inBounds(grid, newPosition):
                if grid[newPosition[0]][newPosition[1]] == letter:
                    numberOfLetter += 1
        result = result and (numberOfLetter <= 2) # dans les sous carrés de 2*2, on autorise maximum 2 lettres identiques à celle qu'on ajoute
    return result

def isPathCompleted(state):
    """Check if the path represented in state is completed"""
    for direction in directions:
        newPosition = [state.path[-1][0] + direction[0],
                       state.path[-1][1] + direction[1]]
        if newPosition[0] == state.endPoint[0] and newPosition[1] == state.endPoint[1]:
            return True
    return False


def noDeadEndWithState(grid, points, state):
    """Check if it exists paths between all the pairs of points, considering the fact that the current state add a point to the grid"""
    if state.path[0] == points[state.letter][0]:
        backup = points[state.letter][0]
        points[state.letter][0] = state.path[-1]
        result = noDeadEnd(grid, points)
        points[state.letter][0] = backup
        return result
    else:
        backup = points[state.letter][1]
        points[state.letter][1] = state.path[-1]
        result = noDeadEnd(grid,points)
        points[state.letter][1] = backup
        return result


def noDeadEnd(grid, points):
    """
    Check if it exists paths between all the pairs of points
    """
    for value in list(points.values()):
        if pathExists(grid, value[0], value[1]) == False:
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
    """Check if a position is inside the bounds of a grid"""
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


def getNextPoints(dico):
    keys = list(dico.keys())
    if len(keys) == 0 : return None
    i = 0
    result = Pair(keys[i], dico.__getitem__(keys[i])[1], dico.__getitem__(keys[i])[0])
    i = i + 1
    while i < len(keys):
        tmp = Pair(keys[i], dico.__getitem__(keys[i])[1], dico.__getitem__(keys[i])[0])
        a = abs(result.start[0] - result.end[0]) + abs(result.start[1] - result.end[1])
        b = abs(tmp.start[0] - tmp.end[0]) + abs(tmp.start[1] - tmp.end[1])
        if a > b:
            result = tmp
        elif a == b :
            if tmp.start[1] > result.start[1]:
                result = tmp
            elif tmp.start[0] > result.start[0]:
                result = tmp
        i += 1
    return result


def abs(n):
    return (n, -n)[n < 0]


#####################
# Launch the search #
#####################

start_time = time.time()

if len(sys.argv) < 2: print("usage: numberlink.py inputFile"); exit(2)
grid = constructGrid(sys.argv[1])
problem = NumberLink(grid)

# print(problem.initial.letter)
# print(problem.initial.position)
# for pair in problem.successor(problem.initial):
#    print(pair[0], pair[1].grid)
# exit(0)

# example of bfs search
node = breadth_first_graph_search(problem)
# example of print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format

print("--- %s seconds ---" % (time.time() - start_time))