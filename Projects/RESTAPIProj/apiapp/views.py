from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def getall(request):
    stdata=Studinfo.objects.all()
    serial=StudSerial(stdata,many=True)
    return Response(data=serial.data)

@api_view(['GET'])
def getid(request,id):
    try:
        stid=Studinfo.objects.get(id=id)
    except Studinfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serial=StudSerial(stid)
    return Response(data=serial.data)
    
@api_view(['DELETE','GET'])
def deleteid(request,id):
    try:
        stid=Studinfo.objects.get(id=id)
    except Studinfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serial=StudSerial(stid)
        return Response(data=serial.data)
    if request.method=='DELETE':
        Studinfo.delete(stid)
        return Response(status=status.HTTP_202_ACCEPTED)
        
@api_view(['POST'])
def insertdata(request):
    if request.method=='POST':
        serial=StudSerial(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def updatedata(request,id):
    try:
        stid=Studinfo.objects.get(id=id)
    except Studinfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serial=StudSerial(stid)
        return Response(data=serial.data)
    if request.method=='PUT':
        serial=StudSerial(data=request.data,instance=stid)
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)