from flask_restplus import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required
from .serializers import stock_notice_adv
from .models import StockNoticeAdvModel

api = Namespace('stock_notice_adv', 'Stock Notice in Advance')
parser = reqparse.RequestParser()
parser.add_argument('notice_date', type=str, required=False, help='Notice Date')
parser.add_argument('rpt_date', type=str, required=False, help='Report Date')
parser.add_argument('predict_finance', type=str, required=False, help='Predict Finance')
parser.add_argument('predict_type', type=str, required=False, help='Predict Type')
parser.add_argument('page', type=int, required=False, help='Page Number')
parser.add_argument('limit', type=int, required=False, help='Page Limit')
parser.add_argument('sort', type=str, required=False, help='Sort')

#2023/11/21解决浏览器登录后还是反复出现401的问题，api.route不需要再设置"/",就是值为''
@api.route('')
class StockNoticeAdv(Resource):
    @api.marshal_with(stock_notice_adv)
    @api.response(404, 'Stock notice in advance not found')
    @api.doc(params={'notice_date': 'Notice Date', 'rpt_date': 'Report Date', 'predict_finance': 'Predict Finance', 'predict_type': 'Predict Type'})
    @api.expect(parser)
    @jwt_required
    def get(self):
        """
        Get stock notice in advance
        """
        args = parser.parse_args()
        return StockNoticeAdvModel.get_stock_notice_adv(args['notice_date'], args['rpt_date'], args['predict_finance'], args['predict_type'], args)