class Studinfo:
    def __init__(self,name):
        self.name=name
        
    def __str__(self):
        return f"My name is {self.name}"

st=Studinfo("Sanket")
print(st)
print(st.name)