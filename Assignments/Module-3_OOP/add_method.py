class Student:
    def __init__(self,x):
        self.x=x
        
    def __add__(self, other):
        return Student(self.x+other.x)


st=Student(10)
st1=Student(20)
ans=st+st1
print(ans.x)
