from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from my_App.utils import detectUser
from .models import User, UserProfile
from .forms import UserForm



# Create your views here.

def index(request):
    # Render the index.html template
    return render(request, 'index.html')

def registerUser(request):
    # Render the registerUser.html template
    
    # Checks if the user is already logged in
    if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in!')
            return redirect('dashboard')
        
    elif request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']  # hashing password
            user = form.save(commit=False)            #this assigns a role to the user registring
            user.set_password(password)               # hashing password contd.
            user.role = User.CUSTOMER                 #this assigns a role to the user registring as a customer
            user.save()                               # this line saves the user
            messages.success(request, 'Account created successfully!')     # displays a success message when account is created before redirecting
            
            return redirect('logregisterUserin')
        
        else:
            print('invalid form')
            print(form.errors)
    else:
      form = UserForm()
      
    context = {
        'form': form,
    }
        
    return render(request, 'registerUser.html', context)

    
   


def login(request):
    # Render the login.html template
    
     if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in!')
            return redirect('calculator')
        
        # logs in the credentials if correct
     elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        #if user credentials are correct
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('calculator')
        
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
     return render(request, 'login.html')

    
def logout(request): 
    auth.logout(request)
    messages.info(request, 'logged out!')
    return redirect('login')



def calculator(request):
    # Render the calculate.html template
    
    #context = {
       # 'first_name': request.user.first_name,  # Pass the logged-in user's first name
   # }
    return render(request, 'calculator.html',)

def result(request):
    # Retrieve query parameters
    age = request.GET.get('age')
    bmi = request.GET.get('bmi')
    status = request.GET.get('status')
    comments = request.GET.get('comments', '')

    # Validate parameters
    if not age or not bmi or not status:
        return render(request, 'calculator.html', {'error': 'Missing required fields.'})

    # Pass data to the result template
    context = {
        'age': age,
        'bmi': bmi,
        'status': status,
        'comments': comments,
    }
    return render(request, 'result.html', context)


def dashboard(request):
    # Render the calculate.html template
    
    context = {
        'first_name': request.user.first_name,  # Pass the logged-in user's first name
    }
    return render(request, 'dashboard.html', context)





# My Account

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


# For dashboard
@login_required(login_url='login')
def customerDashboard(request):
     return render(request, 'accounts/customerDashboard.html')