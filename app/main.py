import flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
from prof_rate import main_prof_rate
from grade import main_grade

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return "Welcome to RMP @ Cal Backend APIs!"
    
@app.route('/ratings/', methods=['GET'])
@cross_origin()
def getProfRatings():
    if 'url' in request.args:
        url = request.args['url']
        return jsonify(main_prof_rate(url))
    else:
        return "Error: No url field provided. Please specify an url."

@app.route('/grades/', methods=['GET'])
@cross_origin()
def getGrade():
    if 'url' in request.args:
        url = request.args['url']
        return jsonify(main_grade(url))
    else:
        return "Error: No url field provided. Please specify an url."

app.run(port=8000)