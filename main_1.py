from random import randint
from colorama import init, Fore, Back, Style

init(autoreset=True)

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
        return Fore.RED + 'Вы уже стреляли сюда...'
class WrongCoordinates(InputException):
    def __str__(self):
        return Fore.RED + 'Введены неверные Координаты!'

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
        self.shooten_ships = 0

    def __str__(self):
        result = Fore.BLUE + '  • ' + ' • '.join(map(str, list(range(1, self.size+1))))
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
            self.shooten_ships += 1
        else:
            self.field_list[coord.x][coord.y] = 'T'
            self.shot_list.append(Dots(coord.x, coord.y))

    def clear_board(self):
        self.ship_list.clear()
        self.busy_list.clear()

class Player:

    def __init__(self, token, size):
        self.token = token
        self.size = size
        self.move_list = list(map(str, range(1, self.size + 1)))
        self.shot_list = []

    def shot_check(self, coord):
        if coord in self.shot_list:
            return True

    def new_shot_cell(self, coord):
        self.shot_list.append(coord)

class AI(Player):
    def move(self):
        player_choice = f'{randint(1, self.size)} {randint(1, self.size)}'
        player_choice = player_choice.split(' ')
        self.shot_list.append(Dots(player_choice[0], player_choice[1]))
        return Dots(int(player_choice[0])-1, int(player_choice[1])-1)

class User(Player):

    def move(self):
        while True:
            try:
                player_choice = input('Куда стрелять? ')
                player_choice = player_choice.split(' ')
                if player_choice[0] not in self.move_list or player_choice[1] not in self.move_list:
                    raise WrongCoordinates
            except WrongCoordinates as e:
                print(e)
            else:
                break
        return Dots(int(player_choice[0])-1, int(player_choice[1])-1)

class Game:

    def __init__(self, size_board):
        self.size = size_board

    def rnd_board(self, hid_=False):
        board = None
        while board is None:
            board = self.rnd_coord(hid_)
        return board
    
    def rnd_coord(self, hide_=False):
        ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size, hide=hide_)
        tries = 0
        for n in ships:
            while True:
                tries += 1
                if tries > 2000:
                    return None
                ship = Ship(Dots(randint(0, self.size), randint(0, self.size)), n, randint(0,1))
                try:
                    board.set_ship(ship)
                except WrongShipException:
                    pass
                else:
                    break
        return board
    
    @staticmethod
    def greet():
        print('Приветствуем вас в игре Морской Бой.'.center(50, ' '))
        print('------------------------------------'.center(50, ' '))
        print('Правила классические, координаты вида (x y)'.center(50, ' '))
        print('Удачной игры!'.center(50, ' '))

    def start(self):
        Board_game_user = self.rnd_board()
        Board_game_ai = self.rnd_board(True)
        User_pl = User(1, self.size)
        AI_pl = AI(2, self.size)

        while True:
            print('Доска игрока')
            print(Board_game_user)
            print('------------------------------')
            print('Доска компьютера')
            print(Board_game_ai)
            while True:
                try:
                    a = User_pl.move()
                    if User_pl.shot_check(a):
                        raise ShotRepeatException
                except ShotRepeatException as e:
                    print(e)
                else:
                    User_pl.new_shot_cell(a)
                    Board_game_ai.shot(a)
                    break
            while True:
                try:
                    b = AI_pl.move()
                    if AI_pl.shot_check(b):
                        raise ShotRepeatException
                except ShotRepeatException:
                    pass
                else:
                    AI_pl.new_shot_cell(b)
                    Board_game_user.shot(b)
                    break
            if Board_game_user.shooten_ships == 11:
                print('Доска игрока')
                print(Board_game_user)
                print('------------------------------')
                print('Доска компьютера')
                print(Board_game_ai)
                print('Победил Компьютер!')
                break
            elif Board_game_ai.shooten_ships == 11:
                print('Доска игрока')
                print(Board_game_user)
                print('------------------------------')
                print('Доска компьютера')
                print(Board_game_ai)
                print('Победил Игрок!')
                break
g = Game(6)
g.greet()
g.start()