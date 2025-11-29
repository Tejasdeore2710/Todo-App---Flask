import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# DB in project root folder: todo.db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# ✅ run on import (also on Render/gunicorn)
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")

        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

        return redirect(url_for("home"))

    allTodo = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template("index.html", allTodo=allTodo)


@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is product page'


@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)

    if request.method == "POST":
        todo.title = request.form.get("title")
        todo.desc = request.form.get("desc")
        db.session.commit()
        return redirect(url_for("home"))

    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    # locally this is still fine
    app.run(debug=True, port=8000)
