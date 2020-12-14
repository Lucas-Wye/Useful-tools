def quick_mod(a, b, m):
    ans = 1
    a = a % m
    while b != 0:
        if b & 1:
            ans = (ans*a) % m
        b >>= 1
        a = (a*a) % m
    return ans


def getW(N, g, P):
    W = [0 for i in range(N)]
    for i in range(N):
        tmp = quick_mod(g, (P-1) * i // N, P)
        W[i] = tmp if ((P - tmp) > tmp) else (tmp - P)

    return W


def getWn(N, g, P):
    # for the matrix
    Wn = [[0 for i in range(N)] for j in range(N)]
    for n in range(N):
        for k in range(N):
            temp = quick_mod(g, (P-1) * n * k // N, P)
            for item in W:
                if temp == (P - item) and temp > item:
                    temp = -item
            Wn[n][k] = temp
    # print Wn[][] regularly
    for i in range(N):
        print("[", end="")
        for j in range(N):
            print('{:<10}'.format(Wn[i][j]), end=" ")
        print("\b\b]")


if __name__ == "__main__":
    P = 479 * (2 ** 21) + 1
    N = 8
    g = 3

    W = getW(N, g, P)
    print(W)
    print(sum(W))
