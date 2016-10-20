from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

# Requires Flask and flask-restful

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

# on http://127.0.0.1:5000/

#@app.route('/') #the following function should be called when there is a http req to /
#def hello():
#    return "<h1>Hello, World!</h1>"

#RESTful feature, resources are updatable, deletable editable etc. like in a DB.
class HelloWorld(Resource):
    # What happens when we try to get this resource
    def get(self):
        # Python list will be turned into a JSON data structure.
        return {'hello': 'world',
            'list':[1, 2, 3]}
# What URL the resource will appear at.  
api.add_resource(HelloWorld, "/")

# Next exercise.
# Meant to be used by other software, not people! Kinda like a DB server.
# So another app will inquire your site for datas.
TODOs = {
    1:{'task': 'build an API'},
    2:{'task': '???'},
    3:{'task': 'profit'}
}

# curl localhost:5000
    
# we don't want our browser to crash when it doesn't exist or something. So 404.
def abort_if_todo_not_found(todo_id):
    if todo_id not in TODOs:
        abort(404, message = "TODO {} does not exist".format(todo_id))

def add_todo(todo_id):
    args = parser.parse_args()
    todo = {'task': args['task']}
    TODOs[todo_id] = todo
    return todo
    
class Todo(Resource):
    """Shows a single TODO item and lets you delete a TODO item.
    """
    def get(self, todo_id):
        abort_if_todo_not_found(todo_id)
        return TODOs[todo_id]
        
    def delete(self, todo_id):
        abort_if_todo_not_found(todo_id)
        del TODOs[todo_id]
        # Number at the ends are status codes. 204 whatever you asked me to do was done/successful.
        # 204 Goes well with when you're absolutely saying nothing, just going OKAY, I've done the thing.
        return '', 204
    
    def put(self, todo_id):
        # Number 201 CREATED is something was successfully created.
        return add_todo(todo_id), 201
    
class TodoList(Resource):
    """ Shows a list of all TODOs and lets you POST to add new tasks.
    """
    def get(self):
        return TODOs
    
    def post(self):
        todo_id = max(TODOs.keys()) + 1
        return add_todo(todo_id), 201
        
api.add_resource(Todo, '/todos/<int:todo_id>')
api.add_resource(TodoList, '/todos')

# curl localhost:5000/todos
# curl localhost:5000/todos/3
# curl -v -X DELETE localhost:5000/todos/2
# curl -v -X POST localhost:5000/todos -d "task=something new"
# curl -v -X PUT localhost:5000/todos/3 -d "task=something different"
# Triggering error 405 Method Not Allowed, Flask handled the error response for us.
# curl -v -X DELETE localhost:5000/todos
    
if __name__ == "__main__":
    app.run(debug = True)

