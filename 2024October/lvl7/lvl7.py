import itertools
from collections import defaultdict, deque
import sys
import os
import gurobipy as gp
from gurobipy import GRB
from functools import cache

def printgrid(grid, x, y):
    for yi in range(y):
        for xi in range(x):
            print(grid[(yi,xi)], end= "")
        print()
    print()

def mycallback(model: gp.Model, where):
    if where == GRB.Callback.MIPSOL:
        obj = round(model.cbGetSolution(model._objvar))
        iscell = model.cbGetSolution(model._iscell)
        x = model._x
        y = model._y
        for yi in range(y):
            for xi in range(x):
                if iscell[(yi, xi)] > 0.5:
                    model._grid[(yi, xi)] = "X"
                else:
                    model._grid[(yi, xi)] = "."

def max_tiles(y, x, grid):
    env = gp.Env(empty=True)
    # print(x, y, dl)
    env.setParam("OutputFlag",0)
    env.setParam("MemLimit", 8)
    env.start()
    model = gp.Model(env = env)
    model.setParam("LogFile", "out.log")
    model.setParam("heuristics", 0.99)
    objvar = model.addVar(vtype = GRB.INTEGER)
    iscell = model.addVars(itertools.product(range(y), range(x)), vtype = GRB.BINARY, obj = -1)
    obj = gp.quicksum(iscell[(yi,xi)] for yi in range(y) for xi in range(x))
    model.addConstr(obj == objvar)
    for yi in range(y):
        for xi in range(x):
            if yi > 0 and xi > 0:
                model.addConstr(iscell[(yi, xi)] + iscell[(yi-1, xi-1)] <= 1)
            if yi > 0 and xi < x-1:
                model.addConstr(iscell[(yi, xi)] + iscell[(yi-1, xi+1)] <= 1)
            if yi < y-1 and xi < x-1:
                model.addConstr(iscell[(yi, xi)] + iscell[(yi+1, xi+1)] <= 1)
            if yi < y-1 and xi > 0:
                model.addConstr(iscell[(yi, xi)] + iscell[(yi+1, xi-1)] <= 1)

            if yi > 0 and xi > 0 and xi < x-1 and yi < y-1:
                model.addConstr(iscell[(yi, xi)] + iscell[(yi-1, xi-1)] + iscell[(yi-1, xi+1)] + iscell[(yi+1, xi+1)] + iscell[(yi+1, xi-1)] >= 1)

            if y - yi >= 8:
                model.addConstr(gp.quicksum(iscell[(yii, xi)] for yii in range(yi, yi+8)) <= 7)
            if x - xi >= 8:
                model.addConstr(gp.quicksum(iscell[(yi, xii)] for xii in range(xi, xi+8)) <= 7)
    
    model._objvar = objvar
    model._grid = grid
    model._x = x
    model._y = y
    model._iscell = iscell
    model.optimize(mycallback)
    return round(objvar.X)

class Node:
    def __init__(self, y, x):
        self.children = dict()
        self.y = y
        self.x = x
        self.filledgrid = False
        self.grid = defaultdict(lambda: ".")

    def addchild(self, child, starty, startx):
        self.children[(starty, startx)] = child

    def fillgrid(self):
        if self.filledgrid: return
        self.filledgrid = True

        for pos, ch in self.children.items():
            ch.fillgrid()
            ys, xs = pos
            yd, xd = ch.y, ch.x

            for yi in range(yd):
                for xi in range(xd):
                    self.grid[(ys+yi,xs+xi)] = ch.grid[(yi,xi)]

@cache
def compute_opt(y, x):
    if y <= 0 or x <= 0: return Node(0, 0), 0
    node = Node(y, x)
    if y <= 8 and x <= 8:
        tiles = max_tiles(y,x,node.grid)
        node.filledgrid = True
        return node, tiles
    else:
        maxopt = 0
        for yi in range(y):
            child1, val1 = compute_opt(yi, x)
            child2, val2 = compute_opt(y-yi-1,x)
            if val1 + val2 > maxopt:
                node.children.clear()
                node.addchild(child1, 0, 0)
                node.addchild(child2, yi+1, 0)
                maxopt = val1+val2
        for xi in range(x):
            child1, val1 = compute_opt(y, xi)
            child2, val2 = compute_opt(y,x-xi-1)
            if val1 + val2 > maxopt:
                node.children.clear()
                node.addchild(child1, 0, 0)
                node.addchild(child2, 0, xi+1)
                maxopt = val1+val2
        if x % 2 == 0 and y % 2 == 0:
            for yi in range(y):
                for xi in range(x):
                    x1 = x-xi-1
                    y1 = yi
                    x2 = xi
                    y2 = y-yi-1
                    x3 = x-2*xi-2
                    y3 = y-2*yi-2
                    
                    if x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0 and x3 >= 0 and y3 >= 0:
                        child1, val1 = compute_opt(y1,x1)
                        child2, val2 = compute_opt(y2,x2)
                        child3, val3 = compute_opt(y3,x3)
                        if val1*2+val2*2+val3>maxopt:
                            maxopt = val1*2+val2*2+val3
                            node.children.clear()
                            node.addchild(child1, 0, 0)
                            node.addchild(child2, 0, x1+1)
                            node.addchild(child1, y-y1, xi+1)
                            node.addchild(child2, yi+1, 0)
                            node.addchild(child3, yi+1, xi+1)
        return node, maxopt


def main():
    T = int(input())

    for i in range(T):
        grid = defaultdict(lambda: ".")
        x,y,n = list(map(int,input().split()))

        xred, yred = x, y

        # if not (x % 2 == 0 and y % 2 == 0 and dl % 2 == 0):
        #     continue
        # printgrid(grid, x, y)
        # print()
        # reduced = True
        # while reduced:
        #     reduced = False
        #     for dl in range(7, 6, -1):
        #         while True:
        #             status, yred, xred, n = reduceinstance(yred, xred, n, grid, dl)
        #             # printgrid(grid, x, y)
        #             # print()
        #             if status == 0:
        #                 break           
        #             else:
        #                 reduced = True
        #                 # printgrid(grid, x, y)     
        #                 break
        #         if reduced: break
            
        node, opt = compute_opt(yred, xred)
        assert(opt >= n)
        node.fillgrid()
        printgrid(node.grid, node.x, node.y)
        
if __name__ == "__main__":
    main()