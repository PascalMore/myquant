from app.v1 import api
from flask_restplus import fields


user = api.model('User', {
    'id': fields.String(readonly=True, description='User ID', attribute='_id.$oid'),
    'username': fields.String(required=True, description='The Username'),
    'email': fields.String(required=True, description='User Email'),
    'roles': fields.List(fields.String, required=True, description='User Roles'),
    'introduction': fields.String(required=False, description='User Introduction'),
    'avatar': fields.String(required=False, description='User photo', default='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif')
})


create_user = api.inherit('User Creation', user, {
    'password': fields.String(required=True, description='User Password'),
})
