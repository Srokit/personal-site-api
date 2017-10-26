import flask
from flask import g, request
import jwt
from validate_email import validate_email
import json

from .Email import Email

app = flask.Flask(__name__)

TOKEN_NAME = os.environ.get('TOKEN_NAME')

@app.before_request
def parse_body():
    if request.data is not None and len(request.data) > 0:
        request.body = json.loads(request.data)

@app.route('/email', methods=['PUT'])
def put_email():
    email = request.body.get('email')
    if validate_email(email) and len(email) <= 100:
        Email.get_or_create(email=email)
        return {'success': True}
    else:
        return {'success': False, 'message': 'Invalid email'}



if __name__ == '__main__':
    app.run(host='0.0.0.0')
