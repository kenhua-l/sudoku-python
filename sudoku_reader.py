import sudoku_util

def main():
	example = "093001600600000079470690000360000700700502001002000043000026037130000006006300150"
	puzzle = convert_to_puzzle(example)
	print_sudoku(example)

def convert_to_puzzle(data):
	return sudoku_util.SudokuPuzzle(data)

def print_sudoku(puzzle):
	for x in range(9):
		for y in range(9):
			if puzzle[x*9 + y] == '0':
				print('-', end='')
			else:
				print(puzzle[x*9 + y], end='')
			if y%3==2:
				print(' ', end='')
		print()
		if x%3==2:
			print()

main()
