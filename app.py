from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db =SQLAlchemy(app)


class Todo(db.Model):
    sno =db.Column(db.Integer, primary_key =True)
    title =db.Column(db.String(200), nullable =False)
    desc =db.Column(db.String(500), nullable =False)
    dt =db.Column(db.DateTime, default =datetime.now())
    def __repr__(self) -> str:
        return  f"{self.sno} - {self.title}"



count =0
@app.route("/", methods =["POST", "GET"])
def home_page():
    if request.method =="POST":
        t =request.form["title"]
        d =request.form["desc"]



        todo =Todo(title =f"{t}", desc =f"{d}")
        db.session.add(todo)
        db.session.commit()
    all =Todo.query.all()
   
 
 
    

    return render_template("index.html", td =all)

@app.route("/products")
def products():
    return "This is a product page"
 

@app.route("/delete/<int:sno>")
def delete(sno):
    deltodo =Todo.query.filter_by(sno =sno).first()
    db.session.delete(deltodo)
    db.session.commit()
    return redirect("/")


@app.route("/up/<int:sno>", methods =["GET", "POST"])
def update(sno):
    if request.method=="POST":
        title =request.form["title"]
        desc =request.form["desc"]
        uptodo =Todo.query.filter_by(sno =sno).first()
        uptodo.title =title
        uptodo.desc =desc
        db.session.add(uptodo)
        db.session.commit()
        return redirect("/")






    uptodo =Todo.query.filter_by(sno =sno).first()


    return render_template("up.html", td=uptodo)

if __name__ == '__main__':
   
    app.run(debug=True)