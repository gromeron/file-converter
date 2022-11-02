from urllib import request
from flask import Flask, request
from flask_restful import Resource

from .models.models import db, User, Task, UserSchema, TaskSchema

app = Flask(__name__)
app.config.from_object('project.config.Config')


user_schema = UserSchema
task_schema = TaskSchema


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


# Views API REST
class ViewUsers(Resource):

    def get(self):
        return [user_schema.dump(user) for user in User.query.all()]

    def post(self):
        new_user = User(username=request.json['username'],\
                    email=request.json['email'],\
                    password=request.json['password'])

        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)

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