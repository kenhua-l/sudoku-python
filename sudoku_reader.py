import sudoku_util
from sudoku_util import SudokuPuzzle
from time import sleep

def main():
	example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
	# example = "403072860701580300200106500000050410000000000037060000002807003004015207075620108"
	puzzle = convert_to_puzzle(example)

	print_sudoku(puzzle.solving_frame)

	ite = 10
	while(sudoku_util.has_certain_possibilities(puzzle.possibilities) and ite > 0):
		sleep(1)
		print(ite)
		puzzle.fill_up_certain_ones()
		print_sudoku(puzzle.solving_frame)
		ite = ite - 1


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
