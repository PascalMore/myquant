from flask_restplus import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required
from .serializers import strategy_execution
from .models import StrategyExecutions


api = Namespace('strategy', 'Strategy Execution Endpoint')
parser = reqparse.RequestParser()
parser.add_argument('strategy_id', type=str, required=False, help='Strategy ID')
parser.add_argument('exe_date', type=str, required=False, help='Execution Date')

@api.route('/execution/')
class StrategyExecution(Resource):
    @api.marshal_with(strategy_execution)
    @api.response(404, 'Strategy execution not found')
    @api.doc(params={'strategy_id': 'Strategy ID', 'exe_date': 'Exection Date'})
    @api.expect(parser)
    @jwt_required
    def get(self):
        """
        Get strategy execution by strategy id of query date
        """
        args = parser.parse_args()
        strategy_execution = StrategyExecutions.get_strategy_execution(args['strategy_id'], args['exe_date'])
        if not strategy_execution:
            api.abort(404, 'Strategy execution not found')
        return strategy_execution

@api.route('/execution/list')
class StrategyExecution(Resource):
    @api.marshal_with(strategy_execution)
    @api.response(404, 'Strategy execution not found')
    @jwt_required
    def get(self):
        """
        Get all strategy execution
        """
        strategy_execution = StrategyExecutions.get_all_strategy_execution()
        if not strategy_execution:
            api.abort(404, 'Strategy execution not found')
        return strategy_execution
