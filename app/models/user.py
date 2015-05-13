# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin


class User(UserMixin):

    # def __init__(self, _first_name, _last_name, _email, _login, _password, _group="None", _active=0):
    #     self.first_name = _first_name
    #     self.last_name = _last_name
    #     self.email = _email
    #     self.login = _login
    #     self.password = _password
    #     self.active = _active
    #     self.group = _group

    # TODO jesli konstruktor ma byc przeladowany, uzyc za przyklad:
    # __init__(self, *args, **kwargs)
    # print 'args: ', args, ' kwargs: ', kwargs
    def __init__(self, record):
        self.first_name = record["first_name"]
        self.last_name = record["last_name"]
        self.email = record["email"]
        self.login = record["login"]
        self.password = record["password"]
        if record["group"] == "None":
            self.group = None
        if record["active"] == 1:
            self.active = True
        else:
            self.active = False

    def set_group(self, _group):
        self.group = _group

    def is_active(self):
        return self.active

    def get_id(self):
        return self.login

    def is_anonymous(self):
        return False

    @staticmethod
    def send_activation_code(_mail, _link):
        import smtplib
        gmail_user = "neo4j.python@gmail.com"
        gmail_pwd = "neo4jpyton"
        FROM = 'neo4j.python@gmail.com'
        TO = [_mail]
        SUBJECT = "Neo4j Python Project - account registration"
        TEXT = "To activate your account just use this registration link: "+_link

        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
        except:
            print("Failed to send mail")