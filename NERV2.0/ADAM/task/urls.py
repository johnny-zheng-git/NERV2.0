######################################
# Time:2020/02/11
# alter: ZWQ
######################################

from flask_restplus import Api
from flask import Blueprint
from .views import find_task,add_task,del_task,updata_task

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
task_mold = Blueprint('task_mold',__name__)
api = Api(task_mold, version='1.0', title='Task API',
    description='ToDoList 任务列表增删改查 API',authorizations =authorizations,security='apikey')

api.add_resource(find_task,'/find')
api.add_resource(add_task,'/add')
api.add_resource(del_task,'/del')
api.add_resource(updata_task,'/updata')
