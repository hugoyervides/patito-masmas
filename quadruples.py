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
            'quadruple_no': len(self.quadruples),
            'operator': operator,
            'l_operand': l_operand,
            'r_operand': r_operand,
            'result': result
        })
    
    def display_quadruples(self):
        print("QN \t OP \t LOP \t ROP \t RES")
        for quadruple in self.quadruples:
            print(str(quadruple["quadruple_no"]) 
                + '\t' + str(quadruple["operator"])
                + '\t' + str(quadruple["l_operand"])
                + '\t' + str(quadruple["r_operand"])
                + '\t' + str(quadruple["result"]))
    
    def update_quadruple(self, address, operator, l_operand, r_operand, result):
        self.quadruples[address] = {
            'quadruple_no': self.quadruples[address]["quadruple_no"],
            'operator': operator,
            'l_operand': l_operand,
            'r_operand': r_operand,
            'result': result
        }