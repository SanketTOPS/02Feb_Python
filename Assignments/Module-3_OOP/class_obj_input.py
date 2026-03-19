class Studinfo:
    def printdata(self,stid,stnm):
        print("ID:",stid)
        print("Name:",stnm)

st=Studinfo()

id=input("Enter an ID:")
nm=input("Enter a Name:")
st.printdata(id,nm)