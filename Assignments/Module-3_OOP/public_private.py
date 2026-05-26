class Studinfo:
    #private
    __stid=101
    __stnm="Sanket"
    
    def __getdata(self): #private
        print("This is getdata")
        print("ID:",self.__stid)
        print("Name:",self.__stnm)
    
    def printdata(self):
        self.__getdata()
    
st=Studinfo()
#st.getdata()
st.printdata()

