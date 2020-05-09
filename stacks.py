# Stacks class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
from quadruples import Quadruples

class Stacks:
    def __init__(self):
        self.operatorStack = []
        self.operandStack = []
        self.quadruples = Quadruples()
        self.resultCounter = 0
    
    def register_operator(self, operator):
        self.operatorStack.append(operator)

    def register_operand(self, variable):
        self.operandStack.append(variable)

    def register_separator(self):
        self.operatorStack.append('$')

    def pop_separator(self):
        if self.operatorStack[-1] == '$':
            self.operatorStack.pop()
            return True
        else:
            return False

    def top_operators(self):
        if len(self.operatorStack) > 0 and self.operandStack[-1] != '$':
            return self.operatorStack[-1]
        else:
            return None

    def top_operand(self):
        if len(self.operandStack) > 0:
            return self.operandStack[-1]
        else:
            return None

    def get_result_var(self):
        result = 't' + str(self.resultCounter)
        self.resultCounter += 1
        return result

    def generate_quadruple(self):
        r_operand = self.operandStack.pop()
        l_operand = self.operandStack.pop()
        operator = self.operatorStack.pop()
        result = self.get_result_var()
        self.operandStack.append(result)
        self.quadruples.add_quadruple(operator,l_operand,r_operand,result)
