from django.contrib.auth.models import User
from django.db import models

class Staff(models.Model):
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
        return f"{self.accountNum}"

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.transcType}"

class Notification(models.Model):
    user = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True, related_name="note_user")
    sender = models.ForeignKey("Staff", on_delete=models.PROTECT, null=True, blank=True, related_name="note_sent")
    recipients = models.ManyToManyField("Customer", related_name="note_received")
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            # "timestamp": self.timestamp,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "read": self.read
        }