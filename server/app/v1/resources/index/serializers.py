from app.v1 import api
from flask_restplus import fields

index_yield = api.model('Index Yield', {
    'index_id': fields.String(required=True, description='Index ID'),
    'calc_date': fields.String(required=True, description='Calc Date'),
    'index_yields': fields.Raw(required=True, description='Index Yields')
})
