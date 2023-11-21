from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import stock_list
from .models import StockList

api = Namespace('stock', 'Stock')


@api.route('/stock_list')
class Stock(Resource):

    @api.marshal_list_with(stock_list)
    @jwt_required
    def get(self):
        """
        Get all stocks
        """
        return StockList.get_all_stocks()