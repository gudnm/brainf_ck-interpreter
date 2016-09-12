'''Goal is to write a brainf*ck REPL and see it in action (should interpret code like ++++++++[>++++[>++>+++>+++>+<<<<-]>+>->+>>+[<]<-]>>.>>---.+++++++..+++.>.<<-.>.+++.------.--------.>+.>++. which prints Hello World!)'''
t = [0]*100
p = [0]
s = [[]]
def run(frame):
    for x in frame:
        if type(x)==list:
            while t[p[0]]:
                run(x)
        elif x == '-': t[p[0]]-=1
        elif x == '+': t[p[0]]+=1
        elif x == '<': p[0]-=1
        elif x == '>': p[0]+=1 
        elif x == ',': t[p[0]]=ord(input())
        elif x == '.': print(chr(t[p[0]]), end='')

while True:
    code = input('? ')
    for c in code:
        if c in '-+<>,.':
            s[-1].append(c)
        elif c == '[':
            s.append([])
        elif c == ']':
            loop = s.pop()
            s[-1].append(loop)
    if len(s)==1 and len(s[0]):
        run(s[0])
        print(p[0], t)
        s = [[]]