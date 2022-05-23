import io
import time

from flask import Flask,request,render_template
from Bio import Entrez

app = Flask(__name__)

@app.route('/',methods=["POST", "GET"])
def start():
    return render_template("start.html")

@app.route('/Homepage',methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        if 'file' not in request.files:
            error = "File not selected"
            return render_template("Homepage.html", error=error)
        file = request.files['file']
        email = request.form.get("email","")
        print(email)
        filename = file.filename
        print(filename)
        if email == "":
            print("no email is needed")
        else:
            print(email)
        if filename == '':
            error = "Filename is empty"
            return render_template("Homepage.html", error=error)
        if filename.endswith(".xlsx") == False:
            error = "This file is not allowed"
            return render_template("Homepage.html", error=error)
        else:
            return render_template("Homepage.html", error="")
    else:
        return render_template("Homepage.html")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.route('/Results',methods=["POST", "GET"])
def results():
    return render_template("Results.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("errorPage.html")



def get_email(reciever):
    import smtplib
    # SERVER = "localhost"
    FROM = 'monty@python.com'
    msg = "lets test this"
    # Send the mail
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(FROM, reciever, msg)
    smtp.quit()


if __name__ == '__main__':
    app.run()
