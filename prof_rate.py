import requests
import json
from bs4 import BeautifulSoup

def get_rating(teacher_name, url):
    rating = None
    try:
        teacher = teacher_name
        r = requests.get(url)
        professors = json.loads(r.text[5:-1])
        rating = professors['response']['docs'][0]['averageratingscore_rf']
    except IndexError:
        print("There's no "+ teacher_name + " on Rate My Professors")
    # print('Professor ' + teacher + '\'s RMF rating is ' + str(rating))
    return rating

def get_course_prof(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find(class_ = "handlebarData theme_is_whitehot")['data-json']
    file = json.loads(info)

    # print(file['meetings'][0]['assignedInstructors'][0]['instructor']['names'][0]['formattedName'])
    return file['meetings'][0]['assignedInstructors'][0]['instructor']['names'][0]['formattedName']

def get_prof_url(teacher_name):
    teacher = teacher_name
    search_url = 'https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=' + teacher + '+AND+schoolid_s%3A1072&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='
    # print(search_url)
    return search_url

def main_prof_rate(course):
    prof = get_course_prof(course)
    prof_url = get_prof_url(prof)
    prof_rating = get_rating(prof, prof_url)
    # print('hereeee')
    print('Professor ' + prof + '\'s RMF rating is ' + str(prof_rating))
    return prof_rating
# prof = get_course_prof('https://classes.berkeley.edu/content/2020-spring-compsci-61b-001-lec-001')
main_prof_rate('https://classes.berkeley.edu/content/2019-fall-eleng-16b-001-lec-001')
main_prof_rate('https://classes.berkeley.edu/content/2020-spring-compsci-61b-001-lec-001')
