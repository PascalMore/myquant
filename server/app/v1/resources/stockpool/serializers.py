from app.v1 import api
from flask_restplus import fields

stock_pool = api.model('Stock Pool', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'asset_id': fields.String(required=True, description='Asset ID'),
    'pool_type': fields.String(required=True, description='Pool Type'),
    'import_date': fields.String(required=True, description='Import Date'),
    'update_timestamp': fields.Raw(required=False, description='Update TimeStamp'),
    'user': fields.String(required=False, description='Pool Owner', default='MYQ')
})
