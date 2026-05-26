class father:
    bal=0
    car=0
    
    def getdata(self):
        self.bal=input("Enter balance details:")
        self.car=input("Enter car's details:")
        
class son(father):
    def printdata(self):
        print("Balance:",self.bal)
        print("Car:",self.car)

sn=son()
sn.getdata()
sn.printdata()

        