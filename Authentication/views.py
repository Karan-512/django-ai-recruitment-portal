from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

User = get_user_model()

def landing_page(request):
    return render(request, 'landing.html')



def login_view(request):

    # Prevent logged-in users from opening login again
    if request.user.is_authenticated:

        if request.user.role == 'jobseeker':
            return redirect('jobseeker_home')

        elif request.user.role == 'company':
            return redirect('company_home')


    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Empty field validation
        if not username or not password:
            messages.error(request, "Both fields are required!")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        # Invalid credentials
        if user is None:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

        # Login user
        login(request, user)

        # Success alert
        messages.success(request, f"Welcome {user.username}!")

        # Role-based redirect
        if user.role == 'jobseeker':
            return redirect('jobseeker_home')

        elif user.role == 'company':
            return redirect('company_home')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        cpass = request.POST.get("password2")
        role = request.POST.get("role")
        obj = User.objects.filter(username = email).exists()
        if obj:
            return render(request,'login.html',{"error":"User already exists. Please try again!"})
        elif(password != cpass):
            return render(request,'register.html',{"error":"Passwords don't match!"})
        else:
            User.objects.create_user(
                username=email,
                first_name=fname,
                last_name=lname,
                email=email,
                password=password,
                role=role)
            return redirect('login')
    else:
        return render(request, 'signup.html')

# @login_required
# def jobseeker_home(request):

#     if request.user.role != 'jobseeker':
#         messages.error(request, "Unauthorized access!")
#         return redirect('login')

#     return render(request, 'jobseeker_home.html')

# @login_required
# def company_home(request):

#     if request.user.role != 'company':
#         messages.error(request, "Unauthorized access!")
#         return redirect('login')

#     return render(request, 'company_home.html')
