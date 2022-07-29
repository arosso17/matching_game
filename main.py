import os
import pygame as pg
import numpy as np

class Box:
    def __init__(self, pos, color, size, off=1):
        self.pos = [pos[0], - size[1] * off]
        self.color = color
        self.dest = pos
        self.falling = True
        self.size = size

    def move(self):
        if self.dest[1] - self.pos[1] >= 4:
            self.pos[1] += 4
        else:
            self.pos[1] = self.dest[1]
            self.falling = False

    def draw(self, win):
        pg.draw.rect(win, self.color, [self.pos[0] + 2, self.pos[1] + 2, self.size[0] - 4, self.size[1] - 4], border_radius=5)


class App:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 600
        self.FPS = 120
        pg.init()
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        self.clock = pg.time.Clock()
        self.win = pg.display.set_mode((self.screenWidth, self.screenHeight))
        pg.display.set_caption("Guess")
        # self.array = [[0 for _ in range(80)] for _ in range(60)]
        self.tab_screen = 0

    def check(self, board, coord, color, group=False):
        if group is False:
            group = [coord]
        if coord[0] > 0:
            if board[coord[0] - 1][coord[1]] == color:
                if [coord[0] - 1, coord[1]] not in group:
                    group.append([coord[0] - 1, coord[1]])
                    nays = self.check(board, [coord[0] - 1, coord[1]], color, group)
                    for nay in nays:
                        if nay not in group:
                            group.append(nay)
        if coord[0] < (len(board) - 1):
            if board[coord[0] + 1][coord[1]] == color:
                if [coord[0] + 1, coord[1]] not in group:
                    group.append([coord[0] + 1, coord[1]])
                    nays = self.check(board, [coord[0] + 1, coord[1]], color, group)
                    for nay in nays:
                        if nay not in group:
                            group.append(nay)
        if coord[1] > 0:
            if board[coord[0]][coord[1] - 1] == color:
                if [coord[0], coord[1] - 1] not in group:
                    group.append([coord[0], coord[1] - 1])
                    nays = self.check(board, [coord[0], coord[1] - 1], color, group)
                    for nay in nays:
                        if nay not in group:
                            group.append(nay)
        if coord[1] < (len(board[0]) - 1):
            if board[coord[0]][coord[1] + 1] == color:
                if [coord[0], coord[1] + 1] not in group:
                    group.append([coord[0], coord[1] + 1])
                    nays = self.check(board, [coord[0], coord[1] + 1], color, group)
                    for nay in nays:
                        if nay not in group:
                            group.append(nay)
        return group

    def game(self):
        colors = ["BLUE", "RED", [30, 190, 30], "YELLOW", "ORANGE", "PURPLE"]
        font_big = pg.font.SysFont('comicsans', 80, True)
        font_small = pg.font.SysFont('comicsans', 25, True)
        board_size = [8, 6]
        size = [int(self.screenWidth / board_size[0]), int(self.screenHeight / board_size[1])]
        board = [[np.random.randint(0, 4) for _ in range(board_size[1])] for _ in range(board_size[0])]
        boxes = [[Box([size[0] * i, (self.screenHeight - size[1]) - (size[1] * j)], colors[board[i][j]], size, j) for j in range(len(board[i]))] for i in range(len(board))]
        run = True
        score = 0
        lose = False
        while run:
            self.clock.tick(self.FPS)
            self.win.fill([0, 0, 0])
            falling = False
            for col in boxes:
                for box in col:
                    if box.falling:
                        falling = True
                        box.move()
                    box.draw(self.win)
            if lose:
                text = font_big.render("YOU LOSE", True, (250, 250, 250))
                text2 = font_big.render("SCORE: " + str(int(score)), True, (250, 250, 250))
                pg.draw.rect(self.win, "BLACK", [375 - max([text.get_width(), text2.get_width()]) // 2, 150, max([text.get_width(), text2.get_width()]) + 50, 175 + text2.get_height()], border_radius=7)
                pg.draw.rect(self.win, "WHITE", [375 - max([text.get_width(), text2.get_width()]) // 2, 150, max([text.get_width(), text2.get_width()]) + 50, 175 + text2.get_height()], 5, border_radius=7)
                self.win.blit(text, (400 - text.get_width()//2, 200))
                self.win.blit(text2, (400 - text2.get_width() // 2, 275))
            else:
                text = font_small.render(f"Score: {int(score)}", True, [255, 255, 255])
                self.win.blit(text, (self.screenWidth - text.get_width() - 10, 10))
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP and not falling:
                    if event.button == 1:
                        pos = pg.mouse.get_pos()
                        pos = [pos[0] // size[0], (board_size[1] - 1) - pos[1] // size[1]]
                        kills = self.check(board, pos, board[pos[0]][pos[1]])
                        if len(kills) > 2:
                            falling = True
                            score += len(kills) ** 1.25 // 1
                            print(score)
                            for kill in kills:
                                board[kill[0]][kill[1]] = None
                                boxes[kill[0]][kill[1]] = None
                        for col in board:
                            while None in col:
                                col.remove(None)
                        for i in range(len(board)):
                            dif = 0
                            for j in range(len(boxes[i])):
                                if boxes[i][j] is None:
                                    dif += 1
                                else:
                                    boxes[i][j].dest = [boxes[i][j].pos[0], boxes[i][j].pos[1] + dif * size[1]]
                                    boxes[i][j].falling = True
                        for col in boxes:
                            while None in col:
                                col.remove(None)
                        for i in range(len(board)):
                            col = board[i]
                            off = 1
                            while len(col) < board_size[1]:
                                if score > 250:
                                    c_num = np.random.randint(0, 6)
                                elif score > 100:
                                    c_num = np.random.randint(0, 5)
                                else:
                                    c_num = np.random.randint(0, 4)
                                col.append(c_num)
                                boxes[i].append(Box([size[0] * i, (self.screenHeight - size[1]) - size[1] * (len(boxes[i]))], colors[c_num], size, off))
                                off += 1
                    lose = True
                    all = [[[i, j], board[i][j]] for i in range(board_size[0]) for j in range(board_size[1])]
                    for po in all:
                        group = self.check(board, po[0], board[po[0][0]][po[0][1]])
                        if len(group) > 2:
                            lose = False
                            break
                        for p in group:
                            all.remove([[p[0], p[1]], board[p[0]][p[1]]])
                    if lose:
                        print("YOU LOSE")
                if event.type == pg.KEYUP:
                    if event.key == pg.K_r:
                        board = [[np.random.randint(0, 4) for _ in range(board_size[0])] for _ in range(board_size[1])]
                        boxes = [[Box([size[0] * i, (self.screenHeight - size[1]) - (size[1] * j)], colors[board[i][j]],size, j) for j in range(len(board[i]))] for i in range(len(board))]
                        score = 0
                        lose = False
                elif event.type == pg.QUIT:
                    run = False


if __name__ == "__main__":
    app = App()
    app.game()

