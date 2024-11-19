from collections import defaultdict
def printgrid(grid, x, y):
    for yi in range(y):
        for xi in range(x):
            print(grid[(yi,xi)], end= " ")
        print()
    print()

def max_tiles(y, x):
    # Initialize grid with zeros to represent empty spaces
    grid = [["."] * x for _ in range(y)]
    tile_count = 0  # Counter to track the number of tiles placed

    # Place tiles in a "checkerboard" style, skipping rows and columns to avoid touching
    for i in range(0, y, 2):  # Only every 2nd row to avoid vertical adjacency
        for j in range(0, x, 2):  # Only every 2nd column to avoid horizontal adjacency
            # Attempt to place a 1x3 tile horizontally if there's room
            if j + 2 < x and grid[i][j] == grid[i][j + 1] == grid[i][j + 2] == ".":
                tile_count += 1
                grid[i][j] = grid[i][j + 1] = grid[i][j + 2] = "X"
            # If horizontal is not possible, attempt a 3x1 tile vertically
            elif i + 2 < y and grid[i][j] == grid[i + 1][j] == grid[i + 2][j] == ".":
                tile_count += 1
                grid[i][j] = grid[i + 1][j] = grid[i + 2][j] = "X"

    # Display the grid for visualization
    

    return tile_count, grid

def main():
    T = int(input())

    for i in range(T):
        grid = defaultdict(lambda: 0)
        x,y,n = list(map(int,input().split()))
        tiles, grid = max_tiles(y, x)
        assert(tiles == n)
        for row in grid:
            print("".join(f"{cell}" for cell in row))
        print()
if __name__ == "__main__":
    main()