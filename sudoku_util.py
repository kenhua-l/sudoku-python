from collections import defaultdict
import copy
# SUDOKU DIMENSION
WIDTH = 3
SQUARE = 9
NUMBERSET = {1,2,3,4,5,6,7,8,9}
SUM = 45

class Flags:
    def __init__(self):
        self.HAS_CERTAIN_POSSIBILITIES = False
        self.CERTAIN_POSSIBILITIES_LIST = []
        self.HAS_EMPTY_POSSIBILITY = False

    def __str__(self):
        ret_str = "Has possibility: " + str(self.HAS_CERTAIN_POSSIBILITIES) + "\n"
        ret_str = ret_str + "List: " + str(self.CERTAIN_POSSIBILITIES_LIST)
        return ret_str

class SudokuPuzzle:
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

    # CHECK
    def find_certain_row(self, possibility):
        row_list = []
        for x, row_ in possibility.items():
            for y, cell_ in row_.items():
                if not (x,y) in self.solving_flags.CERTAIN_POSSIBILITIES_LIST:
                    row_set = [v for k,v in row_.items() if k is not y]
                    row_set = set.union(*row_set)
                    row_set = cell_.difference(row_set)
                    if len(row_set) == 1:
                        possibility[x][y] = row_set
                        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = True
                        row_list.append((x,y))
        self.solving_flags.CERTAIN_POSSIBILITIES_LIST = self.solving_flags.CERTAIN_POSSIBILITIES_LIST + row_list
        return possibility

    def find_certain_col(self, possibility):
        col_list = []
        for i in range(SQUARE):
            has_col = [x for x, row_ in possibility.items() if i in row_.keys()]
            for row_number in has_col:
                if not (row_number,i) in self.solving_flags.CERTAIN_POSSIBILITIES_LIST:
                    cell_ = possibility[row_number][i]
                    col_set = [possibility[x][i] for x in has_col if x is not row_number]
                    col_set = set.union(*col_set)
                    col_set = cell_.difference(col_set)
                    if len(col_set) == 1:
                        possibility[row_number][i] = col_set
                        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = True
                        col_list.append((row_number,i))
        self.solving_flags.CERTAIN_POSSIBILITIES_LIST = self.solving_flags.CERTAIN_POSSIBILITIES_LIST + col_list
        return possibility

    def find_certain_sq(self, possibility): # O(9x3x3)
        sq_list = []
        square_solver = defaultdict(dict)
        for i in range(SQUARE):
            row_number = int(i / WIDTH) * WIDTH
            col_number = int(i * WIDTH % SQUARE)
            for x in range(WIDTH):
                if (row_number+x) in possibility.keys():
                    for y in range(WIDTH):
                        if (col_number+y) in possibility[row_number+x].keys():
                            square_solver[i][(row_number+x, col_number+y)] = possibility[row_number+x][col_number+y]
            for loc_, cell_ in square_solver[i].items():
                if not (loc_) in self.solving_flags.CERTAIN_POSSIBILITIES_LIST:
                    sq_set = [val_ for k, val_ in square_solver[i].items() if k is not loc_]
                    sq_set = set.union(*sq_set)
                    sq_set = cell_.difference(sq_set)
                    if len(sq_set) == 1:
                        possibility[loc_[0]][loc_[1]] = sq_set
                        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = True
                        sq_list.append(loc_)
        self.solving_flags.CERTAIN_POSSIBILITIES_LIST = self.solving_flags.CERTAIN_POSSIBILITIES_LIST + sq_list
        return possibility

    def set_possibilities(self, data):
        possibilities = defaultdict(dict)
        for x in range(SQUARE):
            for y in range(SQUARE):
                if data[x * SQUARE + y] == '0':
                    r,c,s = get_cell_location(x * SQUARE + y)
                    r,c,s = self.get_row_numbers(r), self.get_col_numbers(c), self.get_sq_numbers(s)
                    r,c,s = find_missing(r), find_missing(c), find_missing(s)
                    possibilities[x][y] = intersect_sets(r, c, s)
                    # solving backtracking issue
                    if len(possibilities[x][y]) == 0:
                        self.solving_flags.HAS_EMPTY_POSSIBILITY = True
                    elif len(possibilities[x][y]) == 1:
                        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = True
                        self.solving_flags.CERTAIN_POSSIBILITIES_LIST.append((x,y))
        if not self.solving_flags.HAS_EMPTY_POSSIBILITY:
            possibilities = self.find_certain_row(possibilities)
            possibilities = self.find_certain_col(possibilities)
            possibilities = self.find_certain_sq(possibilities)
        return possibilities

    # SOLVE
    def fill_uncertainly(self):
        self.solving_frame = backtracking(self.solving_frame, 5)

    def fill_up_certain_ones(self):
        temp = self.solving_frame
        for x,y in self.solving_flags.CERTAIN_POSSIBILITIES_LIST:
            val = str(self.possibilities[x][y].pop())
            temp = temp[:x * SQUARE + y] + val + temp[x * SQUARE + y + 1:]
        self.solving_flags.HAS_CERTAIN_POSSIBILITIES = False
        self.solving_flags.HAS_EMPTY_POSSIBILITY = False
        self.solving_flags.CERTAIN_POSSIBILITIES_LIST.clear()
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

def backtracking(frame, safety): #recursive function
    puzzle = SudokuPuzzle(frame)
    # print('safety', safety)
    if puzzle_is_solved(puzzle) or safety <= 0:
        return puzzle.solving_frame
    else:
        pos_ = frame.find('0')
        if(pos_ < 0):
            return frame
        r,c,s = get_cell_location(pos_)
        possible_values = puzzle.possibilities[r][c]
        temp = frame
        for val_ in possible_values:
            temp = temp[:pos_] + str(val_) + temp[pos_ + 1:]
            puzzle_temp = SudokuPuzzle(temp)
            # print(temp)
            if not puzzle_temp.solving_flags.HAS_EMPTY_POSSIBILITY:
                if puzzle_is_solved(puzzle_temp):
                    return puzzle_temp.solving_frame
                else:
                    if has_certain_possibilities(puzzle_temp):
                        ite = 30
                        while has_certain_possibilities(puzzle_temp) and ite > 0:
                            # print('iteration', ite)
                            try:
                                puzzle_temp.fill_up_certain_ones()
                                ite = ite - 1
                                if not has_certain_possibilities(puzzle_temp) and not puzzle_is_solved(puzzle_temp):
                                    puzzle_temp.solving_frame = backtracking(puzzle_temp.solving_frame, safety - 1)
                            except:
                                ite = 0
                    else:
                        puzzle_temp.solving_frame = backtracking(puzzle_temp.solving_frame, safety - 1)
                    if puzzle_is_solved(puzzle_temp):
                        return puzzle_temp.solving_frame
            else:
                continue
        return frame

# CHECK
def puzzle_is_solved(puzzle):
    if '0' in puzzle.solving_frame:
        return False
    else:
        for x in range(9):
            if sum(puzzle.get_row_numbers(x)) != SUM:
                return False
        for y in range(9):
            if sum(puzzle.get_col_numbers(y)) != SUM:
                return False
        for o in range(9):
            if sum(puzzle.get_sq_numbers(o)) != SUM:
                return False
        return True

def main():
    # testing
    # example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
    example = "403072860701580300200106500000050410000000000037060000002807003004015207075620108"
    puzzle = SudokuPuzzle(example)
    print(puzzle.possibilities)

# main()
