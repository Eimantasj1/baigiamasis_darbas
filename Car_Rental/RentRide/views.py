from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "index.html")

def customer_signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        city = request.POST['city']

        if password1 != password2:
            return redirect("/customer_signup")

        # Create or get the User object
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        if created:
            user.set_password(password1)  # Set the password for the new user
            user.save()

        # Create or get the Location object
        location, created = Location.objects.get_or_create(city=city.lower())

        # Create the Customer object
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={'phone': phone, 'location': location, 'type': "Customer"}
        )

        # Automatically log in the user after registration
        login(request, user)

        alert = True
        return render(request, "customer_signup.html", {'alert': alert})

    return render(request, "customer_signup.html")


def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Customer.objects.get(user=user)
                if user1.type == "Customer":
                    login(request, user)
                    return redirect("/customer_homepage")
            else:
                alert = True
                return render(request, "customer_login.html", {'alert':alert})
    return render(request, "customer_login.html")

def logout_view(request):
    logout(request)
    return redirect('/')

def customer_homepage(request):
    return render(request, "customer_homepage.html")