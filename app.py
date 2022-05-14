
from crypt import methods
from curses import intrflush
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

# create an applicatoin that gets named afer the name of our files, which is app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alexandrearduinitavares@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

# define a route that listens to todos / creates
# it partilularly listens to requests that como in with a method post
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print('teste')
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all()) # return a template HTML file


#always include this at the bottom of your code
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000)