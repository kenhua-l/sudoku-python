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
				puzzle.solve()

				print(i, end=' ')
				if sudoku_util.puzzle_is_solved(puzzle):
					print("SUKODU SOLVED")
					win = win + 1
				else:
					print_sudoku(puzzle.solving_frame)
				i = i + 1
	print("%d/%d puzzles solved" %(win, i))

def smain():
	example = "009000200450090700020700009000140006090208010100075000600001090008020074005000300"
	puzzle = convert_to_puzzle(example)

	print_sudoku(puzzle.solving_frame)
	puzzle.solve()

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
