from __main__ import app
from flask import Flask, render_template, url_for, redirect, request, flash, session, send_from_directory
import os
from werkzeug.utils import secure_filename

# importing this allows access to the database
from DBConnector import Database

import requests
import hashlib

#defines our database
db = Database()

UPLOAD_FOLDER = 'static/Profile_pics'
# Defines databases file types that it allows
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'PNG'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile-upload', methods=['GET', 'POST'])
def upload_file():
    current_user = session.get("user")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', "danger")
            return redirect(url_for('userPage'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file',"danger")
            return redirect(url_for('userPage'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user = session.get("user")
            get_user_id = db.queryDB('SELECT User_ID FROM User_Login_TBL WHERE User_Name = ? ', [user])
            filename = str(get_user_id[0][0]) + "_user_pic"
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+ "/" + filename))
            current_user = db.queryDB('SELECT * FROM User_Data_TBL WHERE User_ID = ?', [get_user_id[0][0]])
            change_profile_pic = db.updateDB('UPDATE User_Data_TBL SET User_Profile = ? WHERE User_ID = ?', [filename, get_user_id[0][0]])

            flash(f"{current_user[0][1]}'s profile has been updated!","Success")
            return redirect(url_for('userPage'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/bio-update', methods=['GET', 'POST'])
def bioUpdate():
    if request.method == 'POST':

        text = request.form["bio"]

        
        user = session.get("user")
        get_user_id = db.queryDB('SELECT User_ID FROM User_Login_TBL WHERE User_Name = ? ', [user])
        current_user = db.queryDB('SELECT * FROM User_Data_TBL WHERE User_ID = ?', [get_user_id[0][0]])
        change_user_bio = db.updateDB('UPDATE User_Data_TBL SET User_Bio = ? WHERE User_ID = ?', [text, get_user_id[0][0]])
        flash(f'Bio has updated for {user}!')
        return redirect(url_for('userPage'))

@app.route('/desc-update', methods=['GET', 'POST'])
def descUpdate():
    if request.method == 'POST':

        text = request.form["desc"]

        
        user = session.get("user")
        get_user_id = db.queryDB('SELECT User_ID FROM User_Login_TBL WHERE User_Name = ? ', [user])
        current_user = db.queryDB('SELECT * FROM User_Data_TBL WHERE User_ID = ?', [get_user_id[0][0]])
        change_user_bio = db.updateDB('UPDATE User_Data_TBL SET User_Desc = ? WHERE User_ID = ?', [text, get_user_id[0][0]])
        flash(f'Description has updated for {user}!')

        return redirect(url_for('userPage'))

# This creates a home page for the user to be sent to if theres nothng in the search bar
@app.route("/")
def homePage():
    title = "Home"
    current_user = session.get("user")
    if current_user:
        return render_template("Index.HTML", title = title, current_user=current_user)
    else:
        return render_template("Index.HTML", title = title)
        

@app.route("/about")
def aboutPage():
    title = "About"
    current_user = session.get("user")
    if current_user:
        return render_template("About.html", title = title, current_user=current_user)
    else:
        return render_template("About.html", title = title)

# If /trainers is typed into search bar then it will send the user to the trainers page
@app.route("/trainers")
def trainerPage():
    title = "Trainer Personas"
    current_user = session.get("user")
    trainers = db.queryDB('SELECT * FROM Trainer_TBL')
    trainers_array = []
    for trainer in trainers:
        trainer_data = db.queryDB('SELECT * FROM User_Data_TBL WHERE User_ID = ?', [trainer[1]])
        trainers_array.append(trainer_data)
    user = session.get("user")
    if current_user:
        return render_template("Trainer.html", title = title, current_user=current_user, trainers=trainers_array)
    else:
        return render_template("Trainer.html", title = title, trainers=trainers_array)

# This will redirect the user back to the Home page
@app.route("/home")
def backToHomePage():
    current_user = session.get("user")
    return redirect(url_for("homePage"))

@app.route("/user")
def userPage():
    title = "User"
    user = session.get("user")
    return render_template("User.HTML", title = title, current_user=user)

# This directs you to the sign up page
@app.route("/sign-up")
def signUpPage():
    title = "Sign Up"
    current_user = session.get('user')
    return render_template("signUp.HTML", title = title, current_user=current_user)

@app.route("/Login")
def loginPage():
    title = "Login"
    current_user = session.get("user")
    if current_user:
        flash('User is already logged in, log out to continue!', 'danger')
        return redirect(url_for("homePage"))
    elif current_user == False:
        return render_template("Login.HTML", title = title, current_user=current_user)
    else:
        return render_template("Login.HTML", title = title, current_user=current_user)

@app.route("/logout")
def logout():
    current_user = session.get('user')
    flash("You have been logged out!", 'danger')
    session.pop("user", None)
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("homePage"))

@app.route("/search-user/<string:userSearch>", methods=['GET', 'POST'])
def searchUser(userSearch):
    current_user = session.get("user")
    search = db.queryDB("SELECT * FROM User_Data_TBL WHERE User_Name = ?", [userSearch])


    return render_template("search.html", current_user=current_user, search=search)

@app.route("/UserLogin", methods=['GET', 'POST'])
def userLogin():
    title = "Login"
    current_user = session.get('user')

    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        password = request.form["pword"]
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        found_user = db.queryDB('SELECT * FROM User_Login_TBL WHERE User_Name = ?', [user])
        if found_user:
            stored_password = found_user[0][2]
            if stored_password == hashed_password:
                session["user"] = db.queryDB('SELECT * FROM User_Data_TBL WHERE User_Name = ?', [found_user[0][1]])
                session["email"] = found_user[0][3]
                flash(f"{found_user[0][1]} has been logged in!", 'Success')
                return redirect(url_for("homePage"))
            else:
                flash("Please make sure that you have typed the right password!", "danger")
                return render_template("Login.html", title = title, current_user=current_user)
        else:
            flash("User not found!", 'danger') 
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
        first_name = request.form["fnm"]
        last_name = request.form["lnm"]
        password = request.form["pword"]
        email = request.form["email"]
        membership_type = request.form["mtype"]
        Profile_Pic = 'default.png'

        hashed_email = hashlib.md5(str(email).encode()).hexdigest()
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()

        result = db.queryDB('SELECT * FROM User_Login_TBL WHERE User_Email = ?', [hashed_email])
        result2 = db.queryDB('SELECT * FROM User_Login_TBL WHERE User_Name = ?', [user])
        if result:
            flash("User Email already in use :(", "danger")
            return redirect(url_for("register"))
        elif result2:
            flash("Username already taken please try again!", "danger")
            return redirect(url_for("register"))
        elif first_name.isdigit() == True or last_name.isdigit() == True:
            flash("Personal names cannot be numbers!", "danger")
            return redirect(url_for("register"))
        elif first_name.isalpha() == False or last_name.isalpha() == False:
            flash("Personal names must not contain special characters!", "danger")
            return redirect(url_for("register"))
        else:
            db.updateDB("INSERT INTO User_Login_TBL (User_Name, User_Pass, User_Email) VALUES (?,?,?)", [user, hashed_password, hashed_email])
            get_user_id = db.queryDB('SELECT User_ID FROM User_Login_TBL WHERE User_Name = ? ', [user])
            db.updateDB("INSERT INTO User_Data_TBL (User_ID, User_Name, User_Profile, User_Membership_Type, User_First_Name, User_Last_Name) VALUES (?,?,?,?,?,?)", [get_user_id[0][0], user, Profile_Pic, membership_type, first_name.capitalize(), last_name.capitalize()])
            if membership_type == "Trainer":
                db.updateDB("INSERT INTO Trainer_TBL (User_ID) VALUES (?)", [get_user_id[0][0]])
                
                flash("signed up trainer", "info")
            else:
                pass
            return render_template('Login.html', title='login', current_user=current_user)
    else:
            return redirect(url_for("signUpPage"))
    