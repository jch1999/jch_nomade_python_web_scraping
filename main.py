from flask import Flask, render_template

app = Flask("JobScrapper")


@app.route("/")
def home():
  return render_template("home.html", name="chanho")


@app.route("/hello")
def hello():
  return 'hello you!'


app.run("0.0.0.0")
