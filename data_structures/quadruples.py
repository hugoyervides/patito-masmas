# Class Quadruples
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Moreno - A0138
# Patito ++
class Quadruples:
    def __init__(self):
        #Variables
        self.quadruples = []
        #Lexer injected by the compiler so each quadruple can be stamped
        #with the source line it came from (used by the web IDE debugger)
        self.line_source = None
    #Methods
    def add_quadruple(self, operator, l_operand, r_operand, result):
        self.quadruples.append({
            'quadruple_no':     len(self.quadruples),
            'operator':         operator,
            'l_operand':        l_operand,
            'r_operand':        r_operand,
            'result':           result,
            'line':             self.line_source.lineno if self.line_source else None
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
            'result': result,
            #Backpatching a jump target must keep the original source line
            'line': self.quadruples[address].get("line")
        }