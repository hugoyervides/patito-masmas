from collections import defaultdict

cubo_semantico = defaultdict(
    lambda: defaultdict(lambda: defaultdict(lambda: None)))


#Mathematical operators
cubo_semantico['int']['int']['*']       = 'int'
cubo_semantico['int']['int']['/']       = 'float'
cubo_semantico['int']['int']['+']       = 'int'
cubo_semantico['int']['int']['-']       = 'int'

cubo_semantico['float']['float']['*']   = 'float'
cubo_semantico['float']['float']['/']   = 'float'
cubo_semantico['float']['float']['+']   = 'float'
cubo_semantico['float']['float']['-']   = 'float'

cubo_semantico['char']['char']['*']     = 'Error'
cubo_semantico['char']['char']['/']     = 'Error'
cubo_semantico['char']['char']['+']     = 'Error'
cubo_semantico['char']['char']['-']     = 'Error'

cubo_semantico['int']['float']['+'] = cubo_semantico['float']['int']['+'] = 'float'
cubo_semantico['int']['float']['-'] = cubo_semantico['float']['int']['-'] = 'float'
cubo_semantico['int']['float']['*'] = cubo_semantico['float']['int']['*'] = 'float'
cubo_semantico['int']['float']['/'] = cubo_semantico['float']['int']['/'] = 'float'

cubo_semantico['char']['int']['+'] = cubo_semantico['int']['char']['+']         = 'Error'
cubo_semantico['char']['float']['+'] = cubo_semantico['float']['char']['+']     = 'Error'
cubo_semantico['char']['int']['-'] = cubo_semantico['int']['char']['-']         = 'Error'
cubo_semantico['char']['float']['-'] = cubo_semantico['float']['char']['-']     = 'Error'
cubo_semantico['char']['int']['*'] = cubo_semantico['int']['char']['*']         = 'Error'
cubo_semantico['char']['float']['*'] = cubo_semantico['float']['char']['*']     = 'Error'
cubo_semantico['char']['int']['/'] = cubo_semantico['int']['char']['/']         = 'Error'
cubo_semantico['char']['float']['/'] = cubo_semantico['float']['char']['/']     = 'Error'

#Comparative operators

cubo_semantico['int']['int']['=']   = 'int'
cubo_semantico['int']['int']['>']   = 'bool'
cubo_semantico['int']['int']['<']   = 'bool'
cubo_semantico['int']['int']['<=']  = 'bool'
cubo_semantico['int']['int']['>=']  = 'bool'
cubo_semantico['int']['int']['!=']  = 'bool'
cubo_semantico['int']['int']['==']  = 'bool'
cubo_semantico['int']['int']['||']  = 'bool'
cubo_semantico['int']['int']['&&']  = 'bool'

cubo_semantico['float']['float']['=']   = 'float'
cubo_semantico['float']['float']['<']   = 'bool'
cubo_semantico['float']['float']['>']   = 'bool'
cubo_semantico['float']['float']['<=']  = 'bool'
cubo_semantico['float']['float']['>=']  = 'bool'
cubo_semantico['float']['float']['!=']  = 'bool'
cubo_semantico['float']['float']['==']  = 'bool'
cubo_semantico['float']['float']['||']  = 'bool'
cubo_semantico['float']['float']['&&']  = 'bool'

cubo_semantico['char']['char']['=']     = 'bool'
cubo_semantico['char']['char']['==']    = 'bool'
cubo_semantico['char']['char']['<']     = 'bool'
cubo_semantico['char']['char']['>']     = 'bool'
cubo_semantico['char']['char']['<=']    = 'bool'
cubo_semantico['char']['char']['>=']    = 'bool'
cubo_semantico['char']['char']['!=']    = 'bool'
cubo_semantico['char']['char']['||']    = 'bool'
cubo_semantico['char']['char']['&&']    = 'bool'

cubo_semantico['char']['int']['='] = cubo_semantico['int']['char']['=']         = 'Error'
cubo_semantico['char']['float']['='] = cubo_semantico['float']['char']['=']     = 'Error'
cubo_semantico['int']['char']['=='] = cubo_semantico['char']['int']['==']       = 'Error'
cubo_semantico['float']['char']['=='] = cubo_semantico['char']['float']['==']   = 'Error' 
cubo_semantico['char']['int']['<'] = cubo_semantico['int']['char']['<']         = 'Error'
cubo_semantico['char']['float']['<'] = cubo_semantico['float']['char']['<']     = 'Error'
cubo_semantico['char']['int']['>'] = cubo_semantico['int']['char']['>']         = 'Error'
cubo_semantico['char']['float']['>'] = cubo_semantico['float']['char']['>']     = 'Error'
cubo_semantico['char']['int']['<='] = cubo_semantico['int']['char']['<=']       = 'Error'
cubo_semantico['char']['float']['<='] = cubo_semantico['float']['char']['<=']   = 'Error'
cubo_semantico['char']['int']['>='] = cubo_semantico['int']['char']['>=']       = 'Error'
cubo_semantico['char']['float']['>='] = cubo_semantico['int']['float']['>=']    = 'Error'
cubo_semantico['char']['int']['!='] = cubo_semantico['int']['char']['!=']       = 'Error'
cubo_semantico['char']['float']['!='] = cubo_semantico['float']['char']['!=']   = 'Error'
cubo_semantico['char']['int']['||'] = cubo_semantico['int']['char']['||']       = 'Error'
cubo_semantico['char']['float']['||'] = cubo_semantico['char']['float']['||']   = 'Error'
cubo_semantico['char']['int']['&&'] = cubo_semantico['char']['int']['&&']       = 'Error'
cubo_semantico['char']['float']['&&'] = cubo_semantico['char']['float']['&&']       = 'Error'
