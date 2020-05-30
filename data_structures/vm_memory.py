#Virtual memory datastructure for virtual machine


class Virtualmemory:
    #Atribute declaration
    def __init__(self):
        self.memory = {
            'global' :      {}, #Space for global memory
            'constant' :    {}, #Space for constant memory
            'local':        {}, #Space for local memory
            'temporal':     {}, #Space for temporal memory
            'pointers':     {}
        }
        self.LIMITS = {
            'GLOBAL_LLIMIT' :    1000,
            'GLOBAL_ULIMIT' :    7999,
            'LOCAL_LLIMIT' :     8000,
            'LOCAL_ULIMIT' :     14999,
            'TEMPORAL_LLIMIT' :  20000,
            'TEMPORAL_ULIMIT' :  30000,
            'CONSTANT_LLIMIT' :  15000,
            'CONSTANT_ULIMIT' :  19999,
            'POINTERS_LLIMIT' :  30000,
            'POINTERS_ULIMIT' :  40000  
        }
    #Methods
    def check_address(self, vaddr, context):
        if vaddr in self.memory[context]:
            return self.memory[context][vaddr]
        else:
            return None
            
    def is_pointer(self,vaddr):
        if( vaddr >= self.LIMITS['POINTERS_LLIMIT'] and vaddr <= self.LIMITS['POINTERS_ULIMIT']):
            return self.check_address(vaddr,'pointers')
        else:
            return None

    def update_address(self, vaddr, context, value):
        self.memory[context][vaddr] = value

    def get_value(self, memory_dir):
        if( memory_dir >= self.LIMITS['GLOBAL_LLIMIT'] and memory_dir <= self.LIMITS['GLOBAL_ULIMIT']): #GLOBA MEMORY
            return self.check_address(memory_dir, 'global')
        if( memory_dir >= self.LIMITS['LOCAL_LLIMIT'] and memory_dir <= self.LIMITS['LOCAL_ULIMIT']):
            return self.check_address(memory_dir, 'local')
        if( memory_dir >= self.LIMITS['TEMPORAL_LLIMIT'] and memory_dir <= self.LIMITS['TEMPORAL_ULIMIT']):
            return self.check_address(memory_dir, 'temporal')
        if( memory_dir >= self.LIMITS['CONSTANT_LLIMIT'] and memory_dir <= self.LIMITS['CONSTANT_ULIMIT']):
            return self.check_address(memory_dir, 'constant')
        if( memory_dir >= self.LIMITS['POINTERS_LLIMIT'] and memory_dir <= self.LIMITS['POINTERS_ULIMIT']):
            return self.get_value(self.check_address(memory_dir, 'pointers'))
    
    def update_memory(self, memory_dir, value):
        if( memory_dir >= self.LIMITS['GLOBAL_LLIMIT'] and memory_dir <= self.LIMITS['GLOBAL_ULIMIT']): #GLOBA MEMORY
            self.update_address(memory_dir, 'global', value)
        if( memory_dir >= self.LIMITS['LOCAL_LLIMIT'] and memory_dir <= self.LIMITS['LOCAL_ULIMIT']):
            self.update_address(memory_dir, 'local', value)
        if( memory_dir >= self.LIMITS['TEMPORAL_LLIMIT'] and memory_dir <= self.LIMITS['TEMPORAL_ULIMIT']):
            self.update_address(memory_dir, 'temporal', value)
        if( memory_dir >= self.LIMITS['CONSTANT_LLIMIT'] and memory_dir <= self.LIMITS['CONSTANT_ULIMIT']):
            self.update_address(memory_dir, 'constant', value)
        if( memory_dir >= self.LIMITS['POINTERS_LLIMIT'] and memory_dir <= self.LIMITS['POINTERS_ULIMIT']):
            self.update_address(memory_dir, 'pointers', value)
