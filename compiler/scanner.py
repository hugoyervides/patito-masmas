from ply import lex

#list of token names

reserved = {
    'programa' : 'PROGRAMA',
    'principal' : 'PRINCIPAL',
    'var' : 'VAR',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'funcion' : 'FUNCION',
    'return' : 'RETURN',
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
    'LESS_EQ','MULT','ID','SEMI_COLON',
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
