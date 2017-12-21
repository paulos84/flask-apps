from marshmallow import Schema, fields, pprint, post_load, ValidationError, validates

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
    location = fields.String(required=True)


    #person object defined below is instantiated by this Schema
    @post_load
    def create_person(self, data):
        return Person(**data)

    @validates('age')
    def validate_age(self, age):
        if age < 25:
            # return False
            raise ValidationError('That is too young')

input_dict = {}

input_dict['name'] = input('What is your name?')
input_dict['age'] = input('What is your age?')
input_dict['email'] = input('What is your email? ')
input_dict['location'] = input('What is your location?')

#person = Person(name=input_dict['name'], age=input_dict['age'])

# print the string representation of the person object:
#print(person)

schema = PersonSchema()
#result = schema.dump(person)
result = schema.load(input_dict)

print(result)

