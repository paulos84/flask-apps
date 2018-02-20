from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/docs')  #doc=False

app.register_blueprint(blueprint)
app.config['SWAGGER_UI_JSONEDITOR'] = True

# The model() factory allows you to instantiate and register models to your API or Namespace.
city = api.model('City', {'city': fields.String('The city')})  # 'id': fields.Integer

cities = []
tokyo = {'city': 'Tokyo'}
cities.append(tokyo)


@api.route('/city')
class City(Resource):

    # The marshal_with() decorator will apply the transformation described by model which uses the fields module
    @api.marshal_with(city, envelope='Cities')
    def get(self):
        return cities  # return an iterable

    # pass the api model to the decorator:
    @api.expect(city)
    def post(self):
        cities.append(api.payload)
        return {'result': 'city added!'}, 201

if __name__ == '__main__':
    app.run(debug=True)
