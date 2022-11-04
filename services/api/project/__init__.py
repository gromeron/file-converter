from urllib import request
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from .models.models import db, User, UserSchema, TaskSchema, Task
from datetime import datetime


app = Flask(__name__)

app.config.from_object('project.config.Config')

jwt = JWTManager(app)

user_schema = UserSchema()
task_schema = TaskSchema()


@app.route('/')
def home_test():
    return{"message":"home ok"}

@app.route('/route', methods=['GET'])
def index():
    app.logger.info('home ok')
    #app.logger.info(f'DB_URI = {DB_URI}')
    return {"message": "home ok from ping route"}


# api/auth/signup
class UserAddResource(Resource):    

    # Signup
    def post(self):
        if(request.json['password'] != request.json['confirmPassword']):
            return jsonify("Password and ConfirmPassword must be equals.")

        user = User(username=request.json['username'], email=request.json['email'], password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)

class UserListResource(Resource):

    def get(self):
        return [user_schema.dumps(user) for user in User.query.all()]   

# api/auth/login
class AuthResource(Resource):
    def post(self):       
        username = request.json['username']
        password = request.json['password']

        user = db.session.query(User).filter(User.username == username and User.password == password).first()
        
        access_token = "Username or password invalid."
        if(user != None):
            access_token = create_access_token(identity = username + password)
        return jsonify(access_token = access_token)


# /api/tasks
class ViewTasks(Resource):
    @jwt_required()
    def get(self):
        return [task_schema.dump(task) for task in Task.query.all()]

    @jwt_required()
    def post(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_task = Task(status="UPLOADED",\
                    filename=request.json['fileName'],\
                    new_format=request.json['newFormat'],
                    timestamp=timestamp)

        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task)


# /api/tasks/<int:id_task>
class ViewTask(Resource):

    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))    

    @jwt_required()
    def put(self, id_task):

        return {}

    @jwt_required()
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return 204

    
# /api/files/<filename>
class ViewFiles(Resource):

    def get(self):

        return {}