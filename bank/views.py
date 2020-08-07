import json
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

def index(request):
  pdToggle = 'profile'
  pdT='Profile'
  
  context={'pdToggle':pdToggle, 'pdT':pdT}
  return render(request, 'bank/index.html', context)
  
def profile(request):
  pdToggle = ''
  pdT='Dashboard'
  
  context={'pdToggle':pdToggle, 'pdT':pdT}
  return render(request, 'bank/profile.html', context)

@csrf_exempt
def page(request, file_name):
  f = default_storage.open(f"bank/templates/bank/{file_name}.html")
  page = f.read().decode("utf-8")
  
  return JsonResponse({"page":page}, status=200)