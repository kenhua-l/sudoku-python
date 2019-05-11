import sudoku_util
from sudoku_util import SudokuPuzzle
from time import sleep

def main():
	# example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
	# example = "403072860701580300200106500000050410000000000037060000002807003004015207075620108"
	# example = "0080090725002001000106000080005704600050009000430980008000060200060050047508006001"
	# example = "048001000700006100050900002000190403410637028309024000800009030001400006000500810"
	example = "602005140300000500000007208060080010200701004010040020706200000004000002021300405"
	# example = "008000030700609080004070002100048029000902000820310005500030200090105003080000100"
	# example = "009600080000020000451900006600870903003109200107042008200003859000090000070006104"

	puzzle = convert_to_puzzle(example)

	print_sudoku(puzzle.solving_frame)

	safety = 5
	while not sudoku_util.puzzle_is_solved(puzzle) and safety > 0:
		if sudoku_util.has_certain_possibilities(puzzle):
			ite = 10
			print('strategy one')
			while(sudoku_util.has_certain_possibilities(puzzle) and ite > 0):
				puzzle.fill_up_certain_ones()
				ite = ite - 1
			print_sudoku(puzzle.solving_frame)
		# else:
		# 	print('strategy two')
		# 	puzzle.find_certain_square(puzzle.possibilities)
		# 	print_sudoku(puzzle.solving_frame)
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
