from setuptools import setup, find_packages

setup(
    name="HealthyLife",
    version="2.0.0",
    author="Mahboob Attar",
    author_email="freespace.alltime@gmail.com",
    description="ML-based Healthcare Platform",
    long_description="""# HealthyLife An ML-based Healthcare Platform.  

Features:
- Disease prediction  
- Wellness recommendations by real chatbot  
- Pharmacy & lab integration  
""",
    long_description_content_type="text/markdown",
    license="MIT (Educational Use Only)",
    packages=find_packages(include=["blueprints", "blueprints.*"]),
    install_requires=[
        "backports.tarfile==1.2.0",
        "docopt==0.6.2",
        "flask-cors==6.0.1",
        "importlib-metadata==8.0.0",
        "jaraco.collections==5.1.0",
        "packaging==24.2",
        "pandas==2.3.2",
        "pip-chill==1.0.3",
        "platformdirs==4.2.2",
        "scikit-learn==1.7.1",
        "tomli==2.0.1",
        "yarg==0.1.10",
    ],
    python_requires=">=3.8",
)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

