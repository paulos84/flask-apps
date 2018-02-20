from flask import Flask, Blueprint
from flask_restplus import Api, Resource
from marshmallow import Schema, fields, post_load

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/docs')  #doc=False

app.register_blueprint(blueprint)
app.config['SWAGGER_UI_JSONEDITOR'] = True

#city = api.model('City', {'city': fields.String('The city')})  # 'id': fields.Integer

class City(object):
    def __init__(self, name, population):
        self.name = name
        self.population = population

    def __repr__(self):
        return '{} is the city name. {} is the city population'.format(self.name, self.population)

    @post_load
    def create_city(self, data):
        # validation?
        return City(**data)

class LanguageSchema(Schema):
    name = fields.String()
    population = fields.Integer()



cities = []
#tokyo = {'city': 'Tokyo'}
tokyo = City(name='Tokyo', population=18000000)
cities.append(tokyo)


@api.route('/city')
class City(Resource):

    # The marshal_with() decorator will apply the transformation described by model which uses the fields module

    def get(self):
        return cities  # return an iterable

    # pass the api model to the decorator:
    @api.expect(city)
    def post(self):
        cities.append(api.payload)
        return {'result': 'city added!'}, 201

if __name__ == '__main__':
    app.run(debug=True)
