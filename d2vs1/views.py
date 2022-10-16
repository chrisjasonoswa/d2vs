from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
import pyrebase
from time import sleep
from django.http import JsonResponse
import inflect
from .utils import *
from django.template import Template, Context
from django.template.loader import get_template
from datetime import datetime, timedelta
import time
import requests

from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.model.sms_advanced_textual_request import SmsAdvancedTextualRequest
from infobip_api_client.model.sms_destination import SmsDestination
from infobip_api_client.model.sms_response import SmsResponse
from infobip_api_client.model.sms_textual_message import SmsTextualMessage
from infobip_api_client.api.send_sms_api import SendSmsApi
from infobip_api_client.exceptions import ApiException


# Create your views here.

#Firebase Setup
config = {
  "apiKey": "AIzaSyD3ynKae5tYH0-XP_ZC5d1ndFVjfrQLyAY",
  "authDomain": "d2vs-ee518.firebaseapp.com",
  "databaseURL": "https://d2vs-ee518-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "d2vs-ee518",
  "storageBucket": "d2vs-ee518.appspot.com",
  "messagingSenderId": "501432073504",
  "appId": "1:501432073504:web:962b049fed5aec97e3ab45",
  "measurementId": "G-XZ2GGQD5M3"
}

#Firebase Authentication
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def homepage(request):
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "d2vs1/homepage.html")

def login_view(request):
    # Attempt to sign user in
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    # Check if authentication successful
    if user is not None:
        login(request, user)
        print("Hey")
        headers ={
            "HX-Redirect": reverse("index")
        }
        return HttpResponse(headers=headers)
    #If not show error message
    else:
        print("Hello")
        error_mssg = "<div class='alert alert-danger' role='alert'>Invalid username and/or password</div>"
        return HttpResponse(error_mssg)


def logout_view(request):
    logout(request)
    return redirect("homepage")

@login_required
def index(request):

    username = request.user.get_username()
    user = User.objects.get(id=1)

    system_status = database.child(f"user{user.id}").get()[3].val()
    door_status = database.child(f"user{user.id}").get()[0].val()
    password_list = database.child(f"user{user.id}").child("passwords").get()

    date_today = datetime.today()
    todays_entries = Logs.objects.filter(timestamp__year=date_today.year, timestamp__month=date_today.month, timestamp__day=date_today.day).count()

    count = 0
    for password in password_list:
        if password.val() != 0:
            count +=1
        

    context ={
        "system_status": system_status.upper(),
        "door_status": door_status.upper(),
        "count": count
    }

    return render(request, "d2vs1/dashboard.html",context)

def home(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)
    system_status = database.child(f"user{user.id}").get()[3].val()
    door_status = database.child(f"user{user.id}").get()[0].val()
    password_list = database.child(f"user{user.id}").child("passwords").get()

    date_today = datetime.today()
    todays_entries = Logs.objects.filter(timestamp__year=date_today.year, timestamp__month=date_today.month, timestamp__day=date_today.day).count()
    count = 0
    for password in password_list:
        if password.val() != 0:
            count +=1
    if user.phone_number:
        phone_number = user.phone_number
        phone_number = "+" + str(phone_number)
    else:
        phone_number = "Not Yet Set"

    context ={
        "system_status": system_status.upper(),
        "door_status": door_status.upper(),
        "count": count,
        "todays_entries": todays_entries,
        "phone_number": phone_number,
    }

    return render(request, "d2vs1/home.html",context)



def update_dashboard(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    system_status = database.child(f"user{user.id}").get()[3].val()
    door_status = database.child(f"user{user.id}").get()[0].val()
    password_list = database.child(f"user{user.id}").child("passwords").get()

    date_today = datetime.today()
    todays_entries = Logs.objects.filter(timestamp__year=date_today.year, timestamp__month=date_today.month, timestamp__day=date_today.day).count()

    count = 0
        

    
    for password in password_list:
        if password.val() != 0:
            count +=1
    data = {
        "system_status": system_status.upper(),
        "door_status": door_status.upper(),
        "count": count,
        "todays_entries": todays_entries,
    }
    return JsonResponse(data)
    
def update_phonenumber(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    user.phone_number = "63" + str(request.GET.get('phonenumber'))
    user.save()

    #Update session
    request.user = user
    update_session_auth_hash(request, user)
    login(request, user)

    data = {
        "phonenumber": user.phone_number,
    }

    return JsonResponse(data)

def update_username(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    user.username = request.GET.get('username')
    user.save()
    
    print("New Username Object: " + user.username)
    #Update session
    request.user = user
    update_session_auth_hash(request, user)
    login(request, user)
    print("Request Username" + request.user.get_username())

    data = {
        "username": user.username,
    }

    return JsonResponse(data)


def update_password(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    if request.GET.get('new_password') == request.GET.get('confirmation'):
        user.set_password(request.GET.get('new_password'))
        user.save()
        
        #Update session
        request.user = user
        update_session_auth_hash(request, user)
        login(request, user)
        data ={
            "successful": "true",
            "password": user.password,
        }
        print("Success")
        return JsonResponse(data)
    else:
        data ={
            "successful": "false",
        }
        return JsonResponse(data)


def add_logs(request, status, user_id):
    user = User.objects.get(id=user_id)
    notif = Logs.objects.create(logs_user=user, status=status)

    if notif.status == "alert":
        notif.delete()
        #Check Alarm
        BASE_URL = "https://wp5611.api.infobip.com"
        API_KEY = "3255914b2597342598175cbc157439fd-f56c061f-f513-4cc0-b683-a59c71673b79"

        SENDER = "D2VS"
        RECIPIENT = user.phone_number
        MESSAGE_TEXT = "WARNING! 3 consecutive unsuccessful attempts DETECTED.\n\nSystem is DISABLED."

        client_config = Configuration(
                host= BASE_URL,
                api_key={"APIKeyHeader": API_KEY},
                api_key_prefix={"APIKeyHeader": "App"},
            )

        api_client = ApiClient(client_config)

        sms_request = SmsAdvancedTextualRequest(
                messages=[
                    SmsTextualMessage(
                        destinations=[
                            SmsDestination(
                                to=RECIPIENT,
                            ),
                        ],
                        _from=SENDER,
                        text=MESSAGE_TEXT,
                    )
                ])

        api_instance = SendSmsApi(api_client)

        try:
            api_response: SmsResponse = api_instance.send_sms_message(sms_advanced_textual_request=sms_request)
            print(api_response)
        except ApiException as ex:
            print("Error occurred while trying to send SMS message.")
            print(ex)
        database.child(f"user{user.id}").update({"system_status": "Disabled"})

    return HttpResponse("Log Added Successfully")

def add_logs_get(request):
    user = User.objects.get(id=int(request.GET["id"]))
    Logs.objects.create(logs_user=user, status=request.GET["status"])
    return HttpResponse("Log Added Successfully")

def get_logs(request):
    user = User.objects.get(id=1)
    logs_list = Logs.objects.all().order_by('-timestamp', '-id')

    context = {
        "logs_list": logs_list,
    }
    return render(request, 'd2vs1/all_logs.html', context)

def get_recent_logs(request):
    user = User.objects.get(id=1)
    logs_list = Logs.objects.all().order_by('-timestamp', '-id')[:5]

    context = {
        "logs_list": logs_list,
    }
    return render(request, 'd2vs1/recent_logs.html', context)

def clear_logs(request):
    user = User.objects.get(id=1)
    logs_list = Logs.objects.all().delete()
    data ={
        "mssg" : "Logs Successfully Cleared",
    }
    return JsonResponse(data)

def controls(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    system_status = database.child(f"user{user.id}").get()[3].val()
    
    door_status = database.child(f"user{user.id}").get()[0].val()

    p = inflect.engine()
    password_list = database.child(f"user{user.id}").child("passwords").get()
    passwords = []

    count = 1
    for password in password_list:
        key = p.number_to_words(p.ordinal(count)).capitalize()
        passwords.append({f"{key}": password.val()})
        count += 1
        
    #Manual Control Value
    if door_status == "Closed":
        manual_ctrl = "Open"
    else:
        manual_ctrl = "Close"

    #System Status Value
    if system_status == "Enabled":
        system_control = "Disable"
    else:
        system_control = "Enable"

    #System 
    context = {
        "manual_ctrl": manual_ctrl,
        "system_control": system_control,
        "system_status": system_status,
        "door_status": door_status,
        "passwords": passwords
    }
    return render(request, "d2vs1/controls.html", context)
    #else:
    #    return render(request, "d2vs1/controls_page.html")


def register_knock(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)
    print("Hey")

    database.child(f"user{user.id}").update({"registration": "true"})
    data ={
        "mssg": "Knock Registration Activated",
    }
    return JsonResponse(data)

def update_system_status(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)
    system_status = database.child(f"user{user.id}").get()[3].val()

    if system_status == "Enabled":
        database.child(f"user{user.id}").update({"system_status": "Disabled"})
    else:
        database.child(f"user{user.id}").update({"system_status": "Enabled"})

    system_control = system_status.replace("d", "")
    system_status = database.child(f"user{user.id}").get()[3].val()
 
    data = {
        'system_status' : system_status,
        'system_control': system_control,
    }
    return JsonResponse(data)

def get_current_status(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)
    system_status = database.child(f"user{user.id}").get()[3].val()

    if system_status == "Enabled":
        system_control = "Disable"
    else:
        system_control = "Enable"
    data = {
        'system_control' : system_control,
        'system_status': system_status,
    }
    return JsonResponse(data)

def manual_control(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    door_status = database.child(f"user{user.id}").get()[0].val()
    if door_status == "Opened":
        database.child(f"user{user.id}").update({"door_status": "Closed"})
        manual_ctrl = "Open"
    else:
        database.child(f"user{user.id}").update({"door_status": "Opened"})
        manual_ctrl = "Close"
    
    door_status = database.child(f"user{user.id}").get()[0].val()

    data = {
        'manual_ctrl' : manual_ctrl,
        'door_status': door_status,
    }
    return JsonResponse(data)
def get_current_door_status(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)
    door_status = database.child(f"user{user.id}").get()[0].val()
    num =1


    if door_status == "Opened":
        manual_ctrl = "Close"
    else:
        manual_ctrl = "Open"

    data = {
        'manual_ctrl' : manual_ctrl,
        'door_status': door_status,
    }
    return JsonResponse(data)


def set_password(request):
    username = request.user.get_username()
    user = User.objects.get(id=1)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        password = int(request.POST.get("password"))
        order = request.POST.get("pass_number")
        print(order)
        pass_number = pass_ordinal_to_letter(order)

        database.child(f"user{user.id}").child("passwords").update({f"{pass_number}": password})
        print(pass_number)
        print(password)
        data ={
            "password" : password,
            "order": order,
        }
        return JsonResponse(data)

def del_password(request, key):
    username = request.user.get_username()
    user = User.objects.get(id=1)
    order = pass_ordinal_to_letter(key)
    database.child(f"user{user.id}").child("passwords").update({f"{order}": 0})

    data ={
        "key": key,
        "password": "",
    }
    return JsonResponse(data)

    
def logs(request):
    return render(request, "d2vs1/logs.html")