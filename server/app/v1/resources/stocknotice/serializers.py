from app.v1 import api
from flask_restplus import fields

stock_notice_adv = api.model('Stock Notice in advance', {
    'id': fields.String(readonly=True, description='ID', attribute='_id.$oid'),
    'stock_id': fields.String(required=True, description='Stock ID'),
    'predict_finance': fields.String(required=True, description='Predict Finance'),
    'predict_type': fields.String(required=True, description='Predict Type'),
    'predict_content': fields.String(required=True, description='Predict Content'),
    'change_explain': fields.String(required=False, description='Change Explain'),
    'predict_amt_lower': fields.Float(required=False, description='Predict Amt Lower'),
    'predict_amt_upper': fields.Float(required=False, description='Predict Amt Upper'),
    'preyear_same_period': fields.Float(required=False, description='Preyear Same Period'),
    'add_amp_lower': fields.Float(required=False, description='Add Amp Lower'),
    'add_amp_upper': fields.Float(required=False, description='Add Amp Upper'),
    'notice_date': fields.String(required=False, description='Notice Date'),
    'is_latest': fields.String(required=False, description='Is Latest'),
    'rpt_date': fields.String(required=True, description='Report Date')
})
