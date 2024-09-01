from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from user.models import Address

def signup(request):
    if request.user.is_authenticated:
        return redirect('all_products')
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #print(first_name, last_name, username, email, password)
        user_exists = False

        if User.objects.filter(username=username).exists():
            #print('Username already exists')
            messages.error(request, 'Username already exists')
            user_exists = True

        if User.objects.filter(email=email).exists():
            #print('Email already exists')
            messages.error(request, 'Email already exists')
            user_exists = True

        if user_exists:
            return render(request,'user/signup.html')
        
        user = User.objects.create_user(
            first_name= first_name, 
            last_name= last_name,
            username = username,
            email = email,
            password = password
        )
        user.save()
        messages.success(request, "Account created successfully")

    return render(request,'user/signup.html')

@never_cache
def signin(request):
    if request.user.is_authenticated:
         return redirect('all_products')
    
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is None:
                 messages.error(request, 'Invalid username or password')
                 return render(request,'user/signin.html')
            
            else:
                 login(request, user)
                 return redirect("all_products")
    return render(request,'user/signin.html')

def signout(request):
     logout(request)
     return render(request,"user/signin.html")

def profile(request):
     return render(request,'user/profile.html')

@login_required(login_url="/user/signin")
def profile(request):
     return render(request,'user/profile.html')

def add_addresses(request):
    if request.method == "POST":
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        locality = request.POST.get('locality')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        mobile = request.POST.get('mobile')
        
        address = Address(
               user = request.user,
               address1 = address1,
               address2 = address2,
               locality = locality,
               landmark = landmark,
               city = city,
               state = state,
               country = country,
               zip = zip,
               mobile = mobile
            )
        address.save()
        return redirect('check_out')