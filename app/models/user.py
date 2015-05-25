# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin


class User(UserMixin):

    def __init__(self, record):
        self.first_name = record["first_name"]
        self.last_name = record["last_name"]
        self.email = record["email"]
        self.login = record["login"]
        self.password = record["password"]
        self.is_admin = record["is_admin"]
        self.is_superadmin = record["is_superadmin"]
        self.blocked = record["blocked"]
        if record["group"] == "None":
            self.group = None
        self.active = True

    def set_group(self, _group):
        self.group = _group

    def is_active(self):
        if self.active == 1:
            return True
        else:
            return False

    def get_id(self):
        return self.login

    def is_anonymous(self):
        return False

