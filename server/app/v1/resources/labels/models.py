import json
from app import mongo
from bson.json_util import dumps

class LabelArchs:

    def __init__(self):
        pass

    @staticmethod
    def get_labelarch_by_name(arch_name):
        label_arch = mongo.db.label_arch.find({'label_arch_id': arch_name})
        if label_arch:
            return json.loads(dumps(label_arch))
        return None
    
    @staticmethod
    def get_all_labelarch(arch_type):
        label_arch = mongo.db.label_arch.find({'label_arch_type': arch_type, 'parent_id': ""})
        if label_arch:
            return json.loads(dumps(label_arch))

class AssetLabels:

    def __init__(self):
        pass

    @staticmethod
    def get_label_by_id(arch_name, aid,  date):
        find_label_date = list(mongo.db.asset_label.find({'label_arch_id': arch_name, 'asset_id': aid, 'label_date': {'$lte': date}}).sort([('label_date', -1)]).limit(1))
        if len(find_label_date) > 0:
            latest = list(find_label_date)[0]['label_date']
            asset_label = mongo.db.asset_label.find({'label_arch_id': arch_name, 'asset_id': aid, 'label_date': latest})
            if asset_label:
                return json.loads(dumps(asset_label))
            else:
                return None
        else:
            return None