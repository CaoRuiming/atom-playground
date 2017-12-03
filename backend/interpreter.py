global_sandbox = globals()
local_sandbox = locals()

class AugmentedLine:
	def __init__(self, number, source, scope):
		self.number = number
		self.source = source
		self.result = ""
		self.variable_name = ""
		self.expression = ""
		self.executed = False
		self.parsed = False
		self.scope = scope

	def evaluate(self):
		if self.expression == "":
			self.executed = True
			return
		try:
			returned = eval(self.expression, global_sandbox, local_sandbox)
		except:
			self.executed = True
			self.result = "error"
			return

		self.executed = True
		self.expression_result = returned
		if (len(self.variable_name) > 0):
			self.result = self.variable_name + " = " + format_result(self.expression_result)
			exec(self.result, global_sandbox, local_sandbox)
		else:
			self.result = format_result(self.expression_result)
		self.executed = True

	def parse(self):
		first_equals = self.source.find("=")
		avoid_after = "=<>"
		avoid_before = "*+-/"
		# test for conditional
		if any((c in self.source[first_equals + 1]) for c in avoid_after):
			self.expression = self.source
		# elif any((c in self.source[first_equals - 1]) for c in avoid_before):
		# 	self.expression = self.source
		else:
			self.variable_name = self.source[:first_equals].strip()
			self.expression = self.source[first_equals + 1:].strip()
		self.parsed = True


def format_result(to_format):
	if type(to_format) is str:
		return "\"" + str(to_format) + "\""
	else:
		return str(to_format)