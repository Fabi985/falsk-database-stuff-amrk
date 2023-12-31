from flask import Flask, render_template, url_for, redirect
from datetime import timedelta, datetime

# This creates an app to run the file 
# It will then import routes from another file called "Routes"

app = Flask(__name__)

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=31)


import Routes

if __name__ == "__main__":
    app.run(debug = True)