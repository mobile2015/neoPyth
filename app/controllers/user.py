from app import db
from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from app.models.images import Images
from app.models.utils import Utils
from flask.ext.login import current_user, flash, login_user, login_required, logout_user

from app.models.user import User as UserModel
from py2neo import Node

User = Blueprint('userController', __name__, template_folder='templates', static_folder='static')


@User.route('/cypher', methods=['GET', 'POST'])
@login_required
def user_cypher():
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
        return redirect(url_for('userController.user_cypher'))


@User.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        _login = request.form['login']
        _password = request.form['password']
        tmp = db.find_one("USERS","login",_login)
        if tmp and tmp["login"]=="admin" and Utils.check_password(tmp["password"], _password):
            login_user(UserModel(tmp))
            flash("Hello mr. Super Admin! Have a nice day")
        elif tmp:
            if tmp["blocked"] == 1:
                flash("Permission denied. Your account has been blocked")
                return render_template('user/login.html')
            else:
                if Utils.check_password(tmp["password"], _password):
                    if tmp["active"] == 1:
                        login_user(UserModel(tmp))
                        flash("Welcome " + current_user.login + ". You are logged in!")
                    else:
                        _mail_content = "localhost:5000" + url_for('userController.user_activate') + '?login=' + _login + '&code=' + \
                                        tmp["activation_code"]
                        send_activation_code(tmp["email"], _mail_content)
                        flash("Check your email for activation link. If you are too lazy or "
                              "used fake e-mail just use this link:   " + _mail_content)
                else:
                    flash("Incorrect (incomplete) login or password")
                    return render_template('user/login.html')
        else:
            flash("Incorrect user login")
            return render_template('user/login.html')
        return redirect(url_for('index'))


@User.route('/logout')
@login_required
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
            tmp = db.find_one("USERS","login",_login)
            if tmp:
                print(tmp + "   A")
                flash("Login exists")
                return render_template('user/register.html')
            print(tmp)
            _user = Node("USERS", first_name=_first_name,
                         last_name=_last_name,
                         email=_email,
                         login=_login,
                         password=_password,
                         activation_code=_activation_code,
                         _group="None",
                         active=0,
                         is_admin=0,
                         blocked=0,
                         )
            db.create(_user)
            _mail_content = "localhost:5000" + url_for(
                'userController.user_activate') + '?login=' + _login + '&code=' + _activation_code
            send_activation_code(_email, _mail_content)
            flash(
                "Check your email for activation link. If you are too lazy or used fake e-mail just use this link:  " + _mail_content)
    else:
        flash("Cant create new account while logged in?")
    return redirect(url_for('index'))


@User.route('/activate', methods=['GET', 'POST'])
def user_activate():
    login = request.args.get('login')
    code = request.args.get('code')
    tmp = db.find_one("USERS","login",login)
    if tmp["blocked"] == 1:
        flash("Permission denied. Your account has been blocked")
    elif tmp["active"] == 1:
        flash(login + "your account has already been activated.")
    elif tmp["activation_code"] == code:
        query = 'MATCH (node:USERS) where node.login="' + login + '" set node.active=' + str(1)
        db.cypher.execute(query)
        query = 'MATCH (node:USERS) where node.login="' + login + '" remove node.activation_code'
        db.cypher.execute(query)
        flash("Congrats " + login + " You have just activated your account.")
    else:
        flash("Incomplete or incorrect data!")
    return redirect(url_for('index'))


@User.route('/lock_account', methods=['GET'])
@login_required
def lock_account():
    _login = request.args.get('login')
    tmp = db.find_one("USERS","login",_login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" set node.active=' + str(0) + ', node.blocked=' +str(1)
        db.cypher.execute(query)
        flash("User blocked successfully")
    else:
        flash("User not found")
    return redirect(url_for('userController.admin_panel'))


@User.route('/unlock_account', methods=['GET'])
@login_required
def unlock_account():
    _login = request.args.get('login')
    tmp = db.find_one("USERS","login",_login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" set node.active=' + str(1) + ', node.blocked=' +str(0)
        db.cypher.execute(query)
        flash("User unblocked successfully")
    else:
        flash("User not found")
    return redirect(url_for('userController.admin_panel'))


@User.route('/remove_user', methods=['GET', 'POST'])
@login_required
def remove_user():
    _login = request.args.get('login')
    tmp = db.find_one("USERS","login",_login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" delete node'
        db.cypher.execute(query)
        flash("User removed successfully")
    else:
        flash("User not found")
    return redirect(url_for('userController.admin_panel'))


@User.route('/give_admin', methods=['GET', 'POST'])
@login_required
def give_admin():
    _login = request.args.get('login')
    tmp = db.find_one("USERS","login",_login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" set node.is_admin=1'
        db.cypher.execute(query)
        flash("Admin rights granted")
    else:
        flash("User not found")
    return redirect(url_for('userController.admin_panel'))


@User.route('/take_admin', methods=['GET', 'POST'])
@login_required
def take_admin():
    _login = request.args.get('login')
    tmp = db.find_one("USERS","login",_login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" set node.is_admin=0'
        db.cypher.execute(query)
        flash("User removed successfully")
    else:
        flash("Admin rights revoked")
    return redirect(url_for('userController.admin_panel'))


@User.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if request.method == 'GET':
        query = 'MATCH (n) WHERE (n.login IS NOT NULL and n.login <> "'+current_user.login+'" and n.login<>"admin" ) RETURN n.first_name, n.last_name, n.login, n.blocked, n.is_admin'
        results = db.cypher.execute(query)
        list=[]
        l=[]
        for i in results:
            l.append(i[2])
            l.append(i[0])
            l.append(i[1])
            l.append(i[3])
            l.append(i[4])
            list.append(l)
            l=[]
        return render_template('user/admin_panel.html',list=list, sa=current_user.is_superadmin)
    else:
        return redirect(url_for('index'))

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


@User.route('/panel/images', methods=['GET', 'POST'])
@login_required
def user_images():
    img = Images()

    if request.method == "POST":

        img.save_image(request.files['file'], request.form['node'], current_user.login)
        return redirect(url_for('userController.user_images'))

    else:

        return render_template('user/images.html', images=img.get_user_image_urls(current_user.login))


@User.route('/image/<int:node_id>')
@User.route('/image/show/<int:node_id>')
@login_required
def user_image(node_id):

    if not current_user.login:
        abort(403)

    img = Images()

    return img.get_user_node_image(current_user.login, node_id)

@User.route('/image/remove/<int:node_id>')
@login_required
def user_image_remove(node_id):

    img = Images()
    img.remove_image(node_id)

    return redirect(url_for('userController.user_images'))

