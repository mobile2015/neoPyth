from flask import current_app

__author__ = 'rikkt0r'


class Images:

    def __init__(self):
        pass

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

    @staticmethod
    def get_user_image_url(user_id, node_id):

        if not user_id or not node_id:
            return None

