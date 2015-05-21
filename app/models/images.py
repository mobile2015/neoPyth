from flask import current_app, url_for, send_from_directory, abort
from app import db
import os
import py2neo

__author__ = 'rikkt0r'


class Images:
    def __init__(self):
        self.extensions = current_app.config['ALLOWED_EXTENSIONS']
        self.upload_dir = current_app.config['UPLOAD_FOLDER']

    def __allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.extensions

    @staticmethod
    def __file_name_part(user_id, node_id):
        # yep, zerofill seems strange for a string.. we'll migrate to using IDs instead of login (i hope)
        return str(user_id).zfill(6) + "_" + str(node_id)

    def save_image(self, image, node_id, user_id):

        if image and self.__allowed_file(image.filename) and node_id and user_id:
            try:
                ext = image.filename.rsplit('.', 1)[1]
                filename = self.__file_name_part(user_id, node_id) + "." + ext

                image.save(os.path.join(self.upload_dir, filename))
                db.cypher.execute_one("MATCH (n) WHERE ID(n) = {0} SET n.image = '/user/image/{0}', n.image_sys = '{1}' \
                 return null".format(
                    node_id,
                    os.path.join(self.upload_dir, self.__file_name_part(user_id, node_id) + "." + ext)
                ))

                return True

            except py2neo.cypher.DatabaseError:

                return False

        return False

    def get_user_node_image(self, user_id=None, node_id=None):

        if not node_id:
            abort(404)

        f = None
        start = self.__file_name_part(user_id, node_id)
        print(start)

        for file in os.listdir(self.upload_dir):
            if file.startswith(start):
                f = file

        if not f:
            abort(404)

        return send_from_directory(self.upload_dir, f)

    @staticmethod
    def get_user_image_urls(user_id=None):

        if not user_id:
            return []

        f = []

        a = db.cypher.execute(
            "MATCH (u:User)-[r:HAS]->(n) WHERE HAS(n.image) AND u.login='{}' \
             RETURN n.image as image, ID(n) as node_id;".format(user_id)
        )

        for node in a:
            f.append({
                'id': node['node_id'],
                'url': node['image']
            })

        return f

    @staticmethod
    def remove_image(node_id=None):

        try:
            node = db.cypher.execute_one("MATCH (u:User)-[:HAS]->(n) WHERE ID(n) = {} RETURN n".format(node_id))
            os.remove(node['image_sys'])
            db.cypher.execute_one("MATCH (n) WHERE ID(n) = {0} REMOVE n.image, n.image_sys RETURN null".format(
                node_id
            ))

            return True

        except py2neo.cypher.DatabaseError:

            return False
