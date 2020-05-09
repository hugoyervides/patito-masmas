import yacc
from scanner import tokens, reserved
from stacks import Stacks
from fun_table import Funtable
from var_table import Vartable

#Variable declaration
poper = []
stacks = Stacks()
funTable = Funtable()
varTableCache = Vartable()

#Values for var table
context_func = 'global'
func_type = ''
dir_type = ''
dir_var = ''

#Var and Func Table
var_table = {
        'global' : {
            'var' : {}
        }
}


start = 'PROG'

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.error()
    else:
        print("Syntax error at EOF")

# =====================================================================
# ------------------- GRAMATICA PRINCIPAL ----------------------
# =====================================================================

def p_EMPTY(p):
    'EMPTY :'
    pass

def p_MAIN(p):
    '''MAIN : PRINCIPAL push_main LPAREN RPAREN BLOQUE'''
    pass

def p_PROG(p):
    'PROG : PROGRAMA ID SEMI_COLON VARS FUNCTION MAIN'
    pass

def p_VARS(p):
    '''VARS : VAR TIPO
            | EMPTY'''
    pass

def p_TIPO(p):
    '''TIPO : INT push_type VAR_INT SEMI_COLON TIPO
            | FLOAT push_type VAR_TIPO SEMI_COLON TIPO
            | CHAR push_type VAR_TIPO SEMI_COLON TIPO
            | EMPTY'''
    pass

def p_VAR_INT(p):
    '''VAR_INT : LIST_ID push_var COMMA VAR_INT
                | ID push_var COMMA VAR_INT
                | LIST_ID push_var
                | ID push_var'''
    pass

def p_VAR_TIPO(p):
    '''VAR_TIPO : ID push_var COMMA
                | ID push_var'''
    pass

def p_LIST_ID(p):
    '''LIST_ID : ID push_var LSQ SLEVEL_EXPRESION RSQ
                | ID push_var LSQ SLEVEL_EXPRESION RSQ LSQ SLEVEL_EXPRESION RSQ
    '''
    pass

# =====================================================================
# ------------------- GRAMATICA PARA EXPRESIONES ----------------------
# =====================================================================
def p_EXPRESION(p):
    '''EXPRESION : TLEVEL_EXPRESION r_new_quadruple EXPRESION_AUX'''
    pass

def p_EXPRESION_AUX(p):
    '''EXPRESION_AUX : COMPAR r_new_operator EXPRESION
                    | AND r_new_operator EXPRESION
                    | OR r_new_operator EXPRESION
                    | EMPTY'''
    pass

def p_TLEVEL_EXPRESION(p):
    '''TLEVEL_EXPRESION : SLEVEL_EXPRESION r_new_quadruple_tlevel TLEVEL_EXPRESION_AUX'''
    pass

def p_TLEVEL_EXPRESION_AUX(p):
    '''TLEVEL_EXPRESION_AUX : NOT_EQ r_new_operator TLEVEL_EXPRESION
                            | GREATER_EQ r_new_operator TLEVEL_EXPRESION
                            | LESS_EQ r_new_operator TLEVEL_EXPRESION
                            | GREATER r_new_operator TLEVEL_EXPRESION
                            | LESS r_new_operator TLEVEL_EXPRESION
                            | EMPTY'''
    pass

def p_SLEVEL_EXPRESION(p):
    '''SLEVEL_EXPRESION : FLEVEL_EXPRESION r_new_quadruple_slevel SLEVEL_EXPRESION_AUX'''
    pass

def p_SLEVEL_EXPRESION_AUX(p):
    '''SLEVEL_EXPRESION_AUX : PLUS r_new_operator SLEVEL_EXPRESION
                            | MINUS r_new_operator SLEVEL_EXPRESION
                            | EMPTY'''
    pass

def p_FLEVEL_EXPRESION(p):
    '''FLEVEL_EXPRESION : VALUE_EXPRESION r_new_quadruple_flevel FLEVEL_EXPRESION_AUX'''
    pass

def p_FLEVEL_EXPRESION_AUX(p):
    '''FLEVEL_EXPRESION_AUX : MULT r_new_operator FLEVEL_EXPRESION
                            | DIV r_new_operator FLEVEL_EXPRESION
                            | EMPTY'''
    pass

def p_VALUE_EXPRESION(p):
    '''VALUE_EXPRESION : ID r_new_id
                    | ID DET
                    | LIST_ID
                    | CONSTANTE 
                    | LLAMADA
                    | r_new_lparen LPAREN EXPRESION RPAREN r_new_rparen
    '''

def p_CONSTANTE(p):
    '''CONSTANTE : CTE_I r_new_constant
                | CTE_F r_new_constant
                | CTE_C r_new_constant
                | CTE_S r_new_constant
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
    '''FUNCTION : FUNCION TIPO_FUNC ID push_func LPAREN PARAMETROS RPAREN VARS BLOQUE FUNCTION
                | EMPTY'''
    pass

def p_TIPO_FUNC(p):
    '''TIPO_FUNC : INT
                | FLOAT
                | CHAR
                | VOID'''
    pass

def p_PARAMETROS(p):
    '''PARAMETROS : AUX_PARAM
                | EMPTY'''
    pass

def p_AUX_PARAM(p):
    '''AUX_PARAM : INT ID NEXT_PARAM
                | FLOAT ID NEXT_PARAM
                | CHAR ID NEXT_PARAM'''
    pass

def p_NEXT_PARAM(p):
    '''NEXT_PARAM : COMMA AUX_PARAM
                    | EMPTY '''

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


# =====================================================================
# --------------- PUNTOS NEURALGICOS ----------------
# =====================================================================
def p_r_new_id(p):
    'r_new_id : '
    stacks.register_operand(p[-1])

def p_r_new_constant(p):
    'r_new_constant : '
    stacks.register_operand(p[-1])

def p_r_new_lparen(p):
    'r_new_lparen : '
    stacks.register_separator()

def p_r_new_rparen(p):
    'r_new_rparen : '
    if not stacks.pop_separator():
        print("Invalid Construction of expr")

def p_r_new_operator(p):
    'r_new_operator : '
    stacks.register_operator(p[-1])    

def p_r_new_quadruple_flevel(p):
    'r_new_quadruple_flevel : '
    if stacks.top_operators() in ['*', '/']:
        stacks.generate_quadruple()

def p_r_new_quadruple_slevel(p):
    'r_new_quadruple_slevel : '
    if stacks.top_operators() in ['+', '-']:
        stacks.generate_quadruple()

def p_r_new_quadruple_tlevel(p):
    'r_new_quadruple_tlevel : '
    if stacks.top_operators() in ['!=', '>=', '<=', '>', '<']:
        stacks.generate_quadruple()
    
def p_r_new_quadruple(p):
    'r_new_quadruple : '
    if stacks.top_operators() in ['==','&&','||']:
        stacks.generate_quadruple()




# =====================================================================
# --------------- Tabla de Variables ----------------
# =====================================================================

def p_r_push_type(p):
    'push_type : '
    global dir_type
    dir_type = p[-1]

    print(dir_type)

def p_r_push_func(p):
    'push_func : '
    global context_func
    global func_type
    global var_table

    context_func = p[-1]
    func_type = p[-2]

    var_table[context_func] = {
        'type': func_type,
        'var': {},
    }

def p_r_push_var(p):
    'push_var : '
    global dir_var
    global var_table

    dir_var = p[-1]

    var_table[context_func]['var'][dir_var] = {
        'type': dir_type,
    }

def p_r_push_main(p):
    'push_main : '
    global var_table

    var_table['main'] = {
        'var': {}
    }

def printTable():
    print(var_table)



parser = yacc.yacc()

testScript = '''
    programa patito; 
    var
    int id1, id2, id3;
    principal(){
        a =  1 + id2 * (10 * (id1 + 55)) * id3;
    }
'''

parser.parse(testScript)
printTable()
stacks.quadruples.display_quadruples()


