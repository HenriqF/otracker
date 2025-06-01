
import asyncio
from datetime import date
from ossapi import OssapiAsync
day = date.today()
name = ""
class jogatina:
    def __init__(self):
        self.titulo = None

        self.stars = 0
        self.pp = 0
        self.acuracia = 0
        self.ar = 0
        self.cs = 0
        self.od = 0
        self.rank = None

        self.mods = []
        self.combo = 0
        self.miss = 0
        self.total = 0
        self.score = 0

        self.ss = 0


    def list(self):
        print("="*20,"\n")
        print(self.titulo, ": [", self.stars, "* | ", round(self.pp, 1), "pp]",sep="") if self.pp != None else print(self.titulo, ": [", self.stars, "*]",sep="")

        print("\nEstatisticas:")
        print("Acuracia: ", self.acuracia, " | Rank: ", self.rank)
        print("cs: ", self.cs, " ar: ", self.ar, " od: ", self.od)
        print("Combo: ", self.combo, " - ", self.miss, "x / ", self.total, " - Score: ", self.score ,sep="")

        print("\nMods:")
        for mod in self.mods:
            print(mod.acronym, end=" ")

        print("\nScoreStar: ", self.ss)

        print("\n")
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

    if info[2]:
        name = info[2]
    api = OssapiAsync(int(info[0]), str(info[1])) #idcliente e senha. pra cirar vai no site do osu configuracoes da conta (leia docs)
except:
    print("Coloca as porra no app.txt direito desgrama:")
    print("Primeira linha: Id do cliente")
    print("Segunda linha: Segredo do cliente ( senha )")
    exit()

async def getStuff(player):
    global api
    usere = await api.user(player)

    return(await api.user_scores(usere, type="recent", include_fails=True, limit=1000)) #recent -> 24horas

def process(list):
    plays = []
    for item in list:
        if item.ended_at != None and item.ended_at.date() == day:
            play = jogatina()
            play.titulo = item.beatmapset.title
            play.acuracia = round(item.accuracy*100 ,3)
            play.ar = item.beatmap.ar
            play.cs = item.beatmap.cs
            play.od = item.beatmap.accuracy
            play.rank = item.rank

            play.mods = item.mods
            play.pp = item.pp
            play.stars = item.beatmap.difficulty_rating

            play.score = item.total_score
            play.combo = item.max_combo
            play.miss = item.statistics.miss if item.statistics.miss != None else 0
            play.total = item.beatmap.count_circles + item.beatmap.count_sliders + item.beatmap.count_spinners

            play.ss = round((play.score / 1000000) * play.stars, 2)

            plays.append(play)

    for play in plays:
        play.list()
        pass

while True:
    if name != "":
        process(asyncio.run(getStuff(name)))
        break
    else:
        process(asyncio.run(getStuff(input("Player --> "))))