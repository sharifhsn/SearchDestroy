import random

# cell is the object for belief
# prob is the current probability that target is in cell
# search tracks the number of times that the cell has been searched
class Cell:
    def __init__(self, prob, search, find_prob):
        self.prob = prob
        self.search = search
        self.find_prob = find_prob

# map is a list of list of int
# int is .1, .3, .7, .9 to represent flat, hilly, forested, and caves, respectively
# the int is negative if it is a target, retaining its absolute value
def map_gen(dim, terr):
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
    if terr == 0:
        x = random.randint(0, dim - 1)
        y = random.randint(0, dim - 1)
        map[x][y] *= -1
    else:
        while True:
            x = random.randint(0, dim - 1)
            y = random.randint(0, dim - 1)
            if map[x][y] == terr:
                map[x][y] *= -1
                break
    return map

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def basic_search_1(map, dim):
    # initialize belief
    belief = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(Cell(1 / (dim * dim), 0, (1 - map[i][j]) / (dim * dim)))
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
            return iter + total_dist

        # update rest of belief system
        temp = belief[x][y].prob
        # sfr is the scale factor rate for each cell
        sfr = (1 - temp * abs(map[x][y])) / (1 - temp)
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
            r.append(Cell(1 / (dim * dim), 0, (1 - map[i][j]) / (dim * dim)))
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
                    belief[i][j].find_prob = belief[i][j].prob * (1 - abs(map[i][j]))
        belief[x][y].prob *= abs(map[x][y])
        belief[x][y].find_prob = belief[x][y].prob * (1 - abs(map[x][y]))

        # returns cell with target most likely to be found (prefers flat/forested)
        largest = tuple((0, 0))
        for i in range(len(belief)):
            for j in range(len(belief)):
                if belief[i][j].find_prob > belief[largest[0]][largest[1]].find_prob:
                    largest = tuple((i, j))
                elif belief[i][j].find_prob == belief[largest[0]][largest[1]].find_prob:
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
def improved_search(map, dim):
    # initialize belief
    belief = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(Cell(1 / (dim * dim), 0, (1 - map[i][j]) / (dim * dim)))
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
        if map[x][y] < 0:
            if random.uniform(0, 1) > abs(map[x][y]):
                # success!
                return iter + total_dist
            else:
                print("target found, but false negative")

        # update rest of belief system
        temp = belief[x][y].prob
        # sfr is the scale factor rate for each cell
        sfr = (1 - temp * abs(map[x][y])) / (1 - temp)
        # print("sfr is " + str(sfr))
        for i in range(len(belief)):
            for j in range(len(belief)):
                if tuple((i, j)) != tuple((x, y)):
                    belief[i][j].prob *= sfr
                    belief[i][j].find_prob = belief[i][j].prob * (1 - abs(map[i][j]))
        belief[x][y].prob *= abs(map[x][y])
        belief[x][y].find_prob = belief[x][y].prob * (1 - abs(map[x][y]))

        # returns cell with target most likely to be found (prefers flat/forested)
        largest = tuple((0, 0))
        for i in range(len(belief)):
            for j in range(len(belief)):
                if belief[i][j].find_prob > belief[largest[0]][largest[1]].find_prob:
                    largest = tuple((i, j))
                elif belief[i][j].find_prob == belief[largest[0]][largest[1]].find_prob:
                    m1 = manhattan(i, j, x, y)
                    m2 = manhattan(largest[0], largest[1], x, y)
                    if m1 > m2:
                        largest = tuple((i, j))
                    elif m1 == m2:
                        r = random.randint(0, 1)
                        if r == 0:
                            largest = tuple((i, j))
        lx = largest[0]
        ly = largest[1]
        # follow path
        path = path_points(x, y, lx, ly)
        for p in path:
            a = p[0]
            b = p[1]
            if belief[a][b].find_prob > .5 * belief[lx][ly].find_prob:
                dist = manhattan(x, y, a, b)
                x = a
                y = b
                break

def path_points(x1, y1, x2, y2):
    x = x1
    y = y1
    coords = []
    while x != x2 or y != y2:
        if x < x2:
            x += 1
        elif x > x2:
            x -= 1
        coords.append(tuple((x, y)))
        if x == x2 and y == y2:
            break
        if y < y2:
            y += 1
        elif y > y2:
            y -= 1
        coords.append(tuple((x, y)))
    return coords