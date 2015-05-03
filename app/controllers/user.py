from flask import Blueprint, jsonify, render_template, current_app, url_for, redirect, session, request
from app.models.images import Images
from app.models.utils import Utils

User = Blueprint('userController', __name__, template_folder='templates', static_folder='static')


@User.route('/')
@User.route('/panel')
@Utils.login_required
def user_index():

    return render_template('user/panel.html')


@User.route('/login', methods=['GET', 'POST'])
def user_login():

    if request.method == 'GET':
        return render_template('user/login.html')
    else:

        # TODO Login user
        current_app.logger.info("[INFO] User: {} attempted login".format("SOME_USER"))
        return jsonify({})


@User.route('/logout')
def user_logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect(url_for('index'))


@User.route('/panel/images', methods=['GET', 'POST'])
# @Utils.login_required
def user_images():

    a = Images()

    if request.method == "POST":
        # TODO: upload plikow
        return jsonify({})

    else:
        # TODO: pobieranie plikow z folderu

        return render_template('user/images.html', images=[])