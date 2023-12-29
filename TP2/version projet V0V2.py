from genereTreeGraphviz2 import printTreeGraph

reserved = {
   'if': 'IF',
   'do': 'DO',
   'while': 'WHILE',
   'for': 'FOR',
   'then': 'THEN',
   'print': 'PRINT',
   'float': 'FLOAT',
   'int': 'INT',
   'bool': 'BOOL',
   'void': 'VOID',
   'printString': 'PRINTSTRING',
}

tokens = [
    'NAME', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'COLON', 'AND', 'OR', 'EQUAL', 'EQUALS', 'LOWER', 'HIGHER',
    'LBRACKET', 'RBRACKET', 'DOUBLEQUOTE', 'COMMA'
] + list(reserved.values())

# Tokens


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUAL  = r'='
t_DOUBLEQUOTE  = r'\"'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET  = r'\{'
t_RBRACKET  = r'\}'
t_COLON = r';'
t_AND  = r'\&'
t_OR  = r'\|'
t_EQUALS  = r'=='
t_LOWER  = r'\<'
t_HIGHER  = r'\>'
t_COMMA = r','

def t_STRING(t):
    r'\"[#-~]+(\s*[#-~]*)*\"'
    t.type = reserved.get(t.value,'STRING')    # Check for reserved words
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
strings = {}
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
            print('CALC>', t[1])
    elif t[0] == 'printString':
        print('CALC>', strings[t[2]])
    elif t[0] == 'if':
        print('CALC>', evalExpr(t[1]))
    elif t[0] == 'while':
        print('CALC>', evalExpr(t[1]))
    elif t[0] == 'assign':
        variable_name = t[1]
        expression_result = evalExpr(t[2])
        names[variable_name] = expression_result
        print(f'Assign {variable_name} = {expression_result}')
    elif t[0] == 'bloc':
        evalInst(t[1])
        evalInst(t[2])
    elif t[0] == 'def_function':
        function_name = t[1]
        params = t[2]
        body = t[3]
        return_type = t[4]
        functions[function_name] = {'params': params, 'body': body, 'return_type': return_type}
    elif t[0] == 'function_call':
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

def evalExpr(t):
    print('eval de ', t)
    if t in functions:
        return functions[t]
    if t in names:
        return names[t]
    elif type(t) == int:
        return t
    elif type(t) == str:
        return t
    elif type(t) == bool:
        return t
    elif type(t) == float:
        return t
    elif type(t) == tuple:
        if t[0] == '+':
            return evalExpr(t[1]) + evalExpr(t[2])
        elif t[0] == '-':
            return evalExpr(t[1]) - evalExpr(t[2])
        elif t[0] == '*':
            return evalExpr(t[1]) * evalExpr(t[2])
        elif t[0] == '/':
            return evalExpr(t[1]) // evalExpr(t[2])
        elif t[0] == '%':
            return evalExpr(t[1]) % evalExpr(t[2])
        elif t[0] == '++':
            return evalExpr(t[1]) + 1
        elif t[0] == '--':
            return evalExpr(t[1]) - 1
        elif t[0] == '==':
            return evalExpr(t[1]) == evalExpr(t[2])

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
            | STRING NAME EQUAL expression COLON
            | BOOL NAME EQUAL expression COLON
            | FLOAT NAME EQUAL expression COLON
            | NAME EQUAL expression COLON'''
    if t[1] in ['int', 'float', 'string', 'bool']:
        if isinstance(evalExpr(t[4]), (int, float)) and (t[1] == 'int' or t[1] == 'float'):
            t[0] = ('assign', t[2], t[4])
            names[t[2]] = evalExpr(t[4])
            names[t[2]] = evalExpr(t[4])
        elif isinstance(evalExpr(t[4]), str) and t[1] == 'string':
            t[0] = ('assign', t[2], t[4])
            names[t[2]] = evalExpr(t[4])
        elif isinstance(evalExpr(t[4]), bool) and t[1] == 'bool':
            t[0] = ('assign', t[2], t[4])
            names[t[2]] = evalExpr(t[4])
        else:
            print("Erreur : Type de variable incorrect (REFAIRE LERREUR POUR QUELLE RESSORTE MIEUX AVEC CALC COMME LE DEMANDE LE PROF")
    else:
        t[0] = ('assign', t[1], t[3])
        names[1] = evalExpr(t[3])
def p_statement_upgrade(t):
    '''inst : NAME PLUS PLUS
            | NAME PLUS EQUAL NUMBER
            | NAME MINUS EQUAL NUMBER'''
    if (t[3] == '+'):
        t[0] = ('assign', t[1], ('+',t[1],'1'))
    elif (t[3] == '='):
        t[0] = ('assign', t[1], (t[2],t[1],t[4]))
    else:
        t[0] = ('assign', t[1], t[3])
def p_statement_print(t):
    'inst : PRINT LPAREN expression RPAREN COLON'
    t[0] = ('print',t[3])
def p_statement_names(t):
    '''NAMES : NAMES NAME
                | NAME '''
    if len(t)== 3 :
        t[0] = ('bloc',t[1], t[2])
    else:
        t[0] = ('bloc',t[1], 'empty')
def p_statement_print_string(t):
    'inst : PRINTSTRING LPAREN STRING RPAREN COLON'
    t[0] = ('printString',t[3])
def p_statement_if(t):
    'inst : IF LPAREN expression RPAREN LBRACKET linst RBRACKET'
    t[0] = ('if', t[3], t[6])

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
            | INT NAME LPAREN RPAREN LBRACKET linst RBRACKET
            | FLOAT NAME LPAREN RPAREN LBRACKET linst RBRACKET
            | BOOL NAME LPAREN RPAREN LBRACKET linst RBRACKET
            | STRING NAME LPAREN RPAREN LBRACKET linst RBRACKET
            | VOID NAME LPAREN params RPAREN LBRACKET linst RBRACKET
            | INT NAME LPAREN params RPAREN LBRACKET linst RBRACKET
            | FLOAT NAME LPAREN params RPAREN LBRACKET linst RBRACKET
            | BOOL NAME LPAREN params RPAREN LBRACKET linst RBRACKET
            | STRING NAME LPAREN params RPAREN LBRACKET linst RBRACKET'''
    if len(t) == 8:
        t[0] = ('def_function', t[2], [], t[6], t[1])
    elif len(t) == 9:
        t[0] = ('def_function', t[2], t[4], t[7], t[1])


def p_params(t):
    '''params :
                | NAME COMMA params
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
            | expression COMMA args'''
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

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

#s='1+2;x=4;x=x+1;'
#s='print(1+2);x=4;x=x+1;'
#s='do{ print(1+2);x=x+1;}while(2==1)'
#s='for(i=0;i>2;i+=5){x=4;}'
#s='printString("Zda6+5z t");'
#s='bool x = true;'

### CORRIGER LE FAIT QUE LE ASSIGN OU PRINT N'AFFICHE PAS LA VALEUR MISE A JOUR D'UNE VARIABLE
s = '''
void test(x, y, z) {
    print(x + 100 + z);
    print(y);
    print(17 - 2);
    
    print(separationnnnnnnnnnnnnn);
    
    int h = 1000000000;
    h = 7;
    print(h);
    
    int result = x;
    print(result);
}

test(1, 2, 3);

int h = 500;
h = 2;
print(h);
'''
#with open("1.in") as file: # Use file to refer to the file object

   #s = file.read()

parser.parse(s)

