import string
from enum import Enum, unique
import random
from PIL import Image, ImageDraw, ImageFont
from init import MINESWEEPER_PATH
import init
import re

string_map = dict(enumerate(string.ascii_uppercase, 0))


@unique
class BlockStatu(Enum):
    normal = 1
    opened = 2
    mine = 3
    flag = 4
    ask = 5
    bomb = 6
    hint = 7
    double = 8


class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4


class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = value
        self._around_mine_count = -1
        self._status = BlockStatu.normal

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def get_around_mine_count(self):
        return self._around_mine_count

    def set_around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count

    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value

    x = property(fget=get_x, fset=set_x)
    y = property(fget=get_y, fset=set_y)
    value = property(fget=get_value, fset=set_value, doc='0:非地雷 1:雷')
    around_mine_count = property(fget=get_around_mine_count, fset=set_around_mine_count, doc='四周地雷数量')
    status = property(fget=get_status, fset=set_status, doc='BlockStatus')


class MineBlock:
    def __init__(self, block_width, block_height, mine_count):
        self.safe_area = []
        self._block_width = block_width
        self._block_height = block_height
        self._block = [[Mine(i, j) for i in range(block_width)] for j in range(block_height)]
        for i in random.sample(range(block_width * block_height), mine_count):
            self._block[i // block_width][i % block_height].value = 1
        for i in range(block_height):
            for j in range(block_width):
                if self._block[i][j].value == 0:
                    self.safe_area.append(i * block_width + j)

    def count_around(self, x, y):
        count = 0
        around = self._get_around(x, y)
        for i, j in around:
            if self._block[j][i].value:
                count += 1
        self._block[y][x].around_mine_count = count
        return count

    def _get_around(self, x, y):
        return [(i, j) for i in range(max(0, x - 1), min(self._block_width - 1, x + 1) + 1)
                for j in range(max(0, y - 1), min(self._block_height - 1, y + 1) + 1) if i != x or j != y]

    def open_block(self, x, y):
        if self._block[y][x].status == BlockStatu.flag:
            return 0
        if self._block[y][x].value:
            self._block[y][x].status = BlockStatu.bomb
            return -1

        self._block[y][x].status = BlockStatu.opened
        if y * self._block_width + x in self.safe_area:
            self.safe_area.remove(y * self._block_width + x)
        around_block = self._get_around(x, y)
        around_sum = self.count_around(x, y)
        if around_sum == 0:
            for i, j in around_block:
                if self._block[j][i].around_mine_count == -1:
                    self.open_block(i, j)
        return 1

    def get_block(self, x, y):
        return self._block[y][x]

    def flag(self, x, y):
        if self._block[y][x].status != BlockStatu.opened:
            if self._block[y][x].status == BlockStatu.flag:
                self._block[y][x].status = BlockStatu.normal
            elif self._block[y][x].status == BlockStatu.normal:
                self._block[y][x].status = BlockStatu.flag


class Game:
    def __init__(self, block_width, block_height, mine_count):
        self._block_width = block_width
        self._block_height = block_height
        self._mine_count = mine_count
        self._mine_block = MineBlock(block_width, block_height, mine_count)
        self._game_statu = GameStatus.readied

    def rander(self):
        board = Image.open(MINESWEEPER_PATH + "board.png")
        block = Image.open(MINESWEEPER_PATH + "block.png")
        flag = Image.open(MINESWEEPER_PATH + "flag.png")
        boom = Image.open(MINESWEEPER_PATH + "boom.png")
        num = [Image.open(MINESWEEPER_PATH + "1.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "2.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "3.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "4.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "5.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "6.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "7.png").resize((50, 50)),
               Image.open(MINESWEEPER_PATH + "8.png").resize((50, 50))]
        for i in range(self._block_width):
            for j in range(self._block_height):
                if self._mine_block.get_block(i, j).status == BlockStatu.normal:
                    board.paste(block, (i * 65 + 29, j * 65 + 29))
                    pos = [i * 65 + 35, j * 65 + 50]
                    draw = ImageDraw.Draw(board)
                    fill = "{}{}".format(string_map[i], j)
                    if len(fill) < 3:
                        pos[0] += 10
                    font = ImageFont.truetype(MINESWEEPER_PATH + "consolab.ttf", 30)
                    draw.text(pos, fill, fill=(0, 0, 0),
                              font=font)
                elif self._mine_block.get_block(i, j).status == BlockStatu.bomb:
                    board.paste(boom, (i * 65 + 30, j * 65 + 30))
                elif self._mine_block.get_block(i, j).status == BlockStatu.opened:
                    if self._mine_block.get_block(i, j).around_mine_count != 0:
                        board.paste(num[self._mine_block.get_block(i, j).around_mine_count - 1],
                                    (i * 65 + 35, j * 65 + 35))
                elif self._mine_block.get_block(i, j).status == BlockStatu.flag:
                    board.paste(flag, (i * 65 + 30, j * 65 + 30))
        board.save(init.IMAGE_PATH + "minesweeper.png")

    def open(self, x, y):
        while (self._mine_block.count_around(x, y) != 0 or self._mine_block.get_block(x, y).value) \
                and self._game_statu == GameStatus.readied:
            self._mine_block = MineBlock(block_width=self._block_width, block_height=self._block_height,
                                         mine_count=self._mine_count)
        if self._game_statu == GameStatus.readied:
            self._game_statu = GameStatus.started

        temp = self._mine_block.open_block(x, y)
        if temp == -1:
            self._game_statu = GameStatus.over

    def flag(self, x, y):
        if self._game_statu == GameStatus.readied:
            self._game_statu = GameStatus.started
        self._mine_block.flag(x, y)

    def get_state(self):
        return self._game_statu

    def execute(self, cmd: str):
        if cmd == "" or re.findall('[a-zA-Z]\\s*[0-9]{1,2}', cmd) is None:
            return False
        else:
            cmd = "".join(cmd.split())
            method = cmd[:2]
            parameter = re.findall('[a-zA-Z]\\s*[0-9]{1,2}', cmd)
            for i in parameter:
                if ord(i[0].lower()) - ord('a') < 0 or ord(i[0].lower()) - ord(
                        'a') >= self._block_width:
                    continue
                elif int(i[1:]) < 0 or int(i[1:]) > self._block_height:
                    continue
                else:
                    if method == "翻开":
                        self.open(ord(i[0].lower()) - ord('a'), int(i[1:]))
                    elif method == "插旗":
                        self.flag(ord(i[0].lower()) - ord('a'), int(i[1:]))
                    else:
                        break
            if not self._mine_block.safe_area:
                self._game_statu = GameStatus.win
            return True


if __name__ == "__main__":
    game = Game(9, 9, 9)
    ipt = input()
    game.execute(ipt)
    game.rander()
    while game.get_state() == GameStatus.started:
        ipt = input()
        game.execute(ipt)
        game.rander()
