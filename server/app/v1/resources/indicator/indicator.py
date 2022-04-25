from flask_restplus import Resource, Namespace,reqparse
from flask_jwt_extended import jwt_required
from .serializers import indicator
from .models import IndicatorList

api = Namespace('indicator', 'Indicator')
parser = reqparse.RequestParser()
parser.add_argument('ind', type=str, required=False, help='Indicator ID')
parser.add_argument('date', type=str, required=False, help='Indicator Date')

@api.route('/')
class Indicator(Resource):
    @api.marshal_list_with(indicator)
    @api.doc(params={'ind': 'Indicator ID', 'date': 'Indicator Date'})
    @api.expect(parser)
    @jwt_required
    def get(self):
        """
        Get indicators
        """
        args = parser.parse_args()
        inds = IndicatorList.get_indicators(args['ind'], args['date'])
        if not inds:
            api.abort(404, 'Indicator not found')
        return inds