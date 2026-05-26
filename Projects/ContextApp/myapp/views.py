from django.shortcuts import render
import random

# Create your views here.
def index(request):
    name="Ashok"
    num=random.randint(1111,9999)
    return render(request,'index.html',{'name':name,'num':num})