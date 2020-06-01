from data_structures import Virtualmemory
import numpy as np
from pandas import DataFrame
import json
import sys

class Operations:
    def __init__(self):
        self.virtual_memory = Virtualmemory()
        self.jump_stack = []
        self.mat_stack = []

    def load_constants(self, constants):
        for i in constants:
            constant = json.loads(i)
            self.virtual_memory.update_memory(
                constant['v_address'],
                constant['constant']
            )

    def asignation(self,quadruple):
        l_operand = quadruple['l_operand']
        result = quadruple['result']
        #Check if the result is a pointer
        if self.virtual_memory.is_pointer(result):
            result = self.virtual_memory.is_pointer(result)
        self.virtual_memory.update_memory(
            result,
            self.virtual_memory.get_value(l_operand)
        )

    def write(self, quadruple):
        value = self.virtual_memory.get_value(
            quadruple['result']
        )
        print(value)

    def lee(self, quadruple):
        value = input()
        try:
            val = int(value)
        except ValueError:
            try:
                val = float(value)
            except ValueError:
                val = value
        result = quadruple['result']
        if self.virtual_memory.is_pointer(result):
            result = self.virtual_memory.is_pointer(result)
        self.virtual_memory.update_memory(
            result,
            val
        )

    def goto(self, quadruple):
        return quadruple['result']

    def goto_false(self, quadruple):
        #Check if the operand is false
        if not self.virtual_memory.get_value(quadruple['l_operand']):
            return quadruple['result']
        return None

    def plus_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand + r_operand
        )
        return None

    def minus_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand - r_operand
        )
        return None

    def mult_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand * r_operand
        )
        return None

    def div_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand / r_operand
        )
        return None

    def eq_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand == r_operand
        )
        return None


    def and_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand and r_operand
        )
        return None

    def not_eq_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand != r_operand
        )
        return None

    def greater_eq_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand >= r_operand
        )
        return None

    def less_qp_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand <= r_operand
        )
        return None

    def greater_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand > r_operand
        )
        return None

    def less_op(self, quadruple):
        l_operand = self.virtual_memory.get_value(quadruple['l_operand'])
        r_operand = self.virtual_memory.get_value(quadruple['r_operand'])
        self.virtual_memory.update_memory(
            quadruple['result'],
            l_operand < r_operand
        )
        return None


    def ver(self, quadruple):
        array_index = self.virtual_memory.get_value(quadruple['l_operand'])
        array_llimit = self.virtual_memory.get_value(quadruple['r_operand'])
        array_ulimit = self.virtual_memory.get_value(quadruple['result'])
        #Check the limits
        if(array_index < array_llimit or array_index >= array_ulimit):
            print("Runtime Error: Array out of bounds")
            sys.exit()

    def ebdoroc(self, quadruple):
        #Return tu previos state
        previos_state = self.jump_stack.pop() + 1
        #restore local memory
        self.virtual_memory.restore_local_memory()
        return previos_state

    def eka(self, quadruple):
        self.virtual_memory.new_local_memory()
        return None

    def param(self, quadruple):
        self.virtual_memory.insert_param(
            self.virtual_memory.get_value(quadruple['l_operand'])
        )
        return None
    
    def gosub(self, quadruple):
        self.virtual_memory.save_local_memory()
        self.virtual_memory.update_local_memory()
        self.jump_stack.append(quadruple['quadruple_no'])
        return quadruple['result']

    def return_val(self, qudaruple):
        self.virtual_memory.update_memory(
            qudaruple['l_operand'],
            self.virtual_memory.get_value(qudaruple['result'])
        )
        return None

    def create_matrix(self, quadruple):
        start_vaddr = quadruple['l_operand']
        dimensions = quadruple['result']
        new_matrix = []
        #For to iterate thru memory and load the matrix
        for i in range(0, dimensions[0]):
            row = []
            for j in range(0, dimensions[1]):
                row.append(self.virtual_memory.get_value(start_vaddr))
                start_vaddr += 1
            new_matrix.append(row)
        #add matrix to stack
        self.mat_stack.append(new_matrix)


    def determinant(self, quadruple):
        #get the matrix
        matrix = np.array(self.mat_stack.pop())
        result = quadruple['result']
        #Calculate the determinant and insert it into memory
        self.virtual_memory.update_memory(
            result,
            np.linalg.det(matrix)
        )
    
    def inverse(self, quadruple):
        #get the matrix
        matrix = np.array(self.mat_stack.pop())
        result_start = quadruple['l_operand']
        matrix = np.linalg.inv(matrix)
        for ix, iy in np.ndindex(matrix.shape):
            self.virtual_memory.update_memory(
                result_start,
                matrix[ix][iy]
            )
            result_start += 1
    
    def transpose(self, quadruple):
        #get the matrix
        matrix = np.array(self.mat_stack.pop())
        result_start = quadruple['l_operand']
        matrix = matrix.transpose()
        for ix, iy in np.ndindex(matrix.shape):
            self.virtual_memory.update_memory(
                result_start,
                matrix[ix][iy]
            )
            result_start += 1
    
    def plus_op_arr(self,quadruple):
        #Get the operands and convert them into a Numpy matrix
        r_operand = np.array(self.mat_stack.pop())
        l_operand = np.array(self.mat_stack.pop())
        result_vaddr = quadruple['result']
        result_mat = l_operand + r_operand
        #Update virtual memory with result
        for ix,iy in np.ndindex(result_mat.shape):
            self.virtual_memory.update_memory(
                result_vaddr,
                result_mat[ix][iy]
            )
            result_vaddr += 1

    def minus_op_arr(self, quadruple):
        #Get the operands and convert them into a Numpy matrix
        r_operand = np.array(self.mat_stack.pop())
        l_operand = np.array(self.mat_stack.pop())
        result_vaddr = quadruple['result']
        result_mat = l_operand - r_operand
        #Update virtual memory with result
        for ix,iy in np.ndindex(result_mat.shape):
            self.virtual_memory.update_memory(
                result_vaddr,
                result_mat[ix][iy]
            )
            result_vaddr += 1
    
    def mult_op_arr(self, quadruple):
        #Get the operands and convert them into a Numpy matrix
        r_operand = np.array(self.mat_stack.pop())
        l_operand = np.array(self.mat_stack.pop())
        result_vaddr = quadruple['result']
        result_mat = l_operand.dot(r_operand)
        #Update virtual memory with result
        for ix,iy in np.ndindex(result_mat.shape):
            self.virtual_memory.update_memory(
                result_vaddr,
                result_mat[ix][iy]
            )
            result_vaddr += 1

    def write_mat(self, quadruple):
        #get the dimensions
        dims = quadruple['result']
        start_vaddr = dims['start_address']
        #create the matrix
        new_matrix = []
        #For to iterate thru memory and load the matrix
        for i in range(0, dims['row']):
            row = []
            for j in range(0, dims['col']):
                row.append(self.virtual_memory.get_value(start_vaddr))
                start_vaddr += 1
            new_matrix.append(row)
        #display
        print(DataFrame(new_matrix))

