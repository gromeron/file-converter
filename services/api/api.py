from flask.cli import FlaskGroup
from flask_restful import Api

from project import app, UserAddResource, UserListResource, AuthResource, ViewTasks, ViewTask, ViewFiles
from project.models.models import db

import logging

cli = FlaskGroup(app)

app_context = app.app_context()
app_context.push()

# Console logging
app.logger.setLevel(logging.INFO)

# DB setup
db.init_app(app)
db.drop_all()
db.create_all()
db.session.commit()

# API REST
api = Api(app)

# Users
api.add_resource(UserAddResource, '/api/auth/signup')
api.add_resource(UserListResource, '/api/auth/users')
api.add_resource(AuthResource, '/api/auth/login')

# Tasks
api.add_resource(ViewTasks, '/api/tasks')
api.add_resource(ViewTask, '/api/tasks/<int:id_task>')

# Files
#api.add_resource(ViewFiles, '/api/files/<filename>')


if __name__ == "__main__":
    cli()