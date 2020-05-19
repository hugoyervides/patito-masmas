#Constat table data structure used to store constants
# Victor Hugo Oyervides Covarrubias - A01382836
# Obed Gonzalez Moreno - A01382900

#This datastructure is used to store the constants in a table and generate its address

class Constanttable:
    def __init__(self):
        self.table = []
        self.start_address = 15001
    
    def insert_constant(self, constant, const_type):
        #Check if the constant already exists
        for i in self.table:
            if i['constant'] == constant:
                return i['v_address']
        new_constant = {
            'constant' :    constant,
            'type' :        const_type,
            'v_address' :   self.start_address
        }
        self.start_address += 1
        self.table.append(new_constant)
        return new_constant['v_address']

    def display_table(self):
        print("Displaying constant table")
        print("Cons \t Type \t Address")
        for i in self.table:
            print(
                str(i["constant"]) + '\t' +
                i["type"] + '\t' +
                str(i["v_address"])
            )