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
    '''MAIN : PRINCIPAL LPAREN RPAREN BLOQUE'''
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
    '''FUNCTION : FUNCION TIPO_FUNC ID LPAREN PARAMETROS RPAREN VARS BLOQUE FUNCTION
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
    '''DESDE_CICLO : DESDE ID EQ CTE_I HASTA CTE_I HACER BLOQUE'''
    pass

def p_LECTURA(p):
    '''LECTURA : LEE LPAREN ID RPAREN SEMI_COLON'''
    pass


def p_ESCRITURA(p):
    '''ESCRITURA : ESCRIBE LPAREN TIPO_PARAMETROS RPAREN SEMI_COLON'''
    pass

def p_LLAMADA(p):
    '''LLAMADA : ID LPAREN TIPO_PARAMETROS RPAREN SEMI_COLON'''
    pass

def p_TIPO_PARAMETROS(p):
    '''TIPO_PARAMETROS : ID COMMA TIPO_PARAMETROS
                    | CTE_I COMMA TIPO_PARAMETROS
                    | CTE_F COMMA TIPO_PARAMETROS
                    | CTE_C COMMA TIPO_PARAMETROS
                    | CTE_S COMMA TIPO_PARAMETROS
                    | EXPRESION COMMA TIPO_PARAMETROS
                    | ID
                    | CTE_I
                    | CTE_F
                    | CTE_C
                    | CTE_S
                    | EXPRESION'''
    pass

def p_ESTATUTO(p):
    '''ESTATUTO : SI LPAREN EXPRESION RPAREN ENTONCES BLOQUE ESTATUTO_SINO'''
    pass

def p_ESTATUTO_SINO(p):
    '''ESTATUTO_SINO : SINO BLOQUE
                    | EMPTY'''
    pass

def p_MIENTRAS_CICLO(p):
    '''MIENTRAS_CICLO : MIENTRAS LPAREN EXPRESION RPAREN HAZ BLOQUE'''
    pass

def p_EXPRESION(p):
    '''EXPRESION : ID OPERADOR_LOGICO EXPRESION
                | ID OPERADOR_ARITMETICO EXPRESION
                | ID LIST_ID_TWO OPERADOR_LOGICO EXPRESION
                | ID LIST_ID_TWO OPERADOR_ARITMETICO EXPRESION
                | ID LIST_ID_ONE OPERADOR_LOGICO EXPRESION
                | ID LIST_ID_ONE OPERADOR_ARITMETICO EXPRESION
                | CONSTANTE OPERADOR_LOGICO EXPRESION
                | CONSTANTE OPERADOR_ARITMETICO EXPRESION
                | LLAMADA_ASIGNACION OPERADOR_LOGICO EXPRESION
                | LLAMADA_ASIGNACION OPERADOR_ARITMETICO EXPRESION
                | LPAREN EXPRESION RPAREN EXPRESION
                | LPAREN EXPRESION RPAREN
                | ID
                | ID LIST_ID_TWO
                | ID LIST_ID_ONE
                | LLAMADA_ASIGNACION
                | CONSTANTE'''
    pass

def p_CONSTANTE(p):
    '''CONSTANTE : CTE_I
                | CTE_F
                | CTE_C
                | CTE_S
    '''

def p_OPERADOR_ARITMETICO(p):
    '''OPERADOR_ARITMETICO : PLUS
                            | MINUS
                            | MULT
                            | DIV
    '''

def p_OPERADOR_LOGICO(p):
    '''OPERADOR_LOGICO : AND
                        | OR
                        | GREATER
                        | LESS
                        | GREATER_EQ
                        | LESS_EQ
                        | COMPAR
    '''
    pass

def p_ASIGNACION(p):
    '''ASIGNACION : ID EQ ASIGNACION_AUX SEMI_COLON
                | ID LIST_ID_TWO EQ ASIGNACION_AUX SEMI_COLON
                | ID LIST_ID_ONE EQ ASIGNACION_AUX SEMI_COLON
    '''
    pass

def p_ASIGNACION_AUX(p):
    '''ASIGNACION_AUX : ID
                        | ID LIST_ID_TWO
                        | ID LIST_ID_ONE
                        | LLAMADA_ASIGNACION
                        | EXPRESION
    '''
    pass

def p_LLAMADA_ASIGNACION(p):
    '''LLAMADA_ASIGNACION : ID LPAREN TIPO_PARAMETROS RPAREN'''
    pass

def p_BLOQUE(p):
    '''BLOQUE : LBRACKET OPCION_BLOQUE RBRACKET'''
    pass

def p_OPCION_BLOQUE(p):
    '''OPCION_BLOQUE : LECTURA OPCION_BLOQUE
                    | ESCRITURA OPCION_BLOQUE
                    | LLAMADA OPCION_BLOQUE
                    | ESTATUTO OPCION_BLOQUE
                    | MIENTRAS_CICLO OPCION_BLOQUE
                    | DESDE_CICLO OPCION_BLOQUE
                    | ASIGNACION OPCION_BLOQUE
                    | EMPTY
    '''
    pass

parser = yacc.yacc()

testScript = '''
    programa patito; 
    var 
        int i,j,p[1],h[2][3];
        int Arreglo[10], OtroArreglo[10];
        float valor;
        int Matriz[3][8], OtraMatriz[3][3];
    funcion void inicia(int y)
    var int i;
    {
        i = j + (p - j*2 + j);
        si( j == 1 ) entonces{
            regresa(j);
        }sino{
            regresa(j * fact( j - 1 ));
        }
    }
    funcion void inicia( int j)
    var int x;
    {
        x=0;
        mientras (x < 11) haz{
            Arreglo[3] = y * x;
            x = x +1;
        }
    }
    principal(){
        lee(p);
        j=p*2;
        desde i = 0 hasta 9 hacer{
            Arreglo[2] = Arreglo[2] * fact(Arreglo[1] - p);
        }
        OtroArreglo = Arreglo;
        desde j = 0 hasta 2 hacer{
            desde k = 0 hasta 2 hacer{
                Matriz[3][3] = OtroArreglo[1] * p + j;
            }
        }
        escribe("el determinante es:", valor);
        mientras ( i >= 0) haz{
            escribe("resultado", Arreglo[1], fact(i+2)*valor);
            i = i - 1;
        }
    }
'''

parser.parse(testScript)