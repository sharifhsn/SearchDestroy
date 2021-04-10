from math import inf
import random
import matplotlib.pyplot as plt

# cell is the object for belief
# prob is the current probability that target is in cell
# search tracks the number of times that the cell has been searched
class Cell:
    def __init__(self, prob, search):
        self.prob = prob
        self.search = search

# map is a list of list of int
# int is .1, .3, .7, .9 to represent flat, hilly, forested, and caves, respectively
# the int is negative if it is a target, retaining its absolute value
def map_gen(dim):
    map = []
    for i in range(dim):
        r = []
        for j in range(dim):
            q = random.randint(1, 4)
            if q == 1:
                r.append(.1)
            if q == 2:
                r.append(.3)
            if q == 3:
                r.append(.7)
            if q == 4:
                r.append(.9)
        map.append(r)

    x = random.randint(0, dim - 1)
    y = random.randint(0, dim - 1)
    map[x][y] *= -1

    #print_map(map, (x, y), abs(map[x][y]))
    return map


# F for flat
# H for hilly
# R for forested
# C for maze of caves
def print_map(map, loc, terr):
    print("target is at " + str(loc) + " with terrain " + str(terr))
    for m in map:
        for c in m:
            d = abs(c)
            if d == .1:
                print("F ", end="")
            if d == .3:
                print("H ", end="")
            if d == .7:
                print("R ", end="")
            if d == .9:
                print("C ", end="")

        print()


def naive_search(map, dim):
    # initialize belief
    belief = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(Cell(1 / (dim * dim), 0))
        belief.append(r)
    iter = 0
    dist = 0
    total_dist = 0
    x = random.randint(0, dim - 1)
    y = random.randint(0, dim - 1)
    while True:
        iter += 1
        total_dist += dist
        if map[x][y] < 0 and random.uniform(0, 1) > abs(map[x][y]):
            # success
            print("successfully located at " + str((x, y)))
            print("there were " + str(iter) + " iterations to get here")
            print("our final naive distance was " + str(total_dist))
            return iter + total_dist
        nx = random.randint(0, dim - 1)
        ny = random.randint(0, dim - 1)
        dist = manhattan(x, y, nx, ny)
        x = nx
        y = ny


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def basic_search_1(map, dim):
    # initialize belief
    belief = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(Cell(1 / (dim * dim), 0))
        belief.append(r)
    iter = 0
    dist = 0
    total_dist = 0
    x = random.randint(0, dim - 1)
    y = random.randint(0, dim - 1)
    while True:
        iter += 1
        total_dist += dist
        # query
        # first part of condition checks if it's a target
        # second part of condition checks if it is a false positive
        r = random.uniform(0, 1)
        if map[x][y] < 0 and r > abs(map[x][y]):
            # success!
            print(str(iter) + " number of searches to get to target")
            print(str(total_dist) + " distance travelled")
            return iter + total_dist

        # update rest of belief system
        temp = belief[x][y].prob
        # sfr is the scale factor rate for each cell
        sfr = (1 - temp * abs(map[x][y])) / (1 - temp)
        # print("sfr is " + str(sfr))
        for i in range(len(belief)):
            for j in range(len(belief)):
                if tuple((i, j)) != tuple((x, y)):
                    belief[i][j].prob *= sfr
        belief[x][y].prob *= abs(map[x][y])

        # returns largest
        largest = tuple((0, 0))
        for i in range(len(belief)):
            for j in range(len(belief)):
                if belief[i][j].prob > belief[largest[0]][largest[1]].prob:
                    largest = tuple((i, j))
                elif belief[i][j].prob == belief[largest[0]][largest[1]].prob:
                    m1 = manhattan(i, j, x, y)
                    m2 = manhattan(largest[0], largest[1], x, y)
                    if m1 > m2:
                        largest = tuple((i, j))
                    elif m1 == m2:
                        r = random.randint(0, 1)
                        if r == 0:
                            largest = tuple((i, j))
        dist = manhattan(x, y, largest[0], largest[1])
        x = largest[0]
        y = largest[1]
def basic_search_2(map, dim):
    # initialize belief
    belief = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(Cell(1 / (dim * dim), 0))
        belief.append(r)
    iter = 0
    dist = 0
    total_dist = 0
    x = random.randint(0, dim - 1)
    y = random.randint(0, dim - 1)
    while True:
        iter += 1
        total_dist += dist
        # query
        # first part of condition checks if it's a target
        # second part of condition checks if it is a false positive
        r = random.uniform(0, 1)
        if map[x][y] < 0 and r > abs(map[x][y]):
            # success!
            print(str(iter) + " number of searches to get to target")
            print(str(total_dist) + " distance travelled")
            return iter + total_dist

        # update rest of belief system
        temp = belief[x][y].prob
        # sfr is the scale factor rate for each cell
        sfr = (1 - temp * abs(map[x][y])) / (1 - temp)
        # print("sfr is " + str(sfr))
        for i in range(len(belief)):
            for j in range(len(belief)):
                if tuple((i, j)) != tuple((x, y)):
                    belief[i][j].prob *= sfr
        belief[x][y].prob *= abs(map[x][y])

        # returns cell with target most likely to be found (prefers flat/forested)
        largest = tuple((0, 0))
        for i in range(len(belief)):
            for j in range(len(belief)):
                b = belief[i][j].prob * (1 - abs(map[i][j]))
                l = belief[largest[0]][largest[1]].prob * (1 - abs(map[largest[0]][largest[1]]))
                if b > l:
                    largest = tuple((i, j))
                elif b == l:
                    m1 = manhattan(i, j, x, y)
                    m2 = manhattan(largest[0], largest[1], x, y)
                    if m1 > m2:
                        largest = tuple((i, j))
                    elif m1 == m2:
                        r = random.randint(0, 1)
                        if r == 0:
                            largest = tuple((i, j))
        dist = manhattan(x, y, largest[0], largest[1])
        x = largest[0]
        y = largest[1]
def driver():
    dim = 50
    n = 20

    xs = []
    for i in range(n):
        map = map_gen(dim)
        x = basic_search_2(map, dim)
        xs.append(x)
    avg = sum(xs) / len(xs)
    print("average is " + str(avg))


dim = 50
map = map_gen(dim)
#naive_search(map, dim)
print("check basic_search_2")
#basic_search_1(map, dim)
driver()
#basic_search_2(map, dim)