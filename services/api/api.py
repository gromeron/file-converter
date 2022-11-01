from flask.cli import FlaskGroup

from project import app
from project.models.models import db, User

import logging


cli = FlaskGroup(app)

app_context = app.app_context()
app_context.push()

app.logger.setLevel(logging.INFO)

db.init_app(app)
db.drop_all()
db.create_all()
db.session.commit()

# test
with app.app_context():
    u1 = User(username='Gusefalox', email='gasiferox@gmail.com', password='2524323x')
    db.session.add(u1)
    db.session.commit()
    print(User.query.all())


if __name__ == "__main__":
    cli()