from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


pokedex = [{
    'number': 14,
    'name': 'Kakuna',
    'type': ['bug', 'poison'],
    'weaknesses': ['fire', 'flying', 'psychic', 'rock'],
    'evolutions': [{'number': 15, 'name': 'beedrill'}]
}, {
    'number': 16,
    'name': 'Pidgey',
    'type': ['normal', 'flying'],
    'weaknesses': ['electric', 'ice', 'rock'],
    'evolutions': [{'number': 17, 'name': 'Pidgeotto'},
                   {'number': 18, 'name': 'Pidgeot'}]
}, {
    'number': 51,
    'name': 'Dugtrio',
    'type': ['ground'],
    'weaknesses': ['grass', 'ice', 'water'],
    'evolutions': []
}]


class Pokemon(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('naumber', required=False, type=int, location='args')
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        parser.add_argument('number', type=int, required=True, location='json')

        args = parser.parse_args(strict=True)
        pokemon = {'name': args['name'], 'number': args['number']}

        if pokemon in pokedex:
            return {}

        pokedex.append(pokemon)
        return pokedex[-1]


api.add_resource(Pokemon, '/api/v1/pokemon')

if __name__ == '__main__':
    app.run(debug=True)
