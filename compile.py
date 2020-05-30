from data_structures import Quadruples, Constanttable
from compiler import parser, final_quadruples, constant_table
from compiler import lexer
import json
import sys

def export_constants(file_name):
    output_file = open(file_name, "w")
    constants = constant_table.table
    for i in constants:
        #Convert to JSON and dump it into the file
        i = json.dumps(i)
        output_file.write(str(i) + '\n')

def export_quadruples(file_name):
    output_file = open(file_name, "w")
    quadruples = final_quadruples.quadruples
    for i in quadruples:
        #Convert to JSON and dump it into the file
        i = json.dumps(i)
        output_file.write(str(i) + '\n')

def main():
    #Check if we got the filename by argument
    if(len(sys.argv) == 3):
        try:
            file = open(sys.argv[1], "r")
        except:
            print('File ' + str(sys.argv[1]) + ' not found')
            sys.exit()
        code = file.read()
        file.close()
    else:
        print('Missing parameter') 
        sys.exit()
    #Parse
    parser.parse(code, tracking = True)
    #Save the quadruples in a file
    export_quadruples(sys.argv[2])
    export_constants('c_'+sys.argv[2])

main()