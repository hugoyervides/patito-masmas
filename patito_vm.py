#Patito Virtual Machine
import sys

def main():
    #Check if we have parameters
    if(len(sys.argv) == 2):
        try:
            file = open(sys.argv[1], 'r')
        except:
            print('File ' + str(sys.argv[1]) + ' not found')
            sys.exit()
        code = file.read()
        file.close()
    else:
        print('Missing parameter') 
        sys.exit()
    