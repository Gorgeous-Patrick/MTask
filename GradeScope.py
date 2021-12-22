from bs4 import BeautifulSoup
import requests
from Course import Course
from Assignment import Assignment
import dateutil.parser

def loginGS(email: str, passwd: str):
  session = requests.Session()
  fakeHeader = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
  } # As if I am a browser!
  homePage = session.get('https://www.gradescope.com/', headers = fakeHeader)
  parsedHomePage = BeautifulSoup(homePage.text, 'html.parser')
  # print(parsedHomePage.prettify())
  for form in parsedHomePage.find_all('form'):
    if form.get("action") == "/login":
      for inp in form.find_all('input'):
        if inp.get('name') == "authenticity_token":
          auth_token = inp.get('value')
  # print(auth_token)

  credentials = {
    "utf8": "✓",
    "session[email]": email,
    "session[password]": passwd,
    "session[remember_me]": 0,
    "commit": "Log In",
    "session[remember_me_sso]": 0,
    "authenticity_token": auth_token,
  }

  loginPage = session.post('https://www.gradescope.com/login', params= credentials)
  if len(loginPage.history)!=0 and loginPage.history[0].status_code == requests.codes.found:
    return session
  else:
    print('Login Error\n Check your email and password!')
    exit()

def htmlToCourse(parsedHtml):
  url = "https://www.gradescope.com" + parsedHtml.get("href")
  name = parsedHtml.contents[0].contents[0]
  course = Course(name, url)
  # print(course)
  return course

def htmlToAssignment(parsedHtml):
  nameBlock = parsedHtml.find('th')
  name_1 = nameBlock.find_all('a')
  url = ''
  if (len(name_1)!=0):
    name = name_1[0].contents[0]
    url = "https://www.gradescope.com" + name_1[0].get('href')
  else:
    name = nameBlock.contents[0]
  # print(parsedHtml)
  submissionText = parsedHtml.find('div', class_= 'submissionStatus--text')
  if (submissionText!=None and submissionText.contents[0] == 'No Submission'):
    submitted = False
  else:
    submitted = True
  due = parsedHtml.find('span', class_ = 'submissionTimeChart--dueDate')
  if (due!=None):
    dueStr = due.contents[0]
    dueDate=dateutil.parser.parse(dueStr)
  else:
    dueDate = None
  assignment = Assignment(name, dueDate,submitted, url)
  return assignment

def getCourseList(session):
  courseListPage = session.get('https://www.gradescope.com/account')
  parsedCourseListPage = BeautifulSoup(courseListPage.text, 'html.parser')
  htmlCourses = parsedCourseListPage.find_all('a', class_ = 'courseBox')
  # print(htmlCourses)
  courses = []
  for course in htmlCourses:
    courses.append(htmlToCourse(course))
  return courses

def getCourseAssignmentList(session, course:Course):
  coursePage = session.get(course.gradescopeURL)
  # print(coursePage.text)
  parsedCoursePage = BeautifulSoup(coursePage.text, 'html.parser')
  assignmentTable = parsedCoursePage.find('table', id = 'assignments-student-table')
  htmlAssignments =assignmentTable.find('tbody')
  assignmentEntries = htmlAssignments.find_all('tr')
  assignments=[]
  for assignment in assignmentEntries:
    assignments.append(htmlToAssignment(assignment))
  return assignments

