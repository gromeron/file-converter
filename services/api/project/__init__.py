from urllib import request
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from .models.models import db, User, UserSchema, TaskSchema, Task

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

""" @app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    app.logger.info(f'Usuarios_DB = {users}')
    return {"usuarios": users}

@app.route('/user', methods=['POST'])
def create_user():
    u1 = User(username='Hassler', email='hassler@gmail.com', password='25242344', tasks='')
    app.logger.info(u1)
    db.session.add(u1)
    db.session.commit()
    users = User.query.all()
    app.logger.info(f'Usuarios_DB = {users}')
    return {"message":"okidoki"} """


# api/auth/signup
class UserAddResource(Resource):    

    def post(self):
        if(request.json['password'] != request.json['confirmPassword']):
            return jsonify("Password and ConfirmPassword must be equals.")

        user = User(username=request.json['username'], email=request.json['email'], password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return user_schema.dumps(user)

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

class ViewTasks(Resource):

    def get(self):
        return [task_schema.dump(task) for task in Task.query.all()]

    def post(self):
        new_task = Task(status=request.json['status'],\
                    originalFormat=request.json['originalFormat'],\
                    newFormat=request.json['newFormat'])

        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task)