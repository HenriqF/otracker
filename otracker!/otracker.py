#aiohttp

import asyncio
from datetime import date
from ossapi import OssapiAsync
day = date.today()
class jogatina:
    def __init__(self):
        self.titulo = None
        self.acuracia = 0
        self.ar = 0
        self.cs = 0
        self.od = 0
        self.hp = 0
        self.rank = None

    def list(self):
        print("="*20)
        print(self.titulo, ": ")
        print("Estatisticas:")
        print("Acuracia: ", self.acuracia, " | Rank: ", self.rank)
        print("cs: ", self.cs, " ar: ", self.ar, " od: ", self.od, " hp:", self.hp)
        print("="*20)
        return

try:
    c = ""
    with open("app.txt", "r") as f:
        c = f.read()

    info = []
    current = ""
    for char in c:
        if char == "\n":
            info.append(current)
            current = ""
        else:
            current = current+char
    info.append(current)

    api = OssapiAsync(int(info[0]), str(info[1])) #idcliente e senha. pra cirar vai no site do osu configuracoes da conta (leia docs)
except:
    print("Coloca as porra no app.txt direito desgrama:")
    print("Primeira linha: Id do cliente")
    print("Segunda linha: Segredo do cliente ( senha )")
    exit()

async def getStuff(player):
    global api
    usere = await api.user(player)

    return(await api.user_scores(usere, type="recent", include_fails=True, limit=1000)) #recente -> 24horas

def process(list):
    plays = []
    for item in list:
        if item.started_at != None and item.started_at.date() != day:
            play = jogatina()
            play.titulo = item.beatmapset.title
            play.acuracia = round(item.accuracy*100 ,3)
            play.ar = item.beatmap.ar
            play.cs = item.beatmap.cs
            play.od = item.beatmap.accuracy
            play.hp = item.beatmap.drain
            play.rank = item.rank

            plays.append(play)

    print("Escores de ", day, ":")

    for play in plays:
        play.list()

while True:
    process(asyncio.run(getStuff(input("Player --> "))))