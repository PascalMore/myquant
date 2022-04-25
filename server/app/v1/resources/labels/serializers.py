from app.v1 import api
from flask_restplus import fields

label_arch = api.model('Label Arch', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'label_arch_id': fields.String(required=True, description='The Label Arch ID'),
    'label_id': fields.String(required=True, description='The Label ID'),
    'label_name': fields.String(required=True, description='Label Name'),
    'parent_id': fields.String(required=True, description='Parent ID Of The Label'),
    'path': fields.List(fields.String, required=True, description='Label Path Of The Arch'),
    'update_timestamp': fields.Raw(required=False, description='Update TimeStamp'),
    'user': fields.String(required=False, description='Label Arch Owner', default='MYQ'),
    'label_arch_type': fields.String(required=True, description='Label Arch Type'),
    'tag': fields.String(required=True, description='Tag')
})

asset_label = api.model('Asset Label', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'asset_id': fields.String(required=True, description='Asset ID'),
    'label_arch_id': fields.String(required=True, description='The Label Arch ID'),
    'label_date': fields.String(required=True, description='Label Date'),
    'label_id': fields.String(required=True, description='The Label ID'),
    'value': fields.String(required=True, description='The Label Value'),
    'user': fields.String(required=False, description='Label Arch Owner', default='MYQ'),
    'update_timestamp': fields.Raw(required=False, description='Update TimeStamp'),
    'tag': fields.String(required=True, description='Tag')
})