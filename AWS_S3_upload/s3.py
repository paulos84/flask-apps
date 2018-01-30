"""
You need to have AWS credentials in ~/.aws/credentials
[default]
aws_access_key_id=KEY_ID
aws_secret_access_key=ACCESS_KEY
"""
from flask import Flask, request
import boto3

app = Flask(__name__)

app.debug = True


@app.route('/')
def index():
        return """<form method=POST enctype=multipart/form-data action="upload">
        <input type=file name=myfile>
        <input type=submit>
        </form>"""


@app.route('/upload', methods=['POST'])
def upload():

    s3 = boto3.resource('s3')

    s3.Bucket('elasticbeanstalk-us-east-2-867338818903').put_object(Key='a_random_fie.txt', Body=request.files['myfile'])

if __name__ == '__main__':
    app.run(port=5001, debug=True)
