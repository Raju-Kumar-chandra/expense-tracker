from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout, authenticate)
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, UserProfile
from .forms import RegisterForm, ExpenseForm, IncomeForm


def home(request):

    return render(request, 'tracker/home.html')


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            profile, created = UserProfile.objects.get_or_create(
                user=user
                )

            login(request, user)

            return redirect('dashboard')

        else:

            print(form.errors)

    else:

        form = RegisterForm()

    return render(request, 'tracker/register.html', {
        'form': form
    })

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

    return render(
        request,
        'tracker/login.html'
    )

@login_required
def dashboard(request):

    search_query = request.GET.get('search')

    expenses = Expense.objects.filter(
        user=request.user
    )

    if search_query:

        expenses = expenses.filter(
            title__icontains=search_query
        )

    incomes = Income.objects.filter(
        user=request.user
    )

    total_expense = 0
    total_income = 0

    for expense in expenses:
        total_expense += expense.amount

    for income in incomes:
        total_income += income.amount

    balance = total_income - total_expense

    current_month = datetime.now().month

    monthly_expenses = Expense.objects.filter(
    user=request.user,
    date__month=current_month
    )

    monthly_total = 0
    for expense in monthly_expenses:
        monthly_total += expense.amount
    return render(request, 'tracker/dashboard.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'total_income': total_income,
        'balance': balance,
        'monthly_total': monthly_total,
    })

@login_required
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            return redirect('dashboard')

    else:

        form = ExpenseForm()

    return render(request, 'tracker/add_expense.html', {
        'form': form
    })


def logout_view(request):

    logout(request)

    return redirect('home')

from django.shortcuts import get_object_or_404
@login_required
def delete_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    expense.delete()

    return redirect('dashboard')

@login_required
def edit_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = ExpenseForm(instance=expense)

    return render(
        request,
        'tracker/edit_expense.html',
        {
            'form': form,
            'expense': expense
        }
    )

@login_required
def add_income(request):

    if request.method == 'POST':

        form = IncomeForm(request.POST)

        if form.is_valid():

            income = form.save(commit=False)

            income.user = request.user

            income.save()

            return redirect('dashboard')

    else:

        form = IncomeForm()

    return render(request, 'tracker/add_income.html', {
        'form': form
    })

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
    user=request.user
)

    expenses = Expense.objects.filter(
        user=request.user
    )

    incomes = Income.objects.filter(
        user=request.user
    )

    total_expense = 0
    total_income = 0

    for expense in expenses:
        total_expense += expense.amount

    for income in incomes:
        total_income += income.amount

    balance = total_income - total_expense

    return render(request, 'tracker/profile.html', {

        'profile': profile,

        'total_income': total_income,

        'total_expense': total_expense,

        'balance': balance,
    })

@login_required
def upload_profile_photo(request):

    if request.method == 'POST':

        profile, created = UserProfile.objects.get_or_create(
    user=request.user)

        if request.FILES.get('profile_image'):

            profile.profile_image = request.FILES[
                'profile_image'
            ]

            profile.save()

    return redirect('profile')