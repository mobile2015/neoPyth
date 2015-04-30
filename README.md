# neoPython

## TODO

* ~~szablon aplikacji~~
* cos-1
* GW/KW - Upload zdjęć dla wybranego węzła
* cos-3
* coś-4
* wpiszcie co robicie

### Whats inside

* large app aproach
* Flask (flask, flask-cache, flask-bcrypt)
* Neo4J (py2Neo)
* example controller, model, adapter
* example jinja templates + bootstrap

### Contact us!

* GW - grzegorz-wojcicki@outlook.com
* KW - woznyk@agh.edu.pl
* jeszcze ktos inny
* i jeszcze inny


### Structure

```
├── app
│   ├── controllers
│   │   ├── exampleController.py
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── env (never mind that)
│   ├── models
│   │   ├── adapters
│   │   │   ├── graph.py
│   │   │   ├── helpers
│   │   │   │   ├── edge.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── node.py
│   │   │   ├── __init__.py
│   │   ├── example.py
│   │   ├── __init__.py
│   │   ├── reset.py
│   │   ├── utils.py
│   ├── static
│   │   ├── css
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap-theme.min.css
│   │   │   └── style.css
│   │   ├── fonts
│   │   │   ├── glyphicons-halflings-regular.eot
│   │   │   ├── glyphicons-halflings-regular.svg
│   │   │   ├── glyphicons-halflings-regular.ttf
│   │   │   ├── glyphicons-halflings-regular.woff
│   │   │   └── glyphicons-halflings-regular.woff2
│   │   ├── images
│   │   │   └── favicon.ico
│   │   └── js
│   │       ├── bootstrap.js
│   │       ├── bootstrap.min.js
│   │       ├── example.js
│   │       ├── ie10-viewport-bug-workaround.js
│   │       ├── jquery-1.11.2.min.js
│   │       └── jquery.tmpl.min.js
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
│       └── master_template.html
├── authors.txt
├── config.py
├── config.pyc
├── README.md
├── requirements.txt
├── run.py
├── server.log
└── shell.py

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