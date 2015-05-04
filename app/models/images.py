from flask import current_app, url_for, redirect, send_from_directory, abort
import os

__author__ = 'rikkt0r'


class Images:

    def __init__(self):
        self.extensions = current_app.config['ALLOWED_EXTENSIONS']
        self.upload_dir = current_app.config['UPLOAD_FOLDER']

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.extensions

    def save_image(self, image, node_id, user_id):

        # TODO: save url to database

        if image and self.allowed_file(image.filename):
            filename = str(user_id)+"_"+str(node_id)+"."+image.filename.rsplit('.', 1)[1]
            image.save(os.path.join(self.upload_dir, filename))
            # user_node.extension // 1212_14.png

    @staticmethod
    def get_user_node_image_url(user_id, node_id):

        return url_for('userController.image', user_id=user_id, node_id=node_id)

    def get_user_node_image(self, user_id, node_id):

        if not user_id or not node_id:
            return None

        f = None
        start = str(user_id)+"_"+str(node_id)

        for file in os.listdir(self.upload_dir):
            if file.startswith(start):
                f = file

        if not f:
            abort(404)

        return send_from_directory(self.upload_dir, f)

    def get_user_images_url(self, user_id):

        if not user_id:
            return []

        f = []

        # TODO: getting data from DB

        # start = str(user_id)+"_"
        #
        # for file in os.listdir(self.upload_dir):
        #     if file.startswith(start):
        #         f.append(file)
        #

        return f

