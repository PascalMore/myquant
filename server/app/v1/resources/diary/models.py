import json
from app import mongo 
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

class ArticleList:
    def __init__(self):
        pass

    @staticmethod
    def get_article_list():
        return json.loads(dumps(mongo.db.article.find().sort([('update_timestamp', 1)])))
    
    @staticmethod
    def create_article(d):
        try:
            #设置更新时间戳
            d['update_timestamp'] = datetime.datetime.now()
            res = mongo.db.article.insert_one(d)
            print(res)
            return 0
        except Exception as e:
            print(e)
            return 1
        