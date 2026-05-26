import json

stdata={}

stid=input("Enter an ID:")
stnm=input("Enter a Name:")
stsub=input("Enter a Subject:")

stdata["id"]=stid
stdata["name"]=stnm
stdata["sub"]=stsub

#print(stdata)

fl=open('stud.json','w')
json.dump(stdata,fl)
