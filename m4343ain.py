from random import randint

class BoardException(Exception):
    pass

class InputException(Exception):
    pass

class WrongShipException(BoardException):
    pass

class BoardOut(BoardException):
    def __str__(self):
        return 'Выход за поле...'
class ShotRepeatException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли сюда...'
class WrongCoordinates(InputException):
    def __str__(self):
        return 'Введены неверные Координаты!'

class Dots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dots({self.x},{self.y})'
class Ship:
    def __init__(self, bow, length, pos):
        self.length = length
        self.lives = length
        self.pos = pos
        self.bow = bow

        self.coord = []
        for i in range(self.length):
            x_, y_ = self.bow.x, self.bow.y
            if pos == 0: #horizontal position
                y_ += i
                self.coord.append(Dots(x_,y_))
            if pos == 1: #vertical position
                x_ += i
                self.coord.append(Dots(x_,y_))


class Board:
    def __init__(self, size=6, hide=False):
        self.size = size
        self.field_list = [['O'] * size for i in range(size)]
        self.ship_list = []
        self.busy_list = []
        self.hide = hide
        self.shot_list = []

    def __str__(self):
        result = '  • 1 • 2 • 3 • 4 • 5 • 6 •'
        for row, cell in enumerate(self.field_list):
            result += f'\n{row+1} | ' + ' | '.join(cell) + " |"
        return result

    def set_ship(self, ship):
        for i in ship.coord:
            if i in self.busy_list:            #Ship in busy cell check
                raise WrongShipException
        for i in ship.coord:
            if i.x not in range(self.size) or i.y not in range(self.size):
                raise WrongShipException
        cntr = (
            (-1, 0), (-1, 1), (0, 1),
            (1, 1), (1, 0), (1,-1),
            (0, -1), (-1, -1)
        )
        for i in ship.coord:
            if not self.hide:
                self.field_list[i.x][i.y] = '■'
            self.busy_list.append(Dots(i.x, i.y))
            self.ship_list.append(Dots(i.x, i.y))
            for n in cntr:
                x_, y_ = i.x + n[0], i.y + n[1]
                self.busy_list.append(Dots(x_,y_))

    def shot(self, coord):
        if coord.x not in range(self.size) or coord.y not in range(self.size):
            raise BoardOut
        if coord in self.ship_list:
            self.field_list[coord.x][coord.y] = 'X'
            self.shot_list.append(Dots(coord.x, coord.y))
        else:
            self.field_list[coord.x][coord.y] = '.'
            self.shot_list.append(Dots(coord.x, coord.y))
class Player:
    def __init__(self, token, size):
        self.token = token
        self.size = size
        self.move_list = list(map(str, range(1, self.size + 1)))
    # def move(self):
    #     if self.token % 2 != 0:
    #         while True:
    #             try:
    #                 player_choice = input('Куда ходить? ')
    #                 player_choice = player_choice.split(' ')
    #                 if player_choice[0] not in self.move_list or player_choice[1] not in self.move_list:
    #                     raise WrongCoordinates
    #             except WrongCoordinates as e:
    #                 print(e)
    #             else:
    #                 break
    #     else:
    #         # while True:
    #             # try:
    #         player_choice = f'{randint(1, self.size)} {randint(1, self.size)}'
    #         player_choice = player_choice.split(' ')

    #             #     if player_choice[0] not in self.move_list or player_choice[1] not in self.move_list:
    #             #         raise WrongCoordinates
    #             # except WrongCoordinates:
    #             #     continue
    #             # else:
    #             #     break
class AI(Player):
    def move(self):
        player_choice = f'{randint(1, self.size)} {randint(1, self.size)}'
        player_choice = player_choice.split(' ')
        return Dots(int(player_choice[0]), int(player_choice[1]))
class User(Player):
    def move(self):
        while True:
            try:
                player_choice = input('Куда ходить? ')
                player_choice = player_choice.split(' ')
                if player_choice[0] not in self.move_list or player_choice[1] not in self.move_list:
                    raise WrongCoordinates
            except WrongCoordinates as e:
                print(e)
            else:
                break
        return Dots(int(player_choice[0]), int(player_choice[1]))

class Game:
    def __init__(self, size_board):
        self.size = size_board
    @staticmethod
    def greet():
        print('Приветствуем вас в игре Морской Бой.'.center(50, ' '))
        print('------------------------------------'.center(50, ' '))
        print('Правила классические, координаты вида (x y)'.center(50, ' '))
        print('Удачной игры!'.center(50, ' '))

    def start(self):
        Board_game_user = Board(self.size, False)
        Board_game_ai = Board(self.size, True)
        User_pl = User(1, self.size)
        AI_pl = AI(2, self.size)
        while True:
            print('Доска игрока')
            print(Board_game_user)
            print('------------------------------')
            print('Доска компьютера')
            print(Board_game_ai)
            a = User_pl.move()
            Board_game_ai.shot(a)
            b = AI_pl.move()
            Board_game_user.shot(b)


g = Game(6)
g.greet()
g.start()