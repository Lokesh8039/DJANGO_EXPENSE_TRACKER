from .models import TrackingHistory,CurrentBalance
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.warning(request , "User Not Found")
            return redirect("login_view")
        user = authenticate(username = username,password =password)
        if not user:
            messages.warning(request, "Password is Incorrect")
            return redirect("login_view")
        login(request ,user)
        return redirect("/")
    return render(request,"login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if not bool(username):
            messages.warning(request, "Enter user name") 
            return redirect('register_view')
        if not bool(password):
            messages.warning(request, "Enter user password") 
            return redirect('register_view')
        user = User.objects.filter(username = username)
        if user.exists():
            messages.warning(request, "User Alredy Taken") 
            return redirect('register_view')
        user1 = User.objects.create(username = username , first_name = first_name , last_name = last_name)
        user1.set_password(password)
        user1.save()
        messages.success(request , "Account Created")
        return redirect("login_view")

    return render(request,"register.html")

def logout_view(request):
    logout(request)
    return redirect("login_view")

@login_required(login_url="login_view")
def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        expense_type = "CREDIT"
        if float(amount) < 0:
            expense_type = "DEBIT"

        if float(amount) == 0:
            messages.success(request, "Amount cannot be zero") 
            return redirect('/')

        tracking_history = TrackingHistory.objects.create(amount = amount,
            expense_type = expense_type,
            current_balance = current_balance,
            description = description)
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()
        print(description,amount)
        return redirect('/')
    

    current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
    income = 0
    expense = 0
    
    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type == "CREDIT":
            income += tracking_history.amount
        else:
            expense += tracking_history.amount

    context = {'income' : income,
                'expense' : expense , 
                'transactions' : TrackingHistory.objects.all() , 'current_balance' : current_balance}
    return render(request, 'index.html' , context)




def delete(request,id):
    tracking_history = TrackingHistory.objects.filter(id=id)

    if tracking_history.exists():
        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
        tracking_history = tracking_history.first()
        current_balance.current_balance -= tracking_history.amount
        current_balance.save()
        tracking_history.delete()
    return redirect('/')