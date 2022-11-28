import pygame, os, unittest
from pygame.locals import *
from datetime import datetime
from random import *


pygame.init()
#Centre la fenetre
os.environ['SDL_VIDEO_CENTERED'] = '1'
#Création fenetre
wwidth,wheight = 1280,720

fe = pygame.display.set_mode((wwidth,wheight))
fe.fill((0, 0, 0))
pygame.display.set_caption("SnakeByLC")


pygame.display.update()

#SUPER VARIABLES

version = "1.6.1"

#Détermine les tailles possibles p/r taille écran
#PGCD width et height
a,b=wwidth,wheight
while b>0:
    a,b=b,a%b
pgcd=a
#Diviseurs
sizesOK = [pgcd]
while pgcd>=6:
    pgcd-=1
    if sizesOK[0]%pgcd == 0:
        sizesOK.append(pgcd)

load = True
wdaction = "menu"
menuact = 0
wcsc = 0
score = 0
screenborders = True
mode = "normal"

bgcolor = (255,255,255)

#Clock speed

clockspeed = 4
tmit = clockspeed

#Taille

lenght = 1
objlenght = 6
dellenght = 0
size = sizesOK[2]

#Coords

x,y=100,100
adir="left"
fadir=""
snakeCoords=[(x,y)]

#Couleur serpent

skin="classic"
skinData = 0
sncr=(231, 76, 60)

#Powerud cache

poweruds = True
powCache = [skin,clockspeed,objlenght]
powAction = "action"
powerstats = [0,0] #bonus / malus

#Design vars


psize = 0
while psize <= wwidth*0.75:
    psize+=size

#
# ECRAN DE DEMARRAGE & FONCTIONS UTILITAIRES
#


#Fonc: Ecran de démarrage
def welcomeScreen(phase):
    
    if phase == 3:
        resetScreen()
    pygame.display.update()

#Fonc: récupere une police
def getFont(name,size):
    try:
        return pygame.font.Font("fonts/" + name + ".ttf", size)
    except:
        try:
            return pygame.font.Font(name + ".ttf", size)
        except:
            return pygame.font.SysFont("Helvetica",size)

#Fonc: traduit un booléen en string
def transBool(boo):
    if boo == False:
        return "non"
    else:
        return "oui"
 
#Fonc: converti couleur nom en RGB
def getColorByName(color):
    if color == "darkred":
        return (192, 57, 43)
    elif color == "red":
        return (231, 76, 60)
    elif color == "orange":
        return (230, 126, 34)
    elif color == "darkyellow":
        return (243, 156, 18)
    elif color == "yellow":
        return (241, 196, 15)
    elif color == "darkaqua":
        return (22, 160, 133)
    elif color == "aqua":
        return (26, 188, 156)
    elif color == "darkgreen":
        return (39, 174, 96)
    elif color == "green":
        return (46, 204, 113)
    elif color == "darkblue":
        return (41, 128, 185)
    elif color == "blue":
        return (52, 152, 219)
    elif color == "darkpurple":
        return (142, 68, 173)
    elif color == "purple":
        return (155, 89, 182)
    elif color == "darkmidnight":
        return (44, 62, 80)
    elif color == "midnight":
        return (52, 73, 94)
    elif color == "darkgrey":
        return (127, 140, 141)
    elif color == "grey":
        return (149, 165, 166)
    elif color == "lightgrey":
        return (189, 195, 199)
    elif color == "whitesmoke":
        return (236, 240, 241)
    elif color == "black":
        return (0, 0, 0)
    elif color == "white":
        return (255, 255, 255)

#
# FONCTIONS HISTORIQUE ET SCORE
#


scorepath = os.getenv('APPDATA') + "\\Snake\\score"
historypath = os.getenv('APPDATA') + "\\Snake\\history"

def getHighScore():
    try:
        fichier = open(scorepath + "_" + mode, "r")
        hs = fichier.read()
        fichier.close()
        return int(hs)
    except: 
        try:
            fichier = open(scorepath + "_" + mode, "w")
            fichier.write("0")
            fichier.close()
            return 0
        except:
            os.makedirs(os.getenv('APPDATA') + "\\Snake")
            fichier = open(scorepath + "_" + mode, "w")
            fichier.write("0")
            fichier.close()
            return 0
            

def newScore(score):
    if score > getHighScore():
        fichier = open(scorepath + "_" + mode, "w")
        fichier.write(str(score))
        fichier.close()

def getHistory():
    try:
        fichier = open(historypath, "r")
        history = fichier.readlines()
        fichier.close()
        return [ln.strip() for ln in history] 
    except: 
        try:
            fichier = open(historypath, "w")
            fichier.write("")
            fichier.close()
            return []
        except:
            os.makedirs(os.getenv('APPDATA') + "\\Snake")
            fichier = open(historypath, "w")
            fichier.write("")
            fichier.close()
            return []

def addHistory(bonus,malus,score,diff):
    #Date
    date = datetime.now()
    game_time = str(date.day) + "/" + str(date.month) + "/" + str(date.year) + " " + str(date.hour) + ":" + str(date.minute)
    #Difficulté
    diff = translateMode(diff).lower()
    #Str partie
    gameHistory = game_time + "," + str(bonus) + "," + str(malus) + "," + str(score) + "," + diff + "\n"
    #Intégration
    totalHistory = ""
    for ln in getHistory():
        totalHistory += ln + "\n"
    totalHistory += gameHistory
    fichier = open(historypath, "w")
    fichier.write(totalHistory)
    fichier.close()

def getHistoryGame(nb=1):
    try:
        history = getHistory()
        history.reverse()
        game = history[nb-1]
        return game.split(",")
    except:
        return "" 
#
# TEST UNITAIRE RAPIDE
#
class TestUtils(unittest.TestCase):
    def test_getColorByName(self):
        self.assertTrue(getColorByName("red"))
    def test_transBool(self):
        self.assertTrue(transBool(False))    
    def test_high(self):
        self.assertTrue(getHighScore()) 

if __name__ == '__main__':
    unittest.main()  
#
# FONCTIONS UTILITAIRES DU JEU ET DESIGN
#
    
#Fonc: [UI] met à jour l'affichage des options
def reloadOption(hover=""):
    buttons = ["opt_skin_classic","opt_time_classic","opt_size_classic","opt_bord_classic",
               "opt_objl_classic","clg_easy_classic","clg_normal_classic","clg_hard_classic",
               "clg_vhard_classic","retour_classic"]
    for but in buttons:
        if but == hover + "_classic":
            makeButton(hover + "_hovered")
        else:
            makeButton(but)

#Fonc: [UI] Boutons options
def drawOptBut(text, xO, yO, act="classic"):
    if act == "classic":
        pygame.draw.rect(fe, getColorByName("white"), ((wwidth-1125)+xO, yO, 250, 25))
        pygame.draw.rect(fe, getColorByName("white"), ((wwidth-1125)+(xO-10), yO+4, 5, 16))
        text = getFont("Ubuntu-R",20).render(text, 1, getColorByName("midnight"))
        fe.blit(text, ((wwidth-1125)+xO, yO))
    else:
        pygame.draw.rect(fe, getColorByName("white"), ((wwidth-1125)+xO, yO, 250, 25))
        pygame.draw.rect(fe, getColorByName("black"), ((wwidth-1125)+(xO-10), yO+4, 5, 16))
        text = getFont("Ubuntu-R",20).render(text, 1, getColorByName("black"))
        fe.blit(text, ((wwidth-1125)+xO, yO))

#Fonc: [UI] Boutons challenge
def drawClgBut(text, xO, yO, act="classic"):
    color = (230, 230, 230)
    if text == " Facile" and (mode == "easy" or act == "hovered"):
        color = getColorByName("purple")
    elif text == "Normal" and (mode == "normal" or act == "hovered"):
        color = getColorByName("blue")
    elif text == "  Hard'" and (mode == "hard" or act == "hovered"):
        color = getColorByName("orange")
    elif text == " Extrem" and (mode == "vhard" or act == "hovered"):
        color = getColorByName("darkred")
    if act == "classic":
        textcolor = getColorByName("white")
        if color == (230, 230, 230):
            textcolor = getColorByName("black")
        pygame.draw.rect(fe, color, ((wwidth-1125)+xO, yO, 150, 80))
        text = getFont("Ubuntu-B",25).render(text, 1, textcolor)
        fe.blit(text, ((wwidth-1125)+xO+30, yO+24))
    else:
        color = (color[0]+20,color[1]+20,color[2]+20)
        pygame.draw.rect(fe, color, ((wwidth-1125)+xO, yO, 150, 80))
        text = getFont("Ubuntu-B",25).render(text, 1, getColorByName("white"))
        fe.blit(text, ((wwidth-1125)+xO+30, yO+24))
        

#Fonc: [UI] boutons
def makeButton(bID):
    global size
    fontm = getFont("Ubuntu-B",16)
    
    #Couleur du bouton JOUER quand la sourris n'est pas dessus
    if bID == "jouer_classic":
        pygame.draw.rect(fe, getColorByName("black"), (570, 475, 200, 70))
        pygame.draw.rect(fe, getColorByName("white"), (574, 479, 192, 62))
        text = getFont("Ubuntu-B",29).render("Jouer", 1, getColorByName("black"))
        fe.blit(text, (633, 490))
    #Couleur du bouton JOUER quand la sourris est dessus
    elif bID == "jouer_hovered":
        pygame.draw.rect(fe, getColorByName("black"), (570, 475, 200, 70))
        pygame.draw.rect(fe, getColorByName("black"), (574, 479, 192, 62))
        text = getFont("Ubuntu-B",29).render("Jouer", 1, getColorByName("white"))
        fe.blit(text, (633, 490))
    #Couleur du bouton OPTION quand la sourris n'est pas dessus
    if bID == "options_classic":
        pygame.draw.rect(fe, getColorByName("black"), (620, 560, 100, 30))
        pygame.draw.rect(fe, getColorByName("white"), (623, 563, 94, 24))
        text = fontm.render("Options", 1, getColorByName("black"))
        fe.blit(text, (638, 564))
    #Couleur du bouton OPTION quand la sourris est dessus
    elif bID == "options_hovered":
        pygame.draw.rect(fe, getColorByName("black"), (620, 560, 100, 30))
        pygame.draw.rect(fe, getColorByName("black"), (623, 563, 94, 24))
        text = fontm.render("Options", 1, getColorByName("white"))
        fe.blit(text, (638, 564))
    #Couleur du bouton RETOUR quand la sourris n'est pas dessus
    elif bID == "retour_classic":
        pygame.draw.rect(fe, getColorByName("white"), ((wwidth-1125)+820, 30, 125, 40))
        text = getFont("Ubuntu-R",20).render("Retour", 1, getColorByName("black"))
        fe.blit(text, ((wwidth-1125)+850, 38))
    #Couleur du bouton RETOUR quand la sourris est dessus
    elif bID == "retour_hovered":
        pygame.draw.rect(fe, getColorByName("black"), ((wwidth-1125)+820, 30, 125, 40))
        text = getFont("Ubuntu-R",20).render("Retour", 1, getColorByName("white"))
        fe.blit(text, ((wwidth-1125)+850, 38))
    elif bID == "opt_size_classic":
        drawOptBut("Taille : " + str(size),120,190,"classic")
    elif bID == "opt_size_hovered":
        drawOptBut("Taille : " + str(size),120,190,"hovered")
    elif bID == "opt_time_classic":
        drawOptBut("Vitesse : " + str(clockspeed),120,230,"classic")
    elif bID == "opt_time_hovered":
        drawOptBut("Vitesse : " + str(clockspeed),120,230,"hovered")
    elif bID == "opt_skin_classic":
        drawOptBut("Skin : " + skin,120,350,"classic")
    elif bID == "opt_skin_hovered":
        drawOptBut("Skin : " + skin,120,350,"hovered")
    elif bID == "opt_bord_classic":
        drawOptBut("Bordures : " + transBool(screenborders),120,430,"classic")
    elif bID == "opt_bord_hovered":
        drawOptBut("Bordures : " + transBool(screenborders),120,430,"hovered")
    elif bID == "opt_objl_classic":
        drawOptBut("Grossissement : " + str(objlenght),120,470,"classic")
    elif bID == "opt_objl_hovered":
        drawOptBut("Grossissement : " + str(objlenght),120,470,"hovered")
    elif bID == "clg_easy_classic":
        drawClgBut(" Facile",100,550,"classic")
    elif bID == "clg_easy_hovered":
        drawClgBut(" Facile",100,550,"hovered")
    elif bID == "clg_normal_classic":
        drawClgBut("Normal",300,550,"classic")
    elif bID == "clg_normal_hovered":
        drawClgBut("Normal",300,550,"hovered")
    elif bID == "clg_hard_classic":
        drawClgBut("  Hard'",500,550,"classic")
    elif bID == "clg_hard_hovered":
        drawClgBut("  Hard'",500,550,"hovered")
    elif bID == "clg_vhard_classic":
        drawClgBut(" Extrem",700,550,"classic")
    elif bID == "clg_vhard_hovered":
        drawClgBut(" Extrem",700,550,"hovered")
    pygame.display.update()

#Fonc: remet à 0 l'affichage
def resetScreen(color=getColorByName("white")):
    global bgcolor
    bgcolor = color
    fe.fill(color)
    pygame.display.update()
    
#Fonc: place l'objectif aléatoirement
def objectivePlace():
    global x0,y0
    resetScreen()
    x0 = size*randrange(0,int((wwidth)/size))
    y0 = size*randrange(0,int((wheight)/size))
    while verifQueue(x0,y0) == True:
        x0 = size*randrange(0,int((wwidth)/size))
        y0 = size*randrange(0,int((wheight)/size))

#Fonc: faire apparaitre un "carré"
def drawRect(color,x,y,osize=-1):
    global size
    if osize == -1:
        osize = size
    #Les coordonnées correspondent à l'extrémité
    #Haut-Gauche
    pygame.draw.rect(fe, color, (x, y, osize, osize))

def verifChallenges():
    global mode
    wrong = False
    if mode == "easy":
        if size != sizesOK[1] or clockspeed != 10 or objlenght != 3 or screenborders != False:
            wrong = True
    if mode == "normal":
        if size != sizesOK[2] or clockspeed != 4 or objlenght != 6 or screenborders != True:
            wrong = True
    if mode == "hard":
        if size != sizesOK[2] or clockspeed != 2 or objlenght != 12 or screenborders != True:
            wrong = True
    if mode == "vhard":
        if size != sizesOK[3] or clockspeed != 2 or objlenght != 20 or screenborders != True:
            wrong = True
    if wrong == True:
        mode = ""
        reloadOption()
            

#
# GESTION DU SERPENT
#

#Fonc: vérifier si les coords sont sur le serpent ou pas (
def verifQueue(x,y):
    global snakeCoords
    #POWER-UP d'invincibilité
    if powAction == "nodeathqueue":
        return False
    #Pour chaque carré de la queue on check si c'est égal
    #aux coords de la tête.
    for xy in snakeCoords:
        if xy[0] == x and xy[1] == y:
            return True
    return False

#Fonc: récupère la couleur en fonction de
#l'ID du carré demandé.
def getSkin(rectID):
    global skin,skinData
    #Skin du serpent
    if skin == "classic":
        if rectID == 0:
            #Couleur de la tête du serpent
            return getColorByName("red")
        else:
            #Couleur du corps
            return getColorByName("green")
    else:
        skin = "classic"
        getSkin(rectID)

#Fonc: Mise à jour du serpent à chaque déplacement
def updateSnake():
    global snakeCoords,x,y,skin,skinData,dellenght
    snakeCoords.reverse()
    #Enlève l'affichage du dernier
    lastxy = snakeCoords[0]
    drawRect(getColorByName("white"),lastxy[0],lastxy[1])
    #On supprime le dernier carré (coords)
    if dellenght == 0:
        del snakeCoords[0]
    else:
        dellenght-=1
    #Ajoute les coordonnés actuels
    snakeCoords.append((x,y))
    #sens normal
    snakeCoords.reverse()
    #Affichage
    rectID=-1
    for xy in snakeCoords:
        rectID+=1
        drawRect(getSkin(rectID),xy[0],xy[1])
    #Data : skin clignotant
    if skin == "blink":
        if skinData == 0:
            skinData = 10-clockspeed
        else:
            skinData -= 1

#
# GESTION PARTIE & CONTROLES
#

#Fonc: game over
def sendGameOver():
    global powerstats,x,y,size,clockspeed,score,snakeCoords,load,lenght,wdaction,menuact,tmit,objlenght
   
    #AFFICHAGE écran
    menuact = 0
    wdaction = "menu"
    resetScreen((100,0,100))
    updateSnake()
    drawRect(getSkin(0),x,y)
    font = getFont("Ubuntu-BI",72)
    text = font.render("Game Over.", 1, getColorByName("white"))
    fe.blit(text, (int(wwidth/2)-200, 300))
 
    pygame.display.update()
    pygame.time.Clock().tick(0.5)
    #Game historique
    addHistory(powerstats[0],powerstats[1],score,mode)
    #Vérifie le meilleur score
    newScore(score)
    #RESET partie
    snakeCoords=[(x,y)]
    score = 0
    objectivePlace()
    lenght = 1
    tmit = clockspeed
    updateCache(True)
    powerstats=[0,0]

#Fonc: POWERUDs cache
def updateCache(reset=False):
    global powCache,powAction,skin,clockspeed,objlenght
    if reset == False:
        powCache = [skin,clockspeed,objlenght]
    else:
        powAction = ""
        if powCache[0] != skin:
            skin = powCache[0]
        if powCache[1] != clockspeed:
            clockspeed = powCache[1]
        if powCache[2] != objlenght:
            objlenght = powCache[2]

#Fonc: Traduction nom de code des POWERUDs
def translatePowerud(name=""):
    global powAction
    #Recup le powerud actuel si non précisé
    if name == "":
        name = powAction
    #Listes nom de code/traduite
    powerudsList = ["nogrow","brake","nodeathqueue","blink","moregrow","speed"]
    translatedPowerudsList = ["Grossissement nul","Ralentissement","Queue invincible","Clignotement","Grossissement doublé","Accélération"]
    if name in powerudsList:
        #Si nom de code est dans la liste on prend l'équivalent
        #dans la liste traduite
        return translatedPowerudsList[powerudsList.index(name)]
    else:
        #Si nom de code inexistant, on affiche celui-ci
        return name

#Fonc: Traduction nom de la difficulté
def translateMode(name="",fem=False):
    diff = "FACILE"
    if name == "normal":
        diff = "NORMAL"
        if fem == True: #Féminin
            diff += "E"
    elif name == "hard":
        diff = "DIFFICILE"
    elif name == "vhard":
        diff = "EXTRÊME"
    elif name == "":
        diff = "N/A"
    return diff

#Fonc: gestion power-up (victoire)
def sendPowerud():
    global powAction,powCache,skin,clockspeed,objlenght
    powerup = False
    #50% de chance d'avoir un powerud
    rd = randrange(0,2)
    if poweruds == True:
        if rd != 1:
            updateCache(True)
            return
    else:
        updateCache(True)
        return
    rd = randrange(0,101)
    #Détermination si c'est malus ou bonus
    if mode == "easy":
        if rd >= 20: #80% bonus
            powerup = True
    elif mode == "normal":
        if rd >= 50: #50% bonus (équilibré)
            powerup = True
    elif mode == "hard":
        if rd >= 65: #35% bonus
            powerup = True
    else:
        if rd >= 80: #20% bonus
            powerup = True
    #Reset POWERUD
    updateCache(True)
    #Mise en cache des données
    updateCache()
    #Détermination de l'effet
    if powerup == True:
        #BONUS :)
        bonus = ["nogrow","brake","nodeathqueue"]
        rd=randrange(0,len(bonus))
        powAction = bonus[rd]
        if powAction == "brake":
            clockspeed += 2
        #DESIGN
        #Fond
        resetScreen((223, 255, 221)) #vert clair
        #Nom POWERUD en bas à droite
        text = getFont("Ubuntu-BI",22).render(translatePowerud() + " !", 1, getColorByName("darkgreen"))
        fe.blit(text, (20, 670))
        #Stat
        powerstats[0] = powerstats[0]+1
    else:
        #MALUS :(
        malus = ["blink","moregrow","speed"]
        rd=randrange(0,len(malus))
        powAction = malus[rd]
        #Si mode extr'm et malus speed, on l'enleve
        if mode == "vhard" and powAction == "speed":
            powAction = "blink"
        if powAction == "blink":
            skin = "blink"
        elif powAction == "moregrow":
            objlenght *= 2
        elif powAction == "speed":
            clockspeed -= 1
        #DESIGN
        #Fond
        resetScreen((255, 223, 221)) #rouge clair
        #Nom POWERUD en bas à droite
        text = getFont("Ubuntu-BI",22).render(translatePowerud() + " !", 1, getColorByName("black"))
        fe.blit(text, (20, 670))
        #Stat
        powerstats[1] = powerstats[1]+1
        

#Fonc: modifie les coordonnés en fonction de l'action
def move(dir):
    global x,y,snak1,fadir
    #On enlève l'actuel
    drawRect(getColorByName("white"),x,y)
    #coords
    if dir == "left": #gauche
        #Modifie les coordonnés, et déplace le carré
        x-=size
    if dir == "right": #droite
        x+=size
    if dir == "top": #top
        y-=size
    if dir == "bottom": #bot
        y+=size
    fadir=""
    verifcoords()

#Fonc: Analyse les coordonnés pour diverses utilités.
def verifcoords():
    global x,y,size,clockspeed,score,snakeCoords,load,lenght,wdaction,menuact,tmit,objlenght,dellenght,powAction
    #BORDS DE LA FENETRE
    bordloose = False
    xtemp,ytemp = x,y
    if x < 0:
        x = wwidth-size
    if y < 0:
        y = wheight-size
    if x >= wwidth:
        x = 0
    if y >= wheight:
        y = 0
    if (xtemp != x or ytemp != y) and screenborders == True:
        bordloose = True
    #DEFAITE (Mordu la queue)
    if verifQueue(x,y) == True or bordloose == True:
        sendGameOver()
    #VICTOIRE MANCHE (Objectif)
    if x == x0 and y == y0:
        #Score et objectif
        score+=1
        objectivePlace()
        #VICTOIRE : POWERUD
        sendPowerud()
        if powAction != "nogrow":
            dellenght = objlenght
            lenght+=objlenght
        else:
            powAction = ""
        #Affichage Score
        pygame.display.set_caption("SnakeByLC Score : " + str(score))
    #Maj serpent
    updateSnake()
    

#Prog: Ecran de démarrage
loadScreen = True
screenNb = 91 #Screen de démarrage
while loadScreen:
    screenNb -= 1
    if screenNb == 90:
        welcomeScreen(0)
    elif screenNb == 60:
        welcomeScreen(1)
    elif screenNb == 30:
        welcomeScreen(2)
    elif screenNb == 0:
        welcomeScreen(3)
        loadScreen = False
    pygame.time.Clock().tick(50)

#Main loop
while load:
    #BEFORE START SNAKE
    if wdaction == "snakestart":
        pygame.time.Clock().tick(100)
        if menuact == 2:
            updateCache()
            resetScreen()
            menuact = 0
            x = size*randrange(0,int((wwidth)/size))
            y = size*randrange(0,int((wheight-size)/size))
            snakeCoords=[(x,y)]
            #Objectif
            snak2 = pygame.draw.rect(fe, getColorByName("darkyellow"), (x0, y0, size, size))
            drawRect(getSkin(0),x,y)
            #Text
            text = getFont("Ubuntu-B",22).render("Utilisez ZQSD ou les flèches pour vous déplacer.", 1, getColorByName("black"))
            fe.blit(text, (int(wwidth/2)-230, 400))
            pygame.display.update()
            tmit = 1
            #Display update
        #Events
        for event in pygame.event.get():
            #Type clavier
            if event.type == QUIT:
                load = False
            if event.type == KEYDOWN:
                if fadir == "":
                    fadir = adir
                #Flèches
                if event.key == K_LEFT or event.key == K_a:
                    adir="left"
                    wdaction = "snake"
                    menuact = 2
                elif event.key == K_RIGHT or event.key == K_d:
                    adir="right"
                    wdaction = "snake"
                    menuact = 2
                elif event.key == K_UP or event.key == K_w:
                    adir="top"
                    wdaction = "snake"
                    menuact = 2
                elif event.key == K_DOWN or event.key == K_s:
                    adir="bottom"
                    wdaction = "snake"
                    menuact = 2
    #JEU SNAKE
    if wdaction == "snake":
        if menuact == 2:
            menuact = 0
            resetScreen()
        #Gestion du temps (où 20 ticks = 1 avancement)
        pygame.time.Clock().tick(100) #100 FPS
        if tmit == 0:
            #On avance la tête
            move(adir)
            tmit = clockspeed
            #On remet le curseur de base
            #en cas de cause extérieure
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        tmit -= 1
        #Objectif
        snak2 = pygame.draw.rect(fe, getColorByName("darkyellow"), (x0, y0, size, size))
        #Display update
        pygame.display.update()
        #Events
        for event in pygame.event.get():
            #Type clavier
            if event.type == QUIT:
                load = False
            if event.type == KEYDOWN:
                if fadir == "":
                    fadir = adir
                #Flèches
                if (event.key == K_LEFT or event.key == K_a) and (fadir != "right" or lenght == 1):
                    adir="left"
                elif (event.key == K_RIGHT or event.key == K_d) and (fadir != "left" or lenght == 1):
                    adir="right"
                elif (event.key == K_UP or event.key == K_w) and (fadir != "bottom" or lenght == 1):
                    adir="top"
                elif (event.key == K_DOWN or event.key == K_s) and (fadir != "top" or lenght == 1):
                    adir="bottom"
                elif event.key == K_SPACE:
                    wdaction = "pause"
                    menuact = 1
                elif event.key == K_ESCAPE:
                    sendGameOver()
    #PAUSE GAME
    elif wdaction == "pause":
        if menuact == 1:
            menuact = 0
            text = font.render("Pause.", 1, getColorByName("midnight"))
            fe.blit(text, (int(wwidth/2)-100, int(wheight/2)-100))
            #Display update
            pygame.display.update()
        #Events
        for event in pygame.event.get():
            #Type clavier
            if event.type == QUIT:
                load = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    wdaction = "snake"
                    resetScreen(bgcolor)
    #MENU OPTIONS
    elif wdaction == "options":
        pygame.time.Clock().tick(15)
        if menuact == 0:
            resetScreen()
            #DESIGN PAGE
            #header
            pygame.draw.rect(fe, getColorByName("black"), (0, 0, wwidth, 100))
            text = getFont("Ubuntu-B",50).render("Options", 1, getColorByName("white"))
            fe.blit(text, (100, 18))
            #taille et vitesse(wwidth-1000)
            text = getFont("Ubuntu-B",22).render("GENERAL", 1, getColorByName("black"))
            fe.blit(text, ((wwidth-1125)+100, 150))
            #Skin
            text = getFont("Ubuntu-B",22).render("SKIN", 1, getColorByName("black"))
            fe.blit(text, ((wwidth-1125)+100, 270))
            #Règles
            text = getFont("Ubuntu-B",22).render("RÈGLES", 1, getColorByName("black"))
            fe.blit(text, ((wwidth-1125)+100, 390))
            #Challenges
            text = getFont("Ubuntu-B",22).render("CHALLENGES", 1, getColorByName("black"))
            fe.blit(text, ((wwidth-1125)+100, 510))
            #Boutons
            reloadOption()
            menuact = 1
        
        i=0
        x,y,lenght = (wwidth-1125)+100,310,16
        for i in range(0,16):
            drawRect(getSkin(i),x,y,25)
            x+=25
            i+=1
        x,y,lenght = 0,0,1
        pygame.display.update()
        #EVENTS
        for event in pygame.event.get():
            #Type Souris
            if event.type == pygame.MOUSEMOTION:
                mousecoords = pygame.mouse.get_pos()
                #Hover boutons
                #RETOUR
                if (mousecoords[0] >= (wwidth-1125)+820 and mousecoords[0] <= (wwidth-1125)+945) and (mousecoords[1] >= 30 and mousecoords[1] <= 70):
                    reloadOption("retour")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: taille
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+220) and (mousecoords[1] >= 190 and mousecoords[1] <= 210):
                    reloadOption("opt_size")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: temps
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 230 and mousecoords[1] <= 250):
                    reloadOption("opt_time")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: skin
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 350 and mousecoords[1] <= 370):
                    reloadOption("opt_skin")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: bordures
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 430 and mousecoords[1] <= 450):
                    reloadOption("opt_bord")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPT: grossissement
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 470 and mousecoords[1] <= 490):
                    reloadOption("opt_objl")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Facile
                elif (mousecoords[0] >= (wwidth-1125)+100 and mousecoords[0] <= (wwidth-1125)+250) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_easy")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Normal
                elif (mousecoords[0] >= (wwidth-1125)+300 and mousecoords[0] <= (wwidth-1125)+450) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_normal")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Dur
                elif (mousecoords[0] >= (wwidth-1125)+500 and mousecoords[0] <= (wwidth-1125)+650) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_hard")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #CLG: Extreme
                elif (mousecoords[0] >= (wwidth-1125)+700 and mousecoords[0] <= (wwidth-1125)+850) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    reloadOption("clg_vhard")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    reloadOption()
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
            #Click souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                #RETOUR
                if (mousecoords[0] >= (wwidth-1125)+820 and mousecoords[0] <= (wwidth-1125)+945) and (mousecoords[1] >= 30 and mousecoords[1] <= 70):
                    resetScreen()
                    menuact = 0
                    wdaction = "menu"
                #TAILLE
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+220) and (mousecoords[1] >= 190 and mousecoords[1] <= 210):
                    sizes = sizesOK
                    siID = sizes.index(size)
                    siID += 1
                    if siID == len(sizes):
                        siID = 0
                    size = sizes[siID]
                    reloadOption("opt_size")
                #BORDURES
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 430 and mousecoords[1] <= 450):
                    if screenborders == False:
                        screenborders = True
                    else:
                        screenborders = False
                    reloadOption("opt_bord")
                #VITESSE
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 230 and mousecoords[1] <= 250):
                    speeds = [1,2,3,4,5,6,7,8,9,10]
                    spID = speeds.index(clockspeed)
                    spID += 1
                    if spID == len(speeds):
                        spID = 0
                    clockspeed = speeds[spID]
                    reloadOption("opt_time")
                #GROSSISSEMENT
                elif (mousecoords[0] >= (wwidth-1125)+120 and mousecoords[0] <= (wwidth-1125)+320) and (mousecoords[1] >= 470 and mousecoords[1] <= 490):
                    grosst = [0,1,2,3,4,5,6,8,10,15,20]
                    grID = grosst.index(objlenght)
                    grID += 1
                    if grID == len(grosst):
                        grID = 0
                    objlenght = grosst[grID]
                    reloadOption("opt_objl")
                
                #CLG: Facile
                elif (mousecoords[0] >= (wwidth-1125)+100 and mousecoords[0] <= (wwidth-1125)+250) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "easy"
                    size = sizesOK[1]
                    clockspeed = 10
                    screenborders = False
                    objlenght = 3
                    reloadOption("clg_easy")
                #CLG: Moyen
                elif (mousecoords[0] >= (wwidth-1125)+300 and mousecoords[0] <= (wwidth-1125)+450) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "normal"
                    size = sizesOK[2]
                    clockspeed = 4
                    screenborders = True
                    objlenght = 6
                    reloadOption("clg_normal")
                #CLG: Dur
                elif (mousecoords[0] >= (wwidth-1125)+500 and mousecoords[0] <= (wwidth-1125)+650) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "hard"
                    size = sizesOK[2]
                    clockspeed = 2
                    screenborders = True
                    objlenght = 12
                    reloadOption("clg_hard")
                #CLG: Extreme
                elif (mousecoords[0] >= (wwidth-1125)+700 and mousecoords[0] <= (wwidth-1125)+850) and (mousecoords[1] >= 550 and mousecoords[1] <= 630):
                    mode = "vhard"
                    size = sizesOK[3]
                    clockspeed = 2
                    screenborders = True
                    objlenght = 20
                    reloadOption("clg_vhard")
                #Maj challenge
                verifChallenges()
            #Type Croix
            if event.type == QUIT: 
                load = False
    #MENU D'ACCUEIL
    elif wdaction == "menu":
        pygame.time.Clock().tick(13)
        #Mosaique V2
        for headNbRect in range(0,40):
            #Détermination couleur
            if headNbRect < 20:
                color = (0, 0, 0)
            else:
                color = getColorByName("black")
            #Localisation
            psize = 0
            while psize <= wwidth*0.75:
                psize+=size
            xH = size*randrange(0,int((psize)/size))
            yH = size*randrange(0,int((320)/size))
            #while yH > 30:
                #yH = size*randrange(0,int((wheight-size)/size))
            #Affichage
            pygame.draw.rect(fe, color, (xH, yH, size, size))
        #Logo
        font = getFont("Ubuntu-BI",72)
        #Couleur du logo en blanc et couleur du fond en noir
        logo1 = font.render("SnakeByLC", 1, getColorByName("black"))
        fe.blit(logo1, (46, 116))
        logo2 = font.render("SnakeByLC", 1, getColorByName("white"))
        fe.blit(logo2, (43, 113))
        
        pygame.display.update()
        if menuact == 0:
            #Mise en place du menu
            resetScreen()
          
            
            #BG
            pygame.draw.rect(fe, getColorByName("black"), (psize, 320, wwidth-psize, wheight-320))    
            pygame.draw.rect(fe, getColorByName("black"), (0, 0, wwidth, 320))
            #Affichage version en fonction de la longueur du texte
            verwdth = 40
            if len(version) > 3 and len(version) <= 5:
                verwdth += 15
            elif len(version) > 5 and len(version) <= 7:
                verwdth += 30
            ver = getFont("Ubuntu-BI",22).render(version, 1, getColorByName("black"))
            fe.blit(ver, (wwidth-verwdth, wheight-22))
            #Boutons
            #Jouer
            makeButton("jouer_classic")
            makeButton("options_classic")
            menuact = 1
            
            #Difficulty side
            difftitle = getFont("Ubuntu-BI",16).render("difficulté.", 1, getColorByName("whitesmoke"))
            fe.blit(difftitle, (psize+20, 350))
            #diff text
            diff = translateMode(mode,True)
            difflore = getFont("Ubuntu-B",32).render(diff, 1, getColorByName("white"))
            fe.blit(difflore, (psize+20, 364))
            #Record side
            difftitle = getFont("Ubuntu-BI",16).render("record.", 1, getColorByName("whitesmoke"))
            fe.blit(difftitle, (psize+20, 420))
            difflore = getFont("Ubuntu-B",32).render(str(getHighScore()), 1, getColorByName("white"))
            fe.blit(difflore, (psize+20, 434))
           
            #Dernières games
            pygame.draw.rect(fe, getColorByName("whitesmoke"), (0, 320, 350, wheight-320))    
            lasttitle = getFont("Ubuntu-B",26).render("HISTORIQUE DE PARTIE.", 1, getColorByName("black"))
            fe.blit(lasttitle, (20, 340))
            lastgames = 0
            yGames = 380
            while yGames < wheight-50:
                lastgames += 1
                game = getHistoryGame(lastgames)
                if game != "":
                    #title
                    title = game[0]
                    if lastgames == 1:
                        title += " - Dernière partie"
                    gameHistory = getFont("Ubuntu-B",18).render(title, 1, getColorByName("midnight"))
                    fe.blit(gameHistory, (20, yGames))
                    #score
                    gameHistory = getFont("Ubuntu-B",35).render(game[3], 1, getColorByName("black"))
                    fe.blit(gameHistory, (20, yGames+27))
                 
                    yPWDS = yGames + 29
                  
                    
                    #Difficulté
                    diff = game[4]
                    if diff != "n/a":
                        gameHistory = getFont("Ubuntu-B",18).render("| " + game[4], 1, getColorByName("darkmidnight"))
                        fe.blit(gameHistory, (210, yPWDS+8))
                yGames += 80
            
        for event in pygame.event.get():
            #Type Souris
            if event.type == pygame.MOUSEMOTION:
                mousecoords = pygame.mouse.get_pos()
                #Hover boutons
                #JOUER
                if (mousecoords[0] >= 570 and mousecoords[0] <= 770) and (mousecoords[1] >= 475 and mousecoords[1] <= 545):
                    makeButton("jouer_hovered")
                    makeButton("options_classic")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                #OPTIONS
                elif (mousecoords[0] >= 620 and mousecoords[0] <= 720) and (mousecoords[1] >= 560 and mousecoords[1] <= 590):
                    makeButton("options_hovered")
                    makeButton("jouer_classic")
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
               
            #Type clic souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                #LANCEMENT DU SNAKE
                if (mousecoords[0] >= 570 and mousecoords[0] <= 770) and (mousecoords[1] >= 475 and mousecoords[1] <= 545):
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    objectivePlace()
                    menuact = 2
                    wdaction = "snakestart"
                
                elif (mousecoords[0] >= 620 and mousecoords[0] <= 720) and (mousecoords[1] >= 562 and mousecoords[1] <= 592):
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    wdaction = "options"
                    menuact = 0

            #Type Croix
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    objectivePlace()
                    menuact = 2
                    wdaction = "snakestart"
            if event.type == QUIT:
                load = False

pygame.quit()