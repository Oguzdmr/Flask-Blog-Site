from dataclasses import dataclass
from enum import unique
from os import name
from app import db
from datetime import date


# -------------------------------------------------------

@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    

    def __init__(self, username, password, email, name):
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        

# -------------------------------------------------------------

class Queries:
    # ----------------------------------------------------------------

    def getAllUsers(self):
        try:
            results = User.query.all()
        except:
            results = []

        return results

    def addUser(self, user):
        try:
            addingUser = User(name=user["name"], username=user["username"], email=user["email"], password=user["password"])

            print(" ----------- ADDING USER FROM MODELS ---------")

            print(addingUser)

            db.session.add(addingUser)
            db.session.commit()

            return "Kullanıcı Eklendi.."
        except Exception as e:
            print("HATA VAR CANIMS")
            print("HATA --> ", e)

            return "Kullanıcı Eklenemedi.."

    def oneUser(self, username):
        try:
            result = User.query.filter_by(username=username).all()
        except:
            result = {}

        return result

    # ----------------------------------------------------------------

    
