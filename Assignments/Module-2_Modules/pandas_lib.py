import pandas

data={
    'id':[1,2,3,4,5],
    'name':['sanket','ashok','gopal','hitesh','nirav'],
    'sub':['python','java','html','css','c++']
}

#print(data)
pd=pandas.DataFrame(data)
print(pd)