from app import db
from flask import Blueprint, render_template, url_for, redirect, request, abort
from app.models.images import Images
from app.models.utils import Utils
from flask.ext.login import current_user, flash, login_user, login_required, logout_user

from app.models.user import User as UserModel
from py2neo import Node, Graph

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
        tmp = db.find_one("USERS", "login", _login)
        if tmp and tmp["login"] == "admin" and Utils.check_password(tmp["password"], _password):
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
                        _mail_content = "localhost:5000" + url_for(
                            'userController.user_activate') + '?login=' + _login + '&code=' + \
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
    flash("User " + current_user.login + " logged out!")
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
            tmp = db.find_one("USERS", "login", _login)
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
    tmp = db.find_one("USERS", "login", login)
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
    tmp = db.find_one("USERS", "login", _login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" set node.active=' + str(
            0) + ', node.blocked=' + str(1)
        db.cypher.execute(query)
        flash("User blocked successfully")
    else:
        flash("User not found")
    return redirect(url_for('userController.admin_panel'))


@User.route('/unlock_account', methods=['GET'])
@login_required
def unlock_account():
    _login = request.args.get('login')
    tmp = db.find_one("USERS", "login", _login)
    if tmp:
        query = 'MATCH (node:USERS) where node.login="' + _login + '" set node.active=' + str(
            1) + ', node.blocked=' + str(0)
        db.cypher.execute(query)
        flash("User unblocked successfully")
    else:
        flash("User not found")
    return redirect(url_for('userController.admin_panel'))


@User.route('/remove_user', methods=['GET', 'POST'])
@login_required
def remove_user():
    _login = request.args.get('login')
    tmp = db.find_one("USERS", "login", _login)
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
    tmp = db.find_one("USERS", "login", _login)
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
    tmp = db.find_one("USERS", "login", _login)
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
        query = 'MATCH (n) WHERE (n.login IS NOT NULL and n.login <> "' + current_user.login + '" and n.login<>"admin" ) RETURN n.first_name, n.last_name, n.login, n.blocked, n.is_admin'
        results = db.cypher.execute(query)
        list = []
        l = []
        for i in results:
            l.append(i[2])
            l.append(i[0])
            l.append(i[1])
            l.append(i[3])
            l.append(i[4])
            list.append(l)
            l = []
        return render_template('user/admin_panel.html', list=list, sa=current_user.is_superadmin)
    else:
        return redirect(url_for('index'))


def send_activation_code(_mail, _link):
    import smtplib

    gmail_user = "neo4j.python@gmail.com"
    gmail_pwd = "neo4jpyton"
    FROM = 'neo4j.python@gmail.com'
    TO = [_mail]
    SUBJECT = "Neo4j Python Project - account registration"
    TEXT = "To activate your account just use this registration link: " + _link

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # or port 465 doesn't seem to work!
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

        login = current_user.login

        available = [
            a.node_id for a in
            db.cypher.execute("MATCH (USERS { login:'" + login + "' } )-[:HAS]->(n) RETURN ID(n) as node_id")]
        return render_template('user/images.html',
                               images=img.get_user_image_urls(current_user.login),
                               available=available
                               )


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


@User.route('/savegraph', methods=['GET', 'POST'])
def user_savegraph():
    if request.method == 'GET':
        return render_template('user/savegraph.html')
    else:
        usr_name = request.form['login']
        usr_id = request.form['relation']
        _filename = request.form['filename']

        graph = Graph()

        query1 = "MATCH (USERS {{ login:'{0}' }} )-[:{1}]->(n) RETURN n".format(usr_name, usr_id)
        results = graph.cypher.execute(query1)

        query2 = "MATCH (USERS {{ login:'{0}' }} )-[:{1}]->(n)-[r]->(m) RETURN r".format(usr_name, usr_id)
        results2 = graph.cypher.execute(query2)

        with open(_filename, 'w') as f:
            f.write(usr_name + "\n" + usr_id + "\n")
            s = str(results)
            s2 = str(results2)
            f.write(s)
            f.write(s2)

        return redirect(url_for('index'))


@User.route('/loadgraph', methods=['GET', 'POST'])
def user_loadgraph():
    if request.method == 'GET':
        return render_template('user/loadgraph.html')
    else:
        _file = request.form['plik']

    graph = Graph()

    file = open(_file, 'r')

    wierzch = 0
    login = ""
    relation = ""

    for i, line in enumerate(file):
        # -------------------------------------------
        if i == 0:
            if line[0] != ' ' or line[0] != '-':
                login = line.replace("\n", "")
            else:
                # print ("Can't read user name!")
                break
        # -------------------------------------------
        elif i == 1:
            if line[0] != ' ' or line[0] != '-':
                relation = line.replace("\n", "")
            else:
                # print ("Can't read user id!")
                break
        # -------------------------------------------
        elif i > 1:
            find_user = graph.cypher.execute("MATCH(n:USERS {login:\"" + login + "\"}) RETURN n")
            if len(find_user) != 1:
                # print ("User not found")
                # graph.cypher.execute("CREATE (n:Person { login :\"" + login + "\", title : 'Developer' })")
                break

            if line.replace(" ", "") == "|n\n":
                wierzch = 1
                continue

            # --------------------------------------
            if wierzch == 1 and line[0] != '-':
                if line.replace(" ", "") == "|r\n":
                    wierzch = 2
                    continue
                else:
                    graph.cypher.execute("CREATE" + line.split('|')[1])
                    graph.cypher.execute("MATCH(n:USERS {login:\"" + login + "\"}),(m" + line.split('|')[1].split()[
                        1] + " CREATE n-[:" + relation + "]->m")

            # ---------------------------------------
            if wierzch == 2 and line[0] != '-':
                if line.replace(" ", "") == '':
                    wierzch = 0
                    continue
                else:
                    graph.cypher.execute("MATCH(n" + line.split('|')[1].split('-')[0].replace('(', '') + ",(m" +
                                         line.split('|')[1].split('-')[2].replace('(', '').replace('>',
                                                                                                   '') + " CREATE n-[:" +
                                         line.split('|')[1].split('-')[1].split(':')[1] + "->m")

    file.close()
    return redirect(url_for('index'))
