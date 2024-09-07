

# Create your views here.
from django.shortcuts import render,redirect
from userauthentication.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages   #to display msg to the user
from django.conf import settings     #To connect settings.py
from userauthentication.models import User



# User = settings.AUTH_USER_MODEL   #connected the AUTH_USER_MODEL in settings

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():  #checking if it is valid data or malicious data
            new_user = form.save()
            username = form.cleaned_data.get("username") #grabbing the username
            messages.success(request, f"Hey {username}, Your account was created succesfully ")  #shows a message to super user that user created
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password = form.cleaned_data['password1']
            )
            login(request,new_user)
            return redirect("Backend:index")
    else:
        form = UserRegisterForm()

    context = {
        'form':form
    }
    return render(request,"userauthentication/sign_up.html",context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey.. You are already logged in")
        return redirect("Backend:index")
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:                              #To Handle errors
            user=User.objects.get(email=email)           #we use get instead of all because we need the data of only one customer at a time
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                return redirect("Backend:index")
            else:
                messages.warning(request, "User Does Not Exist, Create An Account")
        except:
            messages.warning(request, f"user with {email} does not exist")

        #functionality that automatically log the user if there is actually a user with such email


    return render(request,"userauthentication/sign_in.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You Have Logged Out")

    return redirect("userauthentication:sign_in")


