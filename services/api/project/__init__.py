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
def user():
    u1 = User(username='Gusefalo', email='gasifero@gmail.com', password='2524323')
    db.session.add(u1)
    db.session.commit()
    users = User.query.all()
    return app.logger.info(f'home ok {users}')