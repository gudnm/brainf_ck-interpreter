import sys
import unittest
import io

class Brainfuck:
	def __init__(self, code, stdin=sys.stdin, stdout=sys.stdout):
		self.stdin = stdin
		self.stdout = stdout
		self.code = code
		self.index_in_code = 0
		self.tape_size = 40
		self.tape = [0]*self.tape_size
		self.pointer = 0
		self.commands = {'+': self.plus, '-': self.minus, '<': self.left, '>': self.right, '[': self.start, ']': self.end, '.': self.out, ',': self.read}

	def __str__(self):
		res = ''
		for cell in self.tape:
			if cell > 9:
				res += str(cell)
			else:
				res += ' ' + str(cell)
		res += '\n'
		for _ in range(self.pointer):
			res += '  '
		res += '^'
		return res

	def run(self, command):
		if type(command) == list:
			# execute if not 0; otherwise move past
			while self.tape[self.pointer]:
				for subcommand in command:
					self.run(subcommand)
			

		self.commands[command]()

	def plus(self):
		self.tape[self.pointer] += 1

	def minus(self):
		self.tape[self.pointer] -= 1

	def left(self):
		if self.pointer == 0:
			self.pointer = self.tape_size-1
		else:
			self.pointer -= 1

	def right(self):
		if self.pointer == self.tape_size-1:
			self.pointer = 0
		else:
			self.pointer += 1

	def start(self):
		if self.tape[self.pointer] == 0:
			bracket_counter = 0
			i = self.index_in_code + 1
			while i < len(self.code):
				if bracket_counter == 0 and self.code[i] == ']':
					self.index_in_code = i
					break
				if self.code[i] == '[':
					bracket_counter += 1
				elif self.code[i] == ']':
					bracket_counter -= 1
				i += 1
			if i == self.tape_size:
				raise Exception('Unbalanced brackets')

	def end(self):
		if self.tape[self.pointer] != 0:
			bracket_counter = 0
			i = self.index_in_code - 1
			while i >= 0:
				if bracket_counter == 0 and self.code[i] == '[':
					self.index_in_code = i
					break
				if self.code[i] == '[':
					bracket_counter += 1
				elif self.code[i] == ']':
					bracket_counter -= 1
				i -= 1
			if i == -1:
				raise Exception('Unbalanced brackets')

	def out(self):
		self.stdout.write(chr(self.tape[self.pointer]))

	def read(self):
		self.tape[self.pointer] = ord(self.stdin.read(1))

	def execute(self):
		code = list(self.code)
		# parse
		self.stdout.write(code)
		while self.index_in_code < len(self.code):
			command = code[self.index_in_code]
			if command in self.commands:
				self.run(command)
			self.index_in_code += 1
			self.stdout.write(self)

if __name__ == '__main__':
	code = ''
	if len(sys.argv) > 1:
		with open(sys.argv[1], 'r') as f:
			code = f.read()
	b = Brainfuck(code)
	b.execute()


# python -m unittest execute (name of file)
class TestBrainfuck(unittest.TestCase):
	def setUp(self):
		self.fake_stdin = io.StringIO('A')
		self.fake_stdout = io.StringIO()
		self.bf = Brainfuck('', self.fake_stdin, self.fake_stdout)
	# 	self.bf = Brainfuck('++++++ [ > ++++++++++ < - ] > +++++ .')

	def test_plus(self):
		self.bf.plus()
		self.assertEqual(self.bf.tape[0], 1)

	def test_minus(self):
		self.bf.minus()
		self.assertEqual(self.bf.tape[0], -1)

	def test_right(self):
		self.bf.right()
		self.assertEqual(self.bf.pointer, 1)

	def test_left(self):
		self.bf.left()

	def test_out(self):
		self.bf.out()
		self.fake_stdout.seek(0)
		self.assertEqual(self.fake_stdout.read(), '\x00')

	def test_read(self):
		self.bf.read()
		self.bf.out()
		self.fake_stdout.seek(0)
		self.assertEqual(self.fake_stdout.read(), 'A')
