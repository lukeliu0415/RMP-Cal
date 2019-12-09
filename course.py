import requests
import json
from bs4 import BeautifulSoup

page = requests.get('https://classes.berkeley.edu/content/2020-spring-compsci-61b-001-lec-001')
soup = BeautifulSoup(page.content, 'html.parser')
info = soup.find(class_ = "handlebarData theme_is_whitehot")['data-json']
file = json.loads(info)

print(file['meetings'][0]['assignedInstructors'][0]['instructor']['names'][0]['formattedName'])
