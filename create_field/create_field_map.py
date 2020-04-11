#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import numpy as np

w = 640
h = 640
SCREEN_SIZE = (w, h)
dot_value = 0.3

grid_n = 160
grid_w = w/grid_n
grid_h = h/grid_n

field = np.zeros((grid_n,grid_n))

for y in range(grid_n):
    for x in range(grid_n):
        #if 33<=y and y<=42 and 33<=x and x<=42:
        #if 17<=y and y<=21 and 17<=x and x<=21:
        if 65<=y and y<=84 and 65<=x and x<=84:
            field[y,x] = dot_value

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"図形の描画")
FPSCLOCK = pygame.time.Clock()

while True:
    screen.fill((0,0,0))
    
    # 図形を描画
    for i in range(grid_n):
        for j in range(grid_n):
            # 黄の矩形
            if field[i,j] == dot_value:
                pygame.draw.rect(screen, (255,0,0),
                Rect(grid_w*i,grid_h*j,grid_w*i+grid_w,grid_h*j+grid_h))
            else:
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

    pygame.display.update()
    FPSCLOCK.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            np.savetxt("./map.csv", field, fmt="%.1f", delimiter=",")
            print("save map")
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:	#もしマウスをクリックしたら
            x,y = event.pos			#クリックした位置を取得
            if field[int(x/grid_w), int(y/grid_h)] == dot_value:
                field[int(x/grid_w), int(y/grid_h)] = 0
            else:
                field[int(x/grid_w), int(y/grid_h)] = dot_value
