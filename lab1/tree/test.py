from tree import createPolishNotation

regExps = ['(a|b)*abb', 'a*b*(aa*|b)']

print(createPolishNotation(regExps[0]))
print('------------------------')
print(createPolishNotation(regExps[1]))