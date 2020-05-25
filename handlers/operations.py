from data_structures import Virtualmemory
import json

class Operations:
    def __init__(self):
        self.virtual_memory = Virtualmemory()
        self.jump_stack = []


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
        self.virtual_memory.update_memory(
            result,
            self.virtual_memory.get_value(l_operand)
        )

    def write(self, quadruple):
        value = self.virtual_memory.get_value(
            quadruple['result']
        )
        print(value)

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