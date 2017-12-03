import sys
from interpreter import *

def main():
	if len(sys.argv) < 2:
		print("Missing file name")
	file_name = sys.argv[1]
	lines = file_to_lines(file_name)
	counter = 1
	for line in lines:
		aug_line = AugmentedLine(counter, line)
		aug_line.parse()
		aug_line.evaluate(sandbox)
		print(aug_line.result)
		counter += 1
	print("done.")

def file_to_lines(file_name):
	file = open(file_name, 'r')
	lines = file.readlines()
	file.close()
	return lines

main()