import flask
from flask import g, request
import jwt
from validate_email import validate_email
import json
from flask_mail import Mail

import config
from BaseModel import db
from Email import Email
from Project import Project

from helpers import send_update_for_project

app = flask.Flask(__name__)
app.config.from_object('config')
mailer = Mail()
mailer.init_app(app)

TOKEN_NAME = config.TOKEN_NAME

@app.before_request
def setup():
    db.connect()
    db.create_tables([Email, Project], safe=True)

    if request.data is not None and len(request.data) > 0:
        request.body = json.loads(request.data)

@app.after_request
def clean_up(request):
    if not db.is_closed():
        db.close()
    return request

@app.route('/email', methods=['PUT'])
def put_email():
    email = request.body.get('email')
    if validate_email(email) and len(email) <= 100:
        Email.get_or_create(email=email)
        return {'success': True}
    else:
        return {'success': False, 'message': 'Invalid email'}

@app.route('/project', methods=['PUT'])
def put_project():
    new_project = request.body.get('project')
    project = Project.create(**new_project)

    email_addresses = [ email.email for email in Email.select().where(True).execute() ]

    send_update_for_project(project, mailer, email_addresses)

    if project is not None:
        return {'success': True}
    else:
        return {'success': False}

@app.route('/project/all', methods=['GET'])
def get_project_all():

    projects = Project.select().where(True).execute()
    projects_as_dicts = [ project.to_dict() for project in projects ]
    return {'success': True, 'projects': projects_as_dicts}

@app.route('/project/{proj_id}', methods=['GET'])
def get_project(proj_id):

    project_as_dict = Project.get(Project.id == proj_id).to_dict()
    return {'success': True, 'project': project_as_dict}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
