from flask import Flask, render_template, request, redirect, url_for
from expense_cli import add_expense, get_expenses, delete_expense, save_expenses

app = Flask(__name__)


@app.route("/")
def index():
    expenses = get_expenses()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        add_expense(
            request.form["amount"],
            request.form["category"],
            request.form["note"]
        )
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:sr_no>", methods=["GET", "POST"])
def edit(sr_no):
    expenses = get_expenses()
    expense = expenses[sr_no - 1]

    if request.method == "POST":
        expense["amount"] = float(request.form["amount"])
        expense["category"] = request.form["category"]
        expense["note"] = request.form["note"]
        save_expenses(expenses)
        return redirect(url_for("index"))

    return render_template("edit.html", expense=expense, sr_no=sr_no)


@app.route("/delete/<int:sr_no>")
def delete(sr_no):
    delete_expense(sr_no)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
