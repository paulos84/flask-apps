from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


pokedex = [{
    'number': '14',
    'name': 'Kakuna',
    'type': ['bug', 'poison'],
    'weaknesses': ['fire', 'flying', 'psychic', 'rock'],
    'evolutions': [{'number': 15, 'name': 'beedrill'}]
}, {
    'number': '16',
    'name': 'Pidgey',
    'type': ['normal', 'flying'],
    'weaknesses': ['electric', 'ice', 'rock'],
    'evolutions': [{'number': 17, 'name': 'Pidgeotto'},
                   {'number': 18, 'name': 'Pidgeot'}]
}, {
    'number': '43',
    'name': 'Dugtrio',
    'type': ['ground'],
    'weaknesses': ['grass', 'ice', 'water'],
    'evolutions': []
}]


class Pokemon(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('number', required=False, type=str, location='args')
        args = parser.parse_args(strict=True)
        number = args.get('number')
        # could have?... if number:
        if number is not None:
            if number in [a['number'] for a in pokedex]:
                return [a for a in pokedex if a['number'] == number][0]
            else:
                return {}
        return pokedex

    #def post(self):
     #   parser = reqparse.RequestParser()
      #  parser.add_argument


api.add_resource(Pokemon, '/api/v1/pokemon')

if __name__ == '__main__':
    app.run(debug=True)
