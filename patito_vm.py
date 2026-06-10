#Patito Virtual Machine
from handlers import Operations
import json
import sys
import os

operations = Operations()
quadruples = []
quad_counter = 0

op_list = {
    "GOTO" :            operations.goto,
    "GOTOF" :           operations.goto_false,
    "+" :               operations.plus_op,
    "-" :               operations.minus_op,
    "*" :               operations.mult_op,
    "/" :               operations.div_op,
    "==" :              operations.eq_op,
    "&&" :              operations.and_op,
    "||" :              operations.or_op,
    "!=" :              operations.not_eq_op,
    ">=" :              operations.greater_eq_op,
    "<=" :              operations.less_qp_op,
    ">" :               operations.greater_op,
    "<" :               operations.less_op,
    "=" :               operations.asignation,
    'WRITE':            operations.write,
    'VER':              operations.ver,
    'EBDOROC':          operations.ebdoroc,
    'EKA':              operations.eka,
    'PARAM':            operations.param,
    'GOSUB':            operations.gosub,
    'RETURN':           operations.return_val,
    'READ' :            operations.lee,
    'CREATE_MATRIX':    operations.create_matrix,
    'DETERMINANT':      operations.determinant,
    'INVERSE':          operations.inverse,
    'TRANSPOSE':        operations.transpose,
    "+_arr" :           operations.plus_op_arr,
    "-_arr" :           operations.minus_op_arr,
    "*_arr" :           operations.mult_op_arr,
    "WRITE_MAT":        operations.write_mat
}

#--- Debug mode (used by the web IDE live debugger) ---
#Usage: python patito_vm.py <file> --debug <event_fd> <command_fd>
#The VM emits JSON events (one per line) on event_fd and reads commands
#(step/continue/pause/quit) from command_fd, so the program's own
#stdin/stdout stay untouched for lee/escribe
DEBUG_RUN_DELAY = 0.025

def _plain(value):
    #Convert numpy scalars and other non JSON friendly values
    if hasattr(value, 'item'):
        try:
            return value.item()
        except (ValueError, TypeError):
            return str(value)
    if isinstance(value, (int, float, str, bool)) or value is None:
        return value
    return str(value)

def _memory_snapshot():
    snapshot = {}
    for segment, contents in operations.virtual_memory.memory.items():
        snapshot[segment] = {str(addr): _plain(val) for addr, val in contents.items()}
    return snapshot

def main():
    global quad_counter
    #Check if we have parameters
    debug = len(sys.argv) == 5 and sys.argv[2] == '--debug'
    if(len(sys.argv) == 2 or debug):
        try:
            file = open(sys.argv[1], 'r')
            file_constants = open('c_' + sys.argv[1], 'r')
        except:
            print('File ' + str(sys.argv[1]) + ' not found')
            sys.exit()
        lines = file.readlines()
        constant_lines = file_constants.readlines()
        file_constants.close()
        file.close()
    else:
        print('Missing parameter')
        sys.exit()

    #Insert quadruples into stack
    for line in lines:
        #Convert to JSON
        line = json.loads(line)
        quadruples.append(line)

    #Dump constants in memory
    operations.load_constants(constant_lines)

    if not debug:
        while quad_counter < len(quadruples):
            #get the current operation
            new_quad_number = op_list[quadruples[quad_counter]['operator']](quadruples[quad_counter])
            if new_quad_number:
                quad_counter = new_quad_number
            else:
                quad_counter += 1
        return

    #--- Debug execution loop ---
    import select
    import time

    event_pipe = os.fdopen(int(sys.argv[3]), 'w', buffering=1)
    command_pipe = os.fdopen(int(sys.argv[4]), 'r')

    def emit(event):
        try:
            event_pipe.write(json.dumps(event, default=str) + '\n')
        except (BrokenPipeError, ValueError):
            pass

    #Record which addresses each operation writes to
    written_addresses = []
    original_update = operations.virtual_memory.update_memory
    def traced_update(memory_dir, value):
        written_addresses.append(memory_dir)
        return original_update(memory_dir, value)
    operations.virtual_memory.update_memory = traced_update

    emit({'event': 'init', 'total': len(quadruples), 'memory': _memory_snapshot()})

    paused = True
    while quad_counter < len(quadruples):
        if paused:
            emit({'event': 'paused', 'quad': quad_counter})
            command = command_pipe.readline().strip()
            if command == '' or command == 'quit':
                break
            if command == 'continue':
                paused = False
            #'step' stays paused and executes exactly one quadruple
        else:
            #Throttle so the live view is followable, and poll for a pause
            time.sleep(DEBUG_RUN_DELAY)
            ready, _, _ = select.select([command_pipe], [], [], 0)
            if ready:
                command = command_pipe.readline().strip()
                if command == '' or command == 'quit':
                    break
                if command == 'pause':
                    paused = True
                    continue
        written_addresses.clear()
        current = quad_counter
        new_quad_number = op_list[quadruples[quad_counter]['operator']](quadruples[quad_counter])
        if new_quad_number:
            quad_counter = new_quad_number
        else:
            quad_counter += 1
        emit({
            'event': 'executed',
            'quad': current,
            'next': quad_counter,
            'writes': sorted(set(written_addresses)),
            'memory': _memory_snapshot(),
        })

main()
