from django.contrib.auth.models import User
from django.db import models
from time import gmtime, strftime

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, default="manager")
    email = models.CharField(max_length=200, null=True)
    whatsappNum = models.CharField(max_length=200, null=True)
    totalCustomer = models.IntegerField(default=0)

    def __str__(self):
        return self.fullName
        
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    tel = models.CharField(max_length=200, null=True)
    dob = models.CharField(max_length=200, null=True)

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "user": self.user.username,
    #         "manager": self.manager,
    #         "fname": self.fname,
    #         "lname": self.lname,
    #         "email": self.email,
    #         "address": self.address,
    #         "tel": self.tel,
    #         "dob": self.dob
    #     }

    def __str__(self):
        return self.user.username

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="customer")
    accountNum = models.IntegerField(null=True, blank=True)
    accountType = models.CharField(default="Savings", max_length=200)
    balance = models.FloatField(default=0.00)
    transactionPin = models.IntegerField(default=1234)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.lname} {self.customer.fname}"

class History(models.Model):
    INCOME = 'Income'
    EXPENDITURE = 'Expenditure'
    
    TRANSC_TYPE =(
      (INCOME,'INCOME'),
      (EXPENDITURE,'EXPENDITURE')
    )

    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    transcType = models.CharField(max_length=20, choices=TRANSC_TYPE)
    amount = models.FloatField(default=0.00)
    naration = models.TextField(blank=True)
    transactionId = models.IntegerField(default=0)
    timestamp = models.CharField(max_length=200, null=True, blank=True)
    seen = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "account": self.account.accountNum,
            "transcType": self.transcType,
            "amount": self.amount,
            "naration": self.naration,
            "transactionId": self.transactionId,
            "timestamp": self.timestamp,
            "seen": self.seen
        }
    
    # def __str__(self):
    #     return f"{self.transactionId}"

class AccountSummary(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.summary

class Notification(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    sender = models.CharField(max_length=200, default='3NITY BANK')
    subject = models.CharField(max_length=255, null=True, blank=True, default='Expenditure')
    body = models.TextField(blank=True)
    timestamp = models.CharField(max_length=200, null=True, blank=True)
    seen = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "account": self.account.accountNum,
            "sender": self.sender,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp,
            "seen": self.seen
        }