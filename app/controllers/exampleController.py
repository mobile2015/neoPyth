from app import cache
from flask import Blueprint, jsonify, render_template, current_app
from app.models.example import ExampleModel

Example = Blueprint('exampleController', __name__, template_folder='templates', static_folder='static')


@Example.route('/')
def example_index():

    return render_template('example/example.html')


@cache.cached(timeout=60)
@Example.route('/data', methods=['GET'])
def example_data():

    a = ExampleModel()
    graph = a.get_some_graph()

    current_app.logger.info("[INFO] Downloaded some graph! yay!")

    return jsonify(graph.serialize)

@Example.route('/reset')
def example_reset():

    a = ExampleModel()
    a.reset_cars()

    return render_template('example/example.html', reset=True)