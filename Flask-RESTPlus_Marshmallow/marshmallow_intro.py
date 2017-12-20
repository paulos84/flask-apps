from marshmallow import Schema, fields, pprint, post_load

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return  '{} is {} years old'.format(self.name, self.age)

class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer()


    #person object defined below is instantiated by this Schema
    @post_load
    def create_person(self, data):
        return Person(**data)

input_dict = {}

input_dict['name'] = input('What is your name?')
input_dict['age'] = input('What is your age?')

#person = Person(name=input_dict['name'], age=input_dict['age'])

# print the string representation of the person object:
#print(person)

schema = PersonSchema()
#result = schema.dump(person)
#result = schema.load(input_dict)

pprint(schema.data)

