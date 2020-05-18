import yacc
from scanner import tokens, reserved
from stacks import Stacks
from fun_table import Funtable
from var_table import Vartable
from semantic import cubo_semantico

#Variable declaration
stacks = Stacks()
funTable = Funtable()

#Cache variables
globalVarTable = Vartable()
tempVarTable = Vartable()

#Values for var table
context_func = 'global'
func_type = ''
dir_type = ''
dir_var = ''
for_var = 0


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
    'PROG : r_new_goto PROGRAMA ID SEMI_COLON VARS r_change_local_context FUNCTION r_complete_goto r_change_global_context r_display_var_table MAIN'
    pass

def p_VARS(p):
    '''VARS : VAR TIPO
            | EMPTY'''
    pass

def p_TIPO(p):
    '''TIPO : INT r_set_var_type VAR_INT SEMI_COLON TIPO
            | FLOAT r_set_var_type VAR_TIPO SEMI_COLON TIPO
            | CHAR r_set_var_type VAR_TIPO SEMI_COLON TIPO
            | EMPTY'''
    pass

def p_VAR_INT(p):
    '''VAR_INT : LIST_ID COMMA VAR_INT
                | ID r_new_variable COMMA VAR_INT
                | LIST_ID
                | ID r_new_variable'''
    pass

def p_VAR_TIPO(p):
    '''VAR_TIPO : ID r_new_variable COMMA
                | ID r_new_variable'''
    pass

def p_LIST_ID(p):
    '''LIST_ID : ID r_new_variable LSQ SLEVEL_EXPRESION RSQ
                | ID r_new_variable LSQ SLEVEL_EXPRESION RSQ LSQ SLEVEL_EXPRESION RSQ
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
                    | IF_STMT OPCION_BLOQUE
                    | IF_ELSE_STMT OPCION_BLOQUE
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
    '''FUNCTION : r_new_function FUNCION TIPO_FUNC ID r_set_fun_name r_new_vartable LPAREN PARAMETROS RPAREN VARS BLOQUE r_end_function FUNCTION 
                | EMPTY'''
    pass

def p_TIPO_FUNC(p):
    '''TIPO_FUNC : INT r_set_fun_type
                | FLOAT r_set_fun_type
                | CHAR r_set_fun_type
                | VOID r_set_fun_type'''
    pass

def p_PARAMETROS(p):
    '''PARAMETROS : AUX_PARAM
                | EMPTY'''
    pass

def p_AUX_PARAM(p):
    '''AUX_PARAM : INT r_set_var_type r_insert_type ID r_new_variable NEXT_PARAM
                | FLOAT r_set_var_type  r_insert_type ID r_new_variable NEXT_PARAM
                | CHAR r_set_var_type r_insert_type ID r_new_variable NEXT_PARAM'''
    pass

def p_NEXT_PARAM(p):
    '''NEXT_PARAM : COMMA AUX_PARAM
                    | EMPTY '''

#CICLO DESDE
#TODO
def p_DESDE_CICLO(p):
    '''DESDE_CICLO : DESDE ID r_new_id_for EQ r_new_operator CTE_I r_new_constant r_new_equal HASTA CTE_I r_new_constant r_new_migajita r_compara_for HACER r_new_gotof BLOQUE r_update_for r_new_goto r_complete_gotof r_clear_for'''
    pass

#CICLO MIENTRAS
def p_MIENTRAS_CICLO(p):
    '''MIENTRAS_CICLO : MIENTRAS r_new_migajita LPAREN EXPRESION RPAREN r_new_gotof HAZ BLOQUE r_new_goto r_complete_gotof'''
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
def p_IF_STMT(p):
    '''IF_STMT : SI LPAREN EXPRESION RPAREN r_new_gotof ENTONCES BLOQUE r_complete_gotof'''
    pass

#ESTATUTO IF ELSE
def p_IF_ELSE_STMT(p):
    'IF_ELSE_STMT : SI LPAREN EXPRESION RPAREN r_new_gotof ENTONCES BLOQUE r_new_goto r_complete_gotof SINO BLOQUE r_complete_goto'
    pass

#ASIGNACION
def p_ASIGNACION(p):
    '''ASIGNACION : EXPRESION ASIGNACION_AUX r_new_equal'''
    pass

def p_ASIGNACION_AUX(p):
    '''ASIGNACION_AUX : EQ r_new_operator ASIGNACION
                    | EMPTY
    '''


# =====================================================================
# --------------- PUNTOS NEURALGICOS LINEALES ----------------
# =====================================================================
def p_r_new_id(p):
    'r_new_id : '
    stacks.register_operand(p[-1])

def p_r_new_constant(p):
    'r_new_constant : '
    stacks.register_operand(p[-1])
    stacks.operandStack

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

def p_r_new_equal(p):
    'r_new_equal : '
    if stacks.top_operators() in ['=']:
        stacks.generate_asignation()

# =====================================================================
# --------------- PUNTOS NEURALGICOS NO LINEALES ----------------
# =====================================================================

def p_r_new_goto(p):
    'r_new_goto : '
    stacks.generate_jump("GOTO")

def p_r_complete_goto(p):
    'r_complete_goto : '
    stacks.complete_jump("GOTO")

def p_r_new_gotof(p):
    'r_new_gotof : '
    stacks.generate_jump("GOTOF")

def p_r_complete_gotof(p):
    'r_complete_gotof : '
    stacks.complete_jump("GOTOF")

def p_r_new_migajita(p):
    'r_new_migajita : '
    stacks.new_migajita("GOTO")

def p_r_new_id_for(p):
    'r_new_id_for : '
    stacks.register_operand(p[-1])
    global for_var
    for_var = p[-1]

def p_r_compara_for(p):
    'r_compara_for : '
    stacks.operatorStack.append('<=')
    stacks.generate_quadruple()

def p_r_update_for(p):
    'r_update_for : '
    global for_var
    stacks.operandStack.append(for_var)
    stacks.operandStack.append('1')
    stacks.operatorStack.append('+')
    stacks.operandStack.append(for_var)
    stacks.generate_quadruple()
    stacks.operatorStack.append('=')
    stacks.generate_asignation()

def p_r_clear_for(p):
    'r_clear_for : '
    stacks.operandStack.pop()


# =====================================================================
# --------------- PUNTOS NEURALGICOS FUNCIONES  ----------------
# =====================================================================

def p_r_new_function(p):
    'r_new_function : '
    stacks.update_fun_address()
    #Create a new parameter array to store param types
    parameters = []
    stacks.updateFunction('parameters', parameters)

#Neurlagic point to insert the type to the parameter table
def p_r_insert_type(p):
    'r_insert_type : '
    stacks.insert_type()

def p_r_set_fun_type(p):
    'r_set_fun_type : '
    stacks.updateFunction('varType',p[-1])

def p_r_set_fun_name(p):
    'r_set_fun_name : '
    stacks.updateFunction('name',p[-1])

def p_r_new_vartable(p):
    'r_new_vartable : '
    stacks.flush_var_table()

def p_r_end_function(p):
    'r_end_function : '
    #Insert the number of variables and parameters into the function table
    stacks.insert_number_param()
    stacks.insert_number_variables()
    #DEBUGN 
    stacks.display_var_table('local')
    stacks.insertToFunTable()
    stacks.add_fun_quadruple()
    stacks.flushFunctionTable()

# =====================================================================
# --------------- PUNTOS NEURALGICOS VARIABLES  ----------------
# =====================================================================

def p_r_set_var_type(p):
    'r_set_var_type : '
    stacks.set_var_type(p[-1])
def p_r_new_variable(p):
    'r_new_variable : '
    if not stacks.insert_variable(p[-1]):
        print("Error: variable already exists")
def p_r_change_local_context(p):
    'r_change_local_context : '
    stacks.change_context('local')
def p_r_change_global_context(p):
    'r_change_global_context : '
    stacks.change_context('global')
def p_r_display_var_table(p):
    'r_display_var_table : '
    stacks.display_var_table('global')
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
    funcion void prueba(int y, float x)
    var 
        int i;
    {
        i = j + 1;
        si ( a > b ) entonces {
            a = a+1;
            b = (10 + 15) * 7;
        } sino {
            b = 1 +1;
        }
    }
    funcion int patito(int x1)
    var
        float x;
        int y;
        char e;
    {
        x = 1 + 1;
    }
    principal(){
        si ( a > b ) entonces {
            a = a+1;
            b = (10 + 15) * 7;
        } sino {
            b = 1 +1;
        }
        a =  b = 1 + id2 * (10 * (id1 + 55)) * id3;
        mientras (a > b) haz{
            a = a + 1;
        }
        mientras ( c > a) haz{
            a = 2 + 1;
        }
        a = 2;

        desde i = 0 hasta 9 hacer{
            a = 10;
        }

        a = 12;
    }
'''

parser.parse(testScript)
#printTable()
stacks.quadruples.display_quadruples()
stacks.funcTable.display_fun_table()

