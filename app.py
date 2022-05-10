import io

from flask import Flask,request,render_template
from Bio import Entrez

app = Flask(__name__)

@app.route('/',methods=["POST", "GET"])
def start():
    return render_template("start.html")

@app.route('/Homepage',methods=["POST", "GET"])
def hello_world():  # put application's code here
    if request.method == "POST":
        file = request.form.get("file", "")

        if not file.endswith(".xlsx"):
            file = "Please select an excel file"
        print(file)
        return render_template("Homepage.html", file=file)
    else:
        return render_template("Homepage.html", file="")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("errorPage.html")


if __name__ == '__main__':
    app.run()
