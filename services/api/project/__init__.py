from flask import Flask


app = Flask(__name__)


@app.route('/')
def home_test():
    return{"message":"home ok"}

@app.route('/route', methods=['GET'])
def index():
    #app.logger.info('home ok')
    #app.logger.info(f'DB_URI = {DB_URI}')
    return {"message": "home ok from ping route"}