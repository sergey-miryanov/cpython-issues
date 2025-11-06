z = None

def t1():
    return {z} if z is not None else set()
    

def t2():
    # try:
    #     return {z} if z is not None else pass
    # except Exception as e:
    #     return e
    pass
    
def t3():
    # try:
    #     return {z} if z is not None else raise Exception('test')
    # except Exception as e:
    #     return e
    pass

def t4():
    try:
        return continue if z is not None else set()
    except Exception as e:
        return e

print (t1())
print (t2())
print (t3())
print (t4())
