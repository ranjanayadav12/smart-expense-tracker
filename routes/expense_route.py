from flask import render_template, request, redirect, session, flash
from model.expense_model import Expense
from database.db import db
from datetime import datetime

from analytics.analytics import (
    calculate_total,
    highest_expense,
    average_expense,
    total_transactions,
    category_insights
)


def parse_date(value):
    if not value:
        return datetime.now().date()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return datetime.now().date()


def expense_routes(app, socketio):

    # Dashboard
    @app.route("/dashboard")
    def dashboard():

        if "user_id" not in session:
            return redirect("/login")

        expenses = Expense.query.filter_by(
            user_id=session["user_id"]
        ).all()

        total = calculate_total(expenses)

        highest = highest_expense(expenses)

        average = average_expense(expenses)

        count = total_transactions(expenses)

        insights = category_insights(expenses)

        return render_template(
            "dashboard.html",
            expenses=expenses,
            total=total,
            highest=highest,
            average=average,
            count=count,
            insights=insights
        )


    # Add Expense
    @app.route("/add_expense", methods=["POST"])
    def add_expense():

        if "user_id" not in session:
            return redirect("/login")

        title = request.form.get("title")
        amount = request.form.get("amount")
        category = request.form.get("category")
        payment_method = request.form.get("payment_method")
        description = request.form.get("description")
        date = request.form.get("date")

        expense = Expense(
            title=title,
            amount=float(amount) if amount else 0.0,
            category=category,
            payment_method=payment_method,
            description=description,
            date=parse_date(date),
            user_id=session["user_id"]
        )

        db.session.add(expense)
        db.session.commit()

        # WebSocket notification
        socketio.send("Expense Added Successfully")

        flash("Expense Added Successfully", "success")

        return redirect("/dashboard")


    # Delete Expense
    @app.route("/delete/<int:id>")
    def delete_expense(id):

        expense = Expense.query.get_or_404(id)

        db.session.delete(expense)
        db.session.commit()

        flash("Expense Deleted Successfully", "danger")

        return redirect("/dashboard")


    # Edit Expense
    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    def edit_expense(id):

        expense = Expense.query.get_or_404(id)

        if request.method == "POST":

            expense.title = request.form.get("title")
            expense.amount = float(request.form.get("amount")) if request.form.get("amount") else 0.0
            expense.category = request.form.get("category")
            expense.payment_method = request.form.get("payment_method")
            expense.description = request.form.get("description")
            expense.date = parse_date(request.form.get("date"))

            db.session.commit()

            flash("Expense Updated Successfully", "warning")

            return redirect("/dashboard")

        return render_template(
            "edit_expense.html",
            expense=expense
        )