from allapps import models
from django.shortcuts import render, HttpResponse, redirect
import random
import json
from .forms import loginform
import time
from django.core.mail import EmailMultiAlternatives, EmailMessage
from hositallogs import settings


# Create your views here.

UPPERCASE = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z'
]
LOWERCASE = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z'
]
SPECIALLETTER = [
    '!', '$', '*', '+', '-',
    ':', '?', '@', '_', '|', '~'
]
DIGITS = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]


def getUsername(hospitalname=None, location=None):
    username = ""
    for var in range(2):
        username += random.choice(UPPERCASE)
        username += random.choice(DIGITS)
        username += random.choice(LOWERCASE)
        username += random.choice(SPECIALLETTER)
        username += random.choice(DIGITS)
    return username


def getPassword():
    password = ""
    for var in range(5):
        password += random.choice(UPPERCASE)
        password += random.choice(DIGITS)
        password += random.choice(LOWERCASE)
        password += random.choice(SPECIALLETTER)
    return password

# def getexpiredate(n): # number from which the date must be incresed
#     expiredate = None
#     day = 12
#     month = 3
#     year = 2021
#     if day + n > 30:
#         day = n - 30 + day
#         if month + 1 > 12:
#             month = 1
#             year += 1
#         else:
#             month += 1
#     else:
#         day += n


def index(request):
    if request.COOKIES.get("session_id") is not None:
        context = {
            "makesession": 0
        }
        return render(request, "index.html", context)
    session_cookie = generatesession_cookies()
    registersession_cookies(session_cookie)
    expiredate = None
    context = {
        "session_id": session_cookie,
        "makesession": 1,
        "expiredate": "Saturday, December 11, 2021 at 2:34:52 PM",
    }
    return render(request, "index.html", context)


def getimagename(file):
    content_ex = file.content_type
    if content_ex == "image/jpg" or content_ex == "image/jpeg":
        file.name = f"{time.strftime('%I%M%d%m%y')}.jpg"
        return True
    else:
        return False


def imageUpload(request):
    if request.method == 'GET':
        return render(request, "imageupload.html")
    elif request.method == 'POST':
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        user = session.user
        if getimagename(request.FILES.get('profilepic')):
            user.hospitalimage = request.FILES.get('profilepic')
            user.save()
            return redirect("/registrationdone/")
        else:
            return redirect("/imageupload/")


def regdone(request):
    try:
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        user = session.user
        username = user.username
        password = user.password
        context = {
            "username": username,
            "password": password,
        }
        return render(request, "registrationdone.html", context)
    except Exception as e:
        print(e)
        return HttpResponse("<h1>505 Internal Server Error</h1>")


def register(request):
    return render(request, "registration.html")


def registerdoc(request):
    try:
        registstrationdata = json.loads(request.body.decode())
        print(registstrationdata)
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        username = getUsername()
        password = getPassword()
        hospital_name = registstrationdata[len(
            registstrationdata) - 1]["hospital name"]
        hospital_email = registstrationdata[len(
            registstrationdata) - 1]["Email id"]
        hospital_location = registstrationdata[len(
            registstrationdata) - 1]["Location"]
        hospital_pincode = registstrationdata[len(
            registstrationdata) - 1]["pincode"]
        hospital_city = registstrationdata[len(registstrationdata) - 1]["city"]
        hospital_fees = registstrationdata[len(registstrationdata) - 1]["fees"]
        location = models.Location(
            address=hospital_location, city=hospital_city, Pincode=hospital_pincode)
        location.save()
        location = models.Location.objects.get(
            address=hospital_location, city=hospital_city, Pincode=hospital_pincode)
        hospital = models.Hospital(name=hospital_name, Location=location,
                                   fees=hospital_fees, username=username, password=password, emailid=hospital_email)
        hospital.save()
        hospital = models.Hospital.objects.get(
            username=username, password=password)
        session.user = hospital
        session.save()
        registstrationdata.pop()
        for var in registstrationdata:
            doctor = models.Doctor(Name=var["name"], Qualification=var["qualification"], Specilization=var["specilization"],
                                   experience=var["experience"], startingtime=var["starttime"], endingtime=var["endtime"], hospital=hospital)
            doctor.save()
        context = {
            "username": username,
            "password": password,
        }
        return render(request, "imageupload.html", context)
    except Exception as e:
        print(e)
        return HttpResponse("<h1>505 Internal Server Error</h1>")


def otpgenerator():
    otp = ""
    for var in range(6):
        otp += random.choice(DIGITS)
    return otp


def otppage(request):
    if request.method == 'GET':
        return render(request, "otppage.html")
    elif request.method == 'POST':
        try:
            enteredotp = request.POST.get("otp")
            session_id = request.COOKIES.get('session_id')
            session = models.sessions.objects.get(sessionToken=session_id)
            if session.otp == int(enteredotp) and session.is_semiauthentic == True:
                user = session.user
                session.is_login = True
                session.is_semiauthentic = False
                session.otp = None
                session.save()
                html_content = f"""
<html>
    <body>
        WELCOME TO HOSPITALLOGS,<br>
        <h3>{user.name}</h3> has login to his HOSPITALLOGS account
    </body>
</html>
                """
                msg = EmailMultiAlternatives(
                    subject="***ALERT***- HospitalLogs",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.emailid]
                    )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect("/profile/")
            else:
                return HttpResponse("<h1>Invalid OTP</h1>")
        except Exception as e:
            print(e)
            return HttpResponse("<h1>505 Internal Server Error</h1>")


def login(request):
    '''
    GET method:-
        1. create a login form
        2. render loginhospital.html

    POST method:-
        1. get the username and password from the request
        2. authenticate the user with help of authenticate function
    '''
    if request.method == "GET":
        try:
            session_id = request.COOKIES.get("session_id")
            session = models.sessions.objects.get(sessionToken=session_id)
            if session.is_login:
                return redirect("/profile/")
            else:
                form = loginform()
                context = {
                    "form":  form
                }
                return render(request, "loginhospital.html", context)
        except Exception as e:
            print(e)
            return redirect("/")

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        session_id = request.COOKIES.get("session_id")
        user = authenticateHospital(username, password)
        if user:
            try:
                session_object = models.sessions.objects.get(
                    sessionToken=session_id)
                session_object.user = user
                otpofsession = otpgenerator()
                session_object.otp = otpofsession
                session_object.is_semiauthentic = True
                session_object.save()
                html_content = f"""
<html>
    <body>
        YOUR OTP TO HOSPTIALLOGS LOGIN: <h1>{otpofsession}</h1>
    </body>
</html>
                """
                msg = EmailMultiAlternatives(
                    subject="OTP- HospitalLogs",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.emailid]
                    )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect("/otppage/")
            except Exception as e:
                print(e)
                return HttpResponse("<h1>505 Internal Server Error</h1>")
        else:
            return HttpResponse("<h1>User no found</h1>")


def generatesession_cookies():
    cookie = random.choice(LOWERCASE) + random.choice(UPPERCASE) + \
        random.choice(DIGITS) + random.choice(SPECIALLETTER)
    return cookie


def registersession_cookies(cookie):
    sessionObj = models.sessions(sessionToken=cookie)
    sessionObj.save()


def authenticateHospital(username, password):
    try:
        user = models.Hospital.objects.get(
            username=username, password=password)
        if user:
            return user
    except Exception as e:
        print(e)
        return False


def profile(request):
    try:
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        user = session.user
        if user is not None:
            doctors = models.Doctor.objects.filter(hospital=user)
            context = {
                "user": user,
                "doctorlist": doctors
            }
            return render(request, "profile.html", context)
        else:
            return redirect("/login/")
    except Exception as e:
        print(e)
        return redirect("/")


def editdoctor(request):
    if request.method == "POST":
        content = json.loads(request.body.decode())
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        user = session.user
        doctor = models.Doctor(Name=content["name"], Qualification=content["qualification"], Specilization=content["specilization"],
                               experience=content["experience"], startingtime=content["starttime"], endingtime=content["endtime"], hospital=user)
        doctor.save()
        return HttpResponse("<h1>asdf</h1>")
    else:
        return redirect("/")


def removedoctor(request):
    try:
        doctortorem = request.POST.get('doctorid')
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        user = session.user
        if user is not None:
            models.Doctor.objects.get(id=doctortorem).delete()
            return HttpResponse("<h3>Remove Doctor</h3>")
        else:
            return HttpResponse("<h1>403 Forrbiden access</h1>")
    except Exception as e:
        print(e)
        return HttpResponse("403 Forrbiden access")


def editprofile(request):
    try:
        editedusername = request.POST.get("usernameedit")
        editedaddress = request.POST.get("addressedit")
        editedcity = request.POST.get("cityedit")
        editedpincode = request.POST.get("pincodeedit")
        editednumberofbeds = request.POST.get("numberofbedsedit")
        if editednumberofbeds == '':
            editednumberofbeds = None
        editedfees = request.POST.get("feeedit")
        editeddiscription = request.POST.get("discriptionedit")
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        user = session.user
        if user.username == editedusername:
            pass
        else:
            user.username = editedusername
        # editing the hospital location
        userslocation = user.Location
        if userslocation.address == editedaddress:
            pass
        else:
            userslocation.address = editedaddress
        if userslocation.city == editedcity:
            pass
        else:
            userslocation.city = editedcity
        if userslocation.Pincode == editedpincode:
            pass
        else:
            userslocation.Pincode = editedpincode
        userslocation.save()
        # ===============end===============
        if user.numberofbeds == editednumberofbeds:
            pass
        else:
            user.numberofbeds = editednumberofbeds
        if user.fees == editedfees:
            pass
        else:
            user.fees = editedfees
        if user.discriptions == editeddiscription:
            pass
        else:
            user.discriptions = editeddiscription
        user.save()
        return redirect("/profile/")
    except Exception as e:
        print(e)
        return HttpResponse("<h1>505 Internal Server Error</h1>")


def logout(request):
    try:
        session_id = request.COOKIES.get("session_id")
        session = models.sessions.objects.get(sessionToken=session_id)
        session.is_login = False
        session.user = None
        session.save()
        return redirect("/login/")
    except Exception as e:
        return redirect("/login/")


def resetingid():
    resetid = ''
    for var in range(5):
        resetid += random.choice(UPPERCASE)
        resetid += random.choice(LOWERCASE)
        resetid += random.choice(SPECIALLETTER)
        resetid += random.choice(DIGITS)
    return resetid


def forgotpassword(request):
    if request.method == 'GET':
        return render(request, "emailforgotpassword.html")
    elif request.method == 'POST':
        resetemailid = request.POST.get("emailforgotpassword")
        resetid = resetingid()
        user = models.Hospital.objects.get(emailid=resetemailid)
        resetobj = models.resetids(resetid=resetid, emailid=resetemailid, user=user)
        resetobj.save()
        # sending the email for reseting the password
        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body style="background-color: rgb(224, 219, 219)">
    <h1>HosptialLogs is a renowned Website that is Created By Aryan yadav</h1>
    <a href=http://127.0.0.1:8000/resetpassword/{resetid}/><button type="button" style="background-color:rgb(247, 152, 69); border:none; color:white;">Reset Password</button></a>
</body>
</html>
        '''.format()
        msg = EmailMultiAlternatives(
            subject="Reset Password - HospitalLogs",
            from_email=settings.EMAIL_HOST_USER,
            to=[resetemailid]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("<h1>Your Can check Your email for resetting the password</h1>")

def resetpassword(request, resetid):
    '''
    get the post request with resetid and filter the orginal password
    then get the resetid from database
    then get the user related to the resetid
    reset the password
    then delete the reset id from the database
    '''
    if request.method == "GET":
        try:
            resetidobj = models.resetids.objects.get(resetid=resetid)
            context = {
                "resetid" : resetid
            }
            return render(request, "resetpassword.html", context)
        except Exception as e:
            print(e)
            return HttpResponse("<h1>403 Forbidden Access</h1>")
    elif request.method == "POST":
        try:
            resetid = models.resetids.objects.get(resetid=resetid)
            password = request.POST.get('originalpassword')
            user = resetid.user
            user.password = password
            user.save()
            resetid.delete()
            return redirect("/login/")
        except Exception as e:
            print(e)
            return HttpResponse("<h1>403 Forbidden Access</h1>")

def search(request):
    '''
    search query:
        based on name of hospital
        based on name of doctor
        based on location
        based on name of problem
    method:
        get the search query from the request
        convert the search query in lower case
        get the detail from names
        get the details from location 
        get the details from problem 
        merge those details
        give them to the search result page
    '''
    try:
        if request.method == "GET":
            query = request.GET.get("searchquery")
            query = query.lower()
            if len(query) <= 50:
                hospitals = models.Hospital.objects.filter(name__contains=query)
                print(hospitals)
                # hospitals = models.Location.objects.filter()
                if len(hospitals) == 0:
                    haveresult = 0  # false
                else:
                    haveresult = 1  # true
                context = {
                    "hospital": hospitals,
                    "haveresult": haveresult
                }
                return render(request, "searchresult.html", context)
            else:
                return "Query Length must be smaller than 50 characters"
    except Exception as e:
        print(e)
        return HttpResponse("<h1>505 Internal Server Error</h1>")

def searchform(request):
    '''
    get the request
    if POST then get the name, location(city) and problem
    search the city, name, location in database
    fetch the hospitals from the information found
    bind the hospitals in single list
    return the searchresult.html 
    '''
    if request.method == "GET":
        return redirect("/")
    elif request.method == "POST":
        searchresult = []
        searchname = request.POST.get("searchname")
        searchcity = request.POST.get("searchcity")
        searchproblem = request.POST.get("searchproblem")
        if searchname != None:
            hbyname = models.Hospital.objects.filter(name__contains=searchname)
            for var in hbyname:
                print(f"hbyname {var}")
                if var not in searchresult:
                    searchresult.append(var)
        if searchcity != None:
            hbycity = models.Location.objects.filter(address__contains=searchcity)
            for var in hbycity:
                cityhospitals = models.Hospital.objects.filter(Location=var)
                for x in cityhospitals:
                    print(f"hbycity {x}")
                    if x not in searchresult:
                        searchresult.append(x)
        if searchproblem != None:
            hbyproblem = models.Doctor.objects.filter(Specilization__contains=searchproblem)
            for var in hbyproblem:
                x = var.hospital
                print(f"hbyproblem {x}")
                if x not in searchresult:
                   searchresult.append(x)
        print(searchresult)
        if len(searchresult) == 0:
            haveresult = 0
        else:
            haveresult = 1
        context = {
            "haveresult" : haveresult,
            "hospital" : searchresult,
        }
        return render(request, "searchresult.html", context)
    else:
        return redirect("/")

def getdetails(request, number):
    user = models.Hospital.objects.get(id=number)
    doctorlist = models.Doctor.objects.filter(hospital=user)
    context = {
        "user": user,
        "doctorlist": doctorlist
    }
    return render(request, "hospitaldetail.html", context)

def aboutus(request):
    return render(request, "aboutus.html")