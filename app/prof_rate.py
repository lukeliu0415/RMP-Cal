import requests
import json
from bs4 import BeautifulSoup

import flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    if 'url' in request.args:
        url = request.args['url']
        return jsonify(main_prof_rate(url))
    else:
        return "Error: No url field provided. Please specify an url."

def get_rating(url):
    try:
        r = requests.get(url)
        professors = json.loads(r.text[5:-1])
        rating = professors['response']['docs'][0]['averageratingscore_rf']
    except IndexError:
        rating = -1
    return rating

def get_course_prof(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find(class_ = "handlebarData theme_is_whitehot")['data-json']
    file = json.loads(info)

    name_data = file['meetings'][0]['assignedInstructors'][0]['instructor']['names'][0]
    given_name = name_data['givenName']
    family_name = name_data['familyName']
    return given_name + " " + family_name

def main_prof_rate(course_url):
    prof = get_course_prof(course_url)
    prof_url = 'https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=' + prof + '+AND+schoolid_s%3A1072&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='
    prof_rating = get_rating(prof_url)
    if prof_rating == -1:
        print("There's no "+ prof + " on Rate My Professors")
    else:
        print('Professor ' + prof + '\'s RMF rating is ' + str(prof_rating))
    return prof_rating

# main_prof_rate('https://classes.berkeley.edu/content/2021-spring-compsci-61b-001-lec-001')

app.run(port=8000)