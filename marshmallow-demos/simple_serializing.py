from marshmallow import Schema, fields

class Person():
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return  '{} is {} years old'.format(self.name, self.age)

class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer()
    email = fields.Email()

input_dict = {}

input_dict['name'] = input('What is your name?')
input_dict['age'] = input('What is your age?')
input_dict['email'] = input('What is your email? ')

person = Person(input_dict['name'], input_dict['age'], input_dict['email'])

# print the string representation of the person object:
#print(person)

schema = PersonSchema()
result = schema.dump(person)

# to deserialize:
result = schema.load(input_dict)

print(result)

