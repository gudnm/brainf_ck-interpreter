import math
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt

def num_length(num):
    if num == 0:
        return 1
    elif num > 0:
        return math.floor(math.log10(num)) + 1
    else:
        return num_length(-num) + 1

class REPL(object):
    def __init__(self, size=12):
        self.tape = [0]*size
        self.pointer = 0

    def __str__(self):
        spaces = 1
        for i in range(self.pointer):
            spaces += 2 + num_length(self.tape[i])
        return str(self.tape) + '\n' + ' '*spaces + '^'

    def execute(self, stack):
        output = ''
        for command in stack:
            if type(command) == list:
                while self.tape[self.pointer] != 0:
                    self.execute(command)
            elif command == '-':
                self.tape[self.pointer] -= 1
            elif command == '+':
                self.tape[self.pointer] += 1
            elif command == '<':
                self.pointer -= 1
            elif command == '>':
                self.pointer += 1
            elif command == ',':
                self.tape[self.pointer] = input()
            elif command == '.':
                output += chr(self.tape[self.pointer])
        if output:
            print(output)


if __name__ == '__main__':
    stack = [[]]
    code = ''
    repl = REPL()
    history = InMemoryHistory()
    while True:
        code = prompt('>>> ', history=history)
        if code == 'q':
            break
        for command in code:
            if command in '+-<>.,':
                stack[-1].append(command)
            elif command == '[':
                stack.append([])
            elif command == ']':
                loop = stack.pop()
                stack[-1].append(loop)
            elif command == '!':
                print(repl)
            elif command == '?':
                print('this is brainf*ck')
            elif command == 'x':
                repl.tape = [0]*len(repl.tape)
                repl.pointer = 0
                print(repl)
        if len(stack) == 1 and len(stack[0]):
            repl.execute(stack[0])
            stack = [[]]
            print(repl)
