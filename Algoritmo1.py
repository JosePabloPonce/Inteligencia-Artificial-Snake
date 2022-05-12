'''
Jose Pablo Ponce
Gabriel Quiroz
Guido Padilla
Oscar Paredez
Proyecto#1
Inteligencia Artificial
Referencia https://www.youtube.com/watch?v=9bBgyOkoBQ0&ab_channel=Kite
'''

import collections
import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 1 #tamano inicial de la serpiente
        self.positions = [((screen_width/2), (screen_height/2))] #centra la serpiente
        self.direction = random.choice([up, down, left, right])  #inicializa en una direccion aleatoria
        self.color = (17, 24, 47) #color
        self.score = 0 #marcador iniciando en 0

    def get_head_position(self):
        return self.positions[0]  #retorna la posicion inicial de la serpiente

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction: #si la serpiente mide un pixel, se mueve en cualquier direccion
            return
        else: #si mide mas de 1, puede seguir recto, derecha o izquierda
            self.direction = point

    def move(self):
        cur = self.get_head_position() #obtener posicion de cabeza
        x,y = self.direction #se obtiene la direccion en la que esta
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height) #se ubica la nueva loc de la cabeza



        if len(self.positions) > 2 and new in self.positions[2:]: #si mide mas de 2 y si la cabeza toca otra parte de la serpiente game over
            self.reset()
        elif(cur[0] == 0 or new[1]==0): #si toca la pared game over
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def garra(self, pointsP):
        xF, yF = pointsP
        xS, yS = self.get_head_position()
        xF = xF/gridsize
        yF = yF/gridsize
        xS = xS/gridsize
        yS = yS/gridsize
        pos = (xS+1, yS+0)
        weight10 = ((xF-(xS+1))**2+(yF-(yS+0))**2)//2
        weight01 = ((xF-(xS+0))**2+(yF-(yS+1))**2)//2
        mweight10 = ((xF-(xS-1))**2+(yF-(yS+0))**2)//2
        mweight01 = ((xF-(xS+0))**2+(yF-(yS-1))**2)//2
        d = { weight10: { 'pos':  (xS+1, yS+0), 'direccion': (1, 0)}, weight01: { 'pos':  (xS+0, yS+1), 'direccion': (0, 1)}, mweight10: { 'pos':  (xS-1, yS+0), 'direccion': (-1, 0)}, mweight01: { 'pos':  (xS+0, yS-1), 'direccion': (0, -1)} }
        od = collections.OrderedDict(sorted(d.items()))
        for k, v in od.items():
            pos = v['pos']
            xW, yW = v['pos']
            direccion = v['direccion']
            pos = (xW*gridsize, yW*gridsize)
            if not(pos in self.positions[2:]) and (xW>=0 and xW<=grid_width) and (yW>=0 and yW<=grid_height):
                return direccion

    def shortest_path(self, pointsP):
        xF, yF = pointsP
        xS, yS = self.get_head_position()
        xF = xF/gridsize
        yF = yF/gridsize
        xS = xS/gridsize
        yS = yS/gridsize
        matrix = []
        for i in range(70):
            a = []
            for j in range(70):
                if (i*gridsize, j*gridsize) in self.positions[2:]:
                    a.append(None)
                else:
                    a.append(((xF-i)**2+(yF-j)**2)//2)
            matrix.append(a)
        moves = []
        return moves

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface): #muestra la serpiente en la superficie
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def playerMovement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Points():
    def __init__(self):
        self.position = (0,0) #posicion
        self.color = (223, 163, 49) #color
        self.randomPosition() #posicion inciaial aleatoria

    def randomPosition(self):
        self.position = (random.randint(10, grid_width-10)*gridsize, random.randint(10, grid_height-10)*gridsize) #posicion aleatoria

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawPoints(surface): #funcion para dibujar la comida en la superficie
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize)) 
            pygame.draw.rect(surface,(255, 255, 255), r)

screen_width = 840
screen_height = 840

gridsize = 12
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawPoints(surface)

    snake = Snake()
    points = Points()

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(120) #reloj seteado a 10 frames por segundo
        snake.playerMovement() #maneja los eventos cuando se hace click
        drawPoints(surface) #se rellena la superficie de azul
        snake.move() #se mueve la serpiente como hagan click
        if snake.get_head_position() == points.position: #si la cabeza toca la comida aumenta en 1
            snake.length += 1
            snake.score += 1
            points.randomPosition()
        snake.draw(surface) #se dibuja serpiente
        points.draw(surface)  #se dibuja comida
        snake.direction = snake.garra(points.position)
        #snake.shortest_path(points.position)
        #handle events
        screen.blit(surface, (0,0)) #se actualiza la superficie
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0)) #se muestra en pantalla puntuacion
        screen.blit(text, (5,10)) #se actualiza el texto
        pygame.display.update() #se actualiza la pantalla

main()