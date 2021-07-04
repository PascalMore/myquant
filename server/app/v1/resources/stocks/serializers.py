from app.v1 import api
from flask_restplus import fields

stock_list = api.model('Stock List', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'code': fields.String(required=True, description='Stock ID'),
    'volunit': fields.Integer(required=True, description='Volunit'),
    'decimal_point': fields.Integer(required=True, description='Decimal_point'),
    'name': fields.String(required=True, description='Stock Name'),
    'sse': fields.String(required=True, description='SSE'),
    'sec': fields.String(required=True, description='SEC', default='stock_cn'),
    'pre_close': fields.Float(required=False, description='Pre-close Price')
})
