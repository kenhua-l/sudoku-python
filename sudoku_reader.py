import sudoku_util
from sudoku_util import SudokuPuzzle
from time import sleep

def mmain():
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

def main():
	example = "102539000900028513358600902830190625020305189519862437201003050483950201005200304"
	puzzle = convert_to_puzzle(example)

	print(puzzle.solving_flags)
	for k,r in puzzle.possibilities.items():
		print(k)
		for c,v in r.items():
			print("   ", c, v)
		# print("row ", k, " ", puzzle.solving_frame[k * 9: k * 9 + 9])

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
