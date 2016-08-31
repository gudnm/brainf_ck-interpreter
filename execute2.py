import sys

class BF(object):
    def __init__(self, size=12):
        self.tape = [0]*size
        self.pointer = 0

    def parse(self, code):
        stack = [[]]
        for command in code:
            if command == '[':
                stack.append([])
            elif command == ']':
                loop = stack.pop()
                stack[-1].append(loop)
            else:
                stack[-1].append(command)
        return stack[0]

    def execute(self, stack):
        for command in stack:
            if type(command) == list:
                while self.tape[self.pointer]:
                    self.tape = self.execute(command)
            elif command == '-':
                self.tape[self.pointer] -= 1
            elif command == '+':
                self.tape[self.pointer] += 1
            elif command == '<':
                self.pointer -= 1
            elif command == '>':
                self.pointer += 1
            elif command == ',':
                self.tape[self.pointer] = ord(input())
            elif command == '.':
                print(chr(self.tape[self.pointer]))#, end='')
        return self.tape
        

if __name__ == '__main__':
    bf = BF()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            bf.execute(bf.parse(f.read()))
