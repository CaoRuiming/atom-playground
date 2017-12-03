
global_sandbox = globals()
local_sandbox = locals()

class AugmentedLine:
	def __init__(self, number, source):
		self.number = number
		self.original = source
		self.source = source.strip()
		self.result = ""
		self.variable_name = ""
		self.expression = ""
		self.executed = False
		self.parsed = False
		self.indent = get_indent(self.original)
		self.scope = local_sandbox
		self.if_flag = False

	#evaluate and store value in result
	def evaluate(self, scope):
		if self.expression == "":
			self.executed = True
			return
		try:
			returned = eval(self.expression, global_sandbox, scope)
		except:
			self.executed = True
			self.result = "error"
			return

		self.executed = True
		self.expression_result = returned
		if (len(self.variable_name) > 0):
			self.result = self.variable_name + " = " + format_result(self.expression_result)
			exec(self.result, global_sandbox, scope)
		else:
			self.result = format_result(self.expression_result)
		self.executed = True

	# get variable name if available, get expression
	def parse(self):
		if self.source.strip() == "":
			self.parsed = True
			return
		first_equals = self.source.find("=")
		avoid_after = "=<>"
		avoid_before = "*+-/"
		# test for conditional
		if any((c in self.source[first_equals + 1]) for c in avoid_after):
			# no variable assignment
			self.expression = self.source
		# elif any((c in self.source[first_equals - 1]) for c in avoid_before):
		# 	self.expression = self.source
		elif self.source[:2] == "if":
			self.expression = self.source[2 : len(self.source) - 1]
			self.if_flag = True
		else:
			# we have a variable assignment
			self.variable_name = self.source[:first_equals].strip()
			self.expression = self.source[first_equals + 1:].strip()
		self.parsed = True

class AugmentedInterpreter:
	def __init__(self, lines):
		self.number_lines = len(lines)
		lines = replace_four_spaces_tabs(lines)
		self.aug_lines = [AugmentedLine(i, lines[i]) for i in range(self.number_lines)]
		self.results = [""] * self.number_lines

	# parse all lines
	def parse(self):
		for aug_line in self.aug_lines:
			aug_line.parse()

	def run(self):
		line_number = -1
		stack = list(local_sandbox)
		curr_indent = 0
		expected_indent = False
		last_if = False
		while(line_number + 1 < self.number_lines):
			line_number = line_number + 1
			# run eval loop
			curr_line = self.aug_lines[line_number]
			if curr_line.source == "":
				#skip empty line
				continue
			if curr_line.indent > curr_indent:
				if expected_indent:
					# entering indented code
					curr_indent = curr_line.indent
					if curr_line.source == "else:":
						curr_line.result = not last_if
						if not last_if:
							# else is true
							expected_indent = True
						else:
							# else is false
							expected_indent = False
					else:
						curr_line.evaluate(local_sandbox)
				else:
					continue
			elif curr_line.indent < curr_indent: 
				# back to higher scope
				curr_indent = curr_line.indent
				if curr_line.source == "else:":
					curr_line.result = not last_if
					if not last_if:
						# else is true
						expected_indent = True
					else:
						# else is false
						expected_indent = False
				else:
					curr_line.evaluate(local_sandbox)
			else:
				# same flow
				curr_line.evaluate(local_sandbox)
			if curr_line.if_flag:
				# contained if statement
				if curr_line.expression_result:
					# if evaluated to true
					expected_indent = True
				else:
					expected_indent = False
				last_if = curr_line.expression_result
			else:
				expected_indent = False

			self.results[line_number] = curr_line.result

	def print_results(self):
		for line in self.aug_lines:
			print(line.result)

	def print_debug_results(self):
		for line in self.aug_lines:
			print("original: ", line.original, " result: ", line.result)








# get how many indents this line of text has (for determining scope)
def get_indent(source):
	return len(source) - len(source.lstrip())

# replace any four spaces by tabs to avoid confusion
def replace_four_spaces_tabs(lines):
	return [line.replace("    ", "\t") for line in lines]

# format output of python expressions
def format_result(to_format):
	if type(to_format) is str:
		return "\"" + str(to_format) + "\""
	else:
		return str(to_format)




























