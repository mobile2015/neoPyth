from app import db
from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from app.models.images import Images
from app.models.utils import Utils
from flask.ext.login import current_user, flash, login_user, login_required, logout_user

from app.models.user import User as UserModel
from py2neo import Node

User = Blueprint('userController', __name__, template_folder='templates', static_folder='static')


@User.route('/')
@User.route('/panel')
@login_required
def user_index():

    if request.method == 'GET':
        return render_template('user/panel.html')
    else:
        _query = request.form['query']
        if _query:
            result = db.cypher.execute(_query)
            s = ""
            if result:
                for res in result:
                    s = s + str(res[0]) + "\n"
                flash(s)
        else:
            flash("No query to execute")
        return redirect(url_for('userController.user_index'))


@User.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        _login = request.form['login']
        _password = request.form['password']
        query = 'MATCH (node:User) WHERE node.login = "' + _login + '" RETURN node'
        cnt = 0
        for tmp in db.cypher.execute(query):
            if Utils.check_password(tmp[0]["password"], _password):
                if tmp[0]["active"] == 1:
                    login_user(UserModel(tmp[0]))
                    flash("Welcome " + _login + ". You are logged in!")
                else:
                    _mail_content = "localhost:5000" + url_for('userController.user_activate') + '?login=' + _login + '&code=' + \
                                    tmp[0]["activation_code"]
                    UserModel.send_activation_code(tmp[0]["email"], _mail_content)
                    flash("Check your email for activation link. If you are too lazy or "
                          "used fake e-mail just use this link:   " + _mail_content)
                cnt += 1
                break
            else:
                flash("Incorrect (incomplete) login or password")
        if cnt == 0:
            flash("Incorrect user login")
        return redirect(url_for('index'))


@User.route('/logout')
def user_logout():
    flash("User "+current_user.login+" logged out!")
    logout_user()
    return redirect(url_for('index'))


@User.route('/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_anonymous():

        if request.method == 'GET':
            return render_template('user/register.html')
        else:
            _activation_code = Utils.random_string(16)
            _first_name = request.form['fname']
            _last_name = request.form['lname']
            _email = request.form['email']
            _login = request.form['login']
            _password = Utils.hash_password(request.form['password'])
            _user = Node("User", first_name=_first_name,
                         last_name=_last_name,
                         email=_email,
                         login=_login,
                         password=_password,
                         _group="None",
                         active=0,
                         activation_code=_activation_code
                         )
            db.create(_user)
            _mail_content = "localhost:5000" + url_for(
                'userController.user_activate') + '?login=' + _login + '&code=' + _activation_code
            UserModel.send_activation_code(_email, _mail_content)
            flash(
                "Check your email for activation link. If you are too lazy or used fake e-mail just use this link: " +
                "localhost:5000" + url_for('userController.user_activate') + '?login=' + _login + '&code=' + _activation_code
            )
    else:
        flash("Cant create new account while logged in?")
    return redirect(url_for('index'))


@User.route('/activate', methods=['GET', 'POST'])
def user_activate():
    login = request.args.get('login')
    code = request.args.get('code')
    query = 'MATCH (node:User) WHERE node.login = "' + login + '" RETURN node'
    for tmp in db.cypher.execute(query):
        if tmp[0]["active"] == 1:
            flash(login + "your account has already been activated.")
        elif tmp[0]["activation_code"] == code:
            query = 'MATCH (node:User) where node.login="' + login + '" set node.active=' + str(1)
            db.cypher.execute(query)
            query = 'MATCH (node:User) where node.login="' + login + '" remove node.activation_code'
            db.cypher.execute(query)
            flash("Congrats " + login + " You have just activated your account.")
        else:
            flash("Incomplete or incorrect data!")
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
    # test: http://localhost:5000/user/image/12/4321

    return img.get_user_node_image(session['user_id'], node_id)

