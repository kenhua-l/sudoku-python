# SUDOKU DIMENSION
WIDTH = 3
SQUARE = 9
NUMBERSET = {1,2,3,4,5,6,7,8,9}
# SQUARE_HASH = { 0:0, 1:3, 2:6, 3:27, 4:30, 5:33, 6:54, 7:57, 8:60 } #hard coded

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
        self.possibilities = {}

    def get_row_numbers(self, row):
        row_ = set(self.main_frame[(row * SQUARE):(row * SQUARE) + SQUARE])
        row_.discard('0')
        return row_

    def get_col_numbers(self, col):
        col_ = set(self.main_frame[col:SQUARE ** 2:SQUARE])
        col_.discard('0')
        return col_

    def get_sq_numbers(self, sq):
        start = (int(sq/WIDTH) * WIDTH * SQUARE) + (sq % WIDTH) * WIDTH
        sq_ = set(self.main_frame[start:start + WIDTH])
        sq_ = sq.union(set(self.main_frame[start + SQUARE:start + SQUARE + WIDTH]), set(self.main_frame[start + SQUARE * 2:start + SQUARE * 2 + WIDTH]))
        sq_.discard('0')
        return sq_

def get_cell_location(ordinal):
    # assume this is 9 x 9 sudoku
    # ordinal in terms of main_frame order
    row = int(ordinal / 9)
    col = int(ordinal % 9)
    square = int(row/3) * 3 + int(col/3)
    return row, col, square


def find_missing(num_set):
    missing = NUMBERSET.difference(num_set)
    return missing

def intersect_sets(horizontal_set, vertical_set, square_set):
    subset = horizontal_set.intersection(vertical_set, square_set)
    return subset

def main():
    # testing
    example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
    puzzle = SudokuPuzzle(example)
    for i in range(81):
        row, col, sq = get_cell_location(i)
        print(puzzle.get_col_numbers(col))

main()
