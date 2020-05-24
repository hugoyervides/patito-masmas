from data_structures import Virtualmemory
import json

class Operations:
    def __init__(self):
        self.virtual_memory = Virtualmemory()

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
