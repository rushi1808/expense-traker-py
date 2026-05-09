from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/select/', views.select_budget, name='select_budget'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path('reports/expenses-summary/', views.reports_expenses_summary, name='expenses_summary'),
    path('tally/', views.tally, name='tally'),
    path('logout/', views.logout_view, name='logout'),
]