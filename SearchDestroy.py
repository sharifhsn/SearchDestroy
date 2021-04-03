import random


# cell is the object for belief
# terrain is 0 for unknown, same as map for others
# prob is the current probability that target is in cell
class Cell:
    def __init__(self, prob, terrain, search):
        self.prob = prob
        self.terrain = terrain
        self.search = search


# map is a list of list of int
# int is 1, 2, 3, 4 to represent flat, hilly, forested, and caves, respectively
# the int is negative if it is a target, retaining its absolute value
def map_gen(dim):
    map = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(random.randint(1, 4))
        map.append(r)
    print(type(map))

    x = random.randint(0, dim - 1)
    y = random.randint(0, dim - 1)
    map[x][y] *= -1

    print_map(map, (x, y), abs(map[x][y]))
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
            # if c == -1:
            #     print("F ", end="")
            # if c == -2:
            #     print("H ", end="")
            # if c == -3:
            #     print("R ", end="")
            # if c == -4:
            #     print("C ", end="")
            if d == 1:
                print("F ", end="")
            if d == 2:
                print("H ", end="")
            if d == 3:
                print("R ", end="")
            if d == 4:
                print("C ", end="")

        print()


def naive_search(map, dim):
    # initialize belief
    belief = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(Cell(1 / 2500, 0, 0))
        belief.append(r)
    iter = 0
    while True:
        iter += 1
        x = random.randint(0, dim - 1)
        y = random.randint(0, dim - 1)
        if map[x][y] < 0:
            r = random.uniform(0, 1)
            if map[x][y] == -1 and r > .1 or map[x][y] == -2 and r > .3 or map[x][y] == -3 and r > .7 or map[x][
                y] == -4 and r > .9:
                # success
                print("sucessfully located at " + str((x, y)))
                print("there were " + str(iter) + " iterations to get here")
                break


dim = 10
map = map_gen(dim)
naive_search(map, dim)