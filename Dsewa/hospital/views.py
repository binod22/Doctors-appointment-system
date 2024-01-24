from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import requests
import json

# Create your views here.


def homepage(request):
    return render(request, 'index.html')





def createaccount(request):
    # initialize user
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
               
                Patient.objects.create(name=name,
                                       email=email,
                                       gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       bloodgroup=bloodgroup)

                user = User.objects.create_user(
                    first_name=name, 
                    email=email, 
                    password=password,
                      username=email)
               
                
                pat_group = Group.objects.get(name='Patient')
               
                pat_group.user_set.add(user)
                
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            error = 'yes'
   
    d = {'error': error}
    
    return render(request, 'createaccount.html', d)



def loginpage(request):
    return render(request, 'login.html')



def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    api_key ='live_secret_key_68791341fdd94846a146f0457ff7b455'
    return_url = request.POST.get('return_url')
    website_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount') 

    print("return url",return_url)
    print("amount",amount)
    print("purchase_order_id",purchase_order_id)

    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": "test Bahadur",
        "email": "test@khalti.com",
        "phone": "9800000001"
        }
    })

    headers = {
        'Authorization': f'key {api_key}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        new_response = json.loads(response.text)
        print(new_response)
        return redirect(new_response['payment_url'])
    except Exception as e:
        print(f"Error: {str(e)}")
        return redirect("home")

def verifykhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)

        if new_res['status'] == 'Completed':
            user = request.user
            print("Payment is compleated{user}".format(user=user))
            
            
            
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect('viewappointments')
    
    




def loginpage(request):
    error = ""
    
    if request.method == 'POST':
        
        u = request.POST['email']
        p = request.POST['password']
        
        user = authenticate(request, username=u, password=p)
        #print("This is "+str(user))
        try:
            
            if user is not None:
                error = "no"
                print("I AM")
               
                login(request,user)


                g = request.user.groups.all()[0].name
                print("this is "+str(g))
                if g == 'Patient':
                    d = {'error': error}
                    #return HttpResponse("Patient Logged in Successfully")
                    return render(request, 'patienthome.html', d)
                elif g =='Doctor':
                    
                    d = {'error': error}
                    #return HttpResponse('Doctor Logged in Successfully')
                    return render(request,'docdash.html', d)
       
        except Exception as e:
            error = "yes"
            print(e)
           
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('loginpage')

def Home(request):
   
    if not request.user.is_active:
        return redirect('homepage')
    
    else:
        g = request.user.groups.all()[0].name
        if g == 'Patient':
            d={'group':g}
            return render(request, 'patienthome.html',d)
        elif g=='Doctor':
            upcomming_appointments = Appointment.objects.filter(doctoremail = request.user, appointmentdate__gte = timezone.now(), status = True).order_by('appointmentdate')
       
            previous_appointments = Appointment.objects.filter(doctoremail = request.user, appointmentdate__lt = timezone.now()).order_by('-appointmentdate')| Appointment.objects.filter(doctoremail = request.user, status = False).order_by('-appointmentdate')
       
            d = {"upcomming_appointments": upcomming_appointments,"previous_appointments": previous_appointments}
                    #return HttpResponse('Doctor Logged in Successfully')
            return render(request,'docdash.html', d)
        else:
            return redirect('index.html')


@login_required(login_url='/login')
def profile(request):
   
    if not request.user.is_active:
        return redirect('loginpage')

    
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        #print(request.user)
        patient_details = Patient.objects.all().filter(email=request.user)
        #print(patient_details)
        d = {'details': patient_details,'group':g}
        return render(request, 'patientprofile.html', d)
    elif g=='Doctor':
        doctor_details = Doctor.objects.all().filter(email=request.user)
        d={'details': doctor_details,'group':g}
        return render(request, 'patientprofile.html', d)



@login_required(login_url='/login')
def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('loginpage')
   
    alldoctors = Doctor.objects.all()
    g = request.user.groups.all()
    print(g)
    g = request.user.groups.all()[0].name
    d = {'alldoctors': alldoctors,'group':g}
    g='Patient'
    if g == 'Patient':
        if request.method == 'POST':
            temp = request.POST['doctoremail']
            doctoremail = temp.split()[0]
            doctorspecialization = temp.split()[2]
            doctorname = temp.split()[1]
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            try:
                Appointment.objects.create(doctorname=doctorname, doctoremail=doctoremail, patientname=patientname, patientemail=patientemail,
                                           appointmentdate=appointmentdate, appointmenttime=appointmenttime, symptoms=symptoms, status=True, prescription="")
                subject = "RE: Your Appointment Bookings At DSEWA"
                print(subject)
                message = "Your Appointment is confirmed \n\n Please check the details below\n\n Doctor Name={doctorname}\n{doctorspecialization}\n\nAppointment Date={appointmentdate}\n\nAppointment Time={appointmenttime}\n".format(doctorname=doctorname, appointmentdate=appointmentdate, appointmenttime=appointmenttime,doctorspecialization=doctorspecialization)
                from_email = "doctorsewa2023@gmail.com"
                print(from_email)
                recipients =[patientemail]
                print(recipients)
                send_mail(subject,message,from_email,recipients)
                print("5")

                error = "no"
            except:
                error = "yes"
            e = {"error": error,}
            return render(request, 'patientmakeappointments.html', e)
        elif request.method == 'GET':
            return render(request, 'patientmakeappointments.html', d)


def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
   
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        # appointmentdate__gte -> greater than
       
        upcomming_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__gte = timezone.now(), status = True).order_by('appointmentdate')
        for i in upcomming_appointments:
            print(i.appointment_id)
        previous_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__lt = timezone.now()).order_by('-appointmentdate')| Appointment.objects.filter(patientemail = request.user, status = False).order_by('-appointmentdate')
       
        d = {"upcomming_appointments": upcomming_appointments,"previous_appointments": previous_appointments,'group':g}
        return render(request, 'patientviewappointments.html', d)

@login_required(login_url='/login')
def update_profile(request):
        
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']

        query_set = Patient.objects.get(email=request.user.email)

        query_set.name = name
        query_set.gender = gender
        query_set.phonenumber = phonenumber
        query_set.address = address
        query_set.birthdate = birthdate
        query_set.bloodgroup = bloodgroup

        query_set.save()

        return redirect('profile')



    patient_details = Patient.objects.all().filter(email=request.user)
    print(patient_details)
    d = {'patient_details': patient_details}
    return render(request, 'updatedetails.html',d)

def doc_register(request):
    # initialize user
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        nmcnumber = request.POST['nmcnumber']
        qualification = request.POST['qualification']
        specialization = request.POST['specialization']
        photo = request.FILES.get('doc_image')
        license_image = request.FILES.get('license_image')

        try:
            if password == repeatpassword:
               
                Doctor.objects.create(name=name,
                                       email=email,
                                       gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       nmc=nmcnumber,
                                       qualification=qualification,
                                       specialization=specialization,
                                       doc_image=photo,
                                       doc_license_image=license_image
                                      )

                user = User.objects.create_user(
                    first_name=name, 
                    email=email, 
                    password=password,
                      username=email)
               
                
                doc_group = Group.objects.get(name='Doctor')
               
                doc_group.user_set.add(user)
                
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            print(e)
            error = 'yes'
   
    d = {'error': error}
    
    return render(request, 'docregister.html', d)



    
    
