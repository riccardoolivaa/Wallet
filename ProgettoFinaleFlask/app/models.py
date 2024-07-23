from . import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


# Qui usiamo SQLite, che crea un file db.sqlite e usa quello.
db_url = 'sqlite:///db_progetto.sqlite'
# Oppure per usare MySQL; di solito host sarà 'localhost'
# e port sarà 3306.
# db_url = 'mysql+mysqlconnector://root:root@localhost:3306/progetto'


app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class User(db.Model):
    iduser = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),nullable=False,unique=True)
    password = db.Column(db.String(16),nullable=False)#aggiungere controllo per la lunghezza minima 


class Transaction(db.Model):
    idtransaction = db.Column(db.Integer,primary_key=True)
    iduser =  db.Column(db.Integer, db.ForeignKey('user.iduser'))
    ammontare = db.Column(db.Float(99999999))
    data = db.Column(db.String())
    tipo = db.Column(db.String(100))
    spesa_guada = db.Column(db.String(20))

