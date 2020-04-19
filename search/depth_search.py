#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import numpy as np

w = 480
h = 480
SCREEN_SIZE = (w, h)

grid_n = 12
grid_w = w/grid_n
grid_h = h/grid_n

# field = np.zeros((grid_n,grid_n))
# field[0] = -1
# field[-1] = -1
# field[:,0] = -1
# field[:,-1] = -1

start_x, start_y = 1, 1
# goal_x, goal_y = 10, 10
# field[goal_x, goal_y] = 2

field = np.array([
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0,-1],
    [-1, 0,-1, 0, 0, 0,-1,-1, 0,-1,-1,-1],
    [-1, 0,-1,-1, 0,-1, 0, 0, 0,-1, 0,-1],
    [-1, 0, 0, 0,-1, 0, 0,-1,-1, 0,-1,-1],
    [-1,-1,-1, 0, 0,-1, 0,-1, 0, 0, 0,-1],
    [-1, 0, 0, 0,-1, 0,-1, 0, 0,-1, 2,-1],
    [-1, 0,-1, 0, 0, 0, 0,-1, 0, 0,-1,-1],
    [-1, 0, 0,-1, 0,-1, 0, 0,-1, 0, 0,-1],
    [-1, 0,-1, 0,-1, 0,-1, 0, 0,-1, 0,-1],
    [-1, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
])

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"図形の描画")
FPSCLOCK = pygame.time.Clock()

def search(x,y):
    # 図形を描画
    screen.fill((0,0,0))
    for i in range(grid_n):
        for j in range(grid_n):
            # 探索済み(赤)
            if field[i,j] == -2:
                pygame.draw.rect(screen, (255,0,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            # 障害物(黒)
            elif field[i,j] == -1:
                pygame.draw.rect(screen, (0,0,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            # ノーマルフィールド(黄)
            elif field[i,j] == 0:
                pygame.draw.rect(screen, (255,255,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            # エージェント(青)
            elif field[i,j] == 1:
                pygame.draw.rect(screen, (0,0,255),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            # ゴール(緑)
            elif field[i,j] == 2:
                pygame.draw.rect(screen, (0,255,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))

    for i in range(grid_n):
        # 白い線
        pygame.draw.line(screen, (0,0,0), 
        (grid_w*i,0), (grid_w*i,h))
    for j in range(grid_n):
        # 白い線
        pygame.draw.line(screen, (0,0,0), 
        (0,grid_h*j), (w,grid_h*j))
    pygame.display.update()
    FPSCLOCK.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    if field[x,y] == 2:
        print("Goal")
        sys.exit()
    field[x, y] = -2
    print(x,y)
    if field[x+1,y] >= 0:
        search(x + 1, y)
    if field[x-1,y] >= 0:
        search(x - 1, y)
    if field[x,y+1] >= 0:
        search(x, y + 1)
    if field[x,y-1] >= 0:
        search(x, y - 1)

    field[x,y] = 0

search(start_x,start_y)