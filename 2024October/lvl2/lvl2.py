
def main():
    T = int(input())

    for i in range(T):
        x,y,n = list(map(int,input().split()))
        for yi in range(y):
            for xi in range(x):
                num = (yi*x)+xi
                print(num//3+1, end=" ")
            print()
        print()
if __name__ == "__main__":
    main()