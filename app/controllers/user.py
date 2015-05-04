from flask import Blueprint, jsonify, render_template, current_app, url_for, redirect, session, request, abort
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

    img = Images()

    session['user_id'] = 12  # TODO apply real session (remove this line / uncomment @Utils.login_required

    if request.method == "POST":

        img.save_image(request.files['file'], request.form['node'], session['user_id'])
        return redirect(url_for('userController.user_images'))

    else:

        # return render_template('user/images.html', images=img.get_user_images_url(session['user_id']))
        return render_template('user/images.html', images=["/user/image/12/1234", "/user/image/12/4321"])


@User.route('/image/<int:user_id>/<int:node_id>')
# @Utils.login_required
def user_image(user_id, node_id):

    session['user_id'] = 12  # TODO apply real session (remove this line / uncomment @Utils.login_required

    if session['user_id'] != user_id:
        abort(403)

    img = Images()

    # test: http://localhost:5000/user/image/12/1234
    #  test: http://localhost:5000/user/image/12/4321

    return img.get_user_node_image(session['user_id'], node_id)

