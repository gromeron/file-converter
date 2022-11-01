from flask import Flask

from .models.models import db, User

app = Flask(__name__)
app.config.from_object('project.config.Config')


@app.route('/')
def home_test():
    return{"message":"home ok"}

@app.route('/route', methods=['GET'])
def index():
    app.logger.info('home ok')
    #app.logger.info(f'DB_URI = {DB_URI}')
    return {"message": "home ok from ping route"}

@app.route('/user', methods=['GET'])
def create_user():
    u1 = User(username='Hassler', email='hassler@gmail.com', password='25242344')
    app.logger.info(u1)
    db.session.add(u1)
    db.session.commit()
    users = User.query.all()
    app.logger.info(f'Usuarios_DB = {users}')
    return {"message":"okidoki"}