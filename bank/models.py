from django.contrib.auth.models import User
from django.db import models

class Staff(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=200, default="manager")
    totalCustomer = models.IntegerField(default=0)

    def __str__(self):
        return self.name.username
        
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    dob = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.fname

class Account(models.Model):
    customer = models.ManyToManyField("Customer", related_name="emails_received")
    accountNum = models.IntegerField(null=True, blank=True)
    accountType = models.CharField(default="savings", max_length=200)
    balance = models.FloatField(default=0.00)
    transactionPin = models.IntegerField(default=1234)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accountNum}"

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class History(models.Model):
    INCOME = 'income'
    EXPENDITURE = 'expenditure'
    
    TRANSC_TYPE =(
      (INCOME,'INCOME'),
      (EXPENDITURE,'EXPENDITURE')
      )
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # type = income (True) or expenditure (False)
    transcType = models.CharField(max_length=20, choices=TRANSC_TYPE)
    amount = models.FloatField(default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.transcType}"

class Notification(models.Model):
    pass