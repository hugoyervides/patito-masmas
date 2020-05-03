# Class Quadruples
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Moreno - A0138
# Patito ++
class Quadruples:
    def __init__(self):
        #Variables
        self.quadruples = []
    #Methods
    def add_quadruple(self, operator, l_operand, r_operand, result):
        self.quadruples.append({
            'operator': operator,
            'l_operand': l_operand,
            'r_operand': r_operand,
            'result': result
        })
    
    def display_quadruples(self):
        for quadruple in self.quadruples:
            print(quadruple)