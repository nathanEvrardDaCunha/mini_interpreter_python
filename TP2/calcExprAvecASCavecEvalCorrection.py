from genereTreeGraphviz2 import printTreeGraph

tokens = (
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE',
    'LPAREN','RPAREN'
    )

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

precedence = (
 
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
 
    )
 
   
    
def p_start(p):
    'start : expression'
    p[0] = ('START',p[1])
    print('Arbre de dérivation = ',p[0])
    printTreeGraph(p[0])
    print('CALC> ',eval(p[0]))

def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    p[0] = ('Expr', p[1],'+' , p[3])

def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = ('Expr', p[1],'*' , p[3])

 
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('Expr','(',p[2],')')

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('Num',p[1])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()



def eval (t):
    #print('eval de ',t, type(t), len(t))
    if type(t) is not tuple : 
        print('tree not tuple', t)
        return t 
    if t[0] is 'START' : return eval(t[1])
    if t[0] == 'Num' : return t[1]
    if t[0] is 'Expr' :
        if t[2] is '+':     return eval(t[1]) + eval(t[3]) 
        if t[2] is '*':     return eval(t[1]) * eval(t[3]) 
        if t[1] is '(' and t[3] is ')': return eval(t[2 ])
    return 'UNK'

s = '(1+2)*3'

yacc.parse(s)