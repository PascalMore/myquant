from flask_restplus import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required
from .serializers import stock_pool
from .models import StockPoolModel

api = Namespace('stock_pool', 'Stock Pool')
parser = reqparse.RequestParser()
parser.add_argument('pool_type', type=str, required=False, help='Pool Type')
parser.add_argument('pool_date', type=str, required=False, help='Pool Date')
parser.add_argument('page', type=int, required=False, help='Page Number')
parser.add_argument('limit', type=int, required=False, help='Page Limit')
parser.add_argument('sort', type=str, required=False, help='Sort')


@api.route('/')
class StockPool(Resource):
    @api.marshal_with(stock_pool)
    @api.response(404, 'Stock pool not found')
    @api.doc(params={'pool_type': 'Pool Type', 'pool_date': 'Pool Date'})
    @api.expect(parser)
    @jwt_required
    def get(self):
        """
        Get stock pool
        """
        args = parser.parse_args()
        return StockPoolModel.get_stock_pool(args['pool_type'], args['pool_date'], args)