from app import create_app, db
from app.models import User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def populate():
  db.drop_all()
  db.create_all()

  user = User(username="test_username", password="test_password")

  db.session.add(user)

@manager.command
def deploy():
  from flask.ext.migrate import upgrade

  upgrade()

if __name__ == '__main__':
    manager.run()