from app.v1 import api
from flask_restplus import fields

indicator = api.model('Indicator', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'asset_id': fields.String(required=True, description='Asset ID'),
    'indicator_id': fields.String(required=True, description='Indicator ID'),
    'indicator_date': fields.String(required=True, description='Indicator Date'),
    'value': fields.Float(required=True, description='Value'),
    'update_timestamp': fields.Raw(required=False, description='Update TimeStamp'),
    'user': fields.String(required=False, description='Indicator Owner', default='MYQ')
})
