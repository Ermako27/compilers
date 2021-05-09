from graphviz import Digraph
import csv
import xlsxwriter

from createTestDfa import *
from printFuncs import *
from regExpTestCases import *
from tree import createPolishNotation, createTree
from dfa import createDfa, minimizeDfa, State, Dfa, checkMatch

regExps = ['(a|b)*abb', 'a*b*(aa*|b)', '(a|b)', '(a|b)*']

def runTestCases(cases):
    for case in cases:
        result = checkMatch(case['regExp'], case['string'])
        case['actual'] = result
        print('regExp: {0}, string: {1}, expected: {2}, actual: {3}'.format(case['regExp'], case['string'], case['expected'], case['actual']))
    return cases

def createCsv(data):
    with open('lab1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['regExp', 'string', 'expected', 'actual'])
        for case in data:
            writer.writerow([case['regExp'], case['string'], case['expected'], case['actual']])

def createXslx(data):
    workbook = xlsxwriter.Workbook('lab1.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0

    worksheet.write(row, 0, 'regExp')
    worksheet.write(row, 1, 'string')
    worksheet.write(row, 2, 'expected')
    worksheet.write(row, 3, 'actual')
    for case in data:
        row += 1
        worksheet.write(row, 0, str(case['regExp']))
        worksheet.write(row, 1, str(case['string']))
        worksheet.write(row, 2, str(case['expected']))
        worksheet.write(row, 3, str(case['actual']))
    workbook.close()

result = runTestCases(testCases)
createCsv(result)
createXslx(result)

# ########## TREE TEST ##########
tree = createTree(regExps[1])
printFollowPos(tree)
printNumed(tree)
renderTree(tree.root)

# ########## DFA TEST ##########
dfa1 = createDfa(regExps[1])
printDfaStates(dfa1)
renderDfa(dfa1, 'dfaGraph')
minimizeRegExpClasses,  minimizeRegExpDfa = minimizeDfa(dfa1)
printMinimizedClasses(minimizeRegExpClasses)
renderDfa(minimizeRegExpDfa, 'minimizeRegExpDfa')

########## DFA MINIMIZATION TEST ##########
# 1
testDfa1 = createTestDfa1()
printDfaStates(testDfa1)
renderDfa(testDfa1, 'testDfa1')
minimizedClasses1,  minimizeTestDfa1 = minimizeDfa(testDfa1)
printMinimizedClasses(minimizedClasses1)
renderDfa(minimizeTestDfa1, 'minimizeTestDfa1')

# # 2
testDfa2 = createTestDfa2()
printDfaStates(testDfa2)
renderDfa(testDfa2, 'testDfa2')
minimizedClasses2,  minimizeTestDfa2 = minimizeDfa(testDfa2)
printMinimizedClasses(minimizedClasses2)
renderDfa(minimizeTestDfa2, 'minimizeTestDfa2')

# 3
testDfa3 = createTestDfa3()
printDfaStates(testDfa3)
renderDfa(testDfa3, 'testDfa3')
minimizedClasses3,  minimizeTestDfa3 = minimizeDfa(testDfa3)
printMinimizedClasses(minimizedClasses3)
renderDfa(minimizeTestDfa3, 'minimizeTestDfa3')

# # 4
testDfa4 = createTestDfa4()
printDfaStates(testDfa4)
renderDfa(testDfa4, 'testDfa4')
minimizedClasses4,  minimizeTestDfa4 = minimizeDfa(testDfa4)
printMinimizedClasses(minimizedClasses4)
renderDfa(minimizeTestDfa4, 'minimizeTestDfa4')

# #5
testDfa5 = createTestDfa5()
printDfaStates(testDfa5)
renderDfa(testDfa5, 'testDfa5')
minimizedClasses5,  minimizeTestDfa5 = minimizeDfa(testDfa5)
printMinimizedClasses(minimizedClasses5)
renderDfa(minimizeTestDfa5, 'minimizeTestDfa5')
