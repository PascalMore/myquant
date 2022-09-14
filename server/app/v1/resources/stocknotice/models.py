import json
from app import mongo_fundamental
from bson.json_util import dumps
from bson.objectid import ObjectId
from dateutil.relativedelta import relativedelta
import datetime

def trans(s):
    if 'NaN' == s:
        return None

def get_next_rpt():
    td = datetime.datetime.now().strftime("%Y%m%d")
    d=['0331', '0430','0831','1031']
    cur = td[-4:]
    if cur > '0430' and cur <= '0831':
        rpt_date = td[:4] + '0630'
    elif cur > '0831'and cur <= '1031':
        rpt_date = td[:4] + '0930'
    elif cur > '1031':
        rpt_date = td[:4] + '1231'
    else:
        if cur <= '0331':
            rpt_date = str(int(td[:4]) - 1) + '1231'
        else:
            rpt_date = td[:4] + '0331'
    return rpt_date

class StockNoticeAdvModel:
    def __init__(self):
        pass

    @staticmethod
    def get_stock_notice_adv(notice_date, rpt_date, predict_finance, predict_type, options):
        query = {}
        page = 1
        limit = 20
        sort = -1

        if notice_date is not None and len(notice_date) > 0:
            query['notice_date'] = notice_date
        else:
            td = datetime.date.today()
            nd = td + relativedelta(days=1)
            query['notice_date'] = {'$lte': nd.strftime("%Y%m%d")}
        if rpt_date is not None and len(rpt_date) > 0:
            query['rpt_date'] = rpt_date
        else:
            query['rpt_date'] = get_next_rpt()

        if predict_finance is not None and len(predict_finance) > 0:
            query['predict_finance'] = predict_finance
        if predict_type is not None and len(predict_type) > 0:
            query['predict_type'] = predict_type
        if options['page'] is not None:
            page = options['page']
        if options['limit'] is not None:
            limit = options['limit']
        if options['sort'] is not None:
            sort = 1 if options['sort'] == '+' else -1
        query['is_latest'] = 'T'

        print(query)
        query_res = list(mongo_fundamental.db.announce_pre.find(query).sort([('notice_date', -1)]))
        if len(query_res) > 0:
            #cur_notice_date = query_res[0]['notice_date']
            #notice_res = list([x for x in query_res if x['notice_date'] == cur_notice_date])
            # 注意对于NaN需要转换为None，才能被JavaScript解析
            x = json.loads(dumps(query_res), parse_constant=trans)
            return x
        else:
            return None
