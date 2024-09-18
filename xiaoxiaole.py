import pgzrun
import random
from pgzrun import *
from pygame import Rect
import math
import time

# 定义游戏相关属性
TITLE = '坤了个坤'
WIDTH = 600
HEIGHT = 720

# 自定义游戏常量
T_WIDTH = 60
T_HEIGHT = 66

# 下方牌堆的位置
DOCK = Rect((90, 564), (T_WIDTH*7, T_HEIGHT))

# 初始化牌组，12*12张牌随机打乱
ts = list(range(1, 13)) * 12
random.shuffle(ts)
tiles = []
docks = []

# 创建牌并添加到牌组
for k in range(7):   # 7层
    for i in range(7-k):
        for j in range(7-k):
            t = ts.pop()
            tile = Actor(f'tile{t}')
            tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9
            tile.tag = t
            tile.layer = k
            tile.status = 1 if k == 6 else 0
            tiles.append(tile)

# 剩余的4张牌放下面
for i in range(4):
    t = ts.pop()
    tile = Actor(f'tile{t}')
    tile.pos = 210 + i * tile.width, 516
    tile.tag = t
    tile.layer = 0
    tile.status = 1
    tiles.append(tile)

# 游戏帧绘制函数
def draw():
    screen.clear()
    screen.blit('back', (0, 0))   # 背景图
    for tile in tiles:
        tile.draw()
        if tile.status == 0:
            screen.blit('mask', tile.topleft)   # 不可点的添加遮罩
    for i, tile in enumerate(docks):
        tile.left = (DOCK.x + i * T_WIDTH)
        tile.top = DOCK.y
        tile.draw()

    # 超过7张，失败
    if len(docks) >= 7:
        screen.blit('end', (0, 0))
    # 没有剩牌，胜利
    elif len(tiles) == 0:
        screen.blit('win', (0, 0))

# 鼠标点击响应
def on_mouse_down(pos):
    global docks
    if len(docks) >= 7 or len(tiles) == 0:
        return
    for tile in reversed(tiles):
        if tile.status == 1 and tile.collidepoint(pos):
            tile.status = 2
            tiles.remove(tile)
            diff = [t for t in docks if t.tag != tile.tag]
            if len(docks) - len(diff) < 2:
                docks.append(tile)
            else:
                docks = diff
            for down in tiles:
                if down.layer == tile.layer - 1 and down.colliderect(tile):
                    for up in tiles:
                        if up.layer == down.layer + 1 and up.colliderect(down):
                            break
                    else:
                        down.status = 1
            return

# 设置倒计时机制
countdown = 180  # 设置倒计时为180秒
start_time = None

def update():
    global start_time
    if start_time is None:
        start_time = time.time()  # 记录游戏开始时间

    # 检查是否超时
    if time.time() - start_time > countdown:
        # 游戏失败逻辑
        screen.blit('end', (0, 0))
        # 这里可以添加游戏失败的处理逻辑，例如显示游戏结束画面

# 重写draw函数以显示倒计时
def draw():
    screen.clear()
    screen.blit('back', (0, 0))   # 背景图
    for tile in tiles:
        tile.draw()
        if tile.status == 0:
            screen.blit('mask', tile.topleft)   # 不可点的添加遮罩
    for i, tile in enumerate(docks):
        tile.left = (DOCK.x + i * T_WIDTH)
        tile.top = DOCK.y
        tile.draw()

    # 显示倒计时
    if start_time is not None:
        elapsed_time = time.time() - start_time
        remaining_time = countdown - elapsed_time
        if remaining_time > 0:
            screen.draw.text(f"剩余时间: {int(remaining_time)} 秒", topleft=(10, 10), color="red")
        else:
            screen.blit('end', (0, 0))  # 倒计时结束时显示失败图像
    # 如果牌堆超过7张，也显示失败图像
    if len(docks) >= 7:
        screen.blit('end', (0, 0))


music.play('bgm')

pgzrun.go()