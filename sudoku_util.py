from collections import defaultdict
# SUDOKU DIMENSION
WIDTH = 3
SQUARE = 9
NUMBERSET = {1,2,3,4,5,6,7,8,9}

class SudokuPuzzle:
	# in grid form where x is row, y is col
	# column dictionary in row where column has list data
	# eg.
	# {
	# 	0 : {
	# 			0 : [1,2,3,4,5]
	# 		}
	# }
    def __init__(self, data):
        self.main_frame = data
        self.solving_frame = data
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
        return possibilities

    # SOLVE
    def fill_up_certain_ones(self):
        temp = self.solving_frame
        for x, set_ in self.possibilities.items():
            # delete = [y for (y, val) in set_.items() if len(val) == 1]
            for y, val in set_.items():
                if len(val) == 1:
                    temp = temp[:x * SQUARE + y] + str(val.pop()) + temp[x * SQUARE + y + 1:]
            # for y in delete: del set_[y]
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
def has_certain_possibilities(possible_dict):
    for x, set_ in possible_dict.items():
        for y, val in set_.items():
            if len(val) == 1:
                return True
    return False

def main():
    # testing
    # example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
    example = "403072860701580300200106500000050410000000000037060000002807003004015207075620108"
    puzzle = SudokuPuzzle(example)
    print(puzzle.possibilities)

# main()
