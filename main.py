import pygame
import random
import sys
import ctypes
import math


def set_screen_prop():
    user32 = ctypes.windll.user32
    screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screenSize


def hsl_to_rgb(h, s, l):
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        elif t < 1/2:
            return q
        elif t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p

    if s == 0:
        r, g, b = l, l, l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return int(r*255), int(g*255), int(b*255)


class Dot:
    def __init__(self):
        self.pos = {'x': centerX, 'y': centerY}
        self.dir = (int(random.random() * 3) | 0) * 2 if modeSettings[currentMode]['dirsCount'] == 6 else int(random.random() * modeSettings[currentMode]['dirsCount']) | 0
        self.step = 0

    def draw(self):
        size = modeSettings[currentMode]['dotSize']
        x = self.pos['x'] - size / 2
        y = self.pos['y'] - size / 2
        newHue = int((hue + (abs(self.pos['x'] - centerX) + abs(self.pos['y'] - centerY)) / gradLen) % 360)
        pygame.draw.rect(sc, colorsList[newHue], (x, y, size, size))

    def move(self):
        self.step += 1
        self.pos['x'] += dirsList[self.dir][0] * dotVelocity
        self.pos['y'] += dirsList[self.dir][1] * dotVelocity

    def changeDir(self):
        if self.step % modeSettings[currentMode]['stepsToTurn'] == 0:
            s = random.random()
            if s > .5:
                self.dir = (self.dir + 1) % modeSettings[currentMode]['dirsCount']
            else:
                self.dir = (self.dir + modeSettings[currentMode]['dirsCount'] - 1) % modeSettings[currentMode]['dirsCount']

    def kill(self):
        percent = random.random() * math.exp(self.step / modeSettings[currentMode]['distance'])
        if percent > 100:
            dotsList.remove(self)


def createDirs():
    for i in range(0, 360, 360 // modeSettings[currentMode]['dirsCount']):
        angle = modeSettings[currentMode]['dirsAngle'] + i
        x = math.cos(angle * math.pi / 180)
        y = math.sin(angle * math.pi / 180)
        dirsList.append((x, y))


def addDot():
    global hue
    if (len(dotsList) < modeSettings[currentMode]['dotsCount']) and (random.random() > .8):
        a = random.randint(2, 4)
        for i in range(a):
            dotsList.append(Dot())
        hue = (hue + 1) % 360


def refreshDot():
    for dot in dotsList:
        dot.move()
        dot.draw()
        dot.changeDir()


def fillColorsList(list, s):
    for i in range(360):
        list.append(tuple(hsl_to_rgb(i / 360, s, .5)))


pygame.init()

clock = pygame.time.Clock()
screenSize = set_screen_prop()
sc = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
pygame.display.set_caption("Patterns")
pygame.mouse.set_visible(False)
qqq = pygame.Surface(screenSize)
qqq.fill((0, 0, 0))
qqq.set_alpha(8)
f1 = pygame.font.SysFont('arial', 20)
text1 = f1.render('Паттерн: ← →', 0, (200, 200, 200))
text2 = f1.render('Выйти:    esc', 0, (200, 200, 200))
place1 = text1.get_rect(center=(screenSize[0] - 70, screenSize[1] - 40))
place2 = text1.get_rect(center=(screenSize[0] - 70, screenSize[1] - 20))

FPS = 60
defaultW = 1366
defaultH = 768
coef = screenSize[1] / defaultH
centerX = screenSize[0] / 2
centerY = screenSize[1] / 2
currentMode = 0
modeSettings = [{'dirsCount': 6, 'dirsAngle': 0, 'stepsToTurn': 20, 'dotSize': 4, 'dotsCount': int(300 * coef), 'dotVelocity': 2, 'distance': int(200 * coef)},
               {'dirsCount': 3, 'dirsAngle': 30, 'stepsToTurn': 40, 'dotSize': 3, 'dotsCount': int(400 * coef), 'dotVelocity': 2, 'distance': int(350 * coef)},
               {'dirsCount': 4, 'dirsAngle': 0, 'stepsToTurn': 24, 'dotSize': 4, 'dotsCount': int(300 * coef), 'dotVelocity': 2, 'distance': int(220 * coef)},
               {'dirsCount': 30, 'dirsAngle': 0, 'stepsToTurn': 15, 'dotSize': 2, 'dotsCount': int(300 * coef), 'dotVelocity': 2, 'distance': int(70 * coef)},
               {'dirsCount': 15, 'dirsAngle': 0, 'stepsToTurn': 2, 'dotSize': 2, 'dotsCount': int(450 * coef), 'dotVelocity': 2, 'distance': int(200 * coef)}]

dirsList = []
dotsList = []
colorsList = []
dotVelocity = 2
hue = 0
gradLen = 2

fillColorsList(colorsList, 1)
createDirs()

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                sys.exit()
            elif i.key == pygame.K_LEFT:
                currentMode -= 1
                if currentMode < 0:
                    currentMode = 4
                dotsList.clear()
                dirsList.clear()
                createDirs()
            elif i.key == pygame.K_RIGHT:
                currentMode = (currentMode + 1) % 5
                dotsList.clear()
                dirsList.clear()
                createDirs()
    print(currentMode)
    sc.blit(qqq, (0, 0))
    sc.blit(text1, place1)
    sc.blit(text2, place2)
    addDot()
    refreshDot()
    pygame.display.update()
    for dot in dotsList:
        dot.kill()
    clock.tick(FPS)
