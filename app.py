import os
from flask import Flask, render_template, request, redirect, flash
from flask_fontawesome import FontAwesome

# from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
# from werkzeug.wrappers import request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(app.root_path, 'todo.db')
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db = SQLAlchemy(app)
fa = FontAwesome(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Task {self.id}: {self.name}'


@app.route('/')
def todo():
    todos = Task.query.order_by(Task.id.desc()).all()
    completetasks = Task.query.filter_by(complete=True).count()
    return render_template('index.html', tasks=todos, ctasks=completetasks)


@app.route('/create', methods=['POST'])
def create():
    task = request.form.get('task')

    new_task = Task(name=task)

    db.session.add(new_task)
    db.session.commit()
    flash("Task created", "info")


    return redirect('/')

@app.route('/complete/<variable>')
def complete_task(variable):
    task = Task.query.get(variable)
    task.complete = True
    db.session.commit()

    flash("Task Completed", "info")
    return redirect('/')

@app.route('/delete/<variable>/')
def delete_task(variable):
    task = Task.query.get(variable)

    db.session.delete(task)
    db.session.commit()

    flash("Task Deleted", "error")
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)