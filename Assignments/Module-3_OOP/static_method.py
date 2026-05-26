class Studinfo:
    @staticmethod
    def getdata():
        print("This is getdata!")
    
    @staticmethod
    def getsum(a,b):
        print("Sum:",a+b)


st=Studinfo()
st.getdata()
st.getsum(45,56)