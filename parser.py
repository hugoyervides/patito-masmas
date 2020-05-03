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

# =====================================================================
# ------------------- GRAMATICA PRINCIPAL ----------------------
# =====================================================================

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
    '''VAR_INT : LIST_ID COMMA VAR_INT
                | ID COMMA VAR_INT
                | LIST_ID
                | ID'''
    pass

def p_VAR_TIPO(p):
    '''VAR_TIPO : ID COMMA
                | ID'''
    pass

def p_LIST_ID(p):
    '''LIST_ID : ID LSQ TIR_EXPRESION RSQ
                | ID LSQ TIR_EXPRESION RSQ LSQ TIR_EXPRESION RSQ
    '''
    pass

# =====================================================================
# ------------------- GRAMATICA PARA EXPRESIONES ----------------------
# =====================================================================
def p_EXPRESION(p):
    '''EXPRESION : SEC_EXPRESION
                | SEC_EXPRESION COMPAR EXPRESION
                | SEC_EXPRESION AND EXPRESION
                | SEC_EXPRESION OR EXPRESION'''
    pass

def p_SEC_EXPRESION(p):
    '''SEC_EXPRESION : TIR_EXPRESION
                    | TIR_EXPRESION NOT_EQ SEC_EXPRESION
                    | TIR_EXPRESION GREATER_EQ SEC_EXPRESION
                    | TIR_EXPRESION LESS_EQ SEC_EXPRESION
                    | TIR_EXPRESION GREATER SEC_EXPRESION
                    | TIR_EXPRESION LESS SEC_EXPRESION'''
    pass

def p_TIR_EXPRESION(p):
    '''TIR_EXPRESION : FOR_EXPRESION
                    | FOR_EXPRESION PLUS TIR_EXPRESION
                    | FOR_EXPRESION MINUS TIR_EXPRESION'''
    pass

def p_FOR_EXPRESION(p):
    '''FOR_EXPRESION : FIF_EXPRESION
                    | FIF_EXPRESION MULT FOR_EXPRESION
                    | FIF_EXPRESION DIV FOR_EXPRESION'''
    pass
 
def p_FIF_EXPRESION(p):
    '''FIF_EXPRESION : ID
                    | ID DET
                    | LIST_ID
                    | CONSTANTE
                    | LLAMADA
                    | LPAREN EXPRESION RPAREN
    '''
    pass

def p_CONSTANTE(p):
    '''CONSTANTE : CTE_I
                | CTE_F
                | CTE_C
                | CTE_S
    '''
    pass

# =====================================================================
# --------------- GRAMATICA PARA BLOQUE ----------------
# =====================================================================
def p_BLOQUE(p):
    '''BLOQUE : LBRACKET OPCION_BLOQUE RBRACKET'''
    pass

def p_OPCION_BLOQUE(p):
    '''OPCION_BLOQUE : LECTURA SEMI_COLON OPCION_BLOQUE
                    | ESCRITURA SEMI_COLON OPCION_BLOQUE
                    | LLAMADA SEMI_COLON OPCION_BLOQUE
                    | ESTATUTO OPCION_BLOQUE
                    | MIENTRAS_CICLO OPCION_BLOQUE
                    | DESDE_CICLO OPCION_BLOQUE
                    | ASIGNACION SEMI_COLON OPCION_BLOQUE
                    | EMPTY
    '''
    pass

# =====================================================================
# --------------- GRAMATICA PARA ELEMENTOS DEL BLOQUE ----------------
# =====================================================================

# FUNCIONES
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

#CICLO DESDE
def p_DESDE_CICLO(p):
    '''DESDE_CICLO : DESDE ID EQ CTE_I HASTA CTE_I HACER BLOQUE'''
    pass

#CICLO MIENTRAS
def p_MIENTRAS_CICLO(p):
    '''MIENTRAS_CICLO : MIENTRAS LPAREN EXPRESION RPAREN HAZ BLOQUE'''
    pass

#LECTURA
def p_LECTURA(p):
    '''LECTURA : LEE LPAREN ID RPAREN'''
    pass

#ESCRITURA
def p_ESCRITURA(p):
    '''ESCRITURA : ESCRIBE LPAREN TIPO_PARAMETROS RPAREN'''
    pass

#LLAMADA
def p_LLAMADA(p):
    '''LLAMADA : ID LPAREN TIPO_PARAMETROS RPAREN'''
    pass

def p_TIPO_PARAMETROS(p):
    '''TIPO_PARAMETROS : EXPRESION
                        | EXPRESION COMMA TIPO_PARAMETROS'''
    pass

#ESTATUTO
def p_ESTATUTO(p):
    '''ESTATUTO : SI LPAREN EXPRESION RPAREN ENTONCES BLOQUE ESTATUTO_SINO'''
    pass

def p_ESTATUTO_SINO(p):
    '''ESTATUTO_SINO : SINO BLOQUE
                    | EMPTY'''
    pass

#ASIGNACION
def p_ASIGNACION(p):
    '''ASIGNACION : ID EQ EXPRESION
                    | LIST_ID EQ EXPRESION'''
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
        si( j == 1 )entonces{
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
            Arreglo[x] = y * x;
            x = x +1;
        }
    }
    principal(){
        lee(p);
        j = p*2;
        desde i=0 hasta 9 hacer{
            Arreglo[i] = Arreglo[i] * fact(Arreglo[i]-p);
        }
        OtroArreglo = Arreglo;
        desde j=0 hasta 2 hacer{
            desde k=0 hasta 7 hacer{
                Matriz[j][k] = OtroArreglo[j+k-fact(p)+p*k] * p + j;
            }
        }
        desde j=0 hasta 2 hacer{
            desde k=0 hasta 2 hacer{
                OtraMatriz[j][k]=k+j;
            }
        }
        valor = OtraMatriz$;
        escribe("El determinante es: ", valor);
        mientras(i >= 0 ) haz{
            escribe("resultado" , Arreglo[i], fact(i+2) * valor);
            i = i - 1;
        }
    }
'''

parser.parse(testScript)