from app.v1 import api
from flask_restplus import fields


article_list = api.model('Article List', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'update_timestamp': fields.Raw(required=True, description='Update TimeStamp'),
    'author': fields.String(required=True, description='Author'),
    'reviewer': fields.String(required=True, description='Reviewer'),
    'title': fields.String(required=True, description='Title'),
    'content_short': fields.String(required=True, description='Abstracts'),
    'content': fields.String(required=True, description='Content'),
    'importance': fields.Integer(required=True, description='Importance'),
    'status': fields.String(required=True, description='Article Status'),
    'display_timestamp': fields.Raw(required=False, description='Display TimeStamp'),
    'comment_disabled': fields.Boolean(required=True, description='Able to Comment'),
    'pageviews': fields.Integer(required=True, description='Page Views Stats'),
    'image_uri': fields.String(required=True, description='Article Cover'),
    'platforms': fields.List(fields.Raw, required=False, description='Platforms')
})
