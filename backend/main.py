import sys
from interpreter import *

# get file name from arguments, execute, and print
def main():
	if len(sys.argv) < 2:
		print("Missing file name")
	file_name = sys.argv[1]
	lines = file_to_lines(file_name)
	interpreter = AugmentedInterpreter(lines)
	interpreter.parse()
	interpreter.run()
	interpreter.print_results()
	print("done.")

# read file name into returned array
def file_to_lines(file_name):
	file = open(file_name, 'r')
	lines = file.readlines()
	file.close()
	return lines

main()