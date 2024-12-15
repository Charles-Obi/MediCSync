import json

import requests
from django.http import HttpResponse
from django.shortcuts import render,redirect
from requests.auth import HTTPBasicAuth

from myapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from myapp.forms import Appointment1Form, ImageUploadForm
from myapp.models import Appointment1, Contact, ImageModel, Users


# Create your views here.
def index(request):
    if request.method == 'POST':
        if Users.objects.filter(
            username = request.POST['username'],
            password = request.POST['password']
        ).exists():
            return render(request,'index.html')
        else:
            return render(request,'login.html')

    else:
        return render(request,'login.html')

def starter(request):
    return render(request, 'starter-page.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def doctors(request):
    return render(request, 'doctors.html')

def contact(request):
    return render(request, 'contact.html')

def departments(request):
    return render(request, 'departments.html')

def gallery(request):
    return render(request, 'gallery.html')

def appointment(request):
   if request.method == 'POST':
       myappointments=Appointment1(
           name=request.POST['name'],
           email=request.POST['email'],
           phone=request.POST['phone'],
           datetime=request.POST['date'],
           department=request.POST['department'],
           doctor=request.POST['doctor'],
           message=request.POST['message']
       )
       myappointments.save()
       return redirect('/appointment')
   else:
       return render(request, 'appointment.html')

def show(request):
    allappointments=Appointment1.objects.all()
    mycontacts = Contact.objects.all()
    return render(request, 'show.html', {
        'appointment':allappointments,
        'mycontact':mycontacts
    })

def delete(request,id):
    appoint = Appointment1.objects.get(id=id)
    appoint.delete()
    return redirect('/show')

def deletecontact(request, id):
    contactz = Contact.objects.get(id = id)
    contactz.delete()
    return redirect('/show')

def contact(request):
     if request.method == 'POST':
         mycontacts=Contact(
             name=request.POST['name'],
             email=request.POST['email'],
             subject=request.POST['subject'],
             message=request.POST['message']
         )
         mycontacts.save()
         return redirect('/contact')
     else:
         return render(request,'contact.html')

def edit(request,id):
    editappointment = Appointment1.objects.get( id = id)
    return render(request,'edit.html', {'appointment':editappointment})

def update(request, id):
    updateinfo = Appointment1.objects.get(id = id)
    form = Appointment1Form(request.POST,instance = updateinfo)
    if form.is_valid():
        form.save()
        return redirect('/show')
    else:
        return render(request,'edit.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/showimage')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def show_image(request):
    images = ImageModel.objects.all()
    return render(request, 'show_image.html', {'images': images})

def register(request):
    if request.method == 'POST':
        members = Users(
            name=request.POST['name'],
            username=request.POST['username'],
            password=request.POST['password']
        )
        members.save()
        return redirect('/login')

    else:
        return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')


def token(request):
    consumer_key = 'yCI5rB1MIP9QkLGCzIvrg5KzLJwTX7nzETOCANqnBPo8qRPA'
    consumer_secret = 'AnxYAtrdmAqgfctG6XpV51C7epaClfqc7AHgDym9TKHR6VZw6kh8ojmA4dIMMCgq'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')


#Mpsesa API views

def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "MediCSync",
            "TransactionDesc": "Hospital charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")