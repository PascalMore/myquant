import json
from app import mongo 
from bson.json_util import dumps
from bson.objectid import ObjectId


class IndicatorList:
    def __init__(self):
        pass

    @staticmethod
    def get_indicators(ind, date):
        find_ind_date = list(mongo.db.asset_indicator.find({"indicator_id": ind, "indicator_date": {'$lte': date}}).sort([('indicator_date', -1)]).limit(1))
        if len(find_ind_date) > 0:
            latest = list(find_ind_date)[0]['indicator_date']
            asset_indicator = mongo.db.asset_indicator.find({'indicator_id': ind, 'indicator_date': latest})
            if asset_indicator:
                return json.loads(dumps(asset_indicator))
            else:
                return None
        else:
            return None
