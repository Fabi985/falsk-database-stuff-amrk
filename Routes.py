from __main__ import app
from flask import Flask, render_template, url_for, redirect, request, flash, session

# importing this allows access to the database
from DBConnector import Database

import requests
import hashlib

#defines our database
db = Database()

# This creates a home page for the user to be sent to if theres nothng in the search bar
@app.route("/")
def homePage():
    title = "Home"
    current_user = session.get("user")
    return render_template("Index.HTML", title = title, current_user=current_user)

# If /about is typed into search bar then it will send the user to an about page
@app.route("/about")
def aboutPage():
    title = "About"
    current_user = session.get("user")
    return render_template("About.HTML", title = title, current_user=current_user)

# This will redirect the user back to the Home page
@app.route("/home")
def backToHomePage():
    current_user = session.get("user")
    return redirect(url_for("homePage"))

@app.route("/user")
def userPage():
    title = "User Page"
    current_user = session.get("user")
    current_user_membership = session.get("membership")
    return render_template("User.HTML", title = title, current_user=current_user, current_user_membership=current_user_membership)

# This directs you to the sign up page
@app.route("/sign-up")
def signUpPage():
    title = "Sign Up"
    current_user = session.get("user")
    return render_template("signUp.HTML", title = title, current_user=current_user)

@app.route("/Login")
def loginPage():
    title = "Login"
    current_user = session.get("user")
    return render_template("Login.html", title = title, current_user=current_user)

@app.route("/data")
def data():
    title = "Data"
    #check to see if user is logged in
    current_user = session.get("user")

    # defines books and use a db.query from the dbconnector.property()
    books = db.queryDB('SELECT * FROM Books_TBL')

    #return our user and books to the data.htrml page
    return render_template("data.HTML", title = title, books = books, current_user=current_user)

@app.route("/logout")
def logout():
    current_user = session.get('user')
    flash("You have been logged out!", 'danger')
    session.pop("user", None)
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("homePage"))

@app.route("/add", methods=["POST"])
def add():
    current_user = session.get("user")
    title = request.form.get("title",'')
    author = request.form.get("author",'')

    db.updateDB("INSERT INTO Books_TBL (title, author) VALUES (?, ?)", [title, author])
    flash("Book Added Sucesfuly","message")

    return redirect(url_for("data"))


@app.route('/delete/<int:Book_ID>', methods=['GET', 'POST'])
def delete(Book_ID):
    current_user = session.get("user")
    book = db.queryDB('SELECT * FROM Books_TBL WHERE Book_ID = ?', [Book_ID])
    if not book:
        flash("Book not found!", "danger")
    else:
        db.updateDB('DELETE FROM Books_TBL WHERE Book_ID = ?', [Book_ID])
        flash("Book deleted scufsefuly!", "success")
    return redirect(url_for('data'))

@app.route("/update/<int:Book_ID>", methods=['GET', 'POST'])
def update(Book_ID):
    title = "Update"
    current_user = session.get("user")
    book = db.queryDB('SELECT * FROM Books_TBL WHERE Book_ID = ?', [Book_ID])

    return render_template("Update.html", title = title, book = book, current_user=current_user)


@app.route("/UserLogin", methods=['GET', 'POST'])
def userLogin():
    title = "Login"
    current_user = session.get('user')

    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pword"]
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        found_user = db.queryDB('SELECT * FROM User_TBL WHERE User_Name = ?', [user])
        print(found_user)
        if found_user:
            stored_password = found_user[0][2]
            if stored_password == hashed_password:
                session["user"] = user
                session["email"] = found_user[0][3]
                session["membership"] = found_user[0][4]
                flash("Login sucesful", 'Success')
                return redirect(url_for("homePage"))
            else:
                flash("Incorect", "danger")
                return render_template("Login.html", title = title, current_user=current_user)
        else:
            flash("user not found", 'danger') 
            return render_template("Login.html", title = title, current_user=current_user)
    if current_user in session:
        flash("Already logged in!", "info")
        return redirect(url_for("homePage"))
    else:
        return render_template("Login.html", title = title, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    current_user = session.get('user')
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pword"]
        email = request.form["email"]
        membership_type = request.form["mtype"]

        print(user, password, email)

        hashed_email = hashlib.md5(str(email).encode()).hexdigest()
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()

        result = db.queryDB('SELECT * FROM User_TBL WHERE User_Name = ? OR User_Email = ?', [user,  hashed_email])
        print(result)
        if result:
            flash("Dont work :(", "danger")
            return redirect(url_for("register"))
        else:
            db.updateDB("INSERT INTO User_TBL (User_Name, User_Pass, User_Email, Membership_Type) VALUES (?,?,?,?)", [user, hashed_password, hashed_email, membership_type])
            return render_template('Login.html', title='login', current_user=current_user)
    else:
            return render_template('signUp.html', title='register', current_user=current_user)
    