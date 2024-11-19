import itertools
from collections import defaultdict, deque
import sys
import os
import gurobipy as gp
from gurobipy import GRB

def printgrid(grid, x, y):
    for yi in range(y):
        for xi in range(x):
            print(grid[(yi,xi)], end= "")
        print()
    print()

def addexclconstr(model, var1, var2, y1, x1, y2, x2):
    if (y1,x1) in var1 and (y2, x2) in var2:
        constraint = model.addConstr(var1[(y1,x1)]+var2[(y2,x2)]<=1)
        # constraint.setAttr("lazy", 1)

def mycallback(model: gp.Model, where):
    if where == GRB.Callback.MIPSOL:
        obj = round(model.cbGetSolution(model._objvar))
        if obj == model._n:
            vert = model.cbGetSolution(model._vert)
            horiz = model.cbGetSolution(model._horiz)

            for k, v in vert.items():
                if v > 0.5:
                    y,x = k
                    model._grid[(y,x)] = "X"
                    model._grid[(y+1,x)] = "X"
            for k, v in horiz.items():
                if v > 0.5:
                    y,x = k
                    model._grid[(y,x)] = "X"
                    model._grid[(y,x+1)] = "X"
            model.terminate()


def max_tiles(y, x, n, grid):
    env = gp.Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()
    model = gp.Model(env = env)
    model.setParam("LogFile", "out.log")
    model.setParam("heuristics", 0.5)
    objvar = model.addVar(vtype = GRB.INTEGER)
    horiz = model.addVars(itertools.product(range(y), range(x-1)), vtype = GRB.BINARY, obj = -1)
    vert = model.addVars(itertools.product(range(y-1), range(x)), vtype = GRB.BINARY, obj = -1)
    obj = gp.quicksum([horiz[(yi,xi)] for yi in range(y) for xi in range(x-1)] + [vert[(yi, xi)] for yi in range(y-1) for xi in range(x)])
    model.addConstr(obj == objvar)
    model.addConstr(objvar == n)
    # model.addConstr(obj == n)
    for yi in range(y):
        for xi in range(x-1):
            for yii in range(yi-1, yi+2):
                for xii in range(xi-2, xi+3):
                    if (xi,yi) != (xii,yii):
                        addexclconstr(model, horiz, horiz, yi, xi, yii, xii)
            for yii in range(yi-2, yi+2):
                for xii in range(xi-1, xi+3):
                    addexclconstr(model, horiz, vert, yi, xi, yii, xii)
    for yi in range(y-1):
        for xi in range(x):
            for yii in range(yi-2, yi+3):
                for xii in range(xi-1, xi+2):
                    if (xi,yi) != (xii,yii):
                        addexclconstr(model, vert, vert, yi, xi, yii, xii)

    
    model._n = n
    model._objvar = objvar
    model._grid = grid
    model._horiz = horiz
    model._vert = vert
    model.optimize(mycallback)
    return model._grid




def reduceinstance(yred, xred, n, grid):
    if yred > 12 and xred % 2 == 1:
        for xi in range(0, xred, 2):
            for yi in range(yred-2, yred):
                grid[(yi,xi)] = "X"
        return 1, yred-3, xred, n-(xred+1)//2
    elif xred > 12 and yred % 2 == 1:
        for yi in range(0, yred, 2):
            for xi in range(xred-2, xred):
                grid[(yi,xi)] = "X"
        return 1, yred, xred-3, n-(yred+1)//2
    elif yred > 12 and xred % 3 == 2:
        for xi in range(xred):
            if xi % 3 != 2:
                grid[(yred-1, xi)] = "X"
        return 1, yred-2, xred, n-(xred+1)//3
    elif xred > 12 and yred % 3 == 2:
        for yi in range(yred):
            if yi % 3 != 2:
                grid[(yi, xred-1)] = "X"
        return 1, yred, xred-2, n-(yred+1)//3
    elif xred > 12:
        for xi in range(xred-5, xred, 2):
            end = yred-4 if yred % 3 == 0 else yred - 2
            for yi in range(end):
                if yi % 3 != 2:
                    grid[(yi, xi)] = "X"
                    n -= 1/2
        grid[(yred-1, xred-1)] = grid[(yred-1, xred-2)] = grid[(yred-1, xred-4)] = grid[(yred-1, xred-5)] = "X"
        n -= 2
        if yred % 3 == 0:
            grid[(yred-3, xred-1)] = grid[(yred-3, xred-2)] = grid[(yred-3, xred-4)] = grid[(yred-3, xred-5)] = "X"
            n -= 2
        return 1, yred, xred-6, round(n)
    else:
        return 0, yred, xred, n

def main():
    T = int(input())

    for i in range(T):
        grid = defaultdict(lambda: ".")
        x,y,n = list(map(int,input().split()))

        xred, yred = x, y

        while max(xred,yred) > 12:
            status, yred, xred, n = reduceinstance(yred, xred, n, grid)
            if status == 0:
                break
            
        max_tiles(yred, xred, n, grid)
        printgrid(grid, x, y)
        # independent_set(y, x, n)
        
if __name__ == "__main__":
    main()