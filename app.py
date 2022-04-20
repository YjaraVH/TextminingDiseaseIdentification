import io

from flask import Flask,request,render_template
from Bio import Entrez

app = Flask(__name__)


@app.route('/',methods=["POST", "GET"])
def hello_world():  # put application's code here
    if request.method == "POST":
        answer = request.form.get("answer", "")
        return render_template("Homepage.html", answer=answer)
    else:
        return render_template("Homepage.html", answer="")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("errorPage.html")


if __name__ == '__main__':
    app.run()
