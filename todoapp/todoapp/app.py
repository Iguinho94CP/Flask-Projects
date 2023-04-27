from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db.init_app(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, default=datetime.utcnow)

    def format_date(self):
        return self.due_date.strftime('%d-%m-%Y')
    


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url_for('index'))


@app.route('/login', methods=['GET'])
def login():
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    due_date_str = request.form['due_date']
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    new_todo = Todo(task=todo, due_date=due_date)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.task = request.form['todo']
        due_date_str = request.form['due_date']
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        todo.due_date = due_date
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', todo=todo)


@app.route('/check/<int:id>', methods=['GET'])
def check(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)
