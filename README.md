# 💸 Expense Tracker — Django

A **premium, full-featured Expense Tracker** web application built with **Python & Django**, featuring a modern dark-themed UI, interactive Chart.js analytics, day-wise Tally ledger, and full budget management — all in **Indian Rupees (₹)**.

---

## 🖥️ Live Preview

> Run locally at `http://127.0.0.1:8000/`

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **User Auth** | Register, Login, Logout with session-based authentication |
| 📊 **Dashboard** | Stats bar (budget, total expenses, remaining), pie chart, recent expenses |
| 💰 **Manage Expenses** | Add, Edit, Delete expenses with category, date, amount & description |
| 🗂️ **Budget Management** | Create budgets with monthly income, start/end dates & category allocations |
| 📒 **Tally (हिसाब)** | Day-wise & monthly ledger with running totals — like an Excel sheet |
| 📈 **Reports & Analytics** | Bar chart (by category) + Line chart (spending over time) using Chart.js |
| 🇮🇳 **Indian Rupee (₹)** | All amounts displayed in ₹ |
| 📱 **Responsive Design** | Clean, mobile-friendly layout |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.13, Django 4.2 |
| **Database** | SQLite (default), MySQL supported |
| **Frontend** | Vanilla HTML5 + CSS3 (no frameworks) |
| **Charts** | Chart.js (CDN) |
| **Fonts** | Google Fonts — Inter |
| **Auth** | Django Sessions |

---

## 📁 Project Structure

```
expense-traker-py/
│
├── python_version/
│   ├── expense_app/
│   │   ├── models.py          # User, Budget, BudgetCategory, Expense models
│   │   ├── views.py           # All view logic
│   │   ├── urls.py            # URL routing
│   │   ├── forms.py           # Django forms
│   │   └── static/
│   │       └── expense_app/
│   │           └── style.css  # Premium CSS design system
│   │
│   ├── expense_tracker/
│   │   ├── settings.py
│   │   └── urls.py
│   │
│   ├── templates/
│   │   ├── base.html                  # Base layout + navbar
│   │   ├── login.html                 # Login page
│   │   ├── register.html              # Register page
│   │   ├── user_dashboard.html        # Dashboard with charts
│   │   ├── expense_list.html          # Expense table
│   │   ├── expense_form.html          # Add / Edit expense
│   │   ├── expense_confirm_delete.html
│   │   ├── budget_list.html           # Budget cards
│   │   ├── budget_form.html           # Create budget
│   │   ├── budget_confirm_delete.html
│   │   ├── expenses_summary.html      # Reports & Analytics
│   │   └── tally.html                 # Day-wise Tally ledger
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ installed
- pip

### 1. Clone the repository

```bash
git clone https://github.com/rushipatil1808/expense-traker-py.git
cd expense-traker-py/python_version
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open your browser and go to 👉 **http://127.0.0.1:8000/**

---

## 📸 Pages Overview

### 🔐 Login & Register
Clean centered card with red brand badge, form validation.

### 📊 Dashboard
- Budget name, total expenses, remaining budget with progress bar
- Pie chart — expense breakdown by category
- Recent expenses table

### 💳 Manage Expenses
Full CRUD table — add, edit, delete expenses with date, category, amount & description.

### 🗂️ Manage Budgets
Budget cards with monthly income, date range, **Select & Add Expense** and **Delete** buttons.

### 📒 Tally (हिसाब)
> Day-wise ledger like an Excel sheet
- Filter by **month & year**
- Each day shows all expenses with **category badge** and **description**
- **Day total** + **Running total** per day
- **Monthly summary sidebar** — click any month to jump to it

### 📈 Reports & Analytics
- **Bar chart** — spending by category
- **Line chart** — spending trend over months

---

## ⚙️ Configuration

### Switch to MySQL

In `python_version/expense_tracker/settings.py`, replace the `DATABASES` section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'expense_tracker',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

Then install the MySQL client:
```bash
pip install mysqlclient
```

---

## 📋 Requirements

```
Django==4.2
```

> Chart.js is loaded via CDN — no npm needed.

---

## 👨‍💻 Author

**Rushi Patil**
- GitHub: [@rushipatil1808](https://github.com/rushipatil1808)

---

## 📄 License

This project is licensed under the **MIT License**.

---

> Built with ❤️ using Python & Django
