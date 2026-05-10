from flask import render_template, request, redirect, session, flash
from model.user_model import User
from database.db import db


# Register User
def register_routes(app):

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":

            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            # Check existing user
            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Email already exists", "danger")
                return redirect("/register")

            # Create new user
            new_user = User(
                name=name,
                email=email
            )

            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash("Registration Successful", "success")

            return redirect("/login")

        return render_template("register.html")


    # Login User
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):

                session["user_id"] = user.id
                session["user_name"] = user.name

                flash("Login Successful", "success")

                return redirect("/dashboard")

            else:
                flash("Invalid Email or Password", "danger")

        return render_template("login.html")


    # Logout
    @app.route("/logout")
    def logout():

        session.clear()

        flash("Logged Out Successfully", "info")

        return redirect("/login")