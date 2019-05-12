Hi!

So you wanna solve some sudoku.
1. Python - nothing fancy
db-reader.py is my programme to convert some xml file into the current .sudoku files so nothing interesting
sudoku_reader.py is the facade to put in my sudoku and solve it.
sudoku_util.py is the where the solving really happens

If you wanna use, just write down the sudoku string (I made the puzzle into a string, appending row after row
with the 0's representing empty cells) in the sudoku_reader and run it

python3 sudoku_reader.py
