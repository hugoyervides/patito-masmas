# Stacks class
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Morneo - A01382900
from quadruples import Quadruples

class Stacks:
    def __init__(self):
        self.operatorStack = []
        self.variableStack = []
        self.quadruples = Quadruples()
        self.resultCounter = 0
    
    def register_operator(self, operator):
        self.operatorStack.append(operator)

    def register_variable(self, variable):
        self.variableStack.append(variable)

    def top_operators(self):
        if len(self.operatorStack) > 0:
            return self.operatorStack[-1]
        else:
            raise Exception("Error, operator stack empty")

    def top_variables(self):
        if len(self.variableStack) > 0:
            return self.variableStack[-1]
        else:
            raise Exception("Error, variable stack empty")

    def get_result_var(self):
        result = 't' + str(self.resultCounter)
        self.resultCounter += 1
        return result

    def generate_quadruple(self):
        r_operand = self.variableStack.pop()
        l_operand = self.variableStack.pop()
        operator = self.operatorStack.pop()
        result = self.get_result_var()
        self.variableStack.append(result)
        self.quadruples.add_quadruple(operator,l_operand,r_operand,result)
