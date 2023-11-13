from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars':cars})

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

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        if created:
            user.set_password(password1)
            user.save()

        location, created = Location.objects.get_or_create(city=city.lower())

        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={'phone': phone, 'location': location, 'type': "Customer"}
        )

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

def search_results(request):
    if request.method == 'POST':
        city = request.POST.get('city', '').lower()
        vehicles_list = Car.objects.filter(location__city=city, is_available=True)
        return render(request, "search_results.html", {'vehicles_list': vehicles_list})
    return redirect('index') 

def car_rent(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cost_per_day = int(car.rent)

    if request.method == "POST":
        days = request.POST.get('days')

        if days.isdigit():
            days = int(days)
            user = request.user
            car_dealer = car.car_dealer
            rent = cost_per_day * days

            if car.is_available:
                car.is_available = False
                car.save()
                order = Order(user=user, car_dealer=car_dealer, car=car, rent=rent, days=days)
                order.save()

                return redirect('past_orders')
            else:
                return HttpResponse("Car is not available")
        else:
            return HttpResponse("Please enter a valid number of days")

    return render(request, 'car_rent.html', {'car': car, 'cost_per_day': cost_per_day})

def car_dealer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    user1 = CarDealer.objects.get(car_dealer=user)
                    if user1.type == "Car Dealer":
                        login(request, user)
                        return redirect(request.GET.get('next', '/all_cars'))
                    else:
                        alert = True
                        return render(request, "car_dealer_login.html", {"alert": alert})
                except CarDealer.DoesNotExist:
                    alert = True
                    return render(request, "car_dealer_login.html", {"alert": alert})
    return render(request, "car_dealer_login.html")

def car_dealer_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        city = request.POST['city']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return redirect('/car_dealer_signup')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save()
        try:
            location = Location.objects.get(city = city.lower())
        except:
            location = None
        if location is not None:
            car_dealer = CarDealer(car_dealer=user, phone=phone, location=location, type="Car Dealer")
        else:
            location = Location(city = city.lower())
            location.save()
            location = Location.objects.get(city = city.lower())
            car_dealer = CarDealer(car_dealer = user, phone=phone, location=location, type="Car Dealer")
        car_dealer.save()
        return render(request, "car_dealer_login.html")
    return render(request, "car_dealer_signup.html")

def all_cars(request):
    dealer = CarDealer.objects.filter(car_dealer=request.user).first()
    cars = Car.objects.filter(car_dealer=dealer)
    return render(request, "all_cars.html", {'cars':cars})

def add_car(request):
    if request.method == "POST":
        car_name = request.POST['car_name']
        city_name = request.POST['city']
        image = request.FILES['image']
        capacity = request.POST['capacity']
        rent = request.POST['rent']
        car_dealer = CarDealer.objects.get(car_dealer=request.user)

        location, created = Location.objects.get_or_create(city=city_name)

        car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
        car.save()

        alert = True
        return render(request, "add_car.html", {'alert': alert})

    return render(request, "add_car.html")

def all_orders(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        if order.is_complete == False:
            all_orders.append(order)
    return render(request, "all_orders.html", {'all_orders':all_orders})

def earnings(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    total_earnings = CarDealer.objects.aggregate(Sum('earnings'))['earnings__sum']
    all_orders = []
    for order in orders:
        all_orders.append(order)
    return render(request, "earnings.html", {'amount':total_earnings, 'all_orders':all_orders})

def edit_car(request, myid):
    car = Car.objects.filter(id=myid)[0]
    if request.method == "POST":
        car_name = request.POST['car_name']
        city = request.POST['city']
        capacity = request.POST['capacity']
        rent = request.POST['rent']

        car.name = car_name
        car.city = city
        car.capacity = capacity
        car.rent = rent
        car.save()

        try:
            image = request.FILES['image']
            car.image = image
            car.save()
        except:
            pass
        alert = True
        return render(request, "edit_car.html", {'alert':alert})
    return render(request, "edit_car.html", {'car':car})

def delete_car(request, myid):
    if not request.user.is_authenticated:
        return redirect("/car_dealer_login")
    car = Car.objects.filter(id=myid)
    car.delete()
    return redirect("/all_cars")

def delete_order(request, myid):
    order = Order.objects.filter(id=myid)
    order.delete()
    return redirect("/past_orders")

def order_details(request):
    car_id = request.POST['id']
    username = request.user
    user = User.objects.get(username=username)
    days = request.POST['days']
    car = Car.objects.get(id=car_id)
    if car.is_available:
        car_dealer = car.car_dealer
        rent = (int(car.rent))*(int(days))
        car_dealer.earnings += rent
        car_dealer.save()
        try:
            order = Order(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days)
            order.save()
        except:
            order = Order.objects.get(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days)
        car.is_available = False
        car.save()
        return render(request, "order_details.html", {'order':order})
    return render(request, "order_details.html")

@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user == order.user and not order.is_complete:
        order.is_complete = True
        order.save()

        if order.is_complete:
            customer = request.user
            customer_orders = Order.objects.filter(user=customer)
            if order not in customer_orders:
                order.user = customer
                order.save()

        return redirect('past_orders')
    elif request.user == order.car_dealer.car_dealer:
        if order.is_complete:
            return HttpResponse("This order is already complete.")
        else:
            order.is_complete = True
            order.save()
            return redirect('all_orders')
    else:
        raise Http404("Order not found or you are not authorized to complete this order")

@login_required
def past_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_complete=True)

    return render(request, 'past_orders.html', {'all_orders': orders})