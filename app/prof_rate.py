import requests
import json
from bs4 import BeautifulSoup

def get_rating(url):
    try:
        r = requests.get(url)
        professors = json.loads(r.text[5:-1])
        rating = professors['response']['docs'][0]['averageratingscore_rf']
    except:
        rating = -1
    return rating

def get_course_profs(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find(class_ = "handlebarData theme_is_whitehot")['data-json']
    file = json.loads(info)

    instructors = file['meetings'][0]['assignedInstructors']
    array = []
    for i in range(len(instructors)):
        name_data = instructors[i]['instructor']['names'][0]
        given_name = name_data['givenName']
        family_name = name_data['familyName']
        array.append(given_name + " " + family_name)

    return array

def main_prof_rate(course_url):
    profs = get_course_profs(course_url)
    ratings = []

    for prof in profs:
        prof_url = 'https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=' + prof + '+AND+schoolid_s%3A1072&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='
        prof_rating = get_rating(prof_url)
        if prof_rating == -1:
            print("There's no "+ prof + " on Rate My Professors")
        else:
            print('Professor ' + prof + '\'s RMF rating is ' + str(prof_rating))
        ratings.append(prof_rating)
    return ratings

# main_prof_rate('https://classes.berkeley.edu/content/2021-spring-compsci-61b-001-lec-001')