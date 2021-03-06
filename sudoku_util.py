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
    def find_certain_cell(self, possibility):
        return possibility

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
        self.solving_frame = backtracking(self.solving_frame)

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

    def solve(self):
        while not puzzle_is_solved(self):
            if has_certain_possibilities(self):
                while has_certain_possibilities(self):
                    self.fill_up_certain_ones()
            else:
                self.fill_uncertainly()

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

def backtracking(frame): #recursive function
    puzzle = SudokuPuzzle(frame)
    if puzzle_is_solved(puzzle):
        return puzzle.solving_frame
    else:
        pos_ = frame.find('0')
        if(pos_ < 0):
            # print('wrong pos_')
            return frame
        r,c,s = get_cell_location(pos_)
        possible_values = puzzle.possibilities[r][c]
        temp = frame
        for val_ in possible_values:
            temp = temp[:pos_] + str(val_) + temp[pos_ + 1:]
            puzzle_temp = SudokuPuzzle(temp)
            # if puzzle_is_solved(puzzle_temp):
                # print('in first else solve')
                # return puzzle_temp.solving_frame
            if not puzzle_temp.solving_flags.HAS_EMPTY_POSSIBILITY:
                if has_certain_possibilities(puzzle_temp):
                    while has_certain_possibilities(puzzle_temp):
                        try:
                            puzzle_temp.fill_up_certain_ones()
                            # if not has_certain_possibilities(puzzle_temp) and not puzzle_is_solved(puzzle_temp):
                                # puzzle_temp.solving_frame = backtracking(puzzle_temp.solving_frame)
                        except Exception as e:
                            print('in except', e)
                            break
                        try:
                            if not has_certain_possibilities(puzzle_temp) and not puzzle_is_solved(puzzle_temp):
                                puzzle_temp.solving_frame = backtracking(puzzle_temp.solving_frame)
                        except Exception as e:
                            print('in except of backtrack', e)
                            break
                else:
                # if not has_certain_possibilities(puzzle_temp) and not puzzle_is_solved(puzzle_temp):
                    puzzle_temp.solving_frame = backtracking(puzzle_temp.solving_frame)
                if puzzle_is_solved(puzzle_temp):
                    # print('in second else solve')
                    return puzzle_temp.solving_frame
            else:
                # print('to continue')
                continue
        # print('dummy return')
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

# SETUP
def get_row_numbers2(row, data):
    row_ = set([int(i) for i in data[(row * SQUARE):(row * SQUARE) + SQUARE]])
    row_.discard(0)
    return row_

def get_col_numbers2(col, data):
    col_ = set([int(i) for i in data[col:SQUARE ** 2:SQUARE]])
    col_.discard(0)
    return col_

def get_sq_numbers2(sq, data):
    start = (int(sq/WIDTH) * WIDTH * SQUARE) + (sq % WIDTH) * WIDTH
    sq_ = set([int(i) for i in data[start:start + WIDTH]])
    sq_ = sq_.union(set([int(i) for i in data[start + SQUARE:start + SQUARE + WIDTH]]))
    sq_ = sq_.union(set([int(i) for i in data[start + SQUARE * 2:start + SQUARE * 2 + WIDTH]]))
    sq_.discard(0)
    return sq_

def set_all(data):
    possibilities = defaultdict(dict)
    has_certain = False
    is_empty = False
    certain_list = []
    safety = 1
    solving = data
    while True and safety > 0:
        for x in range(SQUARE):
            for y in range(SQUARE):
                if solving[x * SQUARE + y] == '0':
                    r,c,s = get_cell_location(x * SQUARE + y)
                    r,c,s = get_row_numbers2(r, solving), get_col_numbers2(c, solving), get_sq_numbers2(s, solving)
                    r,c,s = find_missing(r), find_missing(c), find_missing(s)
                    possibilities[x][y] = intersect_sets(r, c, s)
                    if len(possibilities[x][y]) == 0:
                        is_empty = True
                    elif len(possibilities[x][y]) == 1:
                        has_certain = True
                        certain_list.append((x, y))
        for x,y in certain_list:
            val = str(possibilities[x][y].pop())
            solving = solving[:x * SQUARE + y] + val + solving[x * SQUARE + y + 1:]
        is_empty = False
        has_certain = False
        certain_list = []
        safety = safety - 1
    return solving, possibilities

def main():
    example = "060004000905000480040350000090070800102000904006010030000086040078000206000700050"
    example2 = "241976538000003001083514260438162795062300814100840326000098053300600000895431672"
    puzzle = SudokuPuzzle(example)
    # puzzle.fill_up_certain_ones()
    solution, puzzle2 = set_all(example)
    print(puzzle.solving_flags)
    for k,r in puzzle.possibilities.items():
        print(k)
        for c,v in r.items():
            print("   ", c, v)
        print("row ", k, " ", puzzle.solving_frame[k * 9: k * 9 + 9])
        print("row ", k, " ", solution[k * 9: k * 9 + 9])
        if puzzle2[k]:
            for c,v in puzzle2[k].items():
                print("   ", c, v)

# main()
