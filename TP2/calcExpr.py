from genereTreeGraphviz2 import printTreeGraph  # à copier coller dans le script sinon

tokens = (
    'NUMBER', 'MINUS',
    'PLUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'SEMI'
)

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r'\;'


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

    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),

)

names = {}


def p_bloc(p):
    '''bloc : statement SEMI bloc
    | statement SEMI'''


def p_start(p):
    'start : expression'
    p[0] = ('bloc', p[1])
    print(p[0])
    printTreeGraph(p[0])


def p_assign(p):
    'statement : NAME EGAL expression'
    p[0] = ('assign', p[1], p[3])


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
    p[0] = ('NUMBER',p[1])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

s = 'print(1+2);x=4;x=x+1;'
yacc.parse(s)

    