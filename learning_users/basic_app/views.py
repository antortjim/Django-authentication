from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

# The decorator makes sure that the user is already logged in before logging logout
# i.e being login is required
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Dont commit yet, in case there's a collision
            profile = profile_form.save(commit=False)
            profile.user = user

            # check pic is provided
            if 'profile_pic'  in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            # registration was succesful
            registered = True
        else:
            # the forms were not validated
            print(user_form.errors, profile_form.errors)
    else:
        # the request was made via http
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                             {'user_form': user_form,
                             'profile_form':profile_form,
                             'registered':registered})



def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                print("{} logged in".format(username))
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")

        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request, 'basic_app/login.html',{})
