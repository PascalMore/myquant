import json
from app import mongo
from bson.json_util import dumps

def trans(s):
    if 'NaN' == s:
        return 'NaN'

class StrategyExecutions:

    def __init__(self):
        pass

    @staticmethod
    def get_strategy_execution(strategy_id, exe_date):
        query = {}
        if strategy_id is not None and len(strategy_id) > 0:
            query['strategy_id'] = strategy_id
        if exe_date is not None and len(exe_date) > 0:
            query['exe_date'] = {'$lte': exe_date}
        
        query_res = list(mongo.db.strategy_execution.find(query).sort([('exe_date', -1)]))
        if len(query_res) > 0:
            cur_exe_date = query_res[0]['exe_date']
            strategy_res = list([x for x in query_res if x['exe_date'] == cur_exe_date])
            return json.loads(dumps(strategy_res), parse_constant=trans)
        else:
            return None

    @staticmethod
    def get_all_strategy_execution():
        strategy_res = list(mongo.db.strategy_execution.find().sort([('exe_date', -1)]))
        if (len(strategy_res) > 0):
            return json.loads(dumps(strategy_res))
        else:
            return None