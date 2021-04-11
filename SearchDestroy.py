from math import inf
import random
import matplotlib.pyplot as plt

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

    print_map(map, (x, y), abs(map[x][y]))
    return map


# F for flat
# H for hilly
# R for forested
# C for maze of caves
def print_map(map, loc, terr):
    print("target is at " + str(loc) + " with terrain " + str(terr))
    # for m in map:
    #     for c in m:
    #         d = abs(c)
    #         if d == .1:
    #             print("F ", end="")
    #         if d == .3:
    #             print("H ", end="")
    #         if d == .7:
    #             print("R ", end="")
    #         if d == .9:
    #             print("C ", end="")

    #     print()


def naive_search(map, dim):
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
        if map[x][y] < 0:
            if random.uniform(0, 1) > abs(map[x][y]):
                # success
                print("successfully located at " + str((x, y)))
                print("there were " + str(iter) + " iterations to get here")
                print("our final naive distance was " + str(total_dist))
                return iter + total_dist
            else:
                # strictly for debugging purposes, this condition is for when the correct target is found, but there is a false negative
                print("correct place, but couldn't find")
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
            print("basic 1 has " + str(iter) + " number of searches to get to target")
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
            print("basic 2 has " + str(iter) + " number of searches to get to target")
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
                    belief[i][j].find_prob = belief[i][j].prob * (1 - abs(map[i][j]))
        belief[x][y].prob *= abs(map[x][y])
        belief[x][y].find_prob = belief[x][y].prob * (1 - abs(map[x][y]))

        # returns cell with target most likely to be found (prefers flat/forested)
        largest = tuple((0, 0))
        for i in range(len(belief)):
            for j in range(len(belief)):
                # b = belief[i][j].prob * (1 - abs(map[i][j]))
                # l = belief[largest[0]][largest[1]].prob * (1 - abs(map[largest[0]][largest[1]]))
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
        #print("(x, y) is " + str(tuple((x, y))) + " and prob is " + str(belief[x][y].prob))
        iter += 1
        total_dist += dist
        #print(str(iter) + " iterations")
        # query
        # first part of condition checks if it's a target
        # second part of condition checks if it is a false positive
        if map[x][y] < 0:
            if random.uniform(0, 1) > abs(map[x][y]):
                # success!
                print("improved has " + str(iter) + " number of searches to get to target")
                print(str(total_dist) + " distance travelled")
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
                # b = belief[i][j].prob * (1 - abs(map[i][j]))
                # l = belief[largest[0]][largest[1]].prob * (1 - abs(map[largest[0]][largest[1]]))
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
        #print("largest probability is " + str(largest) + " prob is " + str(belief[largest[0]][largest[1]].prob))
        # follow path
        path = path_points(x, y, lx, ly)
        #print(path)
        for p in path:
            a = p[0]
            b = p[1]
            if belief[a][b].find_prob > .5 * belief[lx][ly].find_prob:
                #print("better prob found at " + str(p))
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

def driver():
    dim = 50
    n = 10
    terr = .1
    t = [.1, .3, .7, .9]
    # avgs1 = []
    # avgs2 = []
    # for i in t:
    #     xs = []
    #     ys = []
    #     for j in range(n):
    #         map = map_gen(dim, i)
    #         x = basic_search_1(map, dim)
    #         xs.append(x)
    #         y = basic_search_2(map, dim)
    #         ys.append(y)
    #     avg = sum(xs) / len(xs)
    #     avgs1.append(avg)
    #     avg2 = sum(ys) / len(ys)
    #     avgs2.append(avg2)
    #     print("basic 1 average is " + str(avg))
    #     print("basic 2 average is " + str(avg2))
    # plt.xlabel("false negative rate in terrain")
    # plt.ylabel("score")
    # plt.plot(t, avgs1)
    # plt.plot(t, avgs2)
    # plt.show()
    avgs = []
    for i in t:
        xs = []
        for j in range(n):
            map = map_gen(dim, i)
            x = improved_search(map, dim)
            xs.append(x)
        avg = sum(xs) / len(xs)
        avgs.append(avg)
        print("average of improved_search is " + str(avg) + " for terrain " + str(i))
    plt.xlabel("false negative rate in terrain")
    plt.ylabel("score")
    plt.title("improved search algorithm")
    plt.plot(t, avgs)
    plt.show()

dim = 50
#map = map_gen(dim, .1)
#naive_search(map, dim)
print("check improved_search")
#basic_search_1(map, dim)
driver()
#basic_search_2(map, dim)
#improved_search(map, dim)
#print(path_points(1, 5, 4, 2))