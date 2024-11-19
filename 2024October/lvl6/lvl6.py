import itertools
from collections import defaultdict, deque
import sys
import os
import gurobipy as gp
from gurobipy import GRB
import math

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
            dl = model._dl
            vert = model.cbGetSolution(model._vert)
            horiz = model.cbGetSolution(model._horiz)

            for k, v in vert.items():
                if v > 0.5:
                    y,x = k
                    for yi in range(y, y+dl):
                        model._grid[(yi,x)] = "X"
            for k, v in horiz.items():
                if v > 0.5:
                    y,x = k
                    for xi in range(x, x+dl):
                        model._grid[(y,xi)] = "X"
            model.terminate()


def max_tiles(y, x, n, grid, dl):
    env = gp.Env(empty=True)
    # print(x, y, dl)
    env.setParam("OutputFlag",0)
    env.setParam("MemLimit", 8)
    env.start()
    model = gp.Model(env = env)
    model.setParam("LogFile", "out.log")
    model.setParam("heuristics", 0.5)
    objvar = model.addVar(vtype = GRB.INTEGER)
    horiz = model.addVars(itertools.product(range(y), range(x-dl+1)), vtype = GRB.BINARY, obj = -1)
    vert = model.addVars(itertools.product(range(y-dl+1), range(x)), vtype = GRB.BINARY, obj = -1)
    obj = gp.quicksum([horiz[(yi,xi)] for yi in range(y) for xi in range(x-dl+1)] + [vert[(yi, xi)] for yi in range(y-dl+1) for xi in range(x)])
    model.addConstr(obj == objvar)
    model.addConstr(objvar == n)
    # model.addConstr(obj == n)
    for yi in range(y):
        for xi in range(x-dl+1):
            for yii in range(yi-1, yi+2):
                for xii in range(xi-dl, xi+dl+1):
                    if (xi,yi) != (xii,yii):
                        addexclconstr(model, horiz, horiz, yi, xi, yii, xii)
            for yii in range(yi-dl, yi+2):
                for xii in range(xi-1, xi+1+dl):
                    addexclconstr(model, horiz, vert, yi, xi, yii, xii)
    for yi in range(y-dl+1):
        for xi in range(x):
            for yii in range(yi-dl, yi+dl+1):
                for xii in range(xi-1, xi+2):
                    if (xi,yi) != (xii,yii):
                        addexclconstr(model, vert, vert, yi, xi, yii, xii)

    
    model._n = n
    model._objvar = objvar
    model._grid = grid
    model._horiz = horiz
    model._vert = vert
    model._dl = dl
    model.optimize(mycallback)
    return model._grid




def reduceinstance(yred, xred, n, grid, dl):
    if yred >= 2*math.lcm(2, dl+1) and xred % 2 == 1:
        for xi in range(0, xred, 2):
            for yi in range(yred-dl, yred):
                grid[(yi,xi)] = "X"
        return 1, yred-dl-1, xred, n-(xred+1)//2
    elif xred >= 2*math.lcm(2, dl+1) and yred % 2 == 1:
        for yi in range(0, yred, 2):
            for xi in range(xred-dl, xred):
                grid[(yi,xi)] = "X"
        return 1, yred, xred-dl-1, n-(yred+1)//2
    elif yred >= 2*math.lcm(2, dl+1) and xred % (dl+1) == dl:
        for xi in range(xred):
            if xi % (dl+1) != dl:
                grid[(yred-1, xi)] = "X"
        return 1, yred-2, xred, n-(xred+1)//(dl+1)
    elif xred >= 2*math.lcm(2, dl+1) and yred % (dl+1) == dl:
        for yi in range(yred):
            if yi % (dl+1) != dl:
                grid[(yi, xred-1)] = "X"
        return 1, yred, xred-2, n-(yred+1)//(dl+1)
    elif xred >= 2*math.lcm(2, dl+1) and yred >= 2*math.lcm(2, dl+1):
        if dl % 2 == 1:
            return 1, yred-1, xred-1, n
        l = math.lcm(2, dl+1)
        for xi in range(xred-l+1, xred, 2):
            for yi in range(dl):
                grid[(yi, xi)] = "X"
                n -= 1/dl
        for yi in range(dl+1, yred, 2):
            i = 0
            for xi in range(xred-l+1, xred):
                if i % (dl+1) != dl:
                    grid[(yi, xi)] = "X"
                    n -= 1/dl   
                i += 1         
        return 1, yred, xred-l, round(n)
    return 0, yred, xred, n

def main():
    T = int(input())

    for i in range(T):
        grid = defaultdict(lambda: ".")
        x,y,n,dl = list(map(int,input().split()))

        xred, yred = x, y

        # if not (x % 2 == 0 and y % 2 == 0 and dl % 2 == 0):
        #     continue
        # printgrid(grid, x, y)
        # print()
        while True:
            status, yred, xred, n = reduceinstance(yred, xred, n, grid, dl)
            # printgrid(grid, x, y)
            # print()
            if status == 0:
                break                
            
        max_tiles(yred, xred, n, grid, dl)
        printgrid(grid, x, y)
        
if __name__ == "__main__":
    main()