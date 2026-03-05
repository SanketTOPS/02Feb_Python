stdata={}

n=int(input("Enter number of students:"))

for i in range(n):
    sid=int(input("Enter Stuent's ID:"))
    sname=input("Enter Student' Name:")
    scity=input("Enter Student's City:")
    
    stdata[sid]={
        'name':sname,
        'city':scity
    }

#print(stdata)
for i,j in stdata.items():
    print(i,j)