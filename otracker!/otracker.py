import asyncio
from datetime import date
from ossapi import OssapiAsync
import os
import ast

####
day = date.today() 
name = "" #nome do player
topplay = 0 #pp da top play (porra)
dailyProgress = [] #plays diarias (formatado) [play.map, play.ss, play.stars, play.miss, play.acuracia]
plays = [] #plays diarais
####

class jogatina:
    def __init__(self):
        self.titulo = None
        self.map = None

        self.date = None

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
    global topplay
    usere = await api.user(player)
    topplay = await api.user_scores(usere, type="best", include_fails=False, limit=1)
    topplay = topplay[0]

    return(await api.user_scores(usere, type="recent", include_fails=False, limit=1000)) #recent -> 24horas || FAZER PRA NAO TER SQUE SENMROE SE=ERPLAY S DE NAO FALHA E ETCETERA,...

def process(list):
    global dailyProgress 
    global plays
    plays = []
    for item in list:
        if item.ended_at != None and item.ended_at.date() == day:
            play = jogatina()

            play.date = item.ended_at

            play.map = item.beatmapset.id
            play.titulo = item.beatmapset.title
            play.acuracia = round(item.accuracy*100 ,3)
            play.ar = item.beatmap.ar
            play.cs = item.beatmap.cs
            play.od = item.beatmap.accuracy
            play.rank = item.rank

            play.mods = item.mods
            play.pp = item.pp if item.pp != None else 0
            play.stars = item.beatmap.difficulty_rating

            play.score = item.total_score
            play.combo = item.max_combo
            play.miss = item.statistics.miss if item.statistics.miss != None else 0
            play.total = item.beatmap.count_circles + item.beatmap.count_sliders + item.beatmap.count_spinners

            play.ss = round((play.score / 1000000) * play.stars *((play.pp/topplay.pp)+1), 2)

            plays.append(play)

    for play in plays:
        dailyProgress.append([play.map, play.ss, play.stars, play.miss, play.acuracia, play.date])
        
    dailyProgress = sorted(dailyProgress, key=lambda x: x[-1])
    dailyProgress = [x[:-1] for x in dailyProgress]
    dailyProgress.insert(0, day)
   
def storeDay(plays):
    global dailyProgress
    day = str(dailyProgress[0])
    
    if not(os.path.exists(f"{name}") and os.path.isdir(f"{name}")):
        os.makedirs(f"{name}", exist_ok=True)

    with open(f"{name}/{day}.txt" ,"w") as f:
        f.write(str(dailyProgress[1:]))
    return

while True:
    if name != "":
        process(asyncio.run(getStuff(name)))
        storeDay(dailyProgress)
        break
    else:
        process(asyncio.run(getStuff(input("Player --> "))))



def listPlays():
    global plays
    for play in plays:
        play.list()
    return

def graphDaily(date):
    try:
        dailyScores = []
        with open(f"{name}/{date}.txt" ,"r") as f:
            dailyScores = ast.literal_eval(f.read())

        print(f"Progress from {date}\n")

        print("="*30)

        all = 0
        maxi = float('-inf')

        for play in dailyScores[1:]:
            header = "         |"
            current = str(play[1])+"ss "

            for i, letter in enumerate(current):
                header = header[:i] + letter + header[i+1:]

            print(header, "#"*int(play[1]))
            maxi = max(maxi, play[1])
            all+=play[1]

        print("="*30)
        print(f"Average ss: {round(all/(len(dailyScores)-1), 2)} | Best ss: {maxi}")
    except Exception as err:
        print(err)
        print("You didnt log your stuff this date. (or you deleted it... you fool, you moron)")


while True:
    msg = input("-->")
    if msg == "playst":
        listPlays()
    elif msg == "grapht":
        graphDaily(day)