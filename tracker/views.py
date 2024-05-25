from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Income, Expense, Budget
from .forms import IncomeForm, ExpenseForm,BudgetForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from decimal import Decimal 
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the desired page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request):
    # return render(request, 'registration/profile.html')
    return render(request, 'tracker/index.html')

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('all_incomes')
    else:
        form = IncomeForm()
    return render(request, 'tracker/add_income.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('all_expenses')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

def edit_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('all_incomes')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'tracker/edit_income.html', {'form': form})

def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('all_expenses')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})

def delete_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    income.delete()
    return redirect('all_incomes')

def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()

    total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expenses



    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
    }
    return render(request, 'tracker/index.html', context)


@login_required
def report(request):
    income_by_month = Income.objects.filter(user=request.user).extra(select={'month': 'strftime("%%Y-%%m", date)'}).values('month').annotate(total_amount=Sum('amount')).order_by('month')
    expense_by_month = Expense.objects.filter(user=request.user).extra(select={'month': 'strftime("%%Y-%%m", date)'}).values('month').annotate(total_amount=Sum('amount')).order_by('month')

    context = {
        'income_by_month': income_by_month,
        'expense_by_month': expense_by_month,
    }
    return render(request, 'tracker/report.html', context)


@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget_progress')
    else:
        form = BudgetForm()
    return render(request, 'tracker/add_budget.html', {'form': form})

@login_required
def budget_progress(request):
    budgets = Budget.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    budget_status = []

    for budget in budgets:
        spent = expenses.filter(category=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
        status = {
            'category': budget.category,
            'limit': budget.limit,
            'spent': spent,
            'remaining': budget.limit - spent,
        }
        budget_status.append(status)

    context = {'budget_status': budget_status}
    return render(request, 'tracker/budget_progress.html', context)



@login_required
def dashboard(request):
    # Get all incomes and expenses for the logged-in user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Calculate total income, total expenses, and total savings
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_savings = total_income - total_expenses

    # Calculate monthly income and expenses
    income_data = []
    expenses_data = []
    months = []

    for month in range(1, 13):
        month_name = datetime(1900, month, 1).strftime('%B')
        months.append(month_name)
        
        monthly_income = incomes.filter(date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        income_data.append(int(monthly_income))
        
        monthly_expenses = expenses.filter(date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_data.append(int(monthly_expenses))

    # Prepare context for rendering the template
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_savings': total_savings,
        'months': months,
        'income_data': income_data,
        'expenses_data': expenses_data,
    }
    
    return render(request, 'tracker/dashboard.html', context)


def chart_data(request):
    # Get all incomes and expenses for the logged-in user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Calculate total income, total expenses, and total savings
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_savings = total_income - total_expenses

    # Calculate monthly income and expenses
    income_data = []
    expenses_data = []
    months = []

    for month in range(1, 13):
        month_name = datetime(1900, month, 1).strftime('%B')
        months.append(month_name)
        
        monthly_income = incomes.filter(date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        income_data.append(int(monthly_income))
        
        monthly_expenses = expenses.filter(date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_data.append(int(monthly_expenses))

    data = {
        'months': months,
        'income_data': income_data,
        'expenses_data': expenses_data,
    }
    return JsonResponse(data)


@login_required
def all_incomes(request):
    all_incomes = Income.objects.filter(user=request.user)  # Assuming you have a way to filter incomes for the current user
    return render(request, 'tracker/all_incomes.html', {'all_incomes': all_incomes})


@login_required
def all_expenses(request):
    all_expenses = Expense.objects.filter(user=request.user)  # Assuming you have a way to filter expenses for the current user
    return render(request, 'tracker/all_expenses.html', {'all_expenses': all_expenses})


@login_required
def index(request):
    # Calculate total income, total expenses, and total savings
    all_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    all_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    all_savings = all_income - all_expenses

     # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Get selected year and month from GET parameters, default to current year and month
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', current_month))

    # Get the past 5 years
    years = [current_year - i for i in range(5)]
    # Define months
    months = [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    # Filter income and expenses based on selected year and month
    filtered_income = Income.objects.filter(date__year=selected_year, date__month=selected_month)
    filtered_expenses = Expense.objects.filter(date__year=selected_year, date__month=selected_month)
    total_income = filtered_income.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = filtered_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expenses

    context = {
        'all_income': all_income,
        'all_expenses': all_expenses,
        'all_savings': all_savings,
        'filtered_income': filtered_income,
        'filtered_expenses': filtered_expenses,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'years': years,
        'months': months,
        'selected_year': selected_year,
        'selected_month': selected_month
    }

    return render(request, 'tracker/index.html', context)