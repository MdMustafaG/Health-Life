from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    return render_template("index.html")

@home_bp.route("/login")
def login():
    return render_template("login.html")

@home_bp.route("/signup")
def signup():
    return render_template("signup.html")