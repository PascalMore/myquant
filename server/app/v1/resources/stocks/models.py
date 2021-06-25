import json
from app import mongo_quantaxis 
from bson.json_util import dumps
from bson.objectid import ObjectId


class StockList:
    def __init__(self):
        pass

    @staticmethod
    def get_all_stocks():
        return json.loads(dumps(mongo_quantaxis.db.stock_list.find().sort([('code', 1)])))
