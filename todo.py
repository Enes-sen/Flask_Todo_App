from flask import Flask,url_for,redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String,Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/enes_/OneDrive/Masaüstü/Todo-app/Todo.db'
db.init_app(app)

@app.route("/")
def Index():
   todos = Todo.query.all()
   return render_template("main.html",todos = todos)

@app.route('/update/<string:id>')
def Update(id):
    print(id)
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("Index"))

@app.route('/delete/<string:id>', methods = ["GET"])
def Delete(id):
    print(id)
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("Index"))

@app.route("/add", methods = ["POST"])
def Add():
   title = request.form.get("title")
   print(title)
   todo = Todo(title = title, complete = False)
   db.session.add(todo)
   db.session.commit()
   return redirect(url_for("Index"))



class Todo(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(80))
    complete : Mapped[bool] = mapped_column(Boolean)


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)