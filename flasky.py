import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import Teacher,Student,Course,Course_Teach_Stu,Admin
from flask_script import Manager,Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,stu=Student,teach=Teacher,admin=Admin,course=Course,stc=Course_Teach_Stu)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command("shell",Shell(make_context=make_shell_context))

if __name__=='__main__':
    manager.run()