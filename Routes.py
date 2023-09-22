from __main__ import app
from flask import Flask, render_template, url_for, redirect, request, flash

# importing this allows access to the database
from DBConnector import Database

#defines our database
db = Database()

# This creates a home page for the user to be sent to if theres nothng in the search bar
@app.route("/")
def homePage():
    title = "Home"
    return render_template("Index.HTML", title = title)

# If /about is typed into search bar then it will send the user to an about page
@app.route("/about")
def aboutPage():
    title = "About"
    return render_template("About.HTML", title = title)

# This will redirect the user back to the Home page
@app.route("/home")
def backToHomePage():
    return redirect(url_for("homePage"))

# This directs you to the sign up page
@app.route("/sign-up")
def signUpPage():
    title = "Sign Up"
    return render_template("signUp.HTML", title = title)

@app.route("/data")
def data():
    title = "Data"
    #check to see if user is logged in
    #current_user = session.get("user")

    # defines books and use a db.query from the dbconnector.property()
    books = db.queryDB('SELECT * FROM Books_TBL')

    #return our user and books to the data.htrml page
    return render_template("data.HTML", title = title, books = books)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title",'')
    author = request.form.get("author",'')

    db.updateDB("INSERT INTO Books_TBL (title, author) VALUES (?, ?)", [title, author])
    flash("Book Added Sucesfuly")

    return redirect(url_for("data"))