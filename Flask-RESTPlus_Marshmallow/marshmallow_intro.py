from marshmallow import Schema, fields

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return  '{} is {} years old'.format(self.name, self.age)

class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer()

input_dict = {}

input_dict['name'] = input('What is your name?')
input_dict['age'] = input('What is your age?')

person = Person(name=input_dict['name'], age=input_dict['age'])

# print the string representation of the person object:
#print(person)

