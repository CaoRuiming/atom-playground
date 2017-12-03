from interpreter import *

counter = 0



def tester(src):
	line1 = AugmentedLine(2, src)
	print(line1.source)
	line1.parse()
	line1.evaluate(scope)
	print(line1.result)
	print("")
	# counter += 1
scope = locals()
tester("x = 2 + 3")
tester("y = x + 2")
tester("y = y + 2")
tester("y = y + 2")
# tester("y - 1")
