from genereTreeGraphviz2 import printTreeGraph

reserved = {
   'if': 'IF',
   'else': 'ELSE',
   'do': 'DO',
   'while': 'WHILE',
   'for': 'FOR',
   'then' : 'THEN',
   'print': 'PRINT',
   'float': 'FLOAT',
   'int': 'INT',
   'bool': 'BOOL',
   'string' : 'STRING',
   'printString' : 'PRINTSTRING',
    'void': 'VOID',
    'return': 'RETURN',
   }

tokens = [
    'NAME','NUMBER','TEXT',
    'PLUS','MINUS','TIMES','DIVIDE', 'PLUSPLUS','MINUSMINUS','BOOLEAN',
    'LPAREN','RPAREN', 'COLON','COMMA', 'AND', 'OR', 'EQUAL', 'EQUALS', 'LOWER','HIGHER','LOWEREQUAL','HIGHEREQUAL',
    'LBRACKET','RBRACKET','DOUBLEQUOTE'
    ]+list(reserved.values())

# Tokens

def t_BOOLEAN(t):
    r'true|false'
    t.type = reserved.get(t.value,'BOOLEAN')    # Check for reserved words
    return t
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

t_PLUS    = r'\+'
t_PLUSPLUS    = r'\+\+'
t_MINUS   = r'-'
t_MINUSMINUS   = r'--'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUAL  = r'='
t_DOUBLEQUOTE  = r'\"'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET  = r'\{'
t_RBRACKET  = r'\}'
t_COLON = r';'
t_COMMA = r','
t_AND  = r'\&'
t_OR  = r'\|'
t_EQUALS  = r'=='
t_LOWER  = r'\<'
t_HIGHER  = r'\>'
t_LOWEREQUAL  = r'\<='
t_HIGHEREQUAL  = r'\>='

def t_TEXT(t):
    r'\"[#-~]+(\s*[#-~]*)*\"'
    t.type = reserved.get(t.value,'TEXT')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
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
lexer = lex.lex()


# Parsing rules




def p_start(t):
    '''start : linst'''
    t[0] = ('start', t[1])
    print(t[0])
    printTreeGraph(t[0])
    evalInst(t[1])

names = {}
functions = {}

def evalInst(t):
    print('evalInst', t)
    if type(t) != tuple:
        print('warning')
        return

    if t[0] == 'print':
        if isinstance(t[1], tuple):
            print('CALC>', evalExpr(t[1]))
        elif t[1] in names:
            print('CALC>', names[t[1]])
        else:
            print('CALC>', evalExpr(t[1]))
    if t[0] == 'printString':
        print('CALC>', t[1])
    if t[0] == 'else':
        evalInst(t[1])
    if t[0] == 'if':
        if t[3]!=None:
            if(evalExpr(t[1])):
                evalInst(t[2])
            else:
                evalInst(t[3])
        else:
            if (evalExpr(t[1])):
                evalInst(t[2])
    if t[0] == 'while':
        while(evalExpr(t[1])):
            evalInst(t[2])
    if t[0] == 'do_while':
        evalInst(t[1])
        while(evalExpr(t[2])):
            evalInst(t[1])
    if t[0] == 'for':
        evalInst(t[1])

        while (evalExpr(t[2])):
            print(evalExpr(t[2]))
            evalInst(t[4])
            evalInst(t[3])
    if t[0]=='assign' :
        names[t[1]]=evalExpr(t[2])
    if t[0]=='upgrade' :
        names[t[1]]=evalExpr(t[2])
    if t[0]=='bloc' :
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'def_function':
        function_name = t[1]
        params = t[2]
        body = t[3]
        return_type = t[4]
        return_value = t[5] if len(t) == 6 else None
        if (isinstance(evalExpr(return_value), (int, float)) and (return_type == 'int' or return_type == 'float'))\
                or (isinstance(evalExpr(return_value), str) and return_type == 'string')\
                or (isinstance(bool(evalExpr(return_value)), bool) and return_type == 'bool'):
            functions[function_name] = {'params': params, 'body': body, 'return_type': return_type, 'return_value': return_value}
        else:
            functions[function_name] = {'params': params, 'body': body, 'return_type': return_type, 'return_value': 'Erreur de type de retour'}
    if t[0] == 'function_call':
        function_name = t[1]
        args = t[2]
        if function_name in functions:
            function_def = functions[function_name]
            if len(args) == len(function_def['params']):
                local_names = dict(zip(function_def['params'], args))
                names.update(local_names)
                evalInst(('bloc',) + (function_def['body'], 'empty'))
            else:
                print(f"Erreur: Nombre incorrect d'arguments pour la fonction {function_name}")
        else:
            print(f"Erreur: La fonction {function_name} n'est pas définie.")
    if t[0] == 'assign_function':
        variable_name = t[1]
        variable_body = t[2]
        variable_type = t[3]
        if ((variable_type == 'int' or variable_type == 'float') and isinstance(evalExpr(functions[variable_body[1]]['return_value']), (int, float)))\
                or (variable_type == 'string' and isinstance(evalExpr(functions[variable_body[1]]['return_value']), str))\
                or (variable_type == 'bool' and isinstance(bool(evalExpr(functions[variable_body[1]]['return_value'])), bool)):
            names[variable_name] = evalExpr(functions[variable_body[1]]['return_value'])
        else:
            names[variable_name] = 'Erreur de type de retour'
    if t[0] == 'print_function':
        print('CALC>', evalExpr(functions[t[1][1]]['return_value']))

def evalExpr(t):
    print('eval de ', t)
    if t in functions:
        return functions[t]
    if t in names : return names[t]
    if type(t) == int: return t
    if type(t) == str: return t
    if type(t) == bool : return t
    if type(t) == float : return t
    if type(t) == tuple:
        if t[0] == '+': return evalExpr(t[1]) + evalExpr(t[2])
        if t[0] == '-': return evalExpr(t[1]) - evalExpr(t[2])
        if t[0] == '*': return evalExpr(t[1]) * evalExpr(t[2])
        if t[0] == '/': return evalExpr(t[1]) // evalExpr(t[2])
        if t[0] == '%': return evalExpr(t[1]) % evalExpr(t[2])
        if t[0] == '++': return evalExpr(t[1]) + 1
        if t[0] == '--': return evalExpr(t[1]) - 1
        if t[0] == '==': return evalExpr(t[1]) == evalExpr(t[2])
        if t[0] == '>': return evalExpr(t[1]) > evalExpr(t[2])
        if t[0] == '<': return evalExpr(t[1]) < evalExpr(t[2])
        if t[0] == '>=': return evalExpr(t[1]) >= evalExpr(t[2])
        if t[0] == '<=': return evalExpr(t[1]) <= evalExpr(t[2])


print()

def p_line(t):
    '''linst : linst inst
            | inst '''
    if len(t) == 3:
        t[0] = ('bloc', t[1], t[2])
    else:
        t[0] = ('bloc', t[1], 'empty')

#IL FAUT IMPLEMENTER lES CONDITIONS POUR AVOIR UN BOOL QUI FONCTIONNE
def p_statement_assign(t):
    '''inst : INT NAME EQUAL expression COLON
            | STRING NAME EQUAL TEXT COLON
            | BOOL NAME EQUAL BOOLEAN COLON
            | FLOAT NAME EQUAL expression COLON
            | NAME EQUAL expression COLON'''

    if t[1] in ['int', 'float', 'string', 'bool']:
        if isinstance(evalExpr(t[4]), (int, float)) and (t[1] == 'int' or t[1] == 'float'):
            t[0] = ('assign', t[2], t[4])
            names[t[2]] = evalExpr(t[4])
        elif isinstance(evalExpr(t[4]), str) and t[1] == 'string':
            t[0] = ('assign', t[2], t[4])
            names[t[2]] = evalExpr(t[4])
        elif t[1] == 'bool':
            t[0] = ('assign', t[2], t[4])
            names[t[2]] = bool(evalExpr(t[4]))
        else:
            print("Erreur : Type de variable incorrect (REFAIRE LERREUR POUR QUELLE RESSORTE MIEUX AVEC CALC COMME LE DEMANDE LE PROF")
    else:
        t[0] = ('assign', t[1], t[3])
        names[t[1]] = evalExpr(t[3])


def p_names(t):
    '''NAMES : NAME COMMA NAMES
            | NAME '''
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = [t[1]] + t[3]


def p_expressions(t):
    '''EXPRESSIONS : expression COMMA EXPRESSIONS
            | expression '''
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = [t[1]] + t[3]





def p_statement_assign_multiple(t):
    '''inst : NAMES EQUAL EXPRESSIONS COLON
            | NAMES EQUAL expression COLON '''

    # t[0] = ('assign', t[1 + 2 * x], t[(len(t) - 1) - 2 * x])
    if type(t[3]) != int and len(t[1]) == len(t[3]):
        t[0] = ('multi_assign', t[1], t[3])
        for i in range(len(t[1])):
            names[t[1][i]] = evalExpr(t[3][i])
    elif type(t[3]) == int:
        t[0] = ('multi_assign', t[1], t[3])
        for i in range(len(t[1])):
            names[t[1][i]] = evalExpr(t[3])



def p_statement_upgrade(t):
    '''inst : NAME PLUSPLUS
            | NAME MINUSMINUS
            | NAME PLUS EQUAL NUMBER
            | NAME MINUS EQUAL NUMBER'''
    if (t[2] == '++'):

        names[t[1]] = evalExpr(t[2])
        t[0] = ('assign', t[1], ('+', t[1], 1))

    elif (t[3] == '='):
        t[0] = ('assign', t[1], (t[2],t[1],t[4]))


def p_statement_print(t):
    'inst : PRINT LPAREN expression RPAREN COLON'
    t[0] = ('print',t[3])

def p_statement_print_function(t):
    'inst : PRINT LPAREN inst RPAREN COLON'
    t[0] = ('print_function',t[3])

def p_statement_print_string(t):
    '''inst : PRINTSTRING LPAREN TEXT RPAREN COLON
            | PRINTSTRING LPAREN NAME RPAREN COLON'''
    t[0] = ('printString',t[3])
def p_statement_if(t):
    'inst : IF LPAREN expression RPAREN LBRACKET linst RBRACKET'
    t[0] = ('if', t[3], t[6])

def p_statement_if_else(t):
    'inst : IF LPAREN expression RPAREN LBRACKET linst RBRACKET ELSE LBRACKET linst RBRACKET'
    t[0] = ('if', t[3], t[6], ('else', t[10]))

def p_statement_while(t):
    'inst : WHILE LPAREN expression RPAREN LBRACKET linst RBRACKET'
    t[0] = ('while', t[3], t[6])

def p_statement_do_while(t):
    'inst : DO LBRACKET linst RBRACKET WHILE LPAREN expression RPAREN'
    t[0] = ('do_while', t[3], t[7])

def p_statement_for(t):
    'inst : FOR LPAREN inst compare COLON inst  RPAREN LBRACKET linst RBRACKET'
    t[0] = ('for', t[3], t[4], t[6],t[9])
def p_expression_compare(t):
    '''compare :
                  | expression EQUALS expression
                  | expression LOWER expression
                  | expression HIGHER expression'''
    t[0] = (t[2], t[1], t[3])

def p_statement_def_function(t):
    '''inst : VOID NAME LPAREN RPAREN LBRACKET linst RBRACKET
            | INT NAME LPAREN RPAREN LBRACKET linst RETURN expression COLON RBRACKET
            | FLOAT NAME LPAREN RPAREN LBRACKET linst RETURN expression COLON RBRACKET
            | BOOL NAME LPAREN RPAREN LBRACKET linst RETURN BOOLEAN COLON RBRACKET
            | STRING NAME LPAREN RPAREN LBRACKET linst RETURN TEXT COLON RBRACKET
            | VOID NAME LPAREN params RPAREN LBRACKET linst RBRACKET
            | INT NAME LPAREN params RPAREN LBRACKET linst RETURN expression COLON RBRACKET
            | FLOAT NAME LPAREN params RPAREN LBRACKET linst RETURN expression COLON RBRACKET
            | BOOL NAME LPAREN params RPAREN LBRACKET linst RETURN BOOLEAN COLON RBRACKET
            | STRING NAME LPAREN params RPAREN LBRACKET linst RETURN TEXT COLON RBRACKET'''
    if len(t) == 8:
        t[0] = ('def_function', t[2], [], t[6], t[1])
    elif len(t) == 9:
        t[0] = ('def_function', t[2], t[4], t[7], t[1])
    elif len(t) == 11:
        t[0] = ('def_function', t[2], [], t[6], t[1], t[8])
    elif len(t) == 12:
        t[0] = ('def_function', t[2], t[4], t[7], t[1], t[9])

def p_statement_assign_function(t):
    '''inst : INT NAME EQUAL inst
            | FLOAT NAME EQUAL inst
            | BOOL NAME EQUAL inst
            | STRING NAME EQUAL inst'''

    t[0] = ('assign_function', t[2], t[4], t[1])

def p_params(t):
    '''params :   NAME COLON params
                | NAME'''
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = [t[1]] + t[3]
    else:
        t[0] = []

def p_statement_function_call_args(t):
    'inst : NAME LPAREN args RPAREN COLON'
    t[0] = ('function_call', t[1], t[3])


def p_args(t):
    '''args :
            | expression
            | expression COLON args'''
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = [t[1]] + t[3]
    else:
        t[0] = []

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression OR expression
                  | expression AND expression
                  | expression EQUALS expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression LOWEREQUAL expression
                  | expression HIGHEREQUAL expression
                  | expression DIVIDE expression'''
    t[0] = (t[2],t[1], t[3])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    t[0] = t[1]

def p_expression_text(t):
    'expression : TEXT'

    t[0] = t[1]


def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

#s='1+2;int x=4;x=x+1;'
#s='print(1+2);int x=4;x=x+1;'
#s='if(2>1){int x=4;x+=2 print(x);}'
#s='int i=0; do{ print(1+2);i=i+1;}while(i==0)'
#s='int i=0; while(3>i){int x=4;i+=2 print(i);}'
#s='for(int i=0;i<4;i++){int x=4; print(i);}'
#s='printString("Zda6+5z t");'
#s='bool x = false;print(x);'
#s='string T ="Test DDZ"; print(T);'
#s='int i=0;i++ print(i>2);'
#s='int i=6;i-=4 print(i);'
#s='void zharks(x;y;z){print(1);}'
#s='i,d,c=2; print(i); print(c); print(d);'
#s='i=2 print(i);'
#s='if(2<1){int x=4;x+=2 print(x);}else{print(15);}'
#int result = test_function(True);
s='''
float test_function(x) {
    x = 20;
    x = x + 100;
    return x;
}

float result = test_function(10);
print(result);
'''
#with open("1.in") as file: # Use file to refer to the file object

   #s = file.read()

parser.parse(s)

