# Expense Tracker - Python Django Version

This is a conversion of the C# ASP.NET MVC Expense Tracker to Python using Django and MySQL.

## Setup

1. Install Python 3.8+ and MySQL.

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create MySQL database:
   ```
   CREATE DATABASE expense_tracker;
   ```

5. Update settings.py with your MySQL credentials.

6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the server:
   ```
   python manage.py runserver
   ```

## Features

- User registration and login
- Budget creation and management
- Expense tracking
- Reports and summaries

Note: Passwords are stored in plain text for simplicity, matching the original C# version. In production, use Django's authentication system with hashed passwords.