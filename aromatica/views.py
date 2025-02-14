from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserAccount, ChangePasswordForm, UserProfileForm
from billing.forms import ShippingForm
from billing.models import ShippingAddress

def category(request, cat):
    #replace any hyohens with spaces
    cat = cat.replace('-', ' ')
    #collect category from url
    try:
        #look for category
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("Category Not Found"))
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserAccount(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
        
    
    return render(request, 'update_user.html', {})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Password sucessfully updated")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    
    else:
        messages.success(request, "Password Update Failed")
        return redirect('home')
    
def update_profile(request):
    if request.user.is_authenticated:
        #get current user's shipping info 
        #current_user, created = Profile.objects.get_or_create(user=request.user)
        current_user = Profile.objects.get(user=request.user)

        shipping_user = ShippingAddress.objects.get(user=request.user)

        #get og form
        form = UserProfileForm(request.POST or None, instance=current_user)

        #get users billing form

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)


        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
 
            return redirect('home')
        return render(request, 'update_profile.html', {'form':form, 'shipping_form':shipping_form})
        
    else:
        return redirect('home')




def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Log In Successful"))
            return redirect('home')
        
        else:
            messages.success(request, ("email or password was incorrect please try again"))
            return redirect('login')
    else: 
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Log Out Sucessful"))
    return redirect('home')

def register_user(request):
    form = SignUpForm
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #log user into aromatica account
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Your Aromatica account has successfully been created "))
            return redirect('update_profile')
        
        else:
            messages.success(request, ("Registration unsuccessful please input details again"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

    

    
    
    