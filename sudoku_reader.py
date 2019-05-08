import sudoku_util
from sudoku_util import SudokuPuzzle
from time import sleep

def main():
	# example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
	example = "403072860701580300200106500000050410000000000037060000002807003004015207075620108"
	# example = "006500100500002938090700506000270060005306700070095000308007050152600007009008200"
	# example = "0080090725002001000106000080005704600050009000430980008000060200060050047508006001"
	puzzle = convert_to_puzzle(example)

	print_sudoku(puzzle.solving_frame)

	safety = 10
	while not sudoku_util.puzzle_is_solved(puzzle) and safety > 0:
		if sudoku_util.has_certain_possibilities(puzzle):
			ite = 10
			print('strategy one')
			while(sudoku_util.has_certain_possibilities(puzzle) and ite > 0):
				puzzle.fill_up_certain_ones()
				ite = ite - 1
			print_sudoku(puzzle.solving_frame)
		else:
			print('strategy two')
			puzzle.fill_up_certain_in_rows()
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
