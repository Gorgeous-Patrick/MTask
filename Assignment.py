from datetime import datetime
class Assignment:
  assignmentName = ''
  dueTime = 0
  gradescopeURL = ''
  submitted = False
  def __init__(self, assignmentName: str, dueTime: datetime, submitted: bool, gradescopeURL:str = '', canvasURL:str = '', canvasID = ''):
    self.assignmentName = assignmentName
    self.dueTime = dueTime
    self.gradescopeURL = gradescopeURL
    self.submitted = submitted
    self.canvasURL = canvasURL
    self.canvasID = canvasID
  def __str__(self):
    return f'{self.assignmentName}: \nDue at {self.dueTime}\nGradeScope at {self.gradescopeURL}\nCanvas at {self.canvasURL}\nSubmitted: {self.submitted}'