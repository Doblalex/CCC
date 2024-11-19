from collections import defaultdict

def printgrid(grid, x, y):
    for yi in range(y):
        for xi in range(x):
            print(grid[(yi,xi)], end= " ")
        print()
    print()

def fillgridmodeasy(grid, x, y):
    id = 3
    for yi in range(y):
        for xi in range((x//3)*3):
            grid[(yi, xi)] = id // 3
            id += 1
    for xi in range((x//3)*3, x):
        for yi in range((y//3)*3):
            grid[(yi, xi)] = id // 3
            id += 1

def gridhard(grid, x, y):
    id = 3
    for yi in range(y-3):
        for xi in range((x//3)*3):
            grid[(yi, xi)] = id // 3
            id += 1
    for xi in range((x//3)*3, x):
        for yi in range((y//3)*3):
            grid[(yi, xi)] = id // 3
            id += 1
    for xi in range((x//3)*3):
        for yi in range(y-3, y):
            grid[(yi, xi)] = id // 3
            id += 1

def main():
    T = int(input())

    for i in range(T):
        grid = defaultdict(lambda: 0)
        x,y,n = list(map(int,input().split()))
        if not ((x % 3) == 2 and (y % 3) == 2):
            fillgridmodeasy(grid, x, y)
        else:
            gridhard(grid, x, y)
        printgrid(grid, x, y)
if __name__ == "__main__":
    main()