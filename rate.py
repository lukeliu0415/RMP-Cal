import requests
import json

teacher = 'Chiang'
URL = 'https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=' + teacher + '+AND+schoolid_s%3A1072&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq='
r = requests.get(URL)

professors = json.loads(r.text[5:-1])
rating = professors['response']['docs'][0]['averageratingscore_rf']

print('Professor ' + teacher + '\'s RMF rating is ' + str(rating))
