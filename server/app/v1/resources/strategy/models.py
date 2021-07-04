import json
from app import mongo
from bson.json_util import dumps

class StrategyExecutions:

    def __init__(self):
        pass

    @staticmethod
    def get_strategy_execution(strategy_id, exe_date):
        query = {}
        if strategy_id is not None:
            query['strategy_id'] = strategy_id
        if exe_date is not None:
            query['exe_date'] = {'$lte': exe_date}

        strategy_res = list(mongo.db.strategy_execution.find(query).sort([('exe_date', -1)]))
        if (len(strategy_res) > 0):
            return json.loads(dumps(strategy_res[0]))
        else:
            return None

    @staticmethod
    def get_all_strategy_execution():
        strategy_res = list(mongo.db.strategy_execution.find().sort([('exe_date', -1)]))
        if (len(strategy_res) > 0):
            return json.loads(dumps(strategy_res))
        else:
            return None