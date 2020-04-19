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

data = "programa patito var int i,j,p[1],h[2][3];"

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

start = 'PROGRAMA'

def p_EMPTY(p):
    'EMPTY: '
    pass

def p_PROG(p):
    'PROG: PROGRAMA ID SEMI_COLON VARS FUNCTION MAIN'
    pass

def p_VARS(p):
    '''VARS: VAR TIPO
    | EMPTY'''
    pass

def p_TIPO(p):
    '''TIPO: INT ID VAR_INT SEMI_COLON TIPO
    | INT ID LIST_ID_ONE VAR_INT SEMI_COLON TIPO
    | INT ID LIST_ID_TWO VAR_INT SEMI_COLON TIPO
    | FLOAT ID VAR_TIPO SEMI_COLON TIPO
    | CHAR ID VAR_TIPO SEMI_COLON TIPO
    | EMPTY'''
    pass

def p_VAR_INT(p):
    '''VAR_INT: COMMA ID LIST_ID_ONE 
    | COMMA ID LIST_ID_TWO 
    | COMMA ID
    | VAR_INT
    | EMPTY'''
    pass

def p_VAR_TIPO(p):
    '''VAR_TIPO: COMMA ID
    | VAR_TIPO
    | EMPTY'''
    pass
def p_TIPO_FUNC(p):
    '''TIPO_FUNC: INT
    | FLOAT 
    | CHAR 
    | VOID
    '''

def p_FUNCTION(p):
    '''FUNCTION: FUNCION TIPO_FUNC ID LPAREN PARAMETROS 
                 RPAREN SEMI_COLON VARS LBRACKET ESTATUTOS
                 RBRACKET FUNCTION
    | EMPTY
    '''
def p_PARAMETROS(p):
    '''PARAMETROS: '''