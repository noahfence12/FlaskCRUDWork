import os
#import re
from turtle import title

from flask import Flask, redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "testDatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Users(db.Model):
    userid = db.Column(db.Integer, unique = True, nullable = False, primary_key = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    date_created = db.Column(db.String(20), unique = False, nullable = False)
    active = db.Column(db.String(3), unique = False, nullable = False)
    orders = db.relationship('Orders')

    #def __repr__(self):
    #    return "<Users %r>" %self.userid

class Orders(db.Model):
    orderid = db.Column(db.Integer, unique = True, nullable = False, primary_key = True)
    order_date = db.Column(db.String(20), unique = False, nullable = False)
    status = db.Column(db.String(20), unique = False, nullable = False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable = False)
    scenes = db.relationship('Scenes')

class Scenes(db.Model):
    scene_name = db.Column(db.String(100), unique = True, primary_key = True)
    scene_status = db.Column(db.String(20), unique = False, nullable = False)
    sensor = db.Column(db.String(100), unique = False, nullable = False)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.orderid'), nullable = False)


#app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    users = None
    #orders = None

    if request.form:

        user = Users(
            userid = request.form.get("userid"),
            first_name=request.form.get("first_name"), last_name=request.form.get("last_name"),
            email = request.form.get("email"), date_created = request.form.get("date_created"), 
            active = request.form.get("active"))
           
        db.session.add(user)
        db.session.commit()
        
    users = Users.query.all()
    #orders = Orders.query.all()

    #users = db.session.query(Users, Orders).filter(Users.userid == Orders.userid)




    return render_template("home.html", users=users)




@app.route("/update", methods=["POST"])
def update():
    newid = request.form.get("newid")
    newfirst = request.form.get("newfirst")
    oldfirst = request.form.get("oldfirst")
    newlast = request.form.get("newlast")
    oldlast = request.form.get("oldlast")
    newemail = request.form.get("newemail")
    newdate = request.form.get("newdate")
    newactive = request.form.get("newactive")

    #neworderid = request.form.get("neworderid")
    #oldorderid = request.form.get("oldorderid")
    #neworderdate = request.form.get("neworderdate")
    #newstatus = request.form.get("newstatus")
    #newuser = request.form.get("newuser")


    user = Users.query.filter_by(first_name=oldfirst).first()
    user.userid = newid
    user.first_name = newfirst
    user.last_name = newlast
    user.email = newemail
    user.date_created = newdate
    user.active = newactive

    #order = Orders.query.filter_by(orderid=oldorderid).first()
    #order.orderid = neworderid
    #order.order_date = neworderdate
    #order.status = newstatus
    #order.userid = newuser

    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    first_name = request.form.get("first_name")
    user = Users.query.filter_by(first_name=first_name).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)