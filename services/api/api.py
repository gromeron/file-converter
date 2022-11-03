from flask.cli import FlaskGroup
from flask_restful import Api

from project import UserAddResource, UserListResource, AuthResource, app, ViewTasks
from project.models.models import db

import logging


cli = FlaskGroup(app)

app_context = app.app_context()
app_context.push()

app.logger.setLevel(logging.INFO)

db.init_app(app)
#db.drop_all()
db.create_all()
#db.session.commit()

# test
#with app.app_context():
#    u1 = User(username='Gusefalox', email='gasiferox@gmail.com', password='2524323x')
#    db.session.add(u1)
#    db.session.commit()
#    print(User.query.all())

# API REST
api = Api(app)

# Users
api.add_resource(UserAddResource, '/api/auth/signup')
api.add_resource(UserListResource, '/api/auth/users')
api.add_resource(AuthResource, '/api/auth/login')

# Tasks
api.add_resource(ViewTasks, '/tasks')


if __name__ == "__main__":
    cli()