#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import numpy as np

w = 480
h = 480
SCREEN_SIZE = (w, h)
dot_value = 1

grid_n = 40
grid_w = w/grid_n
grid_h = h/grid_n

field = np.zeros((grid_n,grid_n))
field[0] = -1
field[-1] = -1
field[:,0] = -1
field[:,-1] = -1

for _ in range(200):
    field[np.random.randint(0,grid_n), np.random.randint(0,grid_n)] = -1

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"図形の描画")
FPSCLOCK = pygame.time.Clock()

start_x, start_y = 1, 1
action_list = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])

while True:
    field[start_x, start_y] = 2
    screen.fill((0,0,0))

    # 図形を描画
    for i in range(grid_n):
        for j in range(grid_n):
            # 黄の矩形
            if field[i,j] == dot_value:
                pygame.draw.rect(screen, (255,0,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            elif field[i,j] == -1:
                pygame.draw.rect(screen, (0,0,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            elif field[i,j] == 2:
                pygame.draw.rect(screen, (0,0,255),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            elif field[i,j] == 0:
                pygame.draw.rect(screen, (255,255,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))

    for i in range(grid_n):
        # 白い線
        pygame.draw.line(screen, (0,0,0), 
        (grid_w*i,0), (grid_w*i,h))
    for j in range(grid_n):
        # 白い線
        pygame.draw.line(screen, (0,0,0), 
        (0,grid_h*j), (w,grid_h*j))

    action = np.random.randint(0,4)

    if field[start_x+action_list[action,0], start_y+action_list[action,1]] != -1:
        start_x += action_list[action,0]
        start_y += action_list[action,1]
        print(start_x,start_y)
    # if action == 0:
    #     if (grid_n-1) > start_x:
    #         start_x += 1
    # elif action == 1:
    #     if 1 < start_x:
    #         start_x -= 1
    # elif action == 2:
    #     if (grid_n-1) > start_y:
    #         start_y += 1
    # elif action == 3:
    #     if 1 < start_y:
    #         start_y -= 1

    pygame.display.update()
    FPSCLOCK.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            # np.savetxt("./map.csv", field, fmt="%.1f", delimiter=",")
            # print("save map")
            sys.exit()
        # if event.type == MOUSEBUTTONDOWN:
        #     x,y = event.pos
        #     if field[int(x/grid_w), int(y/grid_h)] == dot_value:
        #         field[int(x/grid_w), int(y/grid_h)] = 0
        #     else:
        #         field[int(x/grid_w), int(y/grid_h)] = dot_value
