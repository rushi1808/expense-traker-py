import json
import os

FILE_NAME = "expenses.json"


# ---------- Utility Functions ----------

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------- Core Functions ----------

def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    note = input("Enter note: ")

    expenses = load_expenses()
    expenses.append({
        "amount": amount,
        "category": category,
        "note": note
    })
    save_expenses(expenses)

    print("✅ Expense added successfully!")


def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("❌ No expenses found.")
        return

    print("\n--- Expense List ---")
    for i, exp in enumerate(expenses, start=1):  # Sr No
        print(f"{i}. ₹{exp['amount']} | {exp['category']} | {exp['note']}")


def delete_expense_by_srno():
    expenses = load_expenses()

    if not expenses:
        print("❌ No expenses to delete.")
        return

    view_expenses()
    sr_no = int(input("Enter Sr No to delete: "))

    if sr_no < 1 or sr_no > len(expenses):
        print("❌ Invalid Sr No!")
        return

    deleted = expenses.pop(sr_no - 1)  # Sr No → index
    save_expenses(expenses)

    print(f"🗑️ Deleted: ₹{deleted['amount']} | {deleted['category']} | {deleted['note']}")


# ---------- Main Program ----------

def main():
    while True:
        print("\n==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense (by Sr No)")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            delete_expense_by_srno()

        elif choice == "4":
            print("👋 Exiting Expense Tracker.")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
1