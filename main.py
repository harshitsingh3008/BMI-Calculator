import os
from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bmi.sqlite3"
db= SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Records(db.Model):
    __tablename__='records'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    f_name=db.Column(db.String,nullable=False)
    l_name=db.Column(db.String)
    age=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String,nullable=False)
    weight=db.Column(db.Integer,nullable=False)
    height=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String)

db.create_all()

gen=['Male','Female', 'Transgender']
@app.route("/" , methods=["GET", "POST"])
def home():
    data=Records.query.all()
    return render_template('home.html',data=data)

@app.route("/record/create", methods=["GET", "POST"])
def create():
    if request.method=="GET":
        return render_template("add-records.html",gen=gen)
    elif request.method=="POST":
        data=request.form
        new_rc = Records(
            f_name=data["fname"],
            l_name=data["lname"],
            age=data["agee"],
            gender=data["genderr"],
            weight=data["weightt"],
            height=data["heightt"],
            email=data["emaill"]
        )
        db.session.add(new_rc)
        db.session.commit()
        return redirect(url_for('home'))
    
@app.route("/record/<int:id>", methods=["GET", "POST"])
def result(id):
    data=Records.query.filter_by(id=id).first()
    wt=data.weight
    ht=data.height/100
    res=wt/(ht*ht)
    return render_template("result.html",res=res)

@app.route("/record/<int:id>/delete", methods=["GET" , "POST"])
def delete(id):
    data=Records.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/record/<int:id>/update", methods=["GET", "POST"])
def update(id):
    data=Records.query.filter_by(id=id).first()
    if request.method=="GET":
        return render_template("update-record.html", data=data,gen=gen)
    if request.method=="POST":
        update=request.form
        to_update=Records.query.filter_by(id=id).first()
        to_update.l_name=update["lname"]
        to_update.gender=update["genderr"]
        to_update.age=update["agee"]
        to_update.weight=update["weightt"]
        to_update.height=update["heightt"]
        to_update.email=update["emaill"]
        db.session.commit()
        return redirect(url_for('home'))


if __name__ =="__main__":
    app.debug=True
    app.run()