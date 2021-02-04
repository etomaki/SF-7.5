class BoardException(Exception):
    pass

class WrongShipException(BoardException):
    pass


class Dots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Coord({self.x},{self.y})'
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
        self.busy_list = []
        self.hide = hide

    def __str__(self):
        result = '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for row, cell in enumerate(self.field_list):
            result += f'\n{row+1} | ' + ' | '.join(cell) + " |"
        return result

    def set_ship(self, ship):
        if ship.coord in self.busy_list:
            raise WrongShipException
        cntr = (
            (-1, 0), (-1, 1), (0, 1),
            (1, 1), (1, 0), (1,-1),
            (0, -1), (-1, -1)
        )
        for i in ship.coord:
            if not(self.hide):
                self.field_list[i.x][i.y] = '■'
            self.busy_list.append(i)
            for n in cntr:
                cell_busy = Dots(i.x - n[0], i.y - n[1])
                self.busy_list.append(cell_busy)

    def shot(self, coord):
        if coord in self.busy_list:
            self.field_list[coord.x][coord.y] = 'X'
        else:
            self.field_list[coord.x][coord.y] = '.'

    # def contour(self, ship):
    #     cntr = (
    #         (-1, 0), (-1, 1), (0, 1),
    #         (1, 1), (1, 0), (1,-1),
    #         (0, -1), (-1, -1)
    #     )



s = Ship(Dots(1,2), 3, 1)
a = Ship(Dots(4,1), 2, 1)
b = Board()
b.set_ship(a)
b.set_ship(s)
print(s.coord)
print(b)