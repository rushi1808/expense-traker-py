# expense_cli.py

import json
import os

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(amount, category, note):
    expenses = load_expenses()
    expense = {
        "amount": amount,
        "category": category,
        "note": note
    }
    expenses.append(expense)
    save_expenses(expenses)


def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print("\n--- Expense List ---")
    for idx, exp in enumerate(expenses, start=1):
        print(f"{idx}. ₹{exp['amount']} | {exp['category']} | {exp['note']}")
