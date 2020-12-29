import os
import click
from flask_migrate import Migrate
from personal_blog import create_app, db
from personal_blog.models import User, Role, Permission, \
    AnonymousUser, Post, Category

app = create_app('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, AnonymousUser=AnonymousUser, Post=Post,
                Category=Category, Role=Role, Permission=Permission)


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
