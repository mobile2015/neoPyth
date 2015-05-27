# neoPython

### Whats inside

* large app aproach
* Flask (flask, flask-cache)
* Neo4J (py2Neo)
* example controller, model, adapter
* example jinja templates + bootstrap


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
│   │   ├── images.py
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── users_bartek.py
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
│   │   │   ├── ...
│   │   └── js
│   │       ├── ...
│   └── templates
│       ├── errors
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
│           ├── images.html
│           ├── login.html
│           ├── panel.html
│           └── register.html
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
├── tests
│   ├── __init__.py
│   └── services
│       ├── __init__.py
│       └── security_test.py
└── uploads
    ├── 12_1234.png
    └── 12_4321.jpg

```


### Installation
```sh
git clone git@bitbucket.org:rikkt0r/flask-neo4j-template.git
cd flask-neo4j-template
virtualenv -p /usr/bin/python2 env
. env/bin/activate
pip2 install -r app/requirements.txt
python2 run.py
```

### Links

* http://flask.pocoo.org/
* http://flask-bcrypt.readthedocs.org/en/latest/
* http://py2neo.org/2.0/index.html
* https://github.com/mitsuhiko/flask/wiki/Large-app-how-to
* https://github.com/BorisMoore/jquery-tmpl