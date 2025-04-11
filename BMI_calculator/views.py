from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

#def calculator(request):
 #   return render(request, 'calculator.html')


#def result(request):
#    return render(request, 'result.html')

#def registerUser(request):
 #   return render(request, 'registerUser.html')

#def login(request):
 #   return render(request, 'login.html')

