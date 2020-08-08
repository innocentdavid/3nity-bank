import json
import random

from django.core.files.storage import default_storage

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.


@login_required
def index(request):
    user=Customer.objects.get(user=request.user)
    print(user)
    # account = Account.objects.get(customer=user)
    # print(accounnt)
    pdToggle = 'profile'
    pdT = 'Profile'
    ptitle = 'Dashboard'

    context = {'pdToggle': pdToggle, 'pdT': pdT, 'ptitle': ptitle}
    return render(request, 'bank/index.html', context)

@csrf_exempt
def getAllAccount(request):
    action = request.POST['getAllAccounts']
    print(action)


def getAccount(request):
    if request.method == 'POST':
        account = request.POST['account']
        print(account)
        pdToggle = 'profile'
        pdT = 'Profile'
        ptitle = 'Dashboard'

        context = {'pdToggle': pdToggle, 'pdT': pdT, 'ptitle': ptitle}
        return render(request, 'bank/index.html', context)


@login_required
def profile(request):
    pdToggle = ''
    pdT = 'Dashboard'
    ptitle = 'Profile'

    context = {'pdToggle': pdToggle, 'pdT': pdT, 'ptitle': ptitle}
    return render(request, 'bank/profile.html', context)


@csrf_exempt
@login_required
def page(request, file_name):
    f = default_storage.open(f"bank/templates/bank/{file_name}.html")
    page = f.read().decode("utf-8")

    return JsonResponse({"page": page}, status=200)


@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        uname = request.POST["username"]
        username = uname.capitalize()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bank/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bank/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        dob = request.POST["dob"]
        tel = request.POST["tel"]
        address = request.POST["address"]
        # photo = request.FILES["photo"]

        uname = request.POST["username"]
        username = uname.capitalize()
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bank/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError as e:
            print(e)
            return render(request, "bank/register.html", {
                "message": "username address already taken."
            })
        login(request, user)

        managers = []
        staffs = Staff.objects.all()
        for staff in staffs:
            managers.append(staff)

        manager = random.choice(managers)
        customer = Customer(user=request.user, manager=manager, fname=fname,
                            lname=lname, email=email, dob=dob, tel=tel, address=address)
        customer.save()

        staffs = Staff.objects.filter(
            name=User.objects.get(username=str(manager)))
        print(staffs)
        for staff in staffs:
            staff.totalCustomer = int(staff.totalCustomer)+1
            staff.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bank/register.html")
