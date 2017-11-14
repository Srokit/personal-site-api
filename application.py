import flask
from flask import g, request, jsonify
import jwt
from validate_email import validate_email
import json
from flask_mail import Mail
from flask_cors import CORS
import os

import config
from BaseModel import db
from Email import Email
from Project import Project

from helpers import send_update_for_project

app = flask.Flask(__name__)
CORS(app)
app.config.from_object('config')
mailer = Mail()
mailer.init_app(app)

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
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid email'})

@app.route('/project', methods=['PUT'])
def put_project():

    password = request.data.get('ADMIN_PASS')
    if password != config.ADMIN_PASS:
        return jsonify({'success': False, 'message': 'Prohibited'})

    new_project = request.body.get('project')
    new_project['logo_img_name'] = new_project['logoImgName']
    del(new_project['logoImgName'])
    project = Project.create(**new_project)

    email_addresses = [ email.email for email in Email.select().where(True).execute() ]

    send_update_for_project(project, mailer, email_addresses)

    if project is not None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/project/all', methods=['GET'])
def get_project_all():

    projects = Project.select().where(True).execute()
    projects_as_dicts = [ project.to_dict() for project in projects ]
    return jsonify({'success': True, 'projects': projects_as_dicts})

@app.route('/project/{proj_id}', methods=['GET'])
def get_project(proj_id):

    project_as_dict = Project.get(Project.id == proj_id).to_dict()
    return jsonify({'success': True, 'project': project_as_dict})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
