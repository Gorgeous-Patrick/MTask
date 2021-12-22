import datetime
import dateutil
from Assignment import Assignment
import Canvas
from Course import Course
import GradeScope
import config

def filter_assignment(assi:Assignment):
    # print(assi)
    # if assi['submitted']:
    #     return False
    if (assi.dueTime is None):
        return False
    # time = datetime.datetime.fromisoformat('2021-10-01')
    # This is the test time.
    time = datetime.datetime.now()
    now = time.replace(tzinfo=dateutil.tz.tzlocal())
    
    if (assi.submitted):
      return False

    if (now>=assi.dueTime):
        return False
    
    if (assi.dueTime-now>=datetime.timedelta(days=config.threshold_day)):
        return False
    return True



def lFilter(f,l):
  res = list(filter(f, l))
  # print(res)
  return res;

def filter_course(course:Course):
  newAssign = lFilter(filter_assignment, course.assignments)
  course.assignments = newAssign
  if (len(course.assignments) == 0):
    return False
  return True

def fetch():
  GSsession = GradeScope.loginGS(config.GradeScopeEmail, config.GradeScopePasswd)
  GScourses = GradeScope.getCourseList(GSsession)
  for course in GScourses:
    course.setAssignments(GradeScope.getCourseAssignmentList(GSsession, course))
  Canvassession = Canvas.createSess(config.canvasToken)
  Canvascourses = Canvas.fetch_course(Canvassession)
  return lFilter(filter_course, GScourses), lFilter(filter_course, Canvascourses)

def output(gradescope: Course, canvas: Course):
  print('---GradeScope List---')
  for course in gradescope:
    print(course)
  print('---Canvas List---')
  for course in canvas:
    print(course)

gradescope, canvas = fetch()
output(gradescope, canvas)