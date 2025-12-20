import json
import os

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)


def get_expenses():
    return load_expenses()


def add_expense(amount, category, note):
    expenses = load_expenses()
    expenses.append({
        "amount": float(amount),
        "category": category,
        "note": note
    })
    save_expenses(expenses)


def delete_expense(sr_no):
    expenses = load_expenses()
    if 1 <= sr_no <= len(expenses):
        expenses.pop(sr_no - 1)
        save_expenses(expenses)
