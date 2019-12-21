from random import random as rand, randint
from math import exp, sqrt
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
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


def getDist(a: Point, b: Point):
    return (a - b).size()


def getLen(place: [Point], road: [int]):
    ans: float = 0
    for i in range(len(road) - 1):
        ans += getDist(place[road[i + 1]], place[road[i]])
    ans += getDist(place[road[len(road) - 1]], place[road[0]])
    return ans


def temperature(initial: float, final: float, iteration: float, max_iter: int):
    return final + (((initial - final) * (max_iter - iteration)) / max_iter)


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


def printWay(graph: [Point], path: [int]):
    dev_x = []
    dev_y = []
    for i in range(len(path)):
        dev_x.append(graph[path[i]].x)
        dev_y.append(graph[path[i]].y)
    dev_x.append(graph[path[0]].x)
    dev_y.append(graph[path[0]].y)
    plot_cities.set_xdata(dev_x)
    plot_cities.set_ydata(dev_y)
    plt.title(str(getLen(graph, path)))
    plt.draw()
    plt.pause(1e-17)


def getMax(graph: [Point], path: [[int]]):
    ans: int = 0
    for i in range(1, len(path)):
        if getLen(graph, path[ans]) > getLen(graph, path[i]):
            ans = i
    return ans


def main(graph: [Point], path: [[int]], max_iter: int):
    global temper
    temper.append(t_max)
    iterat.append(0)
    plt.draw()
    for it in tqdm(range(1, max_iter)):
        temper.append(temperature(t_max, t_min, it, max_iter))
        iterat.append(it)
        plot_t.set_ydata(temper)
        plot_t.set_xdata(iterat)
        plt.draw()
        if it % 1000 == 0:
            printWay(graph, path[getMax(graph, path)])
        for i in range(len(path)):
            way = path[i].copy()
            first: int = randint(0, len(way) - 1)
            second: int = first
            while second == first:
                second = randint(0, len(way) - 1)
            b = way.copy()
            b[first], b[second] = b[second], b[first]
            if isTransition(getProbability(getLen(graph, b) - getLen(graph, way), temperature(t_max, t_min, it,
                                                                                              max_iter))):
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
    return [path[getMax(graph, path)], max_iter, temper]


# Init the constants
t_max: float = 2
t_min: float = 0
max_iterations: int = 100000
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


temper = []
iterat = []
citiesX = []
citiesY = []

print("Generated ways")

plt.show()

plt.subplot(2, 1, 1)
axes1 = plt.gca()
axes1.set_xlim(0, 10)
axes1.set_ylim(0, 10)
plot_cities,  = axes1.plot(citiesX, citiesY, 'bx-')

plt.subplot(2, 1, 2)
axes2 = plt.gca()
axes2.set_xlim(0, max_iterations)
axes2.set_ylim(t_min, t_max)
plot_t, = axes2.plot(iterat, temper)


a = main(data, ways, max_iterations)

printWay(data, a[0])


plt.subplot(2, 1, 2)
plt.plot(range(1, a[1] + 1), a[2])
plt.xlabel("Iteration")
plt.ylabel("Temperature")
print("Created plots")
plt.show()
