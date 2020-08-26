class Piece:
    def __init__(self, name='', color='', location=None):
        self._name = name
        self._color = color
        self._location = location
        self._status = {
            'last_move': False,
            'attackers': [],
            'attacking': [],
            'defenders': [],
            'defending': []
        }
    def status(self):
        return self._status

    def __str__(self):
        return self._name + self._color

class Board:
    def __init__(self):
        self._board = [
            [Piece('R'), Piece('N'), Piece('B'), Piece('Q'), Piece('K'), Piece('B'), Piece('N'), Piece('R')],
            [Piece('P') for i in range(8)],
            [Piece('') for i in range(8)],
            [Piece('') for i in range(8)],
            [Piece('') for i in range(8)],
            [Piece('') for i in range(8)],
            [Piece('P') for i in range(8)],
            [Piece('R'), Piece('N'), Piece('B'), Piece('Q'), Piece('K'), Piece('B'), Piece('N'), Piece('R')]
        ]
        self._move_log = [{'last_was_full_move': False}]
        self._player = 'w'
        for i in range(2):
            for j in range(8):
                self._board[i][j]._location = (i, j)
                self._board[i][j]._color = 'b'
                self._board[i+6][j]._location = (i+6, j)
                self._board[i+6][j]._color = 'w'

        for i in range(8):
            for j in range(8):
                self.update_attackers_defenders((i, j))
                self.update_attacking_defending((i, j))

    def is_valid_move(self, src, dst):
        if self._board[src[0]][src[1]]._name == ''  or src == dst or \
           self._board[src[0]][src[1]]._color== self._board[dst[0]][dst[1]]._color or \
           self._board[dst[0]][dst[1]]._name == 'K':
            return False

        if self._board[src[0]][src[1]]._name == 'P':
            return self.is_valid_pawn_move(src, dst)
        if self._board[src[0]][src[1]]._name == 'N':
            return self.is_valid_knight_move(src, dst)
        if self._board[src[0]][src[1]]._name == 'B':
            return self.is_valid_bishop_move(src, dst)
        if self._board[src[0]][src[1]]._name == 'R':
            return self.is_valid_rook_move(src, dst)
        if self._board[src[0]][src[1]]._name == 'Q':
            return self.is_valid_queen_move(src, dst)
        if self._board[src[0]][src[1]]._name == 'K':
            return self.is_valid_king_move(src, dst)

    def is_valid_pawn_move(self, src, dst):
        # capture (en-passant not accounted for)
        if src[1] != dst[1]:
            if abs(src[1] - dst[1]) == 1: # next row capture
                if (self._board[dst[0]][dst[1]]._name != '' and self._board[src[0]][src[1]]._color != self._board[dst[0]][dst[1]]._color): # enemy capture
                    if (self._board[src[0]][src[1]]._color == 'w' and src[0] == dst[0]+1) or \
                       (self._board[src[0]][src[1]]._color == 'b' and src[0] == dst[0]-1):
                        return True
                    else:
                        print('cant move backward')
                        return False
                else:
                    print('cant capture your own piece or zilch')
            else:
                print('bad crossing')
                return False
        elif abs(src[0] - dst[0]) == 2:  # 2-move advance
            mid = 5 if self._board[src[0]][src[1]]._color == 'w' else 2
            if (src[0] == 6 and mid == 5) or (src[0] == 1 and mid == 2):
                if self._board[dst[0]][dst[1]]._name == '' and self._board[mid][dst[1]]._name == '':
                    if (mid == 5 and src[0] - dst[0] == 2) or (mid == 2 and dst[0] - src[0] == 2):
                        return True
                    else:
                        print('cant move backward')
                        return False
                else:
                    print('cant move thru')
                    return False
            else:
                print('wrong row')
                return False
        elif abs(src[0] - dst[0]) == 1: # 1-move advance
            if self._board[dst[0]][dst[1]]._name == '':
                if (self._board[src[0]][src[1]]._color == 'w' and src[0] - dst[0] == 1) or \
                   (self._board[src[0]][src[1]]._color == 'b' and dst[0] - src[0] == 1):
                    return True
                else:
                    print('cant move backward')
                    return False
            else:
                print('cant move thru')
                return False
        else:
            print('FTW?')
            return False

    def is_valid_knight_move(self, src, dst):
        jump = (abs(src[0] - dst[0]) == 1 and abs(src[1] - dst[1]) == 2) or \
               (abs(src[0] - dst[0]) == 2 and abs(src[1] - dst[1]) == 1)
        king = self._board[dst[0]][dst[1]]._name == 'K'
        return jump and not king

    def is_valid_bishop_move(self, src, dst):
        # valid jump
        if abs(src[0] - dst[0]) != abs(src[1] - dst[1]):
            return False

        # no pieces in the way
        i, j = src[0], src[1]
        if i < dst[0]:
            if j > dst[1]:  # down-left ward
                i += 1
                j -= 1
                while i < dst[0] and j > dst[1]:
                    if self._board[i][j]._name != '':
                        return False
                    i += 1
                    j -= 1
            else:           # down-right ward
                i += 1
                j += 1
                while i < dst[0] and j < dst[1]:
                    print(i, j, self._board[i][j])
                    if self._board[i][j]._name != '':
                        return False
                    i += 1
                    j += 1
        else:
            if j > dst[1]:  # up-left ward
                i -= 1
                j -= 1
                while i > dst[0] and j > dst[1]:
                    if self._board[i][j]._name != '':
                        return False
                    i -= 1
                    j -= 1
            else:           # up-right ward
                i -= 1
                j += 1
                while i > dst[0] and j < dst[1]:
                    if self._board[i][j]._name != '':
                        return False
                    i -= 1
                    j += 1
        return True

    def is_valid_rook_move(self, src, dst):
        # valid jump
        if src[0] != dst[0] and src[1] != dst[1]:
            return False

        # no pieces in the way
        if src[0] == dst[0]:    # moving across col
            for c in range(min(src[1], dst[1])+1, max(src[1], dst[1])):
                if self._board[src[0]][c]._name != '':
                    return False
        else:                   # moving across row
            for r in range(min(src[0], dst[0])+1, max(src[0], dst[0])):
                if self._board[r][src[1]]._name != '':
                    return False
        return True

    def is_valid_queen_move(self, src, dst):
        return self.is_valid_bishop_move(src, dst) or self.is_valid_rook_move(src, dst)

    def is_valid_king_move(self, src, dst):
        if (src[0] == dst[0] and abs(src[1]-dst[1]) == 1) or \
           (src[1] == dst[1] and abs(src[0]-dst[0]) == 1) or \
           (abs(src[0] - dst[0]) == 1 and abs(src[1] - dst[1]) == 1):
            if self._board[src[0]][src[1]]._color == self._board[dst[0]][dst[1]]:
                return False
            for piece in self._board[dst[0]][dst[1]]._status['attackers'] + self._board[dst[0]][dst[1]]._status['defenders']:
                if piece._name[1] != self._board[src[0]][src[1]]._color:
                    return False
            return True
        return self.is_valid_castle(src, dst)

    def is_valid_castle(self, src, dst):
        if (src == (7, 4) and dst == (7, 6)) or (src == (0, 4) and dst == (0, 6)) or \
           (src == (7, 4) and dst == (7, 2)) or (src == (0, 4) and dst == (0, 2)):
            king = self._board[src[0]][src[1]]
            if king._name == 'K':
                if not king._status['last_move']:
                    if king._status['attackers'] == []:
                        r = 7 if king._color == 'w' else 0
                        if self._board[r][7]._name == 'R' and not self._board[r][7]._status['last_move']:
                            squares = [(r, 5), (r, 6)] if dst == (r, 6) else [(r, 1), (r, 2), (r, 3)]
                            for (i, j) in squares:
                                for piece in self._board[i][j]._status['attackers'] + self._board[i][j]._status['defenders']:
                                    if piece._name[1] != king._color:
                                        print('free squares attacked')
                                        break
                                else:
                                    return True

    def update_attacking_defending_p(self, i, j):
        r = i+1 if self._board[i][j]._color == 'b' else i-1
        if i != 0 and i != 7:
            if j != 0:
                if self._board[i][j]._color != self._board[r][j-1]._color:
                    self._board[i][j]._status['attacking'].append(self._board[r][j-1])
                else:
                    self._board[i][j]._status['defending'].append(self._board[r][j-1])
            if j != 7:
                if self._board[i][j]._color != self._board[r][j-1]._color:
                    self._board[i][j]._status['attacking'].append(self._board[r][j+1])
                else:
                    self._board[i][j]._status['defending'].append(self._board[r][j+1])

    def update_attacking_defending_n(self, i, j):
        possibilities = [(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1),
                         (i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j-2)]
        for p in possibilities:
            if 0 <= p[0] <= 7 and 0 <= p[1] <= 7:
                if self._board[i][j]._color != self._board[p[0]][p[1]]._color:
                    self._board[i][j]._status['attacking'].append(self._board[p[0]][p[1]])
                else:
                    self._board[i][j]._status['defending'].append(self._board[p[0]][p[1]])

    def update_attacking_defending_b(self, i, j):
        r, c = i+1, j+1
        while r <= 7 and c <= 7:
            if self._board[i][j]._color != self._board[r][c]._color:
                self._board[i][j]._status['attacking'].append(self._board[r][c])
            else:
                self._board[i][j]._status['defending'].append(self._board[r][c])
            if self._board[r][c]._name: break
            r, c = r+1, c+1

        r, c = i+1, j-1
        while r <= 7 and c >= 0:
            if self._board[i][j]._color != self._board[r][c]._color:
                self._board[i][j]._status['attacking'].append(self._board[r][c])
            else:
                self._board[i][j]._status['defending'].append(self._board[r][c])
            if self._board[r][c]._name: break
            r, c = r+1, c-1

        r, c = i-1, j+1
        while r >= 0 and c <= 7:
            if self._board[i][j]._color != self._board[r][c]._color:
                self._board[i][j]._status['attacking'].append(self._board[r][c])
            else:
                self._board[i][j]._status['defending'].append(self._board[r][c])
            if self._board[r][c]._name: break
            r, c = r-1, c+1

        r, c = i-1, j-1
        while r >= 0 and c >= 0:
            if self._board[i][j]._color != self._board[r][c]._color:
                self._board[i][j]._status['attacking'].append(self._board[r][c])
            else:
                self._board[i][j]._status['defending'].append(self._board[r][c])
            if self._board[r][c]._name: break
            r, c = r-1, c-1

    def update_attacking_defending_r(self, i, j):
        c = j+1
        while c <= 7:
            if self._board[i][j]._color != self._board[i][c]._color:
                self._board[i][j]._status['attacking'].append(self._board[i][c])
            else:
                self._board[i][j]._status['defending'].append(self._board[i][c])
            if self._board[i][c]._name: break
            c += 1
        c = j-1
        while c >= 0:
            if self._board[i][j]._color != self._board[i][c]._color:
                self._board[i][j]._status['attacking'].append(self._board[i][c])
            else:
                self._board[i][j]._status['defending'].append(self._board[i][c])
            if self._board[i][c]._name: break
            c -= 1
        r = i+1
        while r <= 7:
            if self._board[i][j]._color != self._board[r][j]._color:
                self._board[i][j]._status['attacking'].append(self._board[r][j])
            else:
                self._board[i][j]._status['defending'].append(self._board[r][j])
            if self._board[r][j]._name: break
            r += 1
        r = i-1
        while r >= 0:
            if self._board[i][j]._color != self._board[r][j]._color:
                self._board[i][j]._status['attacking'].append(self._board[r][j])
            else:
                self._board[i][j]._status['defending'].append(self._board[r][j])
            if self._board[r][j]._name: break
            r -= 1

    def update_attacking_defending_q(self, i, j):
        self.update_attacking_defending_b(i, j)
        self.update_attacking_defending_r(i, j)

    def update_attacking_defending_k(self, i, j):
        for r in range(i-1, i+2):
            for c in range(j-1, j+2):
                if 0 <= r <= 7 and 0 <= c <= 7 and (r, c) != (i, j):
                    if self._board[i][j]._color != self._board[r][c]._color:
                        self._board[i][j]._status['attacking'].append(self._board[r][c])
                    else:
                        self._board[i][j]._status['defending'].append(self._board[r][c])

    def update_attacking_defending(self, src):
        i, j = src
        self._board[i][j]._status['attacking'] = []
        self._board[i][j]._status['defending'] = []
        if   self._board[i][j]._name == 'P': self.update_attacking_defending_p(i, j)
        elif self._board[i][j]._name == 'N': self.update_attacking_defending_n(i, j)
        elif self._board[i][j]._name == 'B': self.update_attacking_defending_b(i, j)
        elif self._board[i][j]._name == 'R': self.update_attacking_defending_r(i, j)
        elif self._board[i][j]._name == 'Q': self.update_attacking_defending_q(i, j)
        elif self._board[i][j]._name == 'K': self.update_attacking_defending_k(i, j)

    def update_attackers_defenders(self, src):
        i, j = src
        self._board[i][j]._status['attackers'] = []
        self._board[i][j]._status['defenders'] = []
        for r in range(8):
            for c in range(8):
                if src in self._board[r][c]._status['attacking']:
                    self._board[i][j]._status['attackers'].append(self._board[r][c])
                if src in self._board[r][c]._status['defending']:
                    self._board[i][j]._status['defenders'].append(self._board[r][c])

if __name__ == '__main__':
    board = Board()
