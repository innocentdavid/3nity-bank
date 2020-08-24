import json
import random

from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
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

# random transaction id and account number


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# @login_required

@login_required
def index(request):
    try:
        user = Customer.objects.get(
            user=User.objects.get(username=request.user))
        account = Account.objects.filter(customer=user)

        context = {'account': account}
        return render(request, 'bank/index.html', context)
    except:
        count = Staff.objects.filter(user=User.objects.get(username=request.user)).count()
        if count >= 1:
            return HttpResponseRedirect(reverse("staff"))
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def getNotificationCount(request):
    try:
        user = Customer.objects.get(user=User.objects.get(username=request.user))
        account = Account.objects.get(customer=user)
        count = Notification.objects.filter(account=account, seen=False).count()
        if count >= 1:
            return JsonResponse({"result": count})
        else:
            return JsonResponse({"message": 'Not found!'})
    except:
        return JsonResponse({"result": 0})


@csrf_exempt
def getNotification(request):

    user = Customer.objects.get(user=User.objects.get(username=request.user))
    account = Account.objects.get(customer=user)
    count = Notification.objects.filter(account=account, seen=False).count()
    if count >= 1:
        result = Notification.objects.filter(account=account, seen=False).order_by('-pk')

        return JsonResponse([notification.serialize() for notification in result], safe=False)
    else:
        return JsonResponse({"message": 'Not found!'})

@csrf_exempt
def notfChecked(request):
    data = json.loads(request.body)
    notfId = data.get('notfId')
    notf = Notification.objects.filter(pk=notfId)
    for n in notf:
        n.seen=True
        n.save()

@csrf_exempt
def transfer(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    data = json.loads(request.body)

    # bank = data.get('bank')
    accNum = data.get('accNum')
    amount = data.get('amount')
    category = data.get('catg')
    naration = data.get('naration')
    transPin = data.get('transPin')
    date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    transcId = datetime.now().strftime('%Y%m%d%H%M%S')

    # deduct from user's account
    user = Customer.objects.get(user=User.objects.get(username=request.user))
    acc = Account.objects.filter(customer=user, transactionPin=transPin)
    for a in acc:
        newAmount = a.balance - round(float(amount), 2)
        a.balance = round(newAmount, 2)
        a.save()

        receiver = Account.objects.get(accountNum=accNum)
        sender = Account.objects.get(
            customer=Customer.objects.get(user=request.user))

        senderNaration = f"Your Account was Debited with NGN {data.get('amount')} for {naration} on {date} Your Balance now is NGN {a.balance}"

        senderNotification = Notification(account=sender, body=senderNaration, timestamp=date)
        senderNotification.save()

        senderHistory = History(account=sender, category=category,
                                transcType='Expenditure', amount=amount, naration=senderNaration, timestamp=date)
        senderHistory.save()

        accTo = Account.objects.filter(accountNum=accNum)
        for to in accTo:
            newAmount = to.balance + float(amount)
            to.balance = newAmount
            to.save()

            receiverNaration = f"Your Account was Credited with NGN {data.get('amount')} for {naration} on {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"

            receiverNotification = Notification(
                account=sender, body=receiverNaration, timestamp=date)
            receiverNotification.save()

            receiverHistory = History(
                account=receiver, category='', transcType='Income', amount=amount, naration=receiverNaration, timestamp=date)
            receiverHistory.save()

            return JsonResponse({"message": 'ok', "transcId": transcId, "date": date}, status=200)

        return JsonResponse({"message": 'error'}, status=200)

    return JsonResponse({"message": 'error'}, status=200)


@csrf_exempt
@login_required
def getExpSumr(request):
    data = json.loads(request.body)
    x = data.get('expCatg')
    expCatg = x.capitalize()

    user = Customer.objects.get(user=User.objects.get(username=request.user))
    account = Account.objects.get(customer=user)
    h = History.objects.filter(
        account=account, category=expCatg, transcType='Expenditure').count()
    if h >= 1:
        histories = History.objects.filter(
            account=account, category=expCatg, transcType='Expenditure').order_by('-pk')
        return JsonResponse([history.serialize() for history in histories], safe=False)
    else:
        return JsonResponse({"message": 'No history for this category'}, status=200)

@csrf_exempt
@login_required
def staff(request):
    try:
        q = request.GET['q']
        user = User.objects.get(username=request.user)
        count = Staff.objects.filter(user=user).count()
        if count >= 1:
            staff = Staff.objects.get(user=user)    
            countA = Account.objects.filter(accountNum=request.GET['q']).count()
            if countA < 1:
                customers = Customer.objects.filter(manager=staff)
                context = {"staff": staff, "customers": customers, 'error':'ACCOUNT NOT FOUND! OR CUSTOMER NOT ONE OF YOUR CLIENTS', 'closeErr':'btn fa fa-window-close'}
                return render(request, 'bank/staff.html', context)
            account = Account.objects.filter(accountNum=request.GET['q'])
            for a in account:
                username = a.customer.user.username
                customers = Customer.objects.filter(user=User.objects.get(username=username), manager=staff)
                context = {"staff": staff, "customers": customers}
                    
                return render(request, 'bank/staff.html', context)
        else:
            return HttpResponseRedirect(reverse('index'))

    except:
        user = User.objects.get(username=request.user)
        count = Staff.objects.filter(user=user).count()
        if count >= 1:
            staff = Staff.objects.get(user=user)
            customers = Customer.objects.filter(manager=staff)
            context = {"staff": staff, "customers": customers}
            return render(request, 'bank/staff.html', context)
        else:
            return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def allCustomer(request):
    data = json.loads(request.body)
    user = Customer.objects.get(user=User.objects.get(username=data.get('user')))
    account = Account.objects.get(customer=user)
    count = History.objects.filter(account=account).count()
    if count == 0:
        return JsonResponse({"message": 'No recent transaction!'})
    else:
        user = Customer.objects.get(
            user=User.objects.get(username=data.get('user')))
        account = Account.objects.get(customer=user)
        histories = History.objects.filter(account=account).order_by('-pk')

        return JsonResponse([history.serialize() for history in histories], safe=False)


@csrf_exempt
def totalIncome(request):
    lweek = timezone.now().date() - timedelta(days=7)
    mlweek = lweek - timedelta(days=(lweek.isocalendar()[2] - 1))
    mtweek = mlweek + timedelta(days=7)

    data = json.loads(request.body)
    user = Customer.objects.get(
        user=User.objects.get(username=data.get('user')))
    account = Account.objects.get(customer=user)
    transcType = (data.get("action")).capitalize()
    history = History.objects.filter(
        account=account, transcType=transcType).aggregate(Sum('amount'))
    # history = History.objects.filter(account=account, transcType=transcType,
    #                                  timestamp__gte=mlweek, timestamp__lt=mtweek).aggregate(Sum('amount'))

    return JsonResponse({'totalIncome': history})


@csrf_exempt
def totalCatgExp(request):
    lweek = timezone.now().date() - timedelta(days=7)
    mlweek = lweek - timedelta(days=(lweek.isocalendar()[2] - 1))
    mtweek = mlweek + timedelta(days=7)

    data = json.loads(request.body)
    if data.get('user') == 'request.user.username':
        user = Customer.objects.get(
            user=User.objects.get(username=request.user.username))
    else:
        user = Customer.objects.get(
            user=User.objects.get(username=data.get('user')))
    account = Account.objects.get(customer=user)
    history = History.objects.filter(
        account=account, transcType='Expenditure', category=data['catg']).aggregate(Sum('amount'))
    # history = History.objects.filter(account=account, transcType='Expenditure', category=data['catg'],
    #                                  timestamp__gte=mlweek, timestamp__lt=mtweek).aggregate(Sum('amount'))

    return JsonResponse({'totalCatgExp': history})


@csrf_exempt
def AcctSummary(request):
    data = json.loads(request.body)
    user = Customer.objects.get(
        user=User.objects.get(username=data.get('user')))
    account = Account.objects.get(customer=user)
    if data.get('action') == 'get':
        try:
            summary = AccountSummary.objects.filter(account=account)
            for s in summary:
                return JsonResponse({'summary': s.summary})
            return JsonResponse({'summary': ''})
        except:
            return JsonResponse({'summary': ''})

    else:
        count = AccountSummary.objects.filter(account=account).count()
        if count <= 0:
            summary = AccountSummary(account=account, summary=data['summary'])
            summary.save()
            return JsonResponse({'message': 'ok'})
        else:
            summary = AccountSummary.objects.filter(account=account)
            for x in summary:
                x.summary = data['summary']
                x.save()

                return JsonResponse({'message': 'ok'})
            return JsonResponse({'message': 'error'})


@csrf_exempt
@login_required
def allCustomeComplaints(request):
    return JsonResponse({"message": 'No recent transaction!'})


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
        y = Account.objects.filter(customer=Customer.objects.get(
            user=request.user), accountNum=data.get('accNum')).count()
        if y == 1:
            return JsonResponse({"accName": 'error'}, status=200)

        x = Account.objects.filter(accountNum=data.get('accNum')).count()
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
        x = Account.objects.filter(customer=Customer.objects.get(
            user=request.user), transactionPin=data.get('transPin')).count()
        if x == 1:
            res = Account.objects.filter(customer=Customer.objects.get(
                user=request.user), transactionPin=data.get('transPin'))
            return JsonResponse({"message": 'ok'}, status=200)
        else:
            return JsonResponse({"message": 'None'}, status=404)


@csrf_exempt
@login_required
def airtime(request):
    data = json.loads(request.body)
    user = Customer.objects.get(user=User.objects.get(username=request.user))
    account = Account.objects.filter(customer=user)
    date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    for a in account:
        newBal = a.balance - float(data.get('baAmount'))
        a.balance = round(newBal, 2)

        transcId = datetime.now().strftime('%Y%m%d%H%M%S')
        naration = f"You have been debited with {data['baAmount']} for Airtime to: {data.get('baTel')} | {data.get('networkP')} | transaction id: {transcId}"

        notification = Notification(account=Account.objects.get(
            customer=Customer.objects.get(user=request.user)), body=naration, timestamp=date)
        history = History(account=Account.objects.get(customer=Customer.objects.get(user=request.user)), category='Miscellaneous',
                          transcType='Expenditure', amount=data.get('baAmount'), naration=naration, transactionId=transcId, timestamp=date)

        a.save()
        notification.save()
        history.save()

        return JsonResponse({"message": 'ok', "transcId": transcId, "date": date}, status=200)


@csrf_exempt
@login_required
def bill(request):
    data = json.loads(request.body)
    user = Customer.objects.get(user=User.objects.get(username=request.user))
    account = Account.objects.filter(customer=user)
    date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    for a in account:
        newBal = a.balance - float(data.get('billAmount'))
        a.balance = round(newBal, 2)

        transcId = datetime.now().strftime('%Y%m%d%H%M%S')
        naration = f"Bill for: {data.get('bill')} | {data.get('billId')} | transaction id: {transcId}"

        notification = Notification(account=Account.objects.get(
            customer=Customer.objects.get(user=request.user)), body=naration, timestamp=date)

        history = History(account=Account.objects.get(customer=Customer.objects.get(user=request.user)), category='Shelter',
                          transcType='Expenditure', amount=data.get('billAmount'), naration=naration, transactionId=transcId, timestamp=date)

        a.save()
        notification.save()
        history.save()

        return JsonResponse({"message": 'ok', "transcId": transcId, "date": date}, status=200)


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

            count = Staff.objects.filter(user=User.objects.get(username=request.user)).count()
            if count >= 1:
                return HttpResponseRedirect(reverse("staff"))
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bank/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "bank/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
        date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        # Ensure password matches
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bank/register.html", {
                "message": "Passwords must match."
            })

        managers = []
        staffs = Staff.objects.all()
        for staff in staffs:
            if staff is not None:
                managers.append(staff.user.username)
            else:
                return HttpResponse('<h1>This site is just created! so Please create a user (USERNAME = EXAMPLE@MAIL.COM) and then make him a STAFF in the STAFF MODULE in the /admin page</h1>')
        
        try:
            manager = random.choice(managers)
        except:
            return HttpResponse('<h1>This site is just created! so Please create a user (USERNAME = EXAMPLE@MAIL.COM) and then make him a STAFF in the STAFF MODULE in the /admin page</h1>')

        # Attempt to create new user
        try:
            email = ''
            ruser = User.objects.create_user(username, email, password)
            ruser.save()

        except IntegrityError:
            return render(request, "bank/register.html", {"message": "Email address already taken."})
        
        accountNum = random_with_N_digits(10)
        
        userM = User.objects.get(username=manager)
        userC = User.objects.get(username=username)
        customer = Customer(user=userC, manager=Staff.objects.get(user=userM), fname=fname,lname=lname, email=username, dob=dob, tel=tel, address=address)
        customer.save()

        user = Customer.objects.get(user=userC)
        account = Account(customer=user, accountNum=accountNum,accountType=accountType, balance=10000, transactionPin=transcPin)
        account.save()

        userAccount = Account.objects.get(accountNum=accountNum)
        receiverNaration = f"Your Account was Credited with NGN10,000 for WELCOME BONUS! on {date}"
        receiverNotification = Notification(account=userAccount, subject='Welcome Bonus', body=receiverNaration, timestamp=date)
        receiverNotification.save()

        receiverHistory = History(account=userAccount, category='', transcType='Income', amount=10000, naration=receiverNaration, timestamp=date)
        receiverHistory.save()

        staffs = Staff.objects.filter(user=User.objects.get(username=manager))
        for staff in staffs:
            staff.totalCustomer = int(staff.totalCustomer)+1
            staff.save()
            login(request, ruser)

            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "bank/register.html")
