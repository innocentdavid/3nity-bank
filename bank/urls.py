from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # all other route
    path('staff', views.staff, name="staff"),
    path('check', views.check, name="check"),
    path('page/<str:file_name>', views.page, name='page'),
    path('transfer', views.transfer, name='transfer'),
    path('airtime', views.airtime, name='airtime'),
    path('bill', views.bill, name='bill'),
    path('getExpSumr', views.getExpSumr, name='getExpSumr'),
    path('getNotification', views.getNotification, name='getNotification'),
    path('notfChecked', views.notfChecked, name='notfChecked'),
    path('getNotificationCount', views.getNotificationCount, name='getNotificationCount'),
    path('allCustomer', views.allCustomer, name='allCustomer'),
    path('totalIncome', views.totalIncome, name='totalIncome'),
    path('totalCatgExp', views.totalCatgExp, name='totalCatgExp'),
    path('AcctSummary', views.AcctSummary, name='AcctSummary'),
]