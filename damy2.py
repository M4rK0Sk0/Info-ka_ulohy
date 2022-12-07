sirka = 8
sachovnica = []

w,h = 8,8
def creator(sirka=8):
    global sachovnica
    sachovnica=[[0 for x in range(w)] for y in range(h)]

def check(x:int, y:int):
    for j in range(sirka):
        for i in range(sirka):
            if i==x or j==y or x+y == i+j or j-i ==  y - x:
                if sachovnica[j][i]==1:
                    return False
    return True


def print_nicely():
    for j in range(sirka):
        print(*sachovnica[j])
    #input("Chceš viac?")
    print()

def attack(cd=0):
    global sachovnica
    if cd == 8:
        #print(sachovnica)
        print_nicely()
    else:
        for i in range(sirka):
            if check(i,cd):
                sachovnica[cd][i]=1
                attack(cd+1)
                sachovnica[cd][i] = 0

creator()
attack(0)
# modifikujte tento program tak, aby riešenia nevypisoval do command linu, ale aby vytvoril adresár s názvom riešenia a za každé riešenie vytvoril obrázok typu .png/.jpg, n&a ktorom bude daná situácia zobrazená
# zavoláme si PIL