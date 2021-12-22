from json import dump, load
import config as config
import requests
from Course import Course
from Assignment import Assignment
import time
import dateutil.parser

api_url=config.base_url+"api/v1/"
def createSess(canvasToken):
    s = requests.Session()
    s.params.update({"access_token": canvasToken})
    return s

def get_course_list(sess):
    info=sess.get(api_url+"courses/?enrollment_type=student&enrollment_state=active&state[]=available&per_page=1000").json()
    course_res=[]
    for course in info:
        # course_res.append({
        #     'id': course['id'],
        #     'code': course['course_code']
        # })
        course_res.append(
          Course(course['course_code'], canvasID=course['id'])
        )
    return course_res

def check_handsub():
    with open(config.data_folder+'paper_submitted.json','r') as source:
        return load(source)

def add_handsub(assignment:int):
    data=check_handsub()
    data.append(assignment)
    with open('paper_submitted.json','w') as source:
        return dump(data,source)

def get_assignment_list(sess, id:int):
    info=sess.get(api_url+"courses/%d/assignments?include[]=submission&per_page=1000"% id).json()
    assi_res=[]
    for assi in info:
        # assi_res.append({
        #     'name':assi['name'],
        #     'assignment_id': assi['id'],
        #     'submission_type' : assi['submission_types'],
        #     'due': assi['due_at'],
        #     'submitted': assi.get('submission') is not None,
        #     'url':assi['html_url']
        # })
        if (assi['due_at'] is None):
          dueTime = None
        else:
          UTCdueTime = dateutil.parser.parse(assi['due_at'])
          from_zone = dateutil.tz.tzutc()
          to_zone = dateutil.tz.tzlocal()
          # Tell the datetime object that it's in UTC time zone since 
          # # datetime objects are 'naive' by default
          utc = UTCdueTime.replace(tzinfo=from_zone)
          dueTime = utc.astimezone(to_zone)
        assi_res.append(
          Assignment(assi['name'], dueTime = dueTime, submitted=assi.get('submission') is not None, canvasID=assi['id'], canvasURL=assi['html_url'])
        )
        # print(assi['name'])
    return assi_res

# def filter_assignment(assi):
#     # print(assi)
#     if assi['assignment_id'] in check_handsub():
#         return False
#     if assi['submitted']:
#         return False
#     if (assi['due'] is None):
#         return False
#     sub_time=time.mktime(time.strptime(assi['due'], '%Y-%m-%dT%H:%M:%SZ'))+ 8* 60 *60
#     now=time.time()
#     if (now>=sub_time):
#         return False
    
#     if (sub_time-now>=config.threshold_day * 24*60*60):
#         return False
#     return True


# def fetch_assignment(sess, course_id:int):
#     info=get_assignment_list(course_id, sess)
#     return l_filter(filter_assignment, info)

def fetch_course(sess):
    info=get_course_list(sess)
    course_list=[]
    for course in info:
        course.setAssignments(get_assignment_list(sess, course.canvasID))
        course_list.append(course)
    return course_list

# courses = fetch_course(createSess())
# for course in courses:
#   print(course)
# def write_info(course_info):
#     with open(config.data_folder+'data.json','w') as file:
#         dump({'info':course_info, 'refreshed_at':time.time()}, file)