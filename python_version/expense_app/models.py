from django.db import models
from django.contrib.auth.models import User as AuthUser

# Since Django has built-in User, we'll extend or use it, but for simplicity, create custom User
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # In production, use hashed passwords
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Budget(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class BudgetCategory(models.Model):
    category = models.CharField(max_length=100)
    allocated_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.category

class Expense(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.amount}"