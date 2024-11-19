def main():
    T = int(input())

    for i in range(T):
        a,b = list(map(int,input().split()))
        print((a//3)*b)

if __name__ == "__main__":
    main()