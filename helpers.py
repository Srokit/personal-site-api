
from flask_mail import Message

def send_update_for_project(project, mailer, user_addresses):

    message_text = "Project %s added! Check it out!" % (project.name)

    message = Message(message_text,
        sender="noreply@stans-personal-site.com",
        recipients=user_addresses
        )

    mailer.send(message)
