import yacc
from scanner import tokens, reserved
from stacks import Stacks
from fun_table import Funtable
from semantic import cubo_semantico
from var_tables import Vartables
from fun_handler import Funhandler
from constant_table import Constanttable

#Variable declaration
stacks = Stacks()
funTable = Funtable()
var_tables = Vartables()
fun_handler = Funhandler()
constant_table = Constanttable()

#Cache variables
globalVarTable = Vartable()
tempVarTable = Vartable()

#Values for var table
context_func = 'global'
func_type = ''
dir_type = ''
dir_var = ''
for_stack = []


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
    '''MAIN : PRINCIPAL LPAREN RPAREN BLOQUE'''
    pass

def p_PROG(p):
    'PROG : r_new_goto PROGRAMA ID SEMI_COLON VARS r_change_local_context FUNCTION r_complete_goto r_change_global_context r_display_var_table MAIN r_display_const'
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
    '''CONSTANTE : CTE_I r_new_c_int
                | CTE_F r_new_c_float
                | CTE_C r_new_c_char
                | CTE_S r_new_c_string
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
    '''DESDE_CICLO : DESDE ID r_new_id_for EQ r_new_operator CTE_I r_new_c_int r_new_equal HASTA CTE_I r_new_c_int r_new_migajita r_compara_for HACER r_new_gotof BLOQUE r_update_for r_new_goto r_complete_gotof r_clear_for'''
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
    '''LLAMADA : ID r_verify_function r_generate_era LPAREN TIPO_PARAMETROS RPAREN r_verify_last_parameter r_generate_gosub'''
    pass

def p_TIPO_PARAMETROS(p):
    '''TIPO_PARAMETROS : TIPO_PARAMETROS_AUX
                        | EMPTY'''
    pass

def p_TIPO_PARAMETROS_AUX(p):
    '''TIPO_PARAMETROS_AUX : EXPRESION r_verify_parameter
                            | EXPRESION r_verify_parameter COMMA r_next_parameter TIPO_PARAMETROS_AUX
    '''
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

def p_r_new_c_int(p):
    'r_new_c_int : '
    v_add = constant_table.insert_constant(p[-1],'int')
    stacks.register_operand(v_add)

def p_r_new_c_char(p):
    'r_new_c_char : '
    v_add = constant_table.insert_constant(p[-1],'char')
    stacks.register_operand(v_add)

def p_r_new_c_float(p):
    'r_new_c_float : '
    v_add = constant_table.insert_constant(p[-1],'float')
    stacks.register_operand(v_add)

def p_r_new_c_string(p):
    'r_new_c_string : '
    v_add = constant_table.insert_constant(p[-1],'string')
    stacks.register_operand(v_add)

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
    global for_stack
    for_stack.append(p[-1])

def p_r_compara_for(p):
    'r_compara_for : '
    stacks.operator_stack.append('<=')
    stacks.generate_quadruple()

def p_r_update_for(p):
    'r_update_for : '
    global for_stack
    stacks.operand_stack.append(for_stack[len(for_stack) - 1])
    stacks.operand_stack.append('1')
    stacks.operator_stack.append('+')
    stacks.operand_stack.append(for_stack[len(for_stack) - 1])
    stacks.generate_quadruple()
    stacks.operator_stack.append('=')
    stacks.generate_asignation()

def p_r_clear_for(p):
    'r_clear_for : '
    global for_stack
    for_stack.pop()


# =====================================================================
# --------------- PUNTOS NEURALGICOS FUNCIONES  ----------------
# =====================================================================

def p_r_new_function(p):
    'r_new_function : '
    function_address = stacks.current_quadruple_address() + 1
    fun_handler.update_fun_address(function_address)
    #Create a new parameter array to store param types
    parameters = []
    fun_handler.updateFunction('parameters', parameters)

#Neurlagic point to insert the type to the parameter table
def p_r_insert_type(p):
    'r_insert_type : '
    fun_handler.insert_type(var_tables.current_type)

def p_r_set_fun_type(p):
    'r_set_fun_type : '
    fun_handler.updateFunction('varType',p[-1])

def p_r_set_fun_name(p):
    'r_set_fun_name : '
    fun_handler.updateFunction('name',p[-1])

def p_r_new_vartable(p):
    'r_new_vartable : '
    var_tables.flush_var_table('local')

def p_r_end_function(p):
    'r_end_function : '
    #Insert the number of variables and parameters into the function table
    fun_handler.insert_number_param()
    fun_handler.insert_number_variables(var_tables.local_var_table.size())
    #DEBUGN 
    var_tables.display_var_table('local')
    fun_handler.insertToFunTable()
    stacks.add_fun_quadruple() #TODO
    fun_handler.flushFunctionTable()

# =====================================================================
# --------------- PUNTOS NEURALGICOS LLAMADA FUNCIONES  ----------------
# =====================================================================
def p_r_verify_function(p):
    'r_verify_function : '
    if not fun_handler.check_function(p[-1]):
        print("Error: funtion does not exist")

def p_r_generate_era(p):
    'r_generate_era : '
    #TODO

def p_r_verify_parameter(p):
    'r_verify_parameter : '
    #TODO

def p_r_next_parameter(p):
    'r_next_parameter :'
    #TODO

def p_r_verify_last_parameter(p):
    'r_verify_last_parameter : '
    #TODO

def p_r_generate_gosub(p):
    'r_generate_gosub : '
    #TODO

# =====================================================================
# --------------- PUNTOS NEURALGICOS TABLA VARIABLES  ----------------
# =====================================================================

def p_r_set_var_type(p):
    'r_set_var_type : '
    var_tables.set_var_type(p[-1])

def p_r_new_variable(p):
    'r_new_variable : '
    if not var_tables.insert_variable(p[-1]):
        print("Error: variable already exists")

def p_r_change_local_context(p):
    'r_change_local_context : '
    var_tables.change_context('local')

def p_r_change_global_context(p):
    'r_change_global_context : '
    var_tables.change_context('global')

def p_r_display_var_table(p):
    'r_display_var_table : '
    var_tables.display_var_table('global')

def p_r_display_const(p):
    'r_display_const : '
    constant_table.display_table()


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
fun_handler.funcTable.display_fun_table()

