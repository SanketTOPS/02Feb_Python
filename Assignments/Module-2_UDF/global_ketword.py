"""def getvalue():
    #local
    x=34
    y=90
    print("Sum:",x+y)

getvalue()
print("Mul:",x*y)"""


x=10
def getval():
    global x
    x+=1 #local
    print(x)

getval()