
'''
Jose Pablo Ponce
Gabriel Quiroz
Guido Padilla
Oscar Paredez
Proyecto#1
Inteligencia Artificial

'''
from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt
init()

#Variables iniciales
finalizado = False
body = (17, 24, 47)
head = (17, 24, 47)
foo = (223, 163, 49)


cols = 25
rows = 25

width = 600
height = 600
wr = width/cols
hr = height/rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("snake algoritmo 2")
clock = time.Clock()

#Representacion de un pixel en el grid
class Elemento:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.vecinos = []
        self.camefrom = []

    def show(self, color):
        draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    def add_vecinos(self):
        if self.x > 0:
            self.vecinos.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.vecinos.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.vecinos.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.vecinos.append(grid[self.x][self.y + 1])

            

#REALIZANDO EL ALGORITMO a*
def getpath(comida, serpiente):
    comida.camefrom = []
    for s in serpiente:
        s.camefrom = []
    array1 = [serpiente[-1]]
    array2 = []
    direccion1 = []
    while 1:
        actual = min(array1, key=lambda x: x.f)
        array1 = [array1[i] for i in range(len(array1)) if not array1[i] == actual]
        array2.append(actual)
        for vecino in actual.vecinos:
            if vecino not in array2 and vecino not in serpiente:
                tempg = vecino.g + 1
                if vecino in array1:
                    if tempg < vecino.g:
                        vecino.g = tempg
                else:
                    vecino.g = tempg
                    array1.append(vecino)
                vecino.h = sqrt((vecino.x - comida.x) ** 2 + (vecino.y - comida.y) ** 2)
                vecino.f = vecino.g + vecino.h
                vecino.camefrom = actual
        if actual == comida:
            break
    while actual.camefrom:
        if actual.x == actual.camefrom.x and actual.y < actual.camefrom.y:
            direccion1.append(2)
        elif actual.x == actual.camefrom.x and actual.y > actual.camefrom.y:
            direccion1.append(0)
        elif actual.x < actual.camefrom.x and actual.y == actual.camefrom.y:
            direccion1.append(3)
        elif actual.x > actual.camefrom.x and actual.y == actual.camefrom.y:
            direccion1.append(1)
        actual = actual.camefrom

    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return direccion1




grid = [[Elemento(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_vecinos()

snake = [grid[round(rows/2)][round(cols/2)]]
food = grid[randint(0, rows-1)][randint(0, cols-1)]
current = snake[-1]
direccion = getpath(food, snake)
food_array = [food]

while not finalizado:
    clock.tick(20)
    screen.fill((255,255,255))
    direction = direccion.pop(-1)
    if direction == 0:   
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2: 
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3: 
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    if current.x == food.x and current.y == food.y:
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food in snake):
                break
        food_array.append(food)
        direccion = getpath(food, snake)
    else:
        snake.pop(0)

    for Elemento in snake:
        Elemento.show(body)


    food.show(foo)
    snake[-1].show(head)
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            finalizado = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1