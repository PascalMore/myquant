from app.v1 import api
from flask_restplus import fields


strategy_execution = api.model('Strategy Execution', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'strategy_id': fields.String(required=True, description='The Strategy ID'),
    'exe_date': fields.String(required=True, description='Execute Date'),
    'strategy_res': fields.List(fields.Raw, required=True, description='Strategy Results'),
    'update_timestamp': fields.Raw(required=False, description='Update TimeStamp'),
    'user': fields.String(required=False, description='Strategy Owner', default='MYQ')
})
