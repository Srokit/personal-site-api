import os

DB_URL = os.environ.get('DB_URL')

# Mailer server config vars

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

PORT=os.environ.get('PORT')
