# main.py

from expense_cli import add_expense, view_expenses


def main():
    while True:
        print("\n==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            note = input("Enter note: ")
            add_expense(amount, category, note)
            print("Expense added successfully!")

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            print("Exiting Expense Tracker.")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
