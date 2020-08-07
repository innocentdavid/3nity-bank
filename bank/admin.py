from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(History)
admin.site.register(Notification)