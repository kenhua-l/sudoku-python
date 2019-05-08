from collections import defaultdict
# SUDOKU DIMENSION
WIDTH = 3
SQUARE = 9
NUMBERSET = {1,2,3,4,5,6,7,8,9}

class Flags:
    def __init__(self):
        self.HAS_CERTAIN_POSSIBILITIES = False
        self.CERTAIN_POSSIBILITIES_LIST = []
        self.HAS_CERTAIN_ROW = False
        self.CERTAIN_ROW_LIST = []

class SudokuPuzzle:
	# in grid form where x is row, y is col
	# column dictionary in row where column has set data
	# eg.
	# {
	# 	0 : {
	# 			0 : {1,2,3,4,5}
	# 		}
	# }
    def __init__(self, data):
        self.main_frame = data
        self.solving_frame = data
        self.solving_flags = Flags()
        self.possibilities = self.set_possibilities(self.main_frame)

    # SETUP
    def get_row_numbers(self, row):
        row_ = set([int(i) for i in self.solving_frame[(row * SQUARE):(row * SQUARE) + SQUARE]])
        row_.discard(0)
        return row_

    def get_col_numbers(self, col):
        col_ = set([int(i) for i in self.solving_frame[col:SQUARE ** 2:SQUARE]])
        col_.discard(0)
        return col_

    def get_sq_numbers(self, sq):
        start = (int(sq/WIDTH) * WIDTH * SQUARE) + (sq % WIDTH) * WIDTH
        sq_ = set([int(i) for i in self.solving_frame[start:start + WIDTH]])
        sq_ = sq_.union(set([int(i) for i in self.solving_frame[start + SQUARE:start + SQUARE + WIDTH]]))
        sq_ = sq_.union(set([int(i) for i in self.solving_frame[start + SQUARE * 2:start + SQUARE * 2 + WIDTH]]))
        sq_.discard(0)
        return sq_

    def set_possibilities(self, data):
        possibilities = defaultdict(dict)
        for x in range(SQUARE):
            for y in range(SQUARE):
                if data[x * SQUARE + y] == '0':
                    r,c,s = get_cell_location(x * SQUARE + y)
                    r,c,s = self.get_row_numbers(r), self.get_col_numbers(c), self.get_sq_numbers(s)
                    r,c,s = find_missing(r), find_missing(c), find_missing(s)
                    possibilities[x][y] = intersect_sets(r, c, s)
                    if len(possibilities[x][y]) == 1:
                        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = True
                        self.solving_flags.CERTAIN_POSSIBILITIES_LIST.append((x,y))
        return possibilities

    # CHECK
    def find_certain_row(self):
        for x, row_ in self.possibilities.items():
            for y, cell_ in row_.items():
                row_set = [v for k,v in row_.items() if k is not y]
                row_set = set.union(*row_set)
                row_set = cell_.difference(row_set)
                if len(row_set) == 1:
                    self.HAS_CERTAIN_ROW = True
                    self.CERTAIN_ROW_LIST.append(x, y, row_set.pop())

    # SOLVE
    def fill_up_certain_ones(self):
        temp = self.solving_frame
        for x,y in self.solving_flags.CERTAIN_POSSIBILITIES_LIST:
            val = str(self.possibilities[x][y].pop())
            temp = temp[:x * SQUARE + y] + val + temp[x * SQUARE + y + 1:]
        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = False
        self.solving_flags.CERTAIN_POSSIBILITIES_LIST.clear()
        self.solving_frame = temp
        self.possibilities = self.set_possibilities(self.solving_frame)

    def fill_up_certain_in_rows(self):
        temp = self.solving_frame
        for x, row_ in self.possibilities.items():
            for y, cell_ in row_.items():
                row_set = [v for k,v in row_.items() if k is not y]
                row_set = set.union(*row_set)
                row_set = cell_.difference(row_set)
                if len(row_set) == 1:
                    val = row_set.pop()
                    temp = temp[:x * SQUARE + y] + str(val) + temp[x * SQUARE + y + 1:]
        self.solving_frame = temp
        self.possibilities = self.set_possibilities(self.solving_frame)


def get_cell_location(ordinal):
    # assume this is 9 x 9 sudoku
    # ordinal in terms of main_frame order
    row = int(ordinal / SQUARE)
    col = int(ordinal % SQUARE)
    square = int(row / WIDTH) * WIDTH + int(col / WIDTH)
    return row, col, square

def find_missing(num_set):
    missing = NUMBERSET.difference(num_set)
    return missing

def intersect_sets(horizontal_set, vertical_set, square_set):
    subset = horizontal_set.intersection(vertical_set, square_set)
    return subset

# SOLVE
def has_certain_possibilities(puzzle):
    return puzzle.solving_flags.HAS_CERTAIN_POSSIBILITIES

# CHECK
def puzzle_is_solved(puzzle):
    if '0' in puzzle.solving_frame:
        return False
    else:
        for x in range(9):
            row_ = puzzle.get_row_numbers(x)
            if find_missing(row_):
                return False
        for y in range(9):
            col_ = puzzle.get_col_numbers(y)
            if find_missing(col_):
                return False
        for o in range(9):
            sq_ = puzzle.get_sq_numbers(o)
            if find_missing(sq_):
                return False
        print('SUDOKU SOLVED')
        return True

def main():
    # testing
    # example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
    example = "403072860701580300200106500000050410000000000037060000002807003004015207075620108"
    puzzle = SudokuPuzzle(example)
    print(puzzle.possibilities)

# main()
