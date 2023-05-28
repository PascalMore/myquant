from flask_restplus import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required
from .serializers import index_yield
from .models import IndexYieldModel

api = Namespace('index', 'Index')
parser = reqparse.RequestParser()
parser.add_argument('index_list', type=str, required=True, help='Index List')
parser.add_argument('calc_date', type=str, required=True, help='Calc Date')
parser.add_argument('interval_list', type=str, required=True, help='Interval List')



@api.route('/yield')
class Index(Resource):
    @api.marshal_with(index_yield)
    @api.response(404, 'Index not found')
    @api.doc(params={'index_list': 'Index List', 'calc_date': 'Calc Date', 'interval_list': 'Interval List'})
    @api.expect(parser)
    @jwt_required
    def get(self):
        """
        Get index yields
        """
        args = parser.parse_args()
        return IndexYieldModel.get_index_yields(args['index_list'], args['calc_date'], args['interval_list'])