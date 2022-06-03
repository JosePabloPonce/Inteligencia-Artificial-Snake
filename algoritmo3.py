'''
Jose Pablo Ponce
Gabriel Quiroz
Guido Padilla
Oscar Paredez
Proyecto#1
Inteligencia Artificial

'''
import pygame
from copy import deepcopy
from random import randrange
from os import environ


####################### Ajustes #################
color_mapa = (255, 255, 255)
color_mapa_diagonal = (100, 100, 100)
mapa_width = 600
mapa_height = 600
cantidad_filas = 30
color_serpiente = (0, 0, 0)
color_manzana = (223, 163, 49)
color_serpiente_virtual = (0, 255, 0)
availableSnakeLength = cantidad_filas * cantidad_filas - 3

matriz = [[i, j] for i in range(cantidad_filas) for j in range(cantidad_filas)]

def distancia(pos1, pos2):
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)

def obtener_celdas_vecinas(posicion):
    vecinos = [
                    [posicion[0] + 1, posicion[1]],
                    [posicion[0] - 1, posicion[1]],
                    [posicion[0], posicion[1] + 1],
                    [posicion[0], posicion[1] - 1]
                 ]
    celdas_disponibles = []
    for celda in vecinos:
        if celda in matriz:
            celdas_disponibles.append(celda)
    return celdas_disponibles

cuerpo_serpiente = {tuple(pos): obtener_celdas_vecinas(pos) for pos in matriz}

#########################################################

class Snake:
    def __init__(self, space):
        self.space = space
        self.cuerpo_inicial = [[cantidad_filas // 2 + i, cantidad_filas // 2] for i in range(3)]
        self.turns = {}
        self.direccion = [-1, 0]
        self.score = 0
        self.color_manzana = Square([randrange(cantidad_filas), randrange(cantidad_filas)], self.space, isApple=True)

        self.cuadrados = []
        for posicion in self.cuerpo_inicial:
            self.cuadrados.append(Square(posicion, self.space))

        self.cabeza = self.cuadrados[0]
        self.cola = self.cuadrados[-1]
        self.cola.es_cola = True

        self.camino = []
        self.es_serpiente_virtual = False
        self.total_moves = 0
        self.juego_ganado = False

    def set_movimiento(self, direccion):
        if direccion == 'left':
            if not self.direccion == [1, 0]:
                self.direccion = [-1, 0]
                self.turns[self.cabeza.posicion[0], self.cabeza.posicion[1]] = self.direccion
        if direccion == "right":
            if not self.direccion == [-1, 0]:
                self.direccion = [1, 0]
                self.turns[self.cabeza.posicion[0], self.cabeza.posicion[1]] = self.direccion
        if direccion == "up":
            if not self.direccion == [0, 1]:
                self.direccion = [0, -1]
                self.turns[self.cabeza.posicion[0], self.cabeza.posicion[1]] = self.direccion
        if direccion == "down":
            if not self.direccion == [0, -1]:
                self.direccion = [0, 1]
                self.turns[self.cabeza.posicion[0], self.cabeza.posicion[1]] = self.direccion

    def manzana_spawn(self):
        self.color_manzana = Square([randrange(cantidad_filas), randrange(cantidad_filas)], self.space, isApple=True)
        if not self.celda_esta_libre(self.color_manzana.posicion):
            self.manzana_spawn()

    def draw(self):
        self.color_manzana.dibujar_cuadrado(color_manzana)
        self.cabeza.dibujar_cuadrado(color_serpiente)
        for sqr in self.cuadrados[1:]:
            if self.es_serpiente_virtual:
                sqr.dibujar_cuadrado(color_serpiente_virtual)
            else:
                sqr.dibujar_cuadrado()

    def mover(self):
        for j, celda in enumerate(self.cuadrados):
            p = (celda.posicion[0], celda.posicion[1])
            if p in self.turns:
                turn = self.turns[p]
                celda.mover([turn[0], turn[1]])
                if j == len(self.cuadrados) - 1:
                    self.turns.pop(p)
            else:
                celda.mover(celda.direccion)

    def extender_serpiente(self):
        cola = self.cuadrados[-1]
        self.cuadrados[-1].es_cola = False

        direccion = cola.direccion
        if direccion == [1, 0]:
            self.cuadrados.append(Square([cola.posicion[0] - 1, cola.posicion[1]], self.space))
        if direccion == [-1, 0]:
            self.cuadrados.append(Square([cola.posicion[0] + 1, cola.posicion[1]], self.space))
        if direccion == [0, 1]:
            self.cuadrados.append(Square([cola.posicion[0], cola.posicion[1] - 1], self.space))
        if direccion == [0, -1]:
            self.cuadrados.append(Square([cola.posicion[0], cola.posicion[1] + 1], self.space))

        self.cuadrados[-1].es_cola = True
        self.cuadrados[-1].direccion = direccion

    def manzana_comida(self):
        if (self.cabeza.posicion == self.color_manzana.posicion) and not (self.es_serpiente_virtual) and not (self.juego_ganado):
            self.manzana_spawn()
            self.score += 1
            print(self.score)
            return True

    def mover_hacia(self, posicion):
        if self.cabeza.posicion[0] + 1 == posicion[0]:
            self.set_movimiento('right')
        if self.cabeza.posicion[0] - 1 == posicion[0]:
            self.set_movimiento('left')
        if self.cabeza.posicion[1] + 1 == posicion[1]:
            self.set_movimiento('down')
        if self.cabeza.posicion[1] - 1 == posicion[1]:
            self.set_movimiento('up')
        return

    def celda_esta_libre(self, posicion):
        if posicion[0] >= cantidad_filas or posicion[0] < 0 or posicion[1] >= cantidad_filas or posicion[1] < 0:
            return False
        for celda in self.cuadrados:
            if celda.posicion == posicion:
                return False
        return True

    def bfs(self, s, e):
        q = [s]  # Cola
        visitado = {tuple(posicion): False for posicion in matriz}

        visitado[s] = True

        prev = {tuple(posicion): None for posicion in matriz}

        while q:  # Mientras que la cola no está vacía
            nodo = q.pop(0)
            vecinos = cuerpo_serpiente[nodo]
            for siguiente_nodo in vecinos:
                if self.celda_esta_libre(siguiente_nodo) and not visitado[tuple(siguiente_nodo)]:
                    q.append(tuple(siguiente_nodo))
                    visitado[tuple(siguiente_nodo)] = True
                    prev[tuple(siguiente_nodo)] = nodo

        camino = list()
        p_nodo = e

        nodo_inicial_encontrado = False
        while not nodo_inicial_encontrado:
            if prev[p_nodo] is None:
                return []
            p_nodo = prev[p_nodo]
            if p_nodo == s:
                camino.append(e)
                return camino
            camino.insert(0, p_nodo)

        return []

    def generar_serpiente_virtual(self):
        sepiente_virtual = Snake(self.space)
        for i in range(len(self.cuadrados) - len(sepiente_virtual.cuadrados)):
            sepiente_virtual.extender_serpiente()

        for i, sqr in enumerate(sepiente_virtual.cuadrados):
            sqr.posicion = deepcopy(self.cuadrados[i].posicion)
            sqr.direccion = deepcopy(self.cuadrados[i].direccion)

        sepiente_virtual.direccion = deepcopy(self.direccion)
        sepiente_virtual.turns = deepcopy(self.turns)
        sepiente_virtual.color_manzana.posicion = deepcopy(self.color_manzana.posicion)
        sepiente_virtual.color_manzana.isApple = True
        sepiente_virtual.es_serpiente_virtual = True

        return sepiente_virtual

    def obtener_camino_cola(self):
        posicion_cola = deepcopy(self.cuadrados[-1].posicion)
        self.cuadrados.pop(-1)
        camino = self.bfs(tuple(self.cabeza.posicion), tuple(posicion_cola))
        self.extender_serpiente()
        return camino

    def obtener_celdas_libres(self, posicion):
        freeCells = []
        vecinos = obtener_celdas_vecinas(tuple(posicion))
        for n in vecinos:
            if self.celda_esta_libre(n) and self.color_manzana.posicion != n:
                freeCells.append(tuple(n))
        return freeCells

    def camino_mas_largo_a_cola(self):
        vecinos = self.obtener_celdas_libres(self.cabeza.posicion)
        camino = []
        if vecinos:
            dis = -1000
            for n in vecinos:
                if distancia(n, self.cuadrados[-1].posicion) > dis:
                    sepiente_virtual = self.generar_serpiente_virtual()
                    sepiente_virtual.mover_hacia(n)
                    sepiente_virtual.mover()
                    if sepiente_virtual.manzana_comida():
                        sepiente_virtual.extender_serpiente()
                    if sepiente_virtual.obtener_camino_cola():
                        camino.append(n)
                        dis = distancia(n, self.cuadrados[-1].posicion)
            if camino:
                return [camino[-1]]

    def lookForMove(self):
        vecinos = self.obtener_celdas_libres(self.cabeza.posicion)
        camino = []
        if vecinos:
            camino.append(vecinos[randrange(len(vecinos))])
            sepiente_virtual = self.generar_serpiente_virtual()
            for mover in camino:
                sepiente_virtual.mover_hacia(mover)
                sepiente_virtual.mover()
            if sepiente_virtual.obtener_camino_cola():
                return camino
            else:
                return self.obtener_camino_cola()

    def establecer_camino(self):
        if self.score == availableSnakeLength - 1 and self.color_manzana.posicion in obtener_celdas_vecinas(self.cabeza.posicion):
            camino_ganador = [tuple(self.color_manzana.posicion)]
            return camino_ganador

        sepiente_virtual = self.generar_serpiente_virtual()

        primer_camino = sepiente_virtual.bfs(tuple(sepiente_virtual.cabeza.posicion), tuple(sepiente_virtual.color_manzana.posicion))
        segundo_camino = []

        if primer_camino:
            for posicion in primer_camino:
                sepiente_virtual.mover_hacia(posicion)
                sepiente_virtual.mover()

            sepiente_virtual.extender_serpiente()
            segundo_camino = sepiente_virtual.obtener_camino_cola()

        if segundo_camino:
            return primer_camino
        
        if self.lookForMove():
            return self.lookForMove()

        if self.camino_mas_largo_a_cola() and self.score % 2 == 0:
            return self.camino_mas_largo_a_cola()
        
        if self.obtener_camino_cola():
            return self.obtener_camino_cola()
        
        return

    def update(self):

        self.camino = self.establecer_camino()
        if self.camino:
            self.mover_hacia(self.camino[0])

        self.draw()
        self.mover()

        if self.score == cantidad_filas * cantidad_filas - 3:
            self.juego_ganado = True

            print("Serpiente Gano, Total: ", self.score)
            quit()

        self.total_moves += 1

        if self.manzana_comida():
            self.extender_serpiente()

class Square:
    def __init__(self, posicion, space, isApple = False):
        self.posicion = posicion
        self.direccion = [-1, 0]
        self.space = space

        self.isApple = isApple
        self.es_cola = False

        if self.isApple:
            self.direccion = [0, 0]

    def dibujar_cuadrado(self, clr = color_serpiente):
        x, y = self.posicion[0], self.posicion[1]
        ss = mapa_width // cantidad_filas

        if self.direccion == [-1, 0]:
            if self.es_cola:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss - 1))
            else:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss, ss - 1))

        if self.direccion == [1, 0]:
            if self.es_cola:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss - 1))
            else:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss, ss - 1))

        if self.direccion == [0, 1]:
            if self.es_cola:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss - 1))
            else:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss))

        if self.direccion == [0, -1]:
            if self.es_cola:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss - 1))
            else:
                pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss))

        if self.isApple:
            pygame.draw.rect(self.space, clr, (x * ss, y * ss, ss - 1, ss - 1))

    def mover(self, direccion):
        self.direccion = direccion
        self.posicion[0] += self.direccion[0]
        self.posicion[1] += self.direccion[1]


###########Jugar###############
def drawMap(surface):
    surface.fill(color_mapa)
    x = 0
    y = 0
    for r in range(cantidad_filas):
        x = x + mapa_width // cantidad_filas
        y = y + mapa_width // cantidad_filas
        pygame.draw.line(surface, color_mapa_diagonal, (x, 0), (x, mapa_height))
        pygame.draw.line(surface, color_mapa_diagonal, (0, y), (mapa_width, y))

def play():
    pygame.init()
    mapMetrics = pygame.display.set_mode((mapa_width, mapa_height))
    snake = Snake(mapMetrics)
    
    clock = pygame.time.Clock()
    flag = True
    while flag:
        drawMap(mapMetrics)

        snake.update()

        clock.tick(8)
        pygame.display.update()

play()
#############################