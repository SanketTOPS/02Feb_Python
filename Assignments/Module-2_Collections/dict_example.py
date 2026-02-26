stdata={
    'id':101,
    'name':'sanket',
    'city':'rajkot'
}
#print(stdata)
#print(stdata.keys())
#print(stdata.values())
#print(stdata['name'])
#print(stdata.get("city"))
#print(len(stdata))

"""if 'name' in stdata:
    print("Yes...")
else:
    print("No..")"""

"""if 'sanket' in stdata.values():
    print("Yes...")
else:
    print("No..")"""
    
"""for i in stdata:
    print(i)"""

"""for i in stdata.values():
    print(i)"""
    
"""for i in stdata.items():
    print(i)"""
    
"""for i,j in stdata.items():
    #print(i,j)
    print(f"Key={i} and Value={j}")"""
    
# ------------------------------------- #
print(stdata)
#stdata["sub"]="python"
#stdata.pop("city")
#stdata.clear()
#del stdata['id']
#del stdata
#print(stdata)

newdata=stdata.copy()
print(newdata)