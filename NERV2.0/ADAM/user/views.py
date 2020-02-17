######################################
# Time:2020/02/09
# alter: ZWQ
######################################

from flask_restplus import  Resource, reqparse
from .models import UserModel, RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required,get_raw_jwt
from flask_restplus import Api
from common import api

# _api = Api(app)

parser = reqparse.RequestParser()  # 设置接收参数
parser.add_argument('username', type=str, help='username field cannot be blank', required=True)
parser.add_argument('password', type=str, help='password field cannot be blank', required=True)

class UserRegistration(Resource):
    @api.doc(params={'username': '用户名', 'password': '密码'})
    def post(self):
        data = parser.parse_args()  # 接收参数
        if UserModel.find_by_username(data['username']):
            return {'message':f'User {data["username"]} already exists','code':1}
        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message':f'User {data["username"]} .was created',
                'access_token':access_token,
                'refresh_token':refresh_token,
                'code':0
            }
        except:
            return {'messaeg':'Something went wrong','code':1}, 500


class UserLogin(Resource):
    @api.doc(params={'username': '用户名', 'password': '密码'})
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message':f'User {data["username"]} don\'t exist','code':1}
        if UserModel.verify_hash(data['password'],current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': f'Logged in as {data["username"]}',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'code': 0
            }
        else:
            return {'message':'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        print(jti)
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message':'Access token has been revoked','code':0}
        except:
            return {'messgae':'Somethong went wrong','code':1},500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        jti = get_raw_jwt()['jti']
        print(jti)
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked', 'code': 0}
        except:
            return {'messgae': 'Somethong went wrong', 'code': 1}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token':access_token,'code':0}


class SecretResource(Resource):  # Resource 资源
    @jwt_required
    def get(self):
        ret = get_jwt_identity()
        return {
            'awnswer':ret

        }