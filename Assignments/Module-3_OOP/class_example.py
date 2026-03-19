class student:
    stid=12
    stnm="Sanket"
    
    def getdata(self):
        print("This is getdata from student class!")

#Object
st=student()
print("ID:",st.stid)
print("Name:",st.stnm)
st.getdata()