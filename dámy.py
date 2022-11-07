# počet dám, koľko chcem na šachovnici
print ("Zadaj počet dám")
N = int(input())
# spravíme si šachovnicu
board = [[0]*N for _ in range(N)]
def utok(i, j):
    #čekujeme vertikálne a horizontálne
    for k in range(0,N):
        if board[i][k]==1 or board[k][j]==1:
            return True
    #čekujeme diagonálne
    for k in range(0,N):
        for l in range(0,N):
            if (k+l==i+j) or (k-l==i-j):
                if board[k][l]==1:
                    return True
    return False
def pocet_dam(n):
    if n==0:
        return True
    for i in range(0,N):
        for j in range(0,N):
            if (not(utok(i,j))) and (board[i][j]!=1):
                board[i][j] = 1
                if pocet_dam(n-1)==True:
                    return True
                board[i][j] = 0
    return False
pocet_dam(N)
for i in board:
    print (i)
