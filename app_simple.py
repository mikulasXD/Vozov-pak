
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vozidla.db'
db = SQLAlchemy(app)

class Vozidlo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vyrobce = db.Column(db.String(50))
    model = db.Column(db.String(50))
    stav_tachometru = db.Column(db.Integer)
    palivo = db.Column(db.String(20))

@app.route('/')
def index():
    return '<h1>AutoBazar</h1><a href="/statistiky">Statistiky</a>'

@app.route('/statistiky')
def statistiky():
    celkem = Vozidlo.query.count()
    do_100k = Vozidlo.query.filter(Vozidlo.stav_tachometru <= 100000).count()
    nad_100k = Vozidlo.query.filter(Vozidlo.stav_tachometru > 100000).count()
    
    return f"""
    <h1>Statistiky</h1>
    <p>Celkem: {celkem}</p>
    <p>Do 100 000 km: {do_100k}</p>
    <p>Nad 100 000 km: {nad_100k}</p>
    <a href="/">Zpět</a>
    """

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)