#Patito Virtual Machine
from handlers import Operations
import json
import sys

operations = Operations()
quadruples = []
quad_counter = 0

op_list = {
    "GOTO" :    operations.goto,
    "GOTOF" :   operations.goto_false,
    "+" :       operations.plus_op,
    "-" :       operations.minus_op,
    "*" :       operations.mult_op,
    "/" :       operations.div_op,
    "==" :      operations.eq_op,
    "&&" :      operations.and_op,
    "!=" :      operations.not_eq_op,
    ">=" :      operations.greater_eq_op,
    "<=" :      operations.less_qp_op,
    ">" :       operations.greater_op,
    "<" :       operations.less_op,
    "=" :       operations.asignation,
    'WRITE':    operations.write,
    'EBDOROC':  operations.ebdoroc,
    'EKA':      operations.eka,
    'PARAM':    operations.param,
    'GOSUB':    operations.gosub,
    'RETURN':   operations.return_val,
    'READ' :     operations.lee
    'VER':      operations.ver
}

def main():
    global quad_counter
    #Check if we have parameters
    if(len(sys.argv) == 2):
        try:
            file = open(sys.argv[1], 'r')
            file_constants = open('c_' + sys.argv[1], 'r')
        except:
            print('File ' + str(sys.argv[1]) + ' not found')
            sys.exit()
        lines = file.readlines()
        constant_lines = file_constants.readlines()
        file_constants.close()
        file.close()
    else:
        print('Missing parameter') 
        sys.exit()

    #Insert quadruples into stack
    for line in lines:
        #Convert to JSON
        line = json.loads(line)
        quadruples.append(line)

    #Dump constants in memory
    operations.load_constants(constant_lines)

    while quad_counter < len(quadruples):
        #get the current operation
        new_quad_number = op_list[quadruples[quad_counter]['operator']](quadruples[quad_counter])
        if new_quad_number:
            quad_counter = new_quad_number
        else:
            quad_counter += 1
main()