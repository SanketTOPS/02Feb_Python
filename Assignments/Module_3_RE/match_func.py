import re

mystr="That is Python!"

x=re.match('That',mystr)
print(x)

if x:
    print("Match done!")
else:
    print("Error!")