######################################
# Time:2020/02/07
# alter: ZWQ
######################################

from flask import Blueprint
from flask_restplus import Api
from .views import *

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
user_mold = Blueprint('user_mold', __name__)
api = Api(user_mold, version='1.0', title='USER API',
    description='用户注册 API',authorizations =authorizations,security='apikey')

#注册路由
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
# api.add_resource(AllUsers, '/users')
api.add_resource(SecretResource, '/secret')