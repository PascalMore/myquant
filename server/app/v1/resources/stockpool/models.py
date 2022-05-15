import json
from app import mongo
from bson.json_util import dumps
from bson.objectid import ObjectId

def trans(s):
    if 'NaN' == s:
        return 'NaN'

class StockPoolModel:
    def __init__(self):
        pass

    @staticmethod
    def get_stock_pool(pool_type, pool_date, options):
        query = {}
        type_map = {'basic': '基础池', 'important':'重点池', 'deep': '策略-深度价值'}
        page = 1
        limit = 20
        sort = -1
        if pool_type is not None and len(pool_type) > 0:
            query['pool_type'] = type_map[pool_type]
        if pool_date is not None and len(pool_date) > 0:
            query['import_date'] = {'$lte': pool_date}
        if options['page'] is not None:
            page = options['page']
        if options['limit'] is not None:
            limit = options['limit']
        if options['sort'] is not None:
            sort = 1 if options['sort'] == '+' else -1
        
        print(query)
        query_res = list(mongo.db.asset_pool.find(query).sort([('import_date', -1)]))
        if len(query_res) > 0:
            cur_import_date = query_res[0]['import_date']
            pool_res = list([x for x in query_res if x['import_date'] == cur_import_date])
            return json.loads(dumps(pool_res), parse_constant=trans)
        else:
            return None
