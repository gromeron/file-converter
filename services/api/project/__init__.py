from urllib import request
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from .models.models import db, User, UserSchema, TaskSchema, Task
from werkzeug.utils import secure_filename
import os
from datetime import datetime
#from celery import Celery
import sys

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, current_app, jsonify , make_response
from werkzeug.utils import secure_filename
import os
from os import abort
import subprocess as sp
import sys


FTRANSC = "ftransc"

# Statics

UPLOAD_FOLDER = '/project/media'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'ogg', 'flac'])


app = Flask(__name__)

app.config.from_object('project.config.Config')

# Celery


""" def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["redis://35.239.105.189:6379/0"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
 """
#celery = Celery('tasks', broker= 'redis://35.239.105.189:6379/0')


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
        taskToUpdate = Task.query.get_or_404(id_task)
        taskToUpdate.new_format = request.json.get(
                "newFormat", taskToUpdate.new_format)
        taskToUpdate.status = "UPLOADED";
        db.session.commit()
        return task_schema.dump(taskToUpdate)

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


# Static Files
# /static/<path:filename>
# /api/files/<path:filename>
@app.route('/api/files/<filename>')
def staticfiles(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


# Media Files
@app.route('/api/media/<filename>')
def mediafiles(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		print(f'file value={file}', file=sys.stdout)
  
		if 'file' not in request.files or file.filename == '':
			return redirect(url_for('home'))

		if file and allowed_file(file.filename):

			format = request.form.get("format_select")
			if str(format) in ALLOWED_EXTENSIONS:
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

				# Convert
				print(f'format value={str(format)}')

				dfile = '{}.{}'.format(os.path.splitext(filename)[0], str(format))
				inputF = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				convert_COMMAND_LINE = [FTRANSC, '-f', str(format), inputF]     
				executeOrder66 = sp.Popen(convert_COMMAND_LINE)

				try:
					outs, errs = executeOrder66.communicate(timeout=150)
				except TimeoutError:
					proc.kill()

				ddir = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
  
				return send_from_directory(ddir, dfile, as_attachment=True)

		return render_template('home.html')
	else:
		return redirect(url_for('home'))

#@app.route('/task', methods=['GET'])
#def convertion_instance_test():
#    celery.converter_test