import pygame
from copy import deepcopy
from random import choice, randrange

šír, výš = 10, 20
kocky = 45
ROZ_HRY = šír * kocky, výš * kocky
ROZLIS = 750, 940
FPS = 60

pygame.init()
sc = pygame.display.set_mode(ROZLIS)
hra_sc = pygame.Surface(ROZ_HRY)
hodiny = pygame.time.Clock()

mriežky = [pygame.Rect(x * kocky, y * kocky, kocky, kocky) for x in range(šír) for y in range(výš)]

figúry_poz = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figúry = [[pygame.Rect(x + šír // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figúry_poz]
figúry_rect = pygame.Rect(0, 0, kocky - 2, kocky - 2)
pole = [[0 for i in range(šír)] for j in range(výš)]

ani_poc, ani_rych, ani_limit = 0, 60, 2000

pozadie = pygame.image.load('bg.jpg').convert()
herne_pozadie = pygame.image.load('bg2.jpg').convert()

hlavny_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

nadpis_Tetris = hlavny_font.render('TETRIS', True, pygame.Color('darkorange'))
nadpis_skore = font.render('score:', True, pygame.Color('green'))
nadpis_rekord = font.render('record:', True, pygame.Color('purple'))

daj_farbu = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figúra, nas_figúra = deepcopy(choice(figúry)), deepcopy(choice(figúry))
nas_farba = daj_farbu(), daj_farbu()

skore, riadky = 0, 0
zbieranie_bod = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def skontroluj_hranice():
    if figúra[i].x < 0 or figúra[i].x > šír - 1:
        return False
    elif figúra[i].y > výš - 1 or pole[figúra[i].y][figúra[i].x]:
        return False
    return True


def daj_rekord():
    try:
        with open('rekord!') as f:
            return f.readline()
    except FileNotFoundError:
        with open('rekord!', 'w') as f:
            f.write('0')


def setni_mi_rekord(rekord, skore):
    rec = max(int(rekord), skore)
    with open('rekord', 'w') as f:
        f.write(str(rec))


while True:
    rekord = daj_rekord()
    dx, otočenie = 0, False
    sc.blit(pozadie, (0, 0))
    sc.blit(hra_sc, (20, 20))
    hra_sc.blit(herne_pozadie, (0, 0))
    # časový posun pre plné riadky
    for i in range(riadky):
        pygame.time.wait(200)
    # ovládanie
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                dx = -1
            elif ev.key == pygame.K_RIGHT:
                dx = 1
            elif ev.key == pygame.K_DOWN:
                ani_limit = 100
            elif ev.key == pygame.K_UP:
                rotate = True
    # pohyb x
    stará_figúra = deepcopy(figúra)
    for i in range(4):
        figúra[i].x += dx
        if not skontroluj_hranice():
            figúra = deepcopy(stará_figúra)
            break
    # pohyb y
    ani_poc += ani_rych
    if ani_poc > ani_limit:
        ani_poc = 0
        stará_figúra = deepcopy(figúra)
        for i in range(4):
            figúra[i].y += 1
            if not skontroluj_hranice():
                for i in range(4):
                    pole[stará_figúra[i].y][stará_figúra[i].x] = color
                figúra, color = nas_figúra, nas_farba
                as_figúra, nas_farba = deepcopy(choice(figúry)), daj_farbu()
                anim_limit = 2000
                break
    # otočenie
    stred = figúra[0]
    stará_figúra = deepcopy(figúra)
    if otočenie:
        for i in range(4):
            x = figúra[i].y - stred.y
            y = figúra[i].x - stred.x
            figúra[i].x = stred.x - x
            figúra[i].y = stred.y + y
            if not skontroluj_hranice():
                figúra = deepcopy(stará_figúra)
                break
    # skontroluj riadky
    riadok, riadky = výš - 1, 0
    for row in range(výš - 1, -1, -1):
        počet = 0
        for i in range(šír):
            if pole[row][i]:
                počet += 1
            pole[riadok][i] = pole[row][i]
        if počet < šír:
            riadok -= 1
        else:
            ani_rych += 3
            riadky += 1
    # vypočítať skóre
    skore += zbieranie_bod[riadky]
    # vykresliť mriežky
    [pygame.draw.rect(hra_sc, (40, 40, 40), i_rect, 1) for i_rect in pole]
    # vykresliť figúru
    for i in range(4):
        figúry_rect.x = figúra[i].x * kocky
        figúry_rect.y = figúra[i].y * kocky
        pygame.draw.rect(hra_sc, color, figúry_rect)
    # vykresliť pole
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figúry_rect.x, figúry_rect.y = x * kocky, y * kocky
                pygame.draw.rect(hra_sc, col, figúry_rect)
    # vykresliť ďalšiu figúru
    for i in range(4):
        figúry_rect.x = nas_figúra[i].x * kocky + 380
        figúry_rect.y = nas_figúra[i].y * kocky + 185
        pygame.draw.rect(sc, nas_farba, figúry_rect)
    # draw titles
    sc.blit(nadpis_Tetris, (485, -10))
    sc.blit(nadpis_skore, (535, 780))
    sc.blit(font.render(str(skore), True, pygame.Color('white')), (550, 840))
    sc.blit(nadpis_rekord, (525, 650))
    sc.blit(font.render(rekord, True, pygame.Color('gold')), (550, 710))
    # game over
    for i in range(šír):
        if field[0][i]:
            setni_mi_rekord(rekord, skore)
            field = [[0 for i in range(šír)] for i in range(výš)]
            ani_poc, ani_rych, ani_limit = 0, 60, 2000
            skore = 0
            for i_rect in pole:
                pygame.draw.rect(hra_sc, (), i_rect)
                sc.blit(hra_sc, (20, 20))
                pygame.display.flip()
                hodiny.tick(200)

    pygame.display.flip()
    hodiny.tick(FPS)
