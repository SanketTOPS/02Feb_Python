data=[12,34,45]
try:
    print(data[4])
except IndexError:
    print("Index out of range")