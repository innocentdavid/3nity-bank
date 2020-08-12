import json
import random

from random import randint


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


# @login_required
def index(request):
    
    try:
        user=Customer.objects.get(user=User.objects.get(username=request.user))
        account = Account.objects.filter(customer=user)

        context = {'account':account}
        return render(request, 'bank/profile.html', context)
    except:
        return HttpResponseRedirect(reverse("login"))

@login_required
@csrf_exempt
def getAllAccount(request):
    action = request.POST['getAllAccounts']
    print(action)


@login_required
@csrf_exempt
def getAccount(request):
    if request.method == 'POST':
        pdToggle = 'profile'
        pdT = 'Profile'
        ptitle = 'Dashboard'

        accountNum = request.POST['account']
        user=Customer.objects.get(user=User.objects.get(username=request.user))
        account = Account.objects.filter(customer=user, accountNum=accountNum)

        context = {'pdToggle': pdToggle, 'pdT': pdT, 'ptitle': ptitle, 'account':account}
        return render(request, 'bank/profile.html', context)

@csrf_exempt
def transfer(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    data = json.loads(request.body)

    bank = data.get('bank')
    accNum = data.get('accNum')
    accName = data.get('accName')
    amount = data.get('amount')
    category = data.get('catg')
    naration = data.get('naration')
    transPin = data.get('transPin')
    user=Customer.objects.get(user=User.objects.get(username=request.user))
    
    acc = Account.objects.filter(customer=user, accountNum=accNum, transactionPin=transPin)
    for a in acc:
      newAmount = a.balance - float(amount)
      a.balance = newAmount
      a.save()
      
      history = History(account=Account.objects.get(accountNum=accNum), category=category, transcType='Expenditure', amount=amount, naration=naration)
      history.save()

      return JsonResponse({"message":'ok'}, status=200)
    return JsonResponse({"message":'error'}, status=500)


@login_required
def profile(request):
    pdToggle = ''
    pdT = 'Dashboard'
    ptitle = 'Profile'

    user=Customer.objects.get(user=User.objects.get(username=request.user))
    account = Account.objects.filter(customer=user)
    # return HttpResponse('skd')
    context = {'account': account,'pdToggle': pdToggle, 'pdT': pdT, 'ptitle': ptitle}
    for a in account:
        if a.accountType == "Savings":
            return render(request, 'bank/profile.html', context)
        else:
            return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def page(request, file_name):
    f = default_storage.open(f"pages/{file_name}.html")
    page = f.read().decode("utf-8")

    return JsonResponse({"page": page}, status=200)


@csrf_exempt
@login_required
def check(request):
    data = json.loads(request.body)
    check = data.get('check')
    if check == 'accountNumber':
        x = Account.objects.filter(accountNum=data.get('accNum')).count()
        print(x)
        if x == 1:
            res = Account.objects.filter(accountNum=data.get('accNum'))
            for res in res:
                fname = res.customer.fname
                lname = res.customer.lname
                accName = f"{lname} {fname}"
                return JsonResponse({"accName": accName}, status=200)
        else:
            return JsonResponse({"accName": "None"}, status=404)

    elif check == 'transPin':
        x = Account.objects.filter(customer=Customer.objects.get(user=request.user), transactionPin=data.get('transPin')).count()
        if x == 1:
            res = Account.objects.filter(customer=Customer.objects.get(user=request.user), transactionPin=data.get('transPin'))
            return JsonResponse({"message": 'ok'}, status=200)
        else:
            return JsonResponse({"message": 'None'}, status=404)

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bank/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "bank/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        fname = (request.POST["fname"]).capitalize()
        lname = (request.POST["lname"]).capitalize()
        username = request.POST["email"]
        accountType = request.POST['accountType']
        transcPin = request.POST['transcPin']
        dob = request.POST["dob"]
        tel = request.POST["tel"]
        address = request.POST["address"]
        # photo = request.FILES["photo"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bank/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            email=''
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError as e:
            print(e)
            return render(request, "bank/register.html", {
                "message": "Email address already taken."
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

        accountNum = random_with_N_digits(10)
        print(accountNum)
        rUser = str(request.user).capitalize()
        user=Customer.objects.get(user=User.objects.get(username=rUser))
        account = Account(customer=user, accountNum=accountNum, accountType=accountType, balance=10000, transactionPin=transcPin)
        account.save()

        staffs = Staff.objects.filter(
            name=User.objects.get(username=str(manager)))
        for staff in staffs:
            staff.totalCustomer = int(staff.totalCustomer)+1
            staff.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bank/register.html")
