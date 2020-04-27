import yacc
from scanner import tokens, reserved


start = 'PROG'

symbol_table = {
        'global' : {
            'vars' : {},
        }
}

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
