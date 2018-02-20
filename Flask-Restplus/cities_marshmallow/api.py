from flask import Flask, Blueprint
from flask_restplus import Api, Resource
from marshmallow import Schema, fields, post_load

app = Flask(__name__)
api = Api(app)


class City(object):
    def __init__(self, name, population):
        self.name = name
        self.population = population

    def __repr__(self):
        return '{} is the city name. {} is the city population'.format(self.name, self.population)


class CitySchema(Schema):
    name = fields.String()
    population = fields.Integer()

    @post_load
    def create_city(self, data):
        # validation?
        return City(**data)


city = api.model('City', {'city': fields.String('The city'), 'population': fields.Integer('City population')})
cities = []
tokyo = City(name='Tokyo', population=18000000)
cities.append(tokyo)


@api.route('/city')
class CityRoute(Resource):

    def get(self):
        schema = CitySchema(many=True)  # many=True required as am passing a list of objects rather than one
        return schema.dump(cities)  # converts list of python objects to JSON

    # pass the api model to the decorator:
    @api.expect(city)
    def post(self):
        schema = CitySchema()
        new_city = schema.load(api.payload)
        cities.append(new_city)
        return {'result': 'city added!'}, 201


if __name__ == '__main__':
    app.run(debug=True)
