from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json
from .models import Expense, Category
from .forms import RegisterForm, ExpenseForm, CategoryForm
from django.contrib.auth import logout

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'expenseapp/register.html', {'form': form})

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # YE 2 LINES NAYA ADD KIYA - Remaining ke liye
    budget = 2000
    remaining = budget - int(total)

    cat_data = expenses.values('category__name').annotate(total=Sum('amount'))
    labels = [c['category__name'] for c in cat_data]
    data = [float(c['total']) for c in cat_data]

    return render(request, 'expenseapp/dashboard.html', {
        'expenses': expenses,
        'total': total,
        'remaining': remaining,  # YE BHI ADD KARO
        'budget': budget,
        'labels': json.dumps(labels),
        'data': json.dumps(data)
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenseapp/add_expense.html', {'form': form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)  
            cat.user = request.user       
            cat.save()                    
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'expenseapp/add_category.html', {'form': form})

@login_required
def delete_expense(request, id):
    exp = get_object_or_404(Expense, id=id, user=request.user)
    exp.delete()
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')