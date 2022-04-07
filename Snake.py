'''
Jose Pablo Ponce
Gabriel Quiroz
Guido Padilla
Oscar Paredez
Proyecto#1
Inteligencia Artificial

Referencia https://www.youtube.com/watch?v=9bBgyOkoBQ0&ab_channel=Kite
'''


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

    def initialPosition(self):
        return self.positions[0]  #retorna la posicion inicial de la serpiente

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction: #si la serpiente mide un pixel, se mueve en cualquier direccion
            return
        else: #si mide mas de 1, puede seguir recto, derecha o izquierda
            self.direction = point

    def move(self):
        cur = self.initialPosition() #obtener posicion de cabeza
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
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize) #posicion aleatoria

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawPoints(surface): #funcion para dibujar los puntos en la superficie
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize)) 
                pygame.draw.rect(surface,(13,141,30), r) #pintar verde oscuro mapa
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (94,228,11), rr) #pintar verde claro mapa

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
        clock.tick(10) #reloj seteado a 10 frames por segundo
        snake.playerMovement() #maneja los eventos cuando se hace click
        drawPoints(surface) #se rellena la superficie de azul
        snake.move() #se mueve la serpiente como hagan click
        if snake.initialPosition() == points.position: #si la cabeza toca la comida aumenta en 1
            snake.length += 1
            snake.score += 1
            points.randomPosition()
        snake.draw(surface) #se dibuja serpiente
        points.draw(surface)  #se dibuja comida
        #handle events
        screen.blit(surface, (0,0)) #se actualiza la superficie
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0)) #se muestra en pantalla puntuacion
        screen.blit(text, (5,10)) #se actualiza el texto
        pygame.display.update() #se actualiza la pantalla

main()
