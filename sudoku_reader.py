import sudoku_util
from sudoku_util import SudokuPuzzle
from time import sleep

def main():
	i = 0
	win = 0;
	with open('veryhard.sudoku') as f:
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

def nmain():
	example = "009000200450090700020700009000140006090208010100075000600001090008020074005000300"
	puzzle = convert_to_puzzle(example)

	print_sudoku(puzzle.solving_frame)

	safety = 2
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
