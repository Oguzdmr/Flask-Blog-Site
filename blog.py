from operator import add
from os import name
from flask import render_template, jsonify, request,flash,redirect,url_for,session,logging
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from app import createApp
from app.models import Queries
from flask_cors import CORS
from app.initialize_db import createDB
from passlib.hash import sha256_crypt

#Kullanıcı Kayıt Formu

class RegisterForm(Form):
    name = StringField("Name",validators=[validators.length(min=1,max=25)])
    username = StringField("Username",validators=[validators.length(min=4,max=25)])
    email = StringField("Email",validators=[validators.Email(message= "Geçerli bir email giriniz...")])
    password = PasswordField("Password",validators=[
        validators.DataRequired(message= "Lütfen bir porola girin..")
    ])


class LoginForm(Form):  
    username = StringField("Username",validators=[validators.length(min=4,max=25)])
    password = PasswordField("Password",validators=[
        validators.DataRequired(message= "Lütfen bir porola girin..")
    ])


app = createApp()

CORS(app)
createDB()
queries = Queries()

@app.route("/")
def index():
    try:
        results = queries.getAllUsers()

        users = []

        for user in results:
            users.append({
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "password": user.password,
                "email": user.email,           
            })

        return render_template("index.html", users = users)
    except Exception as e:
        return jsonify({'success': False, 'error': e})
    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        result = queries.oneUser(username)
        
        if result == [] or result == None:
            flash("Kullanıcı bulunamadı...","danger")
            return render_template("login.html",form = form)
        else: 
            for user in result:
                if sha256_crypt.verify(password,user.password):
                    return redirect(url_for("index"))
                else:
                    flash("Yanlış Parola...","danger")
                    return render_template("login.html",form = form)
    else:
        return render_template("login.html",form = form)


@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate(): 

        user = {
        "name" : form.name.data,
        "username": form.username.data,
        "password" : sha256_crypt.encrypt(form.password.data),
        "email" : form.email.data
        }
        queries.addUser(user) 

        flash("Başarıyla kayıt oldunuz...","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form = form)

    

@app.route("/article/<string:id>")
def detail(id):
    return "Article id:"+id
if __name__ == "__main__":
    app.run(debug=True)

