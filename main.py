from random import random as rand, randint
from math import exp, sqrt
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm


class Point:
    x: float = 0
    y: float = 0

    def __init__(self, _x: int = 0, _y: int = 0):
        self.x = _x
        self.y = _y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def size(self):
        return sqrt((self.x ** 2) + (self.y ** 2))

    def __str__(self):
        return str(self.x) + " " + str(self.y)


def normalise(array: []):
    b = array.copy()
    b.sort()
    for ind in range(len(b)):
        array[array.index(b[ind])] = ind
    return array


def getLen(place: [Point], road: [int]):
    ans: float = 0
    for i in range(len(road) - 1):
        a = place[road[i + 1]] - place[road[i]]
        ans += a.size()
    a = place[road[len(road) - 1]] - place[road[0]]
    ans += a.size()
    return ans


def temperature(initial: float, final: float, iteration: float):
    return final + (((initial - final) * (10000 - iteration)) / 10000)


def getProbability(dE: float, temp: float):
    ans = 0
    try:
        ans = exp(-dE / temp)
    except OverflowError:
        ans = float('inf')
    return ans


def isTransition(probability: float):
    value: float = rand()
    return value <= probability


def main(graph: [Point], path: [[int]]):
    temper = [t_max]
    for it in tqdm(range(1, 10001)):
        temper.append(temperature(t_max, t_min, it))
        for i in range(len(path)):
            way = path[i].copy()
            first: int = randint(0, len(way) - 1)
            second: int = first
            while second == first:
                second = randint(0, len(way) - 1)
            b = way.copy()
            b[first], b[second] = b[second], b[first]
            if isTransition(getProbability(getLen(graph, b) - getLen(graph, way), temperature(t_max, t_min, it))):
                path[i] = b
        it += 1
    ans: [Point] = 0
    for i in range(1, len(path)):
        if getLen(graph, path[ans]) > getLen(graph, path[i]):
            ans = i
    dev_x: [int] = []
    dev_y: [int] = []
    for i in range(len(path[ans])):
        dev_x.append(graph[path[ans][i]].x)
        dev_y.append(graph[path[ans][i]].y)
    dev_x.append(graph[path[ans][0]].x)
    dev_y.append(graph[path[ans][0]].y)
    return [dev_x, dev_y, it, temper]


# Init the constants
t_max: float = 80
t_min: float = 0
n: int = int(input())

data = []

for i in range(n):
    data.append(Point(rand() * 10, rand() * 10))
print("Generated DATA")
ways = []

for i in range(n):
    temporary: [] = []
    for j in range(n):
        a = rand()
        temporary.append(a)
    temporary = normalise(temporary)
    while temporary in ways:
        temporary = []
        for j in range(n):
            a = randint(0, n - 1)
            while not (a in temporary):
                a = randint(0, n - 1)
            temporary.append(a)
        temporary = normalise(temporary)
    ways.append(temporary)
print("Generated ways")
a = main(data, ways)


plt.subplot(2, 1, 1)
plt.plot(a[0], a[1], 'bx-', label='cities')
plt.title("Simulated annealing")
plt.xlabel("X coordinate")
plt.ylabel("Y coordinate")


plt.subplot(2, 1, 2)
plt.plot(range(1, a[2] + 1), a[3])
plt.xlabel("Iteration")
plt.ylabel("Temperature")
print("Created plots")

plt.show()
