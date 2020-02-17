######################################
# Time:2020/02/11
# alter: ZWQ
######################################
from flask_restplus import Api
from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import ToDoList  # ToDoList自定义库 ，点击ctrl+left
from common import api



parser = reqparse.RequestParser()
parser.add_argument('taskname', type=str, help='taskname field cannot be blank')
parser.add_argument('accomplish', type=str, help='accomplish field cannot be blank')
parser.add_argument('taskid', type=int, help='taskid field cannot be blank')
def str_to_bool(convert_str):
    '''转换接收json数据str -> bool
    传入值非true/false抛异常
    '''
    convert_str = convert_str.lower()
    if convert_str == 'true':
        return True
    elif convert_str == 'false':
        return  False
    raise RuntimeError('str_to_bool_error')


class find_task(Resource):
    '''查询任务'''
    @jwt_required   # 需要登录或带有access_token 请求
    def get(self):
        username = get_jwt_identity()
        result = ToDoList.find_task_by_username(username)  # 库的类方法，通过用户名查询所有该用户下的任务信息
        task_list = list()
        for i in result:
            task_list.append({i.id:[i.taskname,i.accomplish]})  # 获取到的任务信息转换前端json数据
        return {'message':'success','code':0,'task_list':task_list}

class add_task(Resource):
    '''添加任务'''
    @jwt_required
    @api.doc(params={'taskname': '任务名','accomplish': '完成标志,布尔类型'})  # 添加swagger参数
    def post(self):
        data_parser = parser.parse_args()
        try:
            accomplish = str_to_bool(data_parser['accomplish'])
            new_task = ToDoList(
                username=get_jwt_identity(),
                taskname=data_parser['taskname'],
                accomplish=accomplish
            )
            new_task.save_to_db()
        except Exception as e:
            print(e)
            return {'message':'F','code':1}, 500
        else:
            return {'message': 'success', 'code': 0}


class del_task(Resource):
    '''删除任务'''
    @jwt_required
    @api.doc(params={'taskid': '任务id，int类型'})
    def post(self):
        data = parser.parse_args()
        try:
            ToDoList.del_task(data['taskid'])  # 自定义类方法，通过任务id删除数据
        except Exception as e:
            return {'message': 'F', 'code': 1} , 500
        else:
            return {'message': 'success', 'code': 0}


class updata_task(Resource):
    '''更新任务'''
    @jwt_required
    @api.doc(params={'taskid': '任务id，int类型','accomplish': '完成标志,布尔类型'})
    def post(self):
        data = parser.parse_args()
        try:
            accomplish = str_to_bool(data['accomplish'])
            ToDoList.update_task(data['taskid'],data['taskname'],accomplish)  # 通过任务id定位数据更新任务信息
        except Exception as e:
            print(e)
            return {'message': 'F', 'code': 1}, 500
        else:
            return {'message': 'success', 'code': 0}



