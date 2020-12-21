import requests
import json
from bs4 import BeautifulSoup

def scrape_course(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find(class_ = "handlebarData theme_is_whitehot")['data-json']
    file = json.loads(info)
    course_info = file['course']

    abbreviation = course_info['subjectArea']['code']
    course_number = course_info['catalogNumber']['formatted']

    return [abbreviation, course_number]

def getCourseID(course_info):
    try:
        url = 'https://berkeleytime.com/api/grades/grades_json/'
        r = requests.get(url)
        all_courses = json.loads(r.text)['courses']

        for course in all_courses:
            if course['abbreviation'] == course_info[0] and course['course_number'] == course_info[1]:
                return course['id']

        print('No grades for this course exists')
        return -1
    except Exception as e:
        print(e)
        return -1

def getGradeID(course_id):
    try:
        url = 'https://berkeleytime.com/api/grades/course_grades/' + str(course_id) + '/'
        r = requests.get(url)
        section = json.loads(r.text)[0]
        return section['grade_id']
    except Exception as e:
        print(e)
        return -1

def getGPA(grade_id):
    try:
        url = 'https://berkeleytime.com/api/grades/sections/' + str(grade_id) + '/'
        r = requests.get(url)
        gpa = json.loads(r.text)['course_gpa']
        return gpa
    except Exception as e:
        print(e)
        return -1

def main_grade(url):
    course = scrape_course(url)
    courseID = getCourseID(course)
    gradeID = getGradeID(courseID)
    return getGPA(gradeID)

