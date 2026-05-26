from django.shortcuts import render,redirect
from .forms import *

# Create your views here.
def index(request):
    if request.method=='POST':
        form=Userform(request.POST)
        if form.is_valid():
            form.save()
            print("Record Inserted!")
            return redirect('showdata')
        else:
            print(form.errors)
    return render(request,'index.html')

def showdata(request):
    udata=Userinfo.objects.all()
    return render(request,'showdata.html',{'udata':udata})

def updatedata(request,id):
    uid=Userinfo.objects.get(id=id)
    if request.method=='POST':
        form=Userform(request.POST,instance=uid)
        if form.is_valid():
            form.save()
            print("Record Updated!")
            return redirect('showdata')
        else:
            print(form.errors)
    return render(request,'updatedata.html',{'uid':uid})

def deletedata(request,id):
    uid=Userinfo.objects.get(id=id)
    Userinfo.delete(uid)
    return redirect('showdata')
    