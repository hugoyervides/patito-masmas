from ply import yacc
from .scanner import tokens, reserved
from handlers import Stacks
from handlers import Vartables
from handlers import Funhandler
from data_structures import Constanttable
import sys


#Variable declaration
stacks = Stacks()
var_tables = Vartables()
fun_handler = Funhandler()
constant_table = Constanttable()
for_stack = []
final_quadruples = None
final_constants = None
start = 'PROG'

# =====================================================================
# ------------------- GRAMATICA PRINCIPAL ----------------------
# =====================================================================

def p_EMPTY(p):
    'EMPTY :'
    pass

def p_MAIN(p):
    '''MAIN : PRINCIPAL r_flush_mem LPAREN RPAREN BLOQUE'''
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
    '''LIST_ID : ID r_new_arr LSQ CTE_I r_new_dim RSQ r_generate_arr r_clear_arr
                | ID r_new_arr LSQ CTE_I r_new_dim RSQ LSQ CTE_I r_new_dim RSQ r_generate_arr r_clear_arr
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
                    | ARR
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
                    | RETURN_STM SEMI_COLON OPCION_BLOQUE
                    | EMPTY
    '''
    pass

# =====================================================================
# --------------- GRAMATICA PARA ELEMENTOS DEL BLOQUE ----------------
# =====================================================================

# FUNCIONES
def p_FUNCTION(p):
    '''FUNCTION : r_new_function FUNCION TIPO_FUNC r_clear_mem ID r_set_fun_name r_new_vartable LPAREN PARAMETROS RPAREN VARS r_insert_parameters BLOQUE r_end_function FUNCTION 
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

def p_ARR(p):
    '''ARR : ID r_register_arr LSQ r_new_lparen SLEVEL_EXPRESION r_new_rparen RSQ r_quad_arr
                | ID r_register_arr LSQ r_new_lparen SLEVEL_EXPRESION r_new_rparen RSQ LSQ r_new_lparen SLEVEL_EXPRESION r_new_rparen RSQ r_quad_arr
    '''
    pass

def p_AUX_PARAM(p):
    '''AUX_PARAM : INT r_set_var_type r_insert_type ID r_new_variable NEXT_PARAM
                | FLOAT r_set_var_type  r_insert_type ID r_new_variable NEXT_PARAM
                | CHAR r_set_var_type r_insert_type ID r_new_variable NEXT_PARAM'''
    pass

def p_NEXT_PARAM(p):
    '''NEXT_PARAM : COMMA AUX_PARAM
                    | EMPTY '''

def p_RETURN_STM(p):
    'RETURN_STM : RETURN LPAREN EXPRESION RPAREN r_generate_return'

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
    '''LECTURA : LEE LPAREN ID r_new_id r_new_read RPAREN'''
    pass

#ESCRITURA
def p_ESCRITURA(p):
    '''ESCRITURA : ESCRIBE LPAREN PARAMETRO_ESCRITURA RPAREN'''
    pass

def p_PARAMETRO_ESCRITURA(p):
    '''PARAMETRO_ESCRITURA : PARAMETRO_ESCRITURA_AUX
                            | EMPTY'''
    pass

def p_PARAMETRO_ESCRITURA_AUX(p):
    '''PARAMETRO_ESCRITURA_AUX : EXPRESION r_new_write
                                | EXPRESION r_new_write COMMA PARAMETRO_ESCRITURA_AUX'''

#LLAMADA
def p_LLAMADA(p):
    '''LLAMADA : ID r_verify_function r_generate_era LPAREN r_new_lparen TIPO_PARAMETROS r_new_rparen RPAREN r_verify_last_parameter r_generate_gosub'''
    pass

def p_TIPO_PARAMETROS(p):
    '''TIPO_PARAMETROS : TIPO_PARAMETROS_AUX
                        | EMPTY'''
    pass

def p_TIPO_PARAMETROS_AUX(p):
    '''TIPO_PARAMETROS_AUX : EXPRESION r_verify_parameter
                            | EXPRESION r_verify_parameter COMMA TIPO_PARAMETROS_AUX
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
# --------------- Error handler ----------------
# =====================================================================

def error_handler(line, error):
    print("Error in line", line, error)
    sys.exit()


def p_error(p):
    if p:
        print("Syntax error at line: ",p.lineno , p.type)
        sys.exit()
    
    else:
        print("Syntax error at EOF")
        sys.exit()


# =====================================================================
# --------------- PUNTOS NEURALGICOS LINEALES ----------------
# =====================================================================

def p_r_new_id(p):
    'r_new_id : '
    type_var = var_tables.get_var_type(p[-1])
    mem_address, e = var_tables.get_virtual_mem(p[-1])
    if e:
        error_handler(p.lineno(-1), e)
    stacks.register_operand(mem_address)
    type_var, e = var_tables.get_var_type(p[-1])
    if e:
        error_handler(p.lineno(-1),e)
    stacks.register_type(type_var)


def p_r_new_c_int(p):
    'r_new_c_int : '
    v_add = constant_table.insert_constant(p[-1],'int')
    stacks.register_operand(v_add)
    stacks.register_type('int')

def p_r_new_c_char(p):
    'r_new_c_char : '
    v_add = constant_table.insert_constant(p[-1],'char')
    stacks.register_operand(v_add)
    stacks.register_type('char')

def p_r_new_c_float(p):
    'r_new_c_float : '
    v_add = constant_table.insert_constant(p[-1],'float')
    stacks.register_operand(v_add)
    stacks.register_type('float')

def p_r_new_c_string(p):
    'r_new_c_string : '
    v_add = constant_table.insert_constant(p[-1],'string')
    stacks.register_operand(v_add)
    stacks.register_type('string')

def p_r_new_lparen(p):
    'r_new_lparen : '
    stacks.register_separator()

def p_r_new_rparen(p):
    'r_new_rparen : '
    e = stacks.pop_separator()
    if e:        
        error_handler(p.lineno(-1),e)

def p_r_new_operator(p):
    'r_new_operator : '
    stacks.register_operator(p[-1])    

def p_r_new_quadruple_flevel(p):
    'r_new_quadruple_flevel : '
    if stacks.top_operators() in ['*', '/']:
        e = stacks.generate_quadruple()
        if e:
            error_handler(p.lineno(-1),e)

def p_r_new_quadruple_slevel(p):
    'r_new_quadruple_slevel : '
    if stacks.top_operators() in ['+', '-']:
        e = stacks.generate_quadruple()
        if e:
            error_handler(p.lineno(-1),e)

def p_r_new_quadruple_tlevel(p):
    'r_new_quadruple_tlevel : '
    if stacks.top_operators() in ['!=', '>=', '<=', '>', '<']:
        e = stacks.generate_quadruple()
        if e:
            error_handler(p.lineno(-1),e)
    
def p_r_new_quadruple(p):
    'r_new_quadruple : '
    if stacks.top_operators() in ['==','&&','||']:
        e = stacks.generate_quadruple()
        if e:
            error_handler(p.lineno(-1),e)

def p_r_new_equal(p):
    'r_new_equal : '
    if stacks.top_operators() in ['=']:
        e = stacks.generate_asignation()
        if e:
            error_handler(p.lineno(-1), e)

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
    e = stacks.generate_jump("GOTOF")
    if e:
        error_handler(p.lineno(-1), e)

def p_r_complete_gotof(p):
    'r_complete_gotof : '
    stacks.complete_jump("GOTOF")

def p_r_new_migajita(p):
    'r_new_migajita : '
    stacks.new_migajita("GOTO")

def p_r_new_id_for(p):
    'r_new_id_for : '
    if(var_tables.get_var_type(p[-1]) == None):
        p_error(p)
    else:
        for_stack.append(p[-1])
        type_var = var_tables.get_var_type(p[-1])
        mem_address, e = var_tables.get_virtual_mem(p[-1])
        if e:
            error_handler(p.lineno(-1),e)
        stacks.register_operand(mem_address)
        type_var, e = var_tables.get_var_type(p[-1])
        if e:
            error_handler(p.lineno(-1),e)
        stacks.register_type(type_var)


    
def p_r_compara_for(p):
    'r_compara_for : '
    mem_address, e = var_tables.get_virtual_mem(for_stack[len(for_stack) - 1])
    if e:
        error_handler(p.lineno(-1), e)
    stacks.register_operand(mem_address)
    stacks.register_operator('>=')
    stacks.generate_quadruple()

def p_r_update_for(p):
    'r_update_for : '
    global for_stack
    mem_address, e = var_tables.get_virtual_mem(for_stack[len(for_stack) - 1])
    if e:
        error_handler(p.lineno(-1), e)
    stacks.update_for(mem_address, constant_table.insert_constant(1, 'int'))


def p_r_clear_for(p):
    'r_clear_for : '
    global for_stack
    for_stack.pop()


# =====================================================================
# --------------- PUNTOS NEURALGICOS FUNCIONES  ----------------
# =====================================================================

def p_r_clear_mem(p):
    'r_clear_mem : '
    var_tables.flush_local_mem()

def p_r_new_function(p):
    'r_new_function : '
    function_address = stacks.current_quadruple_address() + 1
    fun_handler.update_fun_address(function_address)
    #Create a new parameter array to store param types
    parameters = []
    fun_handler.updateFunction('parameters', parameters)
    stacks.flush_temp_mem()

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

def p_r_insert_parameters(p):
    'r_insert_parameters : '
    #Insert the number of variables and parameters into the function table
    fun_handler.insert_number_param()
    fun_handler.insert_number_variables(var_tables.local_var_table.size())
    #Insert to function table 
    e = fun_handler.insertToFunTable()
    if e:
        error_handler(p.lineno(-1), e)
    #Check if the function has a result and if it has a result put the variable into the global variable table
    if fun_handler.current_function['varType'] != 'void':
        var_tables.insert_function(
            fun_handler.current_function['name'],
            fun_handler.current_function['varType']
        )
    #DEBUGN 
    var_tables.display_var_table('local')

def p_r_end_function(p):
    'r_end_function : '
    fun_handler.flushFunctionTable()
    stacks.complete_return_jump()
    stacks.add_fun_quadruple()

def p_r_flush_mem(p):
    'r_flush_mem : '
    stacks.flush_temp_mem()

# =====================================================================
# --------------- PUNTOS NEURALGICOS LLAMADA FUNCIONES  ----------------
# =====================================================================
def p_r_verify_function(p):
    'r_verify_function : '
    e = fun_handler.check_function(p[-1])
    if e:
        error_handler(p.lineno(-1), e)
    #Load function parameters into stack
    _ , e = fun_handler.load_called_function(p[-1])
    if e:
        error_handler(p.lineno(-1), e)

def p_r_generate_era(p):
    'r_generate_era : '
    stacks.generate_eka_quadruple(fun_handler.called_function['name'])

def p_r_verify_parameter(p):
    'r_verify_parameter : '
    e = None
    operand_type = stacks.top_types()
    #Check if the type of the parameter matches
    e = fun_handler.check_param_type(operand_type)
    if e:
        error_handler(p.lineno(-1), e)
    #Generate the parameter cuadruple
    stacks.generate_param_quadruple(fun_handler.param_counter)

def p_r_verify_last_parameter(p):
    'r_verify_last_parameter : '
    e = None
    e = fun_handler.check_param_counter()
    if e:
        error_handler(p.lineno(-1), e)

def p_r_generate_gosub(p):
    'r_generate_gosub : '
    #get the funtion return virtual address if we need it
    #get virtual address
    vaddr, e = var_tables.get_var_vaddr(
        fun_handler.called_function['name']
    )
    stacks.generate_gosub_quadruple(fun_handler.called_function, vaddr)


def p_r_generate_return(p):
    'r_generate_return : '
    vaddr, e = var_tables.get_var_vaddr(
        fun_handler.current_function['name']
    )
    if e:
        error_handler(p.lineno(-1), e)
    e = stacks.generate_return_quadruple(fun_handler.current_function['varType'], vaddr)
    if e:
        error_handler(p.lineno(-1), e)
    stacks.generate_return_jump()


# =====================================================================
# --------------- PUNTOS NEURALGICOS TABLA VARIABLES  ----------------
# =====================================================================

def p_r_set_var_type(p):
    'r_set_var_type : '
    var_tables.set_var_type(p[-1])

def p_r_new_variable(p):
    'r_new_variable : '
    e = var_tables.insert_variable(p[-1], None)
    if e:
        error_handler(p.lineno(-1), e)

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

def p_r_new_arr(p):
    'r_new_arr : '
    arr_id = p[-1]
    var_tables.register_arr(arr_id)
    
def p_r_new_dim(p):
    'r_new_dim : '
    #print(p[-1])
    #get a new constant for the dimention upper limit
    dim = constant_table.insert_constant(p[-1], 'int')
    var_tables.register_dim({
        'u_limit':          p[-1],
        'u_limit_constant': dim
    })

def p_r_generate_arr(p):
    'r_generate_arr : '
    e = var_tables.generate_arr()
    if e:
        error_handler(p.lineno(-1), e)
    


def p_r_clear_arr(p):
    'r_clear_arr : '
    var_tables.flush_arr()


# =====================================================================
# --------------- PUNTOS NEURALGICOS I/O ----------------
# =====================================================================

def p_r_new_read(p):
    'r_new_read : '
    stacks.generate_read_quadruple()

def p_r_new_write(p):
    'r_new_write : '
    stacks.generate_write_quadruple()

# =====================================================================
# --------------- PUNTOS NEURALGICOS ARREGLOS ----------------
# =====================================================================

def p_r_register_arr(p):
    'r_register_arr : '
    #Register the array in the stack
    stacks.register_arr(p[-1])

def p_r_quad_arr(p):
    'r_quad_arr : '
    array_name, e = stacks.pop_array()
    if e:
        error_handler(p.lineno(-1), e)
    #define the limits of the array
    upper_limit = var_tables.get_dims(array_name)
    lower_limit = constant_table.insert_constant(0, 'int')
    #get array vaddr
    vaddr, e = var_tables.get_var_vaddr(array_name)
    if e:
        error_handler(p.lineno(-1), e)
    #get array type
    arr_type, e = var_tables.get_var_type(array_name)
    if e:
        error_handler(p.lineno(-1), e)
    #convert the virtual addres into a constant for the virtual machine evaluation
    vaddr_constant = constant_table.insert_constant(vaddr, 'int')
    #generate the quadruples
    e = stacks.generate_arr(lower_limit, upper_limit, vaddr_constant, arr_type)
    #handle type missmatch error
    if e:
        error_handler(p.lineno(-1), e)


#Export quadruples and constants
final_quadruples = stacks.quadruples

#Construct the parser
parser = yacc.yacc()

