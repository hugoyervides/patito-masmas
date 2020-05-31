# Stacks class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900

#This class is used to handle all the stack operations used during the semantics
#Operator Stack, Operand Stack, Type Stack, jump_stack, Migajitas and quadruples

#Add the necesary datastructures
from data_structures import Quadruples
from data_structures import cubo_semantico

class Stacks:
    def __init__(self):
        self.operator_stack = [] #Used to store the operators
        self.operand_stack = []  #Used to store the operands
        self.type_stack = [] #Used to store the type of the operands (Size must match with the operand_stack)
        self.array_stack = [] #Used to store the arrays we are currently working in
        self.jump_stack = { #Used to save pending jumps if we have a GOTO or GOTOF
            'GOTOF' :   [],
            'GOTO' :    []
        } 
        self.migajitas = { #Used to save where the start address of a loop is 
            'GOTOF' :   [],
            'GOTO' :    []
        }
        self.return_stack = [] #Used for pending return Jumps
        self.quadruples = Quadruples() 
        self.result_counter = 0
        self.temp_mem = 20000
        self.pointer_mem = 30000

    #Method to get an operand with its type
    def pop_operand(self):
        operand = self.operand_stack.pop()
        operand_type = self.type_stack.pop()
        return operand, operand_type

    #Method to register a new oeprator into our stackl
    def register_operator(self, operator):
        self.operator_stack.append(operator)

    #Method to register a new operand into our stack
    def register_operand(self, variable):
        self.operand_stack.append(variable)

    #Method to register a new type into our stack
    def register_type(self, variable):
        self.type_stack.append(variable)

    #Method to register a new $ into the operator stack
    #Used to separate the operators of a expresion inside a () )
    def register_separator(self):
        self.operator_stack.append('$')

    #Method to eliminate the $ if it exists in top of the operator stack
    #When we are done evaluating our expresion inside the () )
    def pop_separator(self):
        e = None
        if self.operator_stack[-1] == '$':
            self.operator_stack.pop()
        else:
            e = "Invalid expresion"
        return e

    #Method to get the top of the operators (Used to for neuralgic points)
    def top_operators(self):
        if len(self.operator_stack) > 0 and self.operand_stack[-1] != '$':
            return self.operator_stack[-1]
        else:
            return None

    #Method to get the top operand (Currently not used but may be helpful in the future >:D )
    def top_operand(self):
        if len(self.operand_stack) > 0:
            return self.operand_stack[-1]
        else:
            return None

    def top_types(self):
        if len(self.type_stack) > 0:
            return self.type_stack[-1]
        else:
            return None

    #Method to get a new temporal value name
    def get_result_var(self):
        result = self.temp_mem
        self.temp_mem += 1
        return result
    
    def get_pointer_mem(self):
        result = self.pointer_mem
        self.pointer_mem += 1
        return result

    #The name of this method is really obvious but will it generates a new quadruple when we reach certain neuralgic point
    def generate_quadruple(self):
        e = None
        #Get the right operand and type
        r_operand = self.operand_stack.pop()
        r_type = self.type_stack.pop()
        #Get the left operand and type
        l_operand = self.operand_stack.pop()
        l_type = self.type_stack.pop()
        #Get the operator
        operator = self.operator_stack.pop()
        result = self.get_result_var()
        #Verify with semantics
        type_quad = cubo_semantico[r_type][l_type][operator]
        if(type_quad != 'Error'):
            self.operand_stack.append(result)
            self.type_stack.append(type_quad)
            self.quadruples.add_quadruple(operator,l_operand,r_operand,result)
        else:
            e = "Operation " + str(l_type) + ' ' + str(operator) + ' ' + str(r_type) + " not posible!"
        return e
            

    #This does the same as the previus method but formats the quadruple for asignation ( = NEW_VALUE NULL RESULT)
    def generate_asignation(self):
        e = None
        #Get the right operand and type
        r_operand = self.operand_stack.pop()
        r_type = self.type_stack.pop()
        #get where are we going to save the result and type
        result = self.operand_stack.pop()
        result_type = self.type_stack.pop()
        operator = self.operator_stack.pop()
        #Verify semantics
        type_quad = cubo_semantico[result_type][r_type][operator]
        if(type_quad != 'Error'):
            self.operand_stack.append(result)
            self.type_stack.append(result_type)
            self.quadruples.add_quadruple(operator,r_operand, None, result)
        else:
            e = "Canot asign " + str(r_type) + ' to ' + str(result_type) + '!'
        return e
    
    def generate_param_quadruple(self, param_number):
        #Get the right operand and type
        operand = self.operand_stack.pop()
        #Pop the type (we wont need it)
        self.type_stack.pop()
        #Generate the cuadruple
        self.quadruples.add_quadruple("PARAM", operand, None, "PARAM" + str(param_number))

    def generate_gosub_quadruple(self, function, vaddr):
        self.quadruples.add_quadruple("GOSUB", None, None, function['quadrupleAddress'])
        #Check if the function has a return value
        if function['returnType'] != 'void':
            #Add a tep value to store the function return
            self.operand_stack.append(self.get_result_var())
            self.type_stack.append(function['returnType'])
            #Add a equal to store the return value
            self.operand_stack.append(vaddr)
            self.type_stack.append(function['returnType'])
            self.operator_stack.append('=')
            self.generate_asignation()

    def generate_eka_quadruple(self, function_name):
        self.quadruples.add_quadruple("EKA", None, None, function_name)

    def generate_return_quadruple(self, function_type, return_address):
        e = None
        operand = self.operand_stack.pop()
        operand_type = self.type_stack.pop()
        if (operand_type != function_type):
            e = "Function return type missmatch"
        self.quadruples.add_quadruple("RETURN", return_address, None, operand)
        return e

    #Method for read quadruple generation
    def generate_read_quadruple(self):
        operand = self.operand_stack.pop()
        _ = self.type_stack.pop()
        #Generate quadruple
        self.quadruples.add_quadruple("READ", None, None, operand)

    #Method for escribir quadruple generation
    def generate_write_quadruple(self):
        operand = self.operand_stack.pop()
        _ = self.type_stack.pop()
        self.quadruples.add_quadruple("WRITE", None, None, operand)

    #Method to generate a Goto quadruple
    def generate_jump(self, jumpType):
        e = None
        variable = None
        jumpTo = None
        if len(self.migajitas[jumpType]) > 0:
            jumpTo = self.migajitas[jumpType].pop()
        else:
            self.jump_stack[jumpType].append(len(self.quadruples.quadruples))
        if jumpType != 'GOTO':
            variable = self.operand_stack.pop()
            variable_type = self.type_stack.pop()
            if variable_type != 'bool':
                e = "Expresion is not a boolean!"
        self.quadruples.add_quadruple(jumpType, variable, None, jumpTo)
        return e

    #Method to complete a goto
    def complete_jump(self, jumpType):
        address = self.jump_stack[jumpType].pop()
        jumpAddress = len(self.quadruples.quadruples)
        jumpType = self.quadruples.quadruples[address]["operator"]
        jumpVariable = self.quadruples.quadruples[address]["l_operand"]
        self.quadruples.update_quadruple(address, jumpType, jumpVariable, None, jumpAddress)
    
    #Method to leve migajita de pan
    def new_migajita(self, jumpType):
        self.migajitas[jumpType].append(len(self.quadruples.quadruples))

    #Method to add the end function to que quadruples
    def add_fun_quadruple(self):
        self.quadruples.add_quadruple('EBDOROC', None, None, None)

    #Method the get the current quadruple address
    def current_quadruple_address(self):
        return len(self.quadruples.quadruples) - 1 
    
    #flushes temp memory
    def flush_temp_mem(self):
        self.temp_mem = 20000

    def flush_pointer_mem(self):
        self.temp_mem = 30000

    #Updates for Value
    def update_for(self, lAddress, cAddress):
        self.register_operand(lAddress)
        self.register_type('int')
        self.register_operand(cAddress)
        self.register_type('int')
        self.register_operator('+')
        self.register_operand(lAddress)
        self.generate_quadruple()
        self.register_operator('=')
        self.register_type('int')
        self.generate_asignation()

    #Method to generate a new goto for a return statment 
    def generate_return_jump(self):
        self.return_stack.append(len(self.quadruples.quadruples))
        self.quadruples.add_quadruple('GOTO', None, None, None)

    #Method to complete a return goto
    def complete_return_jump(self):
        #Function ends, complete all returns goto in stack
        while len(self.return_stack) > 0:
            address = self.return_stack.pop()
            jumpAddress = len(self.quadruples.quadruples)
            self.quadruples.update_quadruple(address, 'GOTO', None, None, jumpAddress)

    def register_arr(self, name):
        self.array_stack.append(name)

    def pop_array(self):
        e = None
        #Check the len
        if len(self.array_stack) > 0:
            return self.array_stack.pop(), e
        else:
            e = "Invalid array expresion"
        return None, e
    
    def generate_arr(self ,l_limit ,limit, vaddr, arr_type):
        e = None
        pointer = None
        #Get the indexes
        if len(limit) == 1:
            #Get the operand from the stack
            operand_dim = self.operand_stack.pop()
            dim_type = self.type_stack.pop()
            #Check if the dim type is int
            if dim_type == 'int' or dim_type == 'int_arr':
                self.quadruples.add_quadruple('VER', operand_dim, l_limit, limit[0]['u_limit_constant'])
                pointer = self.get_pointer_mem()
                self.quadruples.add_quadruple('+', operand_dim, vaddr, pointer)
            else:
                e = "Cant use " + str(dim_type) + " as array index"
        elif len(limit) == 2:
            #get the operands
            operand_second_dim = self.operand_stack.pop()
            operand_first_dim = self.operand_stack.pop()
            second_dim_type = self.type_stack.pop()
            first_dim_type = self.type_stack.pop()
            #Check if the dims are int
            if ((second_dim_type == 'int' or second_dim_type == 'int_arr') and (first_dim_type == 'int' or first_dim_type == 'int_arr')):
                self.quadruples.add_quadruple('VER', operand_first_dim, l_limit, limit[0]['u_limit_constant'])
                temp = self.get_result_var()
                self.quadruples.add_quadruple('*', operand_first_dim, limit[0]['u_limit_constant'], temp)
                self.operand_stack.append(temp)
                self.type_stack.append('int')
                self.quadruples.add_quadruple('VER', operand_second_dim, l_limit, limit[1]['u_limit_constant'])
                temp = self.get_result_var()
                self.quadruples.add_quadruple('+', self.operand_stack.pop(), operand_second_dim, temp)
                _ = self.type_stack.pop()
                self.operand_stack.append(temp)
                self.type_stack.append('int')
                pointer = self.get_pointer_mem()
                self.quadruples.add_quadruple('+', temp, vaddr, pointer)
            else:
                e = "Cant use " + str(first_dim_type) + " and " + str(second_dim_type) + " as array index"
        #insert the pointer and the type into the operand stack
        self.operand_stack.append(pointer)
        self.type_stack.append(arr_type)
        return e
    
    #Method to check if the top two operands are arrays
    def check_array_operation(self):
        #Check the size of the type stack        
        if (len(self.type_stack) < 2):
            return False
        if self.type_stack[-1] == 'int_arr' and self.type_stack[-2] == 'int_arr':
            return [self.operand_stack[-2], self.operand_stack[-1]]
        return False
    
    def get_dimensions(self, operand):
        #calculate the dimensions and addresses
        dim={
            'row':              1 if len(operand['dims']) == 1 else operand['dims'][1]['u_limit'], #if the len of the dimensions is 1 then is a array and the row is 1
            'col':              operand['dims'][0]['u_limit'], #Column of first matrix
            'start_address':    operand['mem_address'],
            'end_address':      None
        } 
        #calculate the end address
        if(len(operand['dims']) == 1): #Its an array, end_address = start_address + col - 1
            dim['end_address'] = dim['start_address'] + dim['col'] - 1
        else: #Its a Matrix, end_address = col x row - 1
            dim['end_address'] = dim['start_address'] + dim['col'] * dim['row'] - 1
        return dim

    #Method to handle array asignations
    def array_assignation(self):
        e = None
        r_operand = self.operand_stack.pop()
        l_operand = self.operand_stack.pop()
        _ = self.type_stack.pop()
        _ = self.type_stack.pop()
        operation = self.operator_stack.pop()
        #Get dimensions
        dim1 = self.get_dimensions(l_operand)
        dim2 = self.get_dimensions(r_operand)
        #Check if they are equal
        if(dim1['col'] == dim2['col'] and dim1['row'] == dim2['col']):
            #For loop to generate asignations
            first_start = dim1['start_address']
            second_start = dim2['start_address']
            while(first_start <= dim1['end_address']):
                self.quadruples.add_quadruple(
                    operation,
                    second_start,
                    None,
                    first_start
                )
                second_start += 1
                first_start += 1

        else:
            e = "Matrices must be the same size!"
        return e

    #Method to handle array operations
    def array_operation_quadruple(self):
        e = None #Error handling
        #Check the type of operation
        r_operand = self.operand_stack.pop()
        l_operand = self.operand_stack.pop()
        _ = self.type_stack.pop()
        _ = self.type_stack.pop()
        operation_type = self.operator_stack.pop()
        if not operation_type in ['*','+','-']:
            e = "Operation not posible"
            return e
        
        #Get dimensions
        dim1 = self.get_dimensions(l_operand)
        dim2 = self.get_dimensions(r_operand)
        #Check if the operation is posible in the first place
        if(operation_type == '*' and dim1['col'] != dim2['row']): #Number of colums must be the same as number of rows
            e = "Cannot * a matrix " + str(dim1['row']) + 'x' + str(dim1['col']) + " with a matrix " + str(dim2['row']) + 'x' + str(dim2['col'])
            return e
        if(operation_type in ['+','-'] and (dim1['col'] != dim2['col'] or dim1['row'] != dim2['row'])):
            e = "Cannot + , - a matrix " + str(dim1['row']) + 'x' + str(dim1['col']) + " with a matrix " + str(dim2['row']) + 'x' + str(dim2['col'])
            return e
        #Generate queadruples to let the VM know to create the matrix
        self.quadruples.add_quadruple(
            'CREATE_MATRIX',
            dim1['start_address'],
            dim1['end_address'],
            [dim1['row'], dim1['col']]
        )
        self.quadruples.add_quadruple(
            'CREATE_MATRIX',
            dim2['start_address'],
            dim2['end_address'],
            [dim2['row'], dim2['col']]
        )
        #Generate a temporal matrix in memory for future operations
        new_row = dim1['row']
        new_col = dim2['col']
        new_dims = []
        new_dims.append({
            'u_limit': new_col,
            'u_limit_constant' : None
        })
        if new_row != 1: #Its a matrix, add second dim
            new_dims.append({
                'u_limit': new_row,
                'u_limit_constant' : None
            })
        #Ask for temp memory
        temp_array_start = self.get_result_var()
        #Move temp memory to prevent collision
        self.temp_mem += new_row * new_col - 1
        #insert temporal array into operand stack
        self.operand_stack.append({
            'mem_address': temp_array_start,
            'dims': new_dims
        })
        self.type_stack.append('int_arr')
        #generate the quadruple for operation
        self.quadruples.add_quadruple(
            operation_type,
            'MAT1',
            'MAT2',
            temp_array_start
        )            
        return e

    def array_determinant(self):
        e = None
        arr_type = self.type_stack.pop()
        operand = self.operand_stack.pop()
        if arr_type != 'int_arr':
            e = "Cannot calculate determinant of " + arr_type
            return e
        #Get dimensions
        dim=self.get_dimensions(operand)
        #generate the quadruples
        self.quadruples.add_quadruple(
            'CREATE_MATRIX',
            dim['start_address'],
            dim['end_address'],
            [dim['row'], dim['col']]
        )  
        return_value = self.get_result_var()
        #generate quadruple
        self.quadruples.add_quadruple(
            'DETERMINANT',
            None,
            None,
            return_value
        )
        #Push the result into the stack
        self.type_stack.append('float')
        self.operand_stack.append(return_value)

    def array_transpuesta(self):
        e = None
        arr_type = self.type_stack.pop()
        operand = self.operand_stack.pop()
        if arr_type != 'int_arr':
            e = "Cannot calculate tranpose of " + arr_type
            return e
        #Get dimensions
        dim=self.get_dimensions(operand)
        #Load matrix into the virtual machine
        self.quadruples.add_quadruple(
            'CREATE_MATRIX',
            dim['start_address'],
            dim['end_address'],
            [dim['row'], dim['col']]
        )
        #Generate a temporal matrix in memory for future operations
        new_row = dim['row']
        new_col = dim['col']
        new_dims = []
        new_dims.append({
            'u_limit': new_col,
            'u_limit_constant' : None
        })
        if new_row != 1: #Its a matrix, add second dim
            new_dims.append({
                'u_limit': new_row,
                'u_limit_constant' : None
            })
        #Ask for temp memory
        temp_array_start = self.get_result_var()
        #Move temp memory to prevent collision
        self.temp_mem += new_row * new_col - 1
        #Inser the temporal into the operand stack
        self.operand_stack.append({
            'mem_address': temp_array_start,
            'dims': new_dims
        })
        self.type_stack.append('int_arr')
        #Generate quadruple
        self.quadruples.add_quadruple(
            'TRANSPOSE',
            temp_array_start,
            self.temp_mem,
            None
        )

    
    def array_inversa(self):
        e = None
        arr_type = self.type_stack.pop()
        operand = self.operand_stack.pop()
        if arr_type != 'int_arr':
            e = "Cannot calculate inverse of " + arr_type
            return e
        dim=self.get_dimensions(operand)
        #Load matrix into the virtual machine
        self.quadruples.add_quadruple(
            'CREATE_MATRIX',
            dim['start_address'],
            dim['end_address'],
            [dim['row'], dim['col']]
        )
        #Generate a temporal matrix in memory for future operations
        new_row = dim['row']
        new_col = dim['col']
        new_dims = []
        new_dims.append({
            'u_limit': new_col,
            'u_limit_constant' : None
        })
        if new_row != 1: #Its a matrix, add second dim
            new_dims.append({
                'u_limit': new_row,
                'u_limit_constant' : None
            })
        #Ask for temp memory
        temp_array_start = self.get_result_var()
        #Move temp memory to prevent collision
        self.temp_mem += new_row * new_col - 1
        #Inser the temporal into the operand stack
        self.operand_stack.append({
            'mem_address': temp_array_start,
            'dims': new_dims
        })
        self.type_stack.append('int_arr')
        #Generate quadruple
        self.quadruples.add_quadruple(
            'INVERSE',
            temp_array_start,
            self.temp_mem,
            None
        )
        