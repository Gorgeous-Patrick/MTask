import os
from credentials import canvasToken, GradeScopeEmail, GradeScopePasswd # Create a token.py in the canvas_task folder and write token='<Your token>'
base_url="https://umich.instructure.com/"
threshold_day=7
data_folder=os.path.join(os.environ.get('HOME'),'canvas_task_data/')