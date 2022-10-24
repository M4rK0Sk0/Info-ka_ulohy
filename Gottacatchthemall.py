import requests as req
import json as js
data = req.get('https://raw.githubusercontent.com/yorkcshub/Miscellanous/master/effectiveness.json')
data_json = js.loads(data.text)
preloz = {'super effective':2, 'normal effectivness':1, 'not very effective':0.5, 'no effect':0}
for sila in data_json:
    for utocnik in data_json[sila]:
        temp = attack.get(utocnik,{})
        for obranca in data_json[sila][utocnik]:
            temp[obranca] = preloz[sila]
        attack[utocnik]=temp








