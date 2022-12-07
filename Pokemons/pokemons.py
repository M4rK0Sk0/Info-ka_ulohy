import requests as req
import json as js
data = req.get("https://raw.githubusercontent.com/yorkcshub/Miscellanous/master/effectiveness.json")
data_json = js.loads(data.text)

preloz = {"super effective": 2, "normal effective": 1, "not very effective": 0.5, "no effect": 0}

def silapok(pok1, pok2):
    for sila in data_json:
        if pok1 in data_json[sila]:
            if pok2 in data_json[sila].get(pok1):
                return preloz.get(sila)

def utok(x, y, poks):
    skup1 = []
    skup2 = []
    cel_skup = poks.split(",")
    for i in range(x):
        skup1.append(cel_skup[i])
    for i in range(x, y + x):
        skup2.append(cel_skup[i])
    vys1 = round(vs(skup1, skup2), 1)
    vys2 = round(vs(skup2, skup1), 1)
    if vys2 < vys1:
        output = (vys1, vys2, "Dali sme to!")
    elif skup1 < skup2:
        output = (vys1, vys2, "Vyhrali sme!")
    elif vys1 == vys2:
        output = (vys1, vys2, "Remíza!")
    print(output)


def vs(skup1, skup2):
    vys = 0
    for s1 in skup1:
        if " " in s1:
            s1 = s1.split(" ")
            for s2 in skup2:
                if " " in s2:
                    s2 = s2.split(" ")
                    vys += max(silapok(s1[0], s2[0]) * silapok(s1[0], s2[1]), silapok(s1[1], s2[0]) * silapok(s1[1], s2[1]))
                else:
                    vys += max((silapok(s1[0], s2)), (silapok(s1[1], s2)))
        else:
            for s2 in skup2:
                if " " in s2:
                    s2 = s2.split(" ")
                    vys += (silapok(s1, s2[0]) * silapok(s1, s2[1]))
                else:
                    vys += (silapok(s1, s2))
    return vys

utok(3,4,"Psychic Electric,Fire Water,Ghost Dragon,Water Electric,Fighting Steel,Ghost,Poison Fire,Dark Bug")
