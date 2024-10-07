from django.shortcuts import render, redirect
from .models import Expense, Category
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def list_expenses(request):
    if request.user.is_authenticated:  
        expenses = Expense.objects.filter(user=request.user)  
    else:
        expenses = Expense.objects.none()  

    return render(request, 'expenses/list_expenses.html', {'expenses': expenses})

@login_required
def add_expense(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')

        if not date or not description or not amount or not payment_method or not category_id:
            return render(request, 'expenses/add_expense.html', {
                'error': 'Please fill out all fields.',
                'categories': categories
            })

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'expenses/add_expense.html', {
                'error': 'Category does not exist.',
                'categories': categories
            })
            amount = float(amount)  # Validate amount as a number
        except ValueError:
            return render(request, 'expenses/add_expense.html', {
                'error': 'Please enter a valid number for amount.',
                'categories': categories
            })

        
        expense = Expense(
            user=request.user,
            date=date,
            description=description,
            category=category,
            amount=amount,
            payment_method=payment_method
        )
        expense.save()

        return redirect('list_expenses')

    return render(request, 'expenses/add_expense.html', {'categories': categories})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('add_expense')
        else:
            messages.error(request, 'Invalid username or password.')
            print("Authentication failed.")
    return render(request, 'expenses/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    
    return render(request, 'expenses/register.html')
