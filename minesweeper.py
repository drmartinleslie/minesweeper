import random


class State:
    INCOMPLETE = 1
    WON = 2
    LOST = 3


class Board(object):
    """
    Minesweeper board

    Attributes:
        N: height and width of board
        contains_mine: board from top to bottom, left to right. False means no mine
        uncovered: False means covered
        num_neighbors: number of neighboring mines
        state: INCOMPLETE, WON or LOST
    """

    def __init__(self, N, prop_mines=0.3):
        self.N = N
        self.contains_mine = [[random.random() < prop_mines for j in xrange(N)] for i in xrange(N)]
        self.uncovered = [[False] * N for i in xrange(N)]
        self.num_neighbors = [[0] * N for i in xrange(N)]
        self.__compute_num_neighbors()
        self.state = State.INCOMPLETE

    def __compute_num_neighbors(self):
        for i in xrange(self.N):
            for j in xrange(self.N):
                for k in [i - 1, i, i + 1]:
                    for l in [j - 1, j, j + 1]:
                        if (k != i or l != j) and 0 <= k < self.N and 0 <= l < self.N:
                            if self.contains_mine[k][l]:
                                self.num_neighbors[i][j] += 1

    def __completed(self):
        for i in xrange(self.N):
            for j in xrange(self.N):
                if not self.contains_mine[i][j] and not self.uncovered[i][j]:
                    return False
        return True

    def uncover(self, m, n):
        """
        Click on m down, n across
        """
        self.uncovered[m][n] = True
        if self.contains_mine[m][n]:
            self.state = State.LOST
        elif self.__completed():
            self.state = State.WON

    def uncover_all(self):
        self.uncovered = [[True] * self.N for i in xrange(self.N)]


class CommandLineInterface(object):

    def __init__(self, board):
        self.board = board

    def print_board(self):
        for i in xrange(self.board.N):
            for j in xrange(self.board.N):
                if self.board.uncovered[i][j]:
                    if self.board.contains_mine[i][j]:
                        print "M",
                    else:
                        print self.board.num_neighbors[i][j],
                else:
                    print "#",
            print

    def get_coords(self):
        uncover_coords = raw_input("Input next pair to uncover (e.g. 1,2 uncovers 2nd line, 3rd column): ")
        values = [x for x in uncover_coords.split(',')]
        if len(values) == 2:
            m, n = values
            if m.isdigit() and 0 <= int(m) < self.board.N and n.isdigit() and 0 <= int(n) < self.board.N:
                return int(m), int(n)
        print "Invalid input"
        return self.get_coords()


def main(N):
    board = Board(N)
    ui = CommandLineInterface(board)
    while board.state == State.INCOMPLETE:
        ui.print_board()
        m, n = ui.get_coords()
        board.uncover(m, n)
    if board.state == State.WON:
        print "You won!"
    else:
        print "You lost!"
    board.uncover_all()
    ui.print_board()


if __name__ == "__main__":
    main(4)
