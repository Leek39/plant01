from flask import Flask, request, jsonify
from models import db, Todo

app = Flask(__name__)

# set db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #Performance Optimization

#Database Initialization
db.init_app(app)

# create db table
with app.app_context():
    db.create_all()

# temp memory... (todo db)
# todos = []
# next_id = 1

@app.route('/api/todos', methods=['GET'])
def get_todos():
    "Select all todo list"
    todos = Todo.query.all()
    return jsonify({
        'status' : 'success',
        'data' : [todo.to_dict() for todo in todos],
        'count' : len(todos)
    })

@app.route('/api/todos', methods=['POST'])
def create_todo():
    global next_id  #To 'modify' a global variable inside a function, you need global

    #get JSON request
    data = request.get_json()

    #validation
    if not data or 'title' not in data:
        return jsonify({
            'status' : 'fail',
            'message' : 'title is required'
        }), 400 # bad request

    #new TODO
    #new_todo = {
        #    'id' : next_id,
        #    'title' : data['title'],
    #    'completed' : data.get('completed', False)
    #}

    #todos.append(new_todo)
    #next_id = next_id + 1

    new_todo = Todo(
        title = data['title'],
        completed = data.get('completed', False)
    )

    try:
        db.session.add(new_todo)
        db.session.commit()

        return jsonify({
            'status' : 'success',
            'data' : new_todo.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status' : 'error',
            'message' : 'DB error'
        }),500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    "Update TODO"
    data = request.get_json()

    #find id
    #todo = None
    #for t in todos:
    #    if t['id'] == todo_id:
    #        todo = t
    #       break

    todo = Todo.query.get(todo_id)

    if todo is None:
        return jsonify({
            'status' : 'fail',
            'message' : 'TODO not found'
        }), 404

    #update data
    if 'title' in data:
        #todo['title'] = data['title']
        todo.title = data['title']
    if 'completed' in data:
        #todo['completed'] = data['completed']
        todo.completed = data['completed']

    try:
        db.session.commit()

        return jsonify({
            'status' : 'success',
            'data' : todo.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status' : 'error',
            'message' : 'DB error'
        }), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    "delete TODO"
    #for i, todo in enumerate(todos):
    #    print(f"Index: {i}, value: {todo}")
    #    if todo['id'] == todo_id:
    #        delete_todo = todos.pop(i)
    #        return jsonify({
    #            'status' : 'success',
    #            'data' : delete_todo,
    #            'message' : 'TODO deleted'
    #        })
    #------enumerate : get indext and values
    #todos = [
    #   {'id': 1, 'title': 'Flask test'},
    #   {'id': 2, 'title': 'Python test'}
    #]

    todo = Todo.query.get(todo_id)
    try:
        deleted_data = todo.to_dict()
        db.session.commit()
        db.session.remove()

        return jsonify({
                'status' : 'success',
                'data' : deleted_data,
                'message' : 'TODO deleted'
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status' : 'error',
            'message' : 'DB error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)