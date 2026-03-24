import re

mystr="These is Pythaon!"

#x=re.findall('Py..on',mystr)
x=re.findall('This|That', mystr)
print(x)