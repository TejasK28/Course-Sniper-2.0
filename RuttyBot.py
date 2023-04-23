import requests
import selenium 
from bs4 import BeautifulSoup
import json
import time
import pyfiglet, logging
from termcolor import colored
import Text

# main 2 links to request and retrieve responses
SIS_COURSES_LINK = "http://sis.rutgers.edu/soc/api/courses.json?year=2023&term=9&campus=NB"
SIS_OPEN_COURSES_LINK = "http://sis.rutgers.edu/soc/api/openSections.json?year=2023&term=9&campus=NB"

class Course:
    def __init__(self, index, prof, openStatus):
        self.index = str(index)
        self.prof = str(prof)
        self.openStatus = bool(openStatus)

    def getIndex(self):
        return self.index
    def getOpenStatus(self):
        return self.openStatus



# creates a json with all courses
def getJsonFromLink(link):
    request = requests.get(link)
    jsonOfCourses = json.loads(request.text)
    return jsonOfCourses

def getPopoulatedCourses():
    jsonOfCourses = getJsonFromLink(SIS_COURSES_LINK)
    Courses = []
    for course in jsonOfCourses:
        for section in course["sections"]:
            #print(section["index"], section["instructorsText"], section["openStatus"])
            Courses.append(Course(section["index"], section["instructorsText"], section["openStatus"]))
    return Courses


# method to retrieve the teachers avilible for an index
def getTeachersFromIndex(courses, index):
    pass

#return true if course is open; false otherwise
def isCourseOpen(courses, index):
    for course in courses:
        if course.getIndex() == index and course.getOpenStatus():
            return True
    return False

def keepAliveCourseCheck(courses, indexes):
    counter = 0;
    while True:
        for index in indexes:
            if(isCourseOpen(courses, index)):
                print(f"--------------[OPEN]--:--{counter}--------{index}------\n")
                Text.send("[OPEN] : INDEX IS AVAILABLE")
                Text.send(f"{index}")
                break
            else:
                print(f"--------------[CLOSED]--:--{counter}-------{index}-------\n")
        counter += 1
        time.sleep(1)
        print("\n\n")


def mainMenu():
    response = input("")
    return response

def ascii(text, color):
    print(colored(pyfiglet.figlet_format(text.upper()), color.lower()))



if __name__ == '__main__':
    ascii("ru rah rauh", "RED")
    Courses = getPopoulatedCourses()
    scheduleIndexes = ["07331", "07350", "09542"]
    Text.send("[STARTED] : Search")
    keepAliveCourseCheck(Courses, scheduleIndexes)
