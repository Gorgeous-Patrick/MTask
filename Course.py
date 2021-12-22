class Course:
  def __init__(self, courseName: str, gradescopeURL: str = '', canvasID: int = -1):
    self.courseName = courseName
    self.gradescopeURL = gradescopeURL
    self.assignments = []
    self.canvasID = canvasID;
  def __str__(self):
    title = f'Course Name: {self.courseName}\nGradeScope URL: {self.gradescopeURL}\nAssignments'
    for assignment in self.assignments:
      title+='\n'+assignment.__str__()+'\n'
    return title
  def setAssignments(self, assignments):
    self.assignments = assignments