
from flask_mail import Message

def send_update_for_project(project, mailer, user_addresses):

    message_text = "Project %s added! Check it out!" % (project.name)

    body = "Come back to Stan's site and check out the work I did to make " +\
            "%s a reality!" % (project.name)

    html = "Come back to <strong>Stan's site</strong> and check out the work I did to make " +\
            "<em>%s</em> a reality!" % (project.name)

    message = Message(subject=message_text,
        body=body,
        html=html,
        sender="noreply@stans-personal-site.com",
        recipients=user_addresses
    )

    mailer.send(message)
