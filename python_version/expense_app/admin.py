from django.contrib import admin
from .models import User, Budget, BudgetCategory, Expense

admin.site.register(User)
admin.site.register(Budget)
admin.site.register(BudgetCategory)
admin.site.register(Expense)