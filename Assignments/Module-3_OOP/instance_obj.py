class Studinfo:
    stid=101
    stnm="Sanket"
    
    def getdata(self):
        print("ID:",self.stid)
        print("Name:",self.stnm)

#Object
"""st=Studinfo()
st.getdata()
st.stid=102
st.stnm="Ashok"
st.getdata()"""

# ----------------------- #
#Instance of Class
Studinfo().getdata()
Studinfo().stid=102
Studinfo().stnm="Nirav"
Studinfo().getdata()
