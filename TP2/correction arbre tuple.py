# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 10:06:29 2020

@author: FB
"""





tree=('+', ('+', 1, 2), 3 ) # + associatif à gauche

#tree=('-', ('+', 1, 2), 3 ) # +/- associatif à gauche

#tree= ('*', ('*', ('+', 1, 2), ('+', 3, 4)), ('+', 5, 6))# * associatif à gauche
#tree = ('+', ('+', 1, 2), 3)
tree= ('+', ('*', 2, 3), ('*', 5, 6))
tree=('+', 1, ('+', 2, 3)) # + associatif à droite
tree=('+', ('+', 1, 2), 3 ) # + associatif à gauche


def eval(t):
    print('eval de ',t)
    if type(t) is int : return t
    if type(t) is tuple : 
        if t[0] is '+' : return eval(t[1])+eval(t[2])
        if t[0] is '-' : return eval(t[1])-eval(t[2])
        if t[0] is '*' : return eval(t[1])*eval(t[2])
        if t[0] is '/' : return eval(t[1])//eval(t[2])
     
     
print(tree,' resultat =',eval(tree))
print()

def printExprPrefix(t):
    if type(t) is tuple : 
        print(t[0], end='')
        printExprPrefix(t[1])
        printExprPrefix(t[2])
    if type(t) is int : print(t, end='') 
    
print('prefixe ')
printExprPrefix(tree)
print()

def printExprPostfix(t):
    if type(t) is tuple : 
        printExprPostfix(t[1])
        printExprPostfix(t[2])
        print(t[0], end='')
    if type(t) is int : print(t, end='') 
    
print('postfixe ')
printExprPostfix(tree)

def printExprInfix(t):
    if type(t) is tuple : 
        print('(', end='')
        printExprInfix(t[1])
        print(t[0], end='')
        printExprInfix(t[2])
        print(')', end='')
        
    if type(t) is int : print(t, end='') 

print()
print('infixe ')
printExprInfix(tree)
