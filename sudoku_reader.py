import sudoku_util
from sudoku_util import SudokuPuzzle
from time import sleep

def not_main():
	i = 0
	win = 0;
	with open('hard.sudoku') as f:
		for line in f:
			if not line == "":
				puzzle = convert_to_puzzle(line)

				safety = 3
				while not sudoku_util.puzzle_is_solved(puzzle) and safety > 0:
					if sudoku_util.has_certain_possibilities(puzzle):
						ite = 20
						while(sudoku_util.has_certain_possibilities(puzzle) and ite > 0):
							puzzle.fill_up_certain_ones()
							ite = ite - 1
					else:
						puzzle.fill_uncertainly()
					safety = safety - 1
				print(i, end=' ')
				if sudoku_util.puzzle_is_solved(puzzle):
					print("SUKODU SOLVED")
					win = win + 1
				else:
					print_sudoku(puzzle.solving_frame)
				i = i + 1
	print("%d/%d puzzles solved" %(win, i))

def main():
	example = "079400600600073400100000007090050700086204590002060040200000008007310004001007320"
	example = "400500061300004700070090000940800007007000400100005029000050090001700003260009004"
	puzzle = convert_to_puzzle(example)

	print_sudoku(puzzle.solving_frame)

	safety = 3
	while not sudoku_util.puzzle_is_solved(puzzle) and safety > 0:
		if sudoku_util.has_certain_possibilities(puzzle):
			ite = 20
			while(sudoku_util.has_certain_possibilities(puzzle) and ite > 0):
				puzzle.fill_up_certain_ones()
				ite = ite - 1
			print_sudoku(puzzle.solving_frame)
		else:
			puzzle.fill_uncertainly()
			print_sudoku(puzzle.solving_frame)
		print(safety)
		safety = safety - 1

	if sudoku_util.puzzle_is_solved(puzzle):
		print_sudoku(puzzle.solving_frame)
	else:
		print(puzzle.possibilities)

def convert_to_puzzle(data):
	return SudokuPuzzle(data)

def print_sudoku(puzzle):
	for x in range(9):
		for y in range(9):
			if puzzle[x * 9 + y] == '0':
				print('-', end='')
			else:
				print(puzzle[x*9 + y], end='')
			if y%3==2:
				print(' ', end='')
		print()
		if x%3==2:
			print()

main()
