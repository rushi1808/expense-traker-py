from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import User, Budget, Expense, BudgetCategory
from .forms import RegisterForm, LoginForm, ExpenseForm, BudgetForm
import re
import json
from datetime import datetime, timedelta
from django.db.models import Sum
from collections import defaultdict

def home(request):
    if request.session.get('user_id'):
        return redirect('user_dashboard')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
                messages.error(request, 'Password must contain at least 8 characters including at least one uppercase letter, one lowercase letter, and one digit.')
                return render(request, 'register.html', {'form': form})
            
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                messages.error(request, 'Invalid email format.')
                return render(request, 'register.html', {'form': form})
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return render(request, 'register.html', {'form': form})
            
            user = User(username=username, password=password, email=email)
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                return redirect('user_dashboard')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)
    current_budget = Budget.objects.filter(user=user).first()
    
    if not current_budget:
        return render(request, 'user_dashboard.html', {'message': 'No budget found.'})
    
    # Top expense day in last week
    date_threshold = datetime.now() - timedelta(days=7)
    top_expense_day = Expense.objects.filter(user=user, date__gte=date_threshold).values('date').annotate(total=Sum('amount')).order_by('-total').first()
    top_expense_date = top_expense_day['date'] if top_expense_day else None
    
    # Recent expenses
    recent_expenses = Expense.objects.filter(user=user).order_by('-date')[:5]
    
    # Budget summary
    total_expenses = Expense.objects.filter(user=user, budget=current_budget).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = current_budget.monthly_income - total_expenses
    budget_spent_percentage = (total_expenses / current_budget.monthly_income) * 100 if current_budget.monthly_income > 0 else 0
    
    expense_breakdown_qs = Expense.objects.filter(user=user, budget=current_budget).values('category').annotate(amount=Sum('amount')).order_by('category')
    expense_breakdown = {item['category']: float(item['amount']) for item in expense_breakdown_qs}

    context = {
        'current_budget': current_budget,
        'remaining_budget': remaining_budget,
        'budget_spent_percentage': budget_spent_percentage,
        'recent_expenses': recent_expenses,
        'top_expense_day': top_expense_date.strftime('%Y-%m-%d') if top_expense_date else None,
        'expense_breakdown': json.dumps(expense_breakdown),
        'budget_name': current_budget.name,
        'total_expenses': total_expenses,
    }
    return render(request, 'user_dashboard.html', context)

def expense_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    expenses = Expense.objects.filter(user=user)
    return render(request, 'expense_list.html', {'expenses': expenses})

def expense_create(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    selected_budget_id = request.session.get('selected_budget_id')
    if not selected_budget_id:
        messages.error(request, 'Please select a budget first.')
        return redirect('budget_list')
    
    budget = Budget.objects.get(id=selected_budget_id, user=user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = user
            expense.budget = budget
            category = expense.category
            if category == 'Other' and 'custom_category' in request.POST:
                expense.category = request.POST['custom_category']
            
            # Check budget allocation
            budget_category = BudgetCategory.objects.filter(budget=budget, category=expense.category).first()
            if budget_category:
                allocated_amount = budget.monthly_income * (budget_category.allocated_percentage / 100)
                spent = Expense.objects.filter(user=user, category=expense.category).aggregate(Sum('amount'))['amount__sum'] or 0
                if spent + expense.amount > allocated_amount:
                    messages.warning(request, 'Warning: You are exceeding the allocated budget for this category.')
            
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expense_form.html', {'form': form})

def expense_edit(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    expense = get_object_or_404(Expense, pk=pk, user=user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_form.html', {'form': form})

def expense_delete(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    expense = get_object_or_404(Expense, pk=pk, user=user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expense_confirm_delete.html', {'expense': expense})

def budget_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    budgets = Budget.objects.filter(user=user)
    return render(request, 'budget_list.html', {'budgets': budgets})

def budget_create(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    # For simplicity, create budget form, but for custom with categories, need more
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = user
            budget.save()
            # Assume categories are added separately or in form
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'budget_form.html', {'form': form})

def select_budget(request, pk):
    request.session['selected_budget_id'] = pk
    return redirect('expense_create')

def budget_delete(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    budget = get_object_or_404(Budget, pk=pk, user=user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'budget_confirm_delete.html', {'budget': budget})

def reports_expenses_summary(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)

    expenses_by_category = Expense.objects.filter(user=user).values('category').annotate(amount=Sum('amount')).order_by('category')

    # SQLite-compatible: group by month/year in Python
    all_expenses = Expense.objects.filter(user=user).order_by('date')
    monthly_totals = defaultdict(float)
    for exp in all_expenses:
        key = exp.date.strftime('%b %Y')
        monthly_totals[key] += float(exp.amount)

    expenses_over_time = [{'label': k, 'amount': v} for k, v in monthly_totals.items()]

    context = {
        'expenses_by_category': expenses_by_category,
        'expenses_over_time': expenses_over_time,
    }
    return render(request, 'expenses_summary.html', context)


def logout_view(request):
    request.session.flush()
    return redirect('login')


def tally(request):
    """
    Tally — Day-wise & Monthly Ledger.
    Shows all expenses grouped by day with running totals,
    and a monthly summary section.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)

    # Filter params
    now = datetime.now()
    selected_year  = int(request.GET.get('year',  now.year))
    selected_month = int(request.GET.get('month', now.month))

    # All expenses for this user ordered by date desc
    all_expenses = Expense.objects.filter(user=user).order_by('date', 'id')

    # ── Monthly Summary ──
    monthly_map = defaultdict(float)
    for exp in all_expenses:
        key = (exp.date.year, exp.date.month)
        monthly_map[key] += float(exp.amount)

    monthly_summary = []
    for (yr, mo), total in sorted(monthly_map.items()):
        monthly_summary.append({
            'year': yr,
            'month': mo,
            'month_name': datetime(yr, mo, 1).strftime('%B %Y'),
            'total': round(total, 2),
        })

    # ── Day-wise for selected month ──
    filtered = all_expenses.filter(date__year=selected_year, date__month=selected_month)

    day_map = defaultdict(list)
    for exp in filtered:
        day_map[exp.date].append(exp)

    day_rows = []
    running_total = 0.0
    for day in sorted(day_map.keys()):
        day_expenses = day_map[day]
        day_total = sum(float(e.amount) for e in day_expenses)
        running_total += day_total
        day_rows.append({
            'date': day,
            'day_name': day.strftime('%A'),
            'expenses': day_expenses,
            'day_total': round(day_total, 2),
            'running_total': round(running_total, 2),
        })

    month_grand_total = round(running_total, 2)

    # Build year/month options for filter
    years  = sorted(set(k[0] for k in monthly_map.keys()), reverse=True) or [now.year]
    months = [
        (1,'January'),(2,'February'),(3,'March'),(4,'April'),
        (5,'May'),(6,'June'),(7,'July'),(8,'August'),
        (9,'September'),(10,'October'),(11,'November'),(12,'December'),
    ]

    context = {
        'day_rows': day_rows,
        'monthly_summary': monthly_summary,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'selected_month_name': datetime(selected_year, selected_month, 1).strftime('%B %Y'),
        'month_grand_total': month_grand_total,
        'years': years,
        'months': months,
    }
    return render(request, 'tally.html', context)