# neoPython

### Whats inside

* large app aproach
* Flask (flask, flask-cache)
* Neo4J (py2Neo)
* example controller, model, adapter
* example jinja templates + bootstrap

### Installation
```sh
git clone https://github.com/mobile2015/neoPyth.git
cd neoPyth
virtualenv -p /usr/bin/python2 env
. env/bin/activate
pip2 install -r app/requirements.txt
python2 run.py
```

### Links

* http://flask.pocoo.org/
* http://py2neo.org/2.0/index.html
* https://github.com/mitsuhiko/flask/wiki/Large-app-how-to
* https://github.com/BorisMoore/jquery-tmpl

### Structure

```
├── app
│   ├── controllers
│   │   ├── example.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── __init__.py
│   ├── models
│   │   ├── adapters
│   │   │   ├── graph.py
│   │   │   ├── helpers
│   │   │   │   ├── edge.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── node.py
│   │   │   └── __init__.py
│   │   ├── example.py
│   │   ├── groups.py
│   │   ├── images.py
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── utils.py
│   ├── services
│   │   ├── __init__.py
│   │   └── security.py
│   ├── static
│   │   ├── css
│   │   │   ├── ...
│   │   ├── fonts
│   │   │   ├── ...
│   │   ├── images
│   │   │   └── favicon.ico
│   │   └── js
│   │       ├── ...
│   └── templates
│       ├── errors
│       │   ├── error_401.html
│       │   ├── error_403.html
│       │   ├── error_404.html
│       │   ├── error_410.html
│       │   └── error_500.html
│       ├── example
│       │   └── example.html
│       ├── index.html
│       ├── macros
│       │   └── import.html
│       ├── master_template.html
│       └── user
│           ├── activation.html
│           ├── admin_panel.html
│           ├── images.html
│           ├── loadgraph.html
│           ├── login.html
│           ├── panel.html
│           ├── register.html
│           └── savegraph.html
├── config.py
├── LICENSE
├── README.md
├── requirements.txt
├── run.py
├── save-load
│   ├── addSampleGraph.py
│   ├── parser.py
│   ├── removeGraph.py
│   └── saveGraphToFile.py
├── server.log
├── shell.py
├── test.dump
├── tests
│   ├── __init__.py
│   └── services
│       ├── __init__.py
│       └── security_test.py
└── uploads

```