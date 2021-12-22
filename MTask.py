import Canvas
import GradeScope
import config
def fetch():
  GSsession = GradeScope.loginGS('xxx@umich.edu', 'xxx')
  GScourses = GradeScope.getCourseList(GSsession)
  for course in GScourses:
    course.setAssignments(GradeScope.getCourseAssignmentList(GSsession, course))
  