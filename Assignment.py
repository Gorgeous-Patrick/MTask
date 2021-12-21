from datetime import datetime
class Assignment:
  assignmentName = ''
  dueTime = 0
  gradescopeURL = ''
  submitted = False
  def __init__(self, assignmentName: str, dueTime: datetime, submitted: bool, gradescopeURL:str):
    self.assignmentName = assignmentName
    self.dueTime = dueTime
    self.gradescopeURL = gradescopeURL
    self.submitted = submitted
  def __str__(self):
    return f'{self.assignmentName}: \nDue at {self.dueTime}\nGradeScope at {self.gradescopeURL}\nSubmitted: {self.submitted}'