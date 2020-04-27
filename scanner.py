import lex
import yacc

#list of token names

reserved = {
    'programa' : 'PROGRAMA',
    'principal' : 'PRINCIPAL',
    'var' : 'VAR',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'funcion' : 'FUNCION',
    'void' : 'VOID',
    'lee' : 'LEE',
    'escribe' : 'ESCRIBE',
    'si' : 'SI',
    'entonces' : 'ENTONCES',
    'sino' : 'SINO',
    'mientras' : 'MIENTRAS',
    'haz' : 'HAZ',
    'desde' : 'DESDE',
    'hasta' : 'HASTA',
    'hacer' : 'HACER',
    'null' : 'NULL'
}

tokens = [
    'CTE_I','CTE_F','CTE_C','CTE_S',
    'COMMENT','PLUS','DIV',
    'MINUS','LPAREN','RPAREN',
    'LBRACKET','RBRACKET','AND',
    'OR','COMPAR',
    'COLON','DET','TRAN',
    'INV','EQ','NOT_EQ',
    'GREATER','LESS','GREATER_EQ',
    'LESS_EQ','MULT','ID',
    'LIST_ID_ONE','LIST_ID_TWO','SEMI_COLON',
    'COMMA','DOT', 'RSQ', 'LSQ'
] + list(reserved.values())

#Regulars expression rules for simple tokens

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULT      = r'\*'
t_DIV       = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMPAR    = r'=='
t_EQ        = r'='
t_LBRACKET  = r'{'
t_RBRACKET  = r'}'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_COLON     = r':'
t_SEMI_COLON= r';'
t_DET       = r'\$'
t_TRAN      = r'¡'
t_INV       = r'\?'
t_COMMA     = r','
t_DOT       = r'\.'
t_NOT_EQ    = r'!='
t_GREATER_EQ= r'>='
t_LESS_EQ   = r'<='
t_GREATER   = r'>'
t_LESS      = r'<'
t_RSQ       = r'\]'
t_LSQ       = r'\['
t_CTE_C     = r'\'[A-Za-z]\''
t_CTE_S     = r'".+"'
t_LIST_ID_TWO=r'(\[)[1-9]+[0-9]*(\])(\[)[0-9]+[0-9]*(\])'
t_LIST_ID_ONE=r'(\[)[1-9]+[0-9]*(\])'
t_ignore  = ' \t'



def t_ignore_COMMENT(t):
    r'%%.*'
    pass

def t_ID(t):
    r'[A-Za-z]+[A-Za-z0-9]*'
    t.type = reserved.get(t.value,'ID') #Checks for reserved words
    return t

def t_CTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_F(t):
    r'(-)?[0-9]+(\.[0-9]+)?'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

data = "programa patito; var int i,j,p[1],h[2][3];"

lexer.input(data)

funcTable = {}

"""
fill_funcTable(lexer)


def fill_funcTable(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break
            # No more input
        elif tok.type == 'PROGRAMA':
            funcTable['global'] = ['global', 'void', '', fill_varTable(lexer)]

        elif tok.type == 'FUNCION':
            type = lexer.token().value
            name = lexer.token().value
            params = getParams(lexer)
            funcTable[name] = [name, type, params, fill_varTable(lexer)]

def fill_varTable(lexer):
    var_table = {}
    var_lexer = lexer

    while True:
        tok = var_lexer.token()

        if tok.type == 'VAR':
            while True:
                tok = var_lexer.token()
                if tok.type == 'INT' or tok.type == 'CHAR' or tok.type == 'FLOAT':
                    var_type = tok.type
                    while not tok.type == 'SEMI_COLON':
                        tok = var_lexer.token()
                        if tok.type == 'ID':
                            var_table[tok.value] = [tok.value, var_type, '']
        elif tok.type == 'FUNCION' or tok.type == 'PRINCIPAL' or not tok:
            break


    return var_table
"""

start = 'PROG'


def getParams(lexer):
    params = []


    return params



def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

def p_EMPTY(p):
    'EMPTY :'
    pass

def p_MAIN(p):
    '''MAIN : PROGRAMA LPAREN RPAREN LBRACKET BLOQUE RBRACKET'''
    pass

def p_PROG(p):
    'PROG : PROGRAMA ID SEMI_COLON VARS FUNCTION MAIN'
    pass

def p_VARS(p):
    '''VARS : VAR TIPO
            | EMPTY'''
    pass

def p_TIPO(p):
    '''TIPO : INT VAR_INT SEMI_COLON TIPO
            | FLOAT VAR_TIPO SEMI_COLON TIPO
            | CHAR VAR_TIPO SEMI_COLON TIPO
            | EMPTY'''
    pass

def p_VAR_INT(p):
    '''VAR_INT : ID LIST_ID_ONE COMMA VAR_INT
                | ID LIST_ID_TWO COMMA VAR_INT
                | ID COMMA VAR_INT
                | ID LIST_ID_ONE
                | ID LIST_ID_TWO
                | ID'''
    pass

def p_VAR_TIPO(p):
    '''VAR_TIPO : ID COMMA
                | ID'''
    pass

def p_FUNCTION(p):
    '''FUNCTION : FUNCION TIPO_FUNC ID LPAREN PARAMETROS RPAREN SEMI_COLON VARS LBRACKET BLOQUE RBRACKET FUNCTION
                | EMPTY'''
    pass

def p_TIPO_FUNC(p):
    '''TIPO_FUNC : INT
                | FLOAT
                | CHAR
                | VOID'''
    pass

def p_PARAMETROS(p):
    '''PARAMETROS : INT ID
                | FLOAT ID
                | CHAR ID
                | COMMA PARAMETROS'''
    pass

def p_DESDE_CICLO(p):
    '''DESDE_CICLO : DESDE ID EQ CTE_I HASTA CTE_I HACER LBRACKET BLOQUE RBRACKET
                    | EMPTY'''
    pass

def p_LECTURA(p):
    '''LECTURA : LEE LPAREN ID RPAREN SEMI_COLON
    '''
    pass


def p_ESCRITURA(p):
    '''ESCRITURA : ESCRIBE LPAREN TIPO_PARAMETROS RPAREN SEMI_COLON
                | EMPTY'''
    pass

def p_LLAMADA(p):
    '''LLAMADA : ID LPAREN TIPO_PARAMETROS RPAREN SEMI_COLON
            | EMPTY'''
    pass

def p_TIPO_PARAMETROS(p):
    '''TIPO_PARAMETROS : ID COMMA TIPO_ESCRITURA
                    | CTE_I COMMA TIPO_ESCRITURA
                    | CTE_F COMMA TIPO_ESCRITURA
                    | CTE_C COMMA TIPO_ESCRITURA
                    | CTE_S COMMA TIPO_ESCRITURA
                    | ID
                    | CTE_I
                    | CTE_F
                    | CTE_C
                    | CTE_S'''
    pass

def p_ESTATUTO(p):
    '''ESTATUTO : SI LPAREN EXPRESION RPAREN ENTONCES LBRACKET BLOQUE SEMI_COLON RBRACKET ESTATUTO_SINO
                | EMPTY'''
    pass

def p_ESTATUTO_SINO(p):
    '''ESTATUTO_SINO : SINO LBRACKET BLOQUE SEMI_COLON RBRACKET
                    | EMPTY'''
    pass

def p_MIENTRAS_CICLO(p):
    '''MIENTRAS_CICLO : MIENTRAS LPAREN EXPRESION RPAREN HAZ LBRACKET BLOQUE SEMI_COLON RBRACKET
                    | EMPTY'''
    pass

def p_EXPRESION(p):
    '''EXPRESION : EXPRESION_ARITMETICA
                | EXPRESION_LOGICA'''
    pass

def p_EXPRESION_ARITMETICA(p):
    '''EXPRESION_ARITMETICA : ID PLUS EXPRESION_ARITMETICA
                            | ID MINUS EXPRESION_ARITMETICA
                            | ID MULT EXPRESION_ARITMETICA
                            | ID DIV EXPRESION_ARITMETICA
                            | ID'''
    pass

def p_EXPRESION_LOGICA(p):
    '''EXPRESION_LOGICA : ID AND EXPRESION_LOGICA
                        | ID OR EXPRESION_LOGICA
                        | ID GREATER EXPRESION_LOGICA
                        | ID LESS EXPRESION_LOGICA
                        | ID GREATER_EQ EXPRESION_LOGICA
                        | ID LESS_EQ EXPRESION_LOGICA
                        | ID COMPAR
                        | ID'''
    pass

def p_BLOQUE(p):
    '''BLOQUE : DESDE_CICLO BLOQUE
            | LECTURA BLOQUE
            | ESCRITURA BLOQUE
            | LLAMADA BLOQUE
            | ESTATUTO BLOQUE
            | MIENTRAS_CICLO BLOQUE
            | EMPTY'''
    pass

parser = yacc.yacc()
