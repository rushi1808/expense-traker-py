from flask import Flask, render_template, request, redirect, url_for
from expense_cli import add_expense, get_expenses, delete_expense

app = Flask(__name__)


@app.route("/")
def index():
    expenses = get_expenses()
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        note = request.form["note"]

        add_expense(amount, category, note)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:sr_no>")
def delete(sr_no):
    delete_expense(sr_no)
    return redirect(url_for("index"))


# ✅ THIS WAS MISSING
if __name__ == "__main__":
    app.run(debug=True)
