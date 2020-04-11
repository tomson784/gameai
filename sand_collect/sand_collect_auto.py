# Qテーブルのみの学習
# 通常移動、積み下ろし、積み上げ、壁の衝突
# 土砂の塊の重心から分散を求めて、分散が小さいほど報酬を上げる

import pygame
from pygame.locals import *
import sys
import numpy as np
import os
from datetime import datetime
SCR_RECT = Rect(0, 0, 800, 640) # 画面サイズ

# マップのクラス
class Map:
    def __init__(self, map_n=0):
        # マップデータ
        self.map = np.loadtxt("./field/field{}.txt".format(map_n)).astype(np.int32)
        self.row,self.col = len(self.map), len(self.map[0]) # マップの行数,列数を取得
        self.imgs = [None] * 16             # マップチップ
        self.msize = 32                      # 1マスの大きさ[px]
    # マップの描画
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(self.imgs[self.map[i][j]], (j*self.msize,i*self.msize))

# 画像の読み込み
def load_img(filename, colorkey=None):
    img = pygame.image.load(filename)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0,0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img

# 土砂の塊の重心の分散を計算して評価を変更する
def eval_action(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    # eval_var = np.abs(np.mean((x - x_mean)*(y - y_mean)))
    eval_var = np.mean((x - x_mean)**2) + np.mean((y - y_mean)**2)
    # if eval_var == np.nan:
    #     eval_var = 0.01
    #     print(eval_var)
    sys.stdout.write("      {:.5f}".format(eval_var))
    return np.round(1/(eval_var+1), decimals=5)

def main(max_step, episode, map_n, greed_e, r1, r2, r3, r4, r5, def_r, test, fps):
    save_path = "./log/{0}_map{1}".format(datetime.now().strftime("%y%m%d%H"), map_n)
    if test != True:
        os.makedirs(save_path)

    Q = np.zeros([15,20,2,4])
    # Q = np.load("./log/19090512_map0/Qtable_ep00090.npy")
    # learning rate
    lr = 0.8
    # 割引率
    y = 0.95
    # fps = 30
    agent_direction = 0
    r = 0
    # max_step = 10000
    # episode = 100
    # # 積み上げ報酬
    # r1 = 0.5
    # # 積み下ろし報酬
    # r2 = 2
    # # 評価低下
    # r3 = -1

    for ep in range(episode):
        step = 0
        s_buc = 0
        s_buc_next = 0
        act = 0
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        map = Map(map_n)
        map.imgs[0] =  pygame.image.load("./image/sand.png")
        map.imgs[1] =  pygame.image.load("./image/white.png")
        map.imgs[2] =  pygame.image.load("./image/track.png")
        map.imgs[3] =  pygame.image.load("./image/wheel.png")
        map.imgs[4] =  pygame.image.load("./image/wheel_bucket.png")
        goal_id = np.where(map.map==2)
        FPSCLOCK = pygame.time.Clock()
        rAll = 0
        collision_n = 0
        while step < max_step:
            # if step < 100:
            #     pygame.image.save(screen, "./screen_shot/ep{0:0=3}_step{1:0=3}.png".format(ep,step))
            wheel_id = np.where(map.map>=3)
            wheel = map.map[wheel_id[0], wheel_id[1]]
            s_row, s_col = wheel_id
            #print(wheel_id)
            if wheel == 4:
                s_buc = 1
            elif wheel == 3:
                s_buc = 0
            else:
                print("error!")
                pygame.quit()
                sys.exit()

            step += 1
            sys.stdout.write("\rstep: {}/{} | episode: {}/{} | collision: {} | reward: {:.3f} | sum reward: {:.3f}".format(
                    step, max_step, ep, episode, collision_n, r, rAll))
            if np.random.uniform() < greed_e:
                act = np.random.randint(0, 4)
            else:
                act = np.argmax(Q[s_row,s_col,s_buc,:] + np.random.randn(1, 4)*(1.0/(step + 1)))
            map.draw(screen)
            # イベント処理
            for event in pygame.event.get():
                # 終了用のイベント処理
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()
            # ホイールローダーの向きはいったん放置
            if 0 == act:
                # map.imgs[4] = pygame.transform.rotate(map.imgs[4], 90)
                # surf4 = map.imgs[4].get_rect()
                # surf4.center = (wheel_id[1]*map.msize+map.msize/2,
                #                wheel_id[0]*map.msize+map.msize/2)
                # map.imgs[3] = pygame.transform.rotate(map.imgs[3], 90)
                # surf3 = map.imgs[3].get_rect()
                # surf3.center = (wheel_id[1]*map.msize+map.msize/2,
                #                 wheel_id[0]*map.msize+map.msize/2)
                # if wheel == 4:
                #     screen.blit(map.imgs[4], surf4)
                # if wheel == 3:
                #     screen.blit(map.imgs[3], surf3)
                if wheel_id[1] > 0:
                    # 貨物状態
                    if wheel == 4:
                        # 土砂にぶつかる場合
                        if map.map[wheel_id[0], wheel_id[1]-1] == 0:
                            # print("積み下ろす必要がある")
                            r = r3
                            collision_n += 1
                        else:
                            map.map[wheel_id[0], wheel_id[1]] = 1
                            # 積み下ろし
                            if map.map[wheel_id[0], wheel_id[1]-1] == 2:
                                map.map[wheel_id[0], wheel_id[1]-1] = 3
                                x_c, y_c = np.where(map.map==0)
                                r = r2*eval_action(x_c, y_c)
                                s_buc_next = 0
                            # 非目的地
                            else:
                                map.map[wheel_id[0], wheel_id[1]-1] = 4
                                s_buc_next = 1
                                r = def_r
                    # 空状態
                    if wheel == 3:
                        map.map[wheel_id[0], wheel_id[1]] = 1
                        # 積み上げ
                        if map.map[wheel_id[0], wheel_id[1]-1] == 0:
                            map.map[wheel_id[0], wheel_id[1]-1] = 4
                            x_c, y_c = np.where(map.map==0)
                            r = r1*eval_action(x_c, y_c)
                            s_buc_next = 1
                        # ゴール
                        elif map.map[wheel_id[0], wheel_id[1]-1] == 2:
                            map.map[wheel_id[0], wheel_id[1]-1] = 3
                            r = r5
                            s_buc_next = 0
                            collision_n += 1
                        # 無し
                        else:
                            map.map[wheel_id[0], wheel_id[1]-1] = 3
                            s_buc_next = 0
                            r = def_r
                else:
                    # print("over the workspace")
                    r = r4
                    collision_n += 1

            if 1 == act:
                if wheel_id[1] < (map.col-1):
                    if wheel == 4:
                        if map.map[wheel_id[0], wheel_id[1]+1] == 0:
                            # print("積み下ろす必要がある")
                            r = r3
                            collision_n += 1
                        else:
                            map.map[wheel_id[0], wheel_id[1]] = 1
                            if map.map[wheel_id[0], wheel_id[1]+1] == 2:
                                map.map[wheel_id[0], wheel_id[1]+1] = 3
                                x_c, y_c = np.where(map.map==0)
                                r = r2*eval_action(x_c, y_c)
                                s_buc_next = 0
                            else:
                                map.map[wheel_id[0], wheel_id[1]+1] = 4
                                s_buc_next = 1
                                r = def_r
                    if wheel == 3:
                        map.map[wheel_id[0], wheel_id[1]] = 1
                        if map.map[wheel_id[0], wheel_id[1]+1] == 0:
                            map.map[wheel_id[0], wheel_id[1]+1] = 4
                            x_c, y_c = np.where(map.map==0)
                            r = r1*eval_action(x_c, y_c)
                            s_buc_next = 1
                        elif map.map[wheel_id[0], wheel_id[1]+1] == 2:
                            map.map[wheel_id[0], wheel_id[1]+1] = 3
                            r = r5
                            s_buc_next = 0
                            collision_n += 1
                        else:
                            map.map[wheel_id[0], wheel_id[1]+1] = 3
                            s_buc_next = 0
                            r = def_r
                else:
                    # print("over the workspace")
                    r = r4
                    collision_n += 1

            if 2 == act:
                if wheel_id[0] > 0:
                    if wheel == 4:
                        if map.map[wheel_id[0]-1, wheel_id[1]] == 0:
                            # print("積み下ろす必要がある")
                            r = r3
                            collision_n += 1
                        else:
                            map.map[wheel_id[0], wheel_id[1]] = 1
                            if map.map[wheel_id[0]-1, wheel_id[1]] == 2:
                                map.map[wheel_id[0]-1, wheel_id[1]] = 3
                                x_c, y_c = np.where(map.map==0)
                                r = r2*eval_action(x_c, y_c)
                                s_buc_next = 0
                            else:
                                map.map[wheel_id[0]-1, wheel_id[1]] = 4
                                s_buc_next = 1
                                r = def_r
                    if wheel == 3:
                        map.map[wheel_id[0], wheel_id[1]] = 1
                        if map.map[wheel_id[0]-1, wheel_id[1]] == 0:
                            map.map[wheel_id[0]-1, wheel_id[1]] = 4
                            x_c, y_c = np.where(map.map==0)
                            r = r1*eval_action(x_c, y_c)
                            s_buc_next = 1
                        elif map.map[wheel_id[0]-1, wheel_id[1]] == 2:
                            map.map[wheel_id[0]-1, wheel_id[1]] = 3
                            r = r5
                            s_buc_next = 0
                            collision_n += 1
                        else:
                            map.map[wheel_id[0]-1, wheel_id[1]] = 3
                            s_buc_next = 0
                            r = def_r
                else:
                    # print("over the workspace")
                    r = r4
                    collision_n += 1

            if 3 == act:
                if wheel_id[0] < (map.row-1):
                    if wheel == 4:
                        if map.map[wheel_id[0]+1, wheel_id[1]] == 0:
                            # print("積み下ろす必要がある")
                            r = r3
                            collision_n += 1
                        else:
                            map.map[wheel_id[0], wheel_id[1]] = 1
                            if map.map[wheel_id[0]+1, wheel_id[1]] == 2:
                                map.map[wheel_id[0]+1, wheel_id[1]] = 3
                                x_c, y_c = np.where(map.map==0)
                                r = r2*eval_action(x_c, y_c)
                                s_buc_next = 0
                            else:
                                map.map[wheel_id[0]+1, wheel_id[1]] = 4
                                s_buc_next = 1
                                r = def_r
                    if wheel == 3:
                        map.map[wheel_id[0], wheel_id[1]] = 1
                        if map.map[wheel_id[0]+1, wheel_id[1]] == 0:
                            map.map[wheel_id[0]+1, wheel_id[1]] = 4
                            x_c, y_c = np.where(map.map==0)
                            r += r1*eval_action(x_c, y_c)
                            s_buc_next = 1
                        elif map.map[wheel_id[0]+1, wheel_id[1]] == 2:
                            map.map[wheel_id[0]+1, wheel_id[1]] = 3
                            r = r5
                            s_buc_next = 0
                            collision_n += 1
                        else:
                            map.map[wheel_id[0]+1, wheel_id[1]] = 3
                            s_buc_next = 0
                            r = def_r
                else:
                    # print("over the workspace")
                    r = r4
                    collision_n += 1

            s_row_next, s_col_next = np.where(map.map>=3)
            Q[s_row, s_col, s_buc, act] = Q[s_row, s_col, s_buc, act] +\
                lr*(r + y*np.max(Q[s_row_next, s_col_next, s_buc_next, :]) - Q[s_row, s_col, s_buc, act])
            rAll += r
            if map.map[goal_id[0], goal_id[1]] == 1:
                map.map[goal_id[0], goal_id[1]] = 2

            clear = np.where(map.map==0)
            if not bool(len(clear[0])):
                sys.stdout.write("  clear")
                break
            pygame.display.update()
            FPSCLOCK.tick(fps)
        if test != True:
            if ep%5 == 0:
                np.save(save_path + "/Qtable_ep{0:0=5}.npy".format(ep), Q)
        print()

if __name__ == "__main__":
    main(max_step=20000,
         episode=20,
         map_n=5,
         greed_e=0.1,
         r1=5, # 積み上げ報酬
         r2=10, # 積み下ろし報酬
         r3=-5, # 積み上げ状態での土砂ぶつかり報酬
         r4=-0.1, # 壁衝突報酬
         r5=-10, # 空状態でのゴール通過報酬
         def_r=-0.01, # ただ移動しているだけでは減点されていく
         test=True,
         fps=2000) 

