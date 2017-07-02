
keys = [ 'biaodian/execise/time_limit' ]

def validate( key, value ):
    try:
        return key in keys and type(value) == type("") and len(value) < 512
    exept:
        return false
