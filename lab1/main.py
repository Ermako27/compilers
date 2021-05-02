regExp = '(a|b)*abb'

def expandWithPlus(regExp):
    result = ''
    for i in range(len(regExp) - 1):
        if regExp[i].isalpha():
            if regExp[i + 1].isalpha():
                result += regExp[i] + '+'
            
            if regExp[i + 1] == '(':
                result += regExp[i] + '+'
            
            if regExp[i + 1] == ')':
                result += regExp[i]
            
            if regExp[i + 1] == '*' or regExp[i + 1] == '|':
                result += regExp[i]

        elif regExp[i] == '(':
            result += regExp[i]
        elif regExp[i] == ')':
            if regExp[i + 1].isalpha():
                result += regExp[i] + '+'

            if regExp[i + 1] == '(':
                result += regExp[i] + '+'

            if regExp[i + 1] == '*' or regExp[i + 1] == '|' or  regExp[i + 1] == ')':
                result += regExp[i]
        elif regExp[i] == '*':
            if regExp[i + 1].isalpha() or regExp[i + 1] == '(':
                result += regExp[i] + '+'
            else:
                result += regExp[i]
        elif regExp[i] == '|':
            result += regExp[i]
        
    result += regExp[len(regExp) - 1]
    return result

print(expandWithPlus('a|(b)'))