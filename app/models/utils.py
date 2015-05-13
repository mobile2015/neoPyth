# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import hashlib
import uuid

__author__ = 'rikkt0r'

import random
import base64
from hashlib import md5
from datetime import datetime
from functools import wraps
from flask import redirect, current_app, request


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def ssl_required(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_app.config.get("SSL"):
                if request.is_secure:
                    return fn(*args, **kwargs)
                else:
                    return redirect(request.url.replace("http://", "https://"))
            return fn(*args, **kwargs)
        return decorated_view

    @staticmethod
    def format_datetime(timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y @ %H:%M')

    @staticmethod
    def from_unix(timestamp):
        return datetime.fromtimestamp(int(timestamp)).strftime('%d-%m-%Y @ %H:%M')

    @staticmethod
    def to_utf8(text):
        return text.decode('utf-8')

    @staticmethod
    def serialize_datetime(timestamp):
        if timestamp is None:
            return None
        return timestamp.strftime("%d-%m-%Y @ %H:%M")

    @staticmethod
    def uniquify(seq):
        checked = []
        for e in seq:
            if e not in checked:
                checked.append(e)
        return sorted(checked)

    @staticmethod
    def md5(data=None):
        return md5(data).hexdigest()

    @staticmethod
    def md5optimal(a_file, block_size=65536):
        buf = a_file.read(block_size)
        while len(buf) > 0:
            md5.update(buf)
            buf = a_file.read(block_size)
        return md5.digest()

    @staticmethod
    def base64_decode(hsh):
        return base64.b64decode(hsh)

    @staticmethod
    def base64_encode(string):
        return base64.b64encode(string)

    @staticmethod
    def random_string(seed_length=8):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        seed = ""

        for i in range(seed_length):
            seed += alphabet[random.randrange(len(alphabet))]

        return seed

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod
    def no_empty_params(rule):
        # used for site-map
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)