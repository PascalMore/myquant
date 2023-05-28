import json
from bson.json_util import dumps
from bson.objectid import ObjectId
import QUANTAXIS as qa
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import calendar
import pandas as pd

def trans(s):
    if 'NaN' == s:
        return 'NaN'

def find_cur_start(td, date_list,inter):
    td = datetime.strptime(td, "%Y-%m-%d")
    start_d = None
    if inter == 'td':
        this_td_start = date_list.index.tolist()[-1]
        start_d = date_list[date_list.index < this_td_start.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == 'week':
        this_week_start = td - timedelta(days=td.weekday())
        #print(date_list.index.tolist()[0].strftime("%Y-%m-%d"))
        #print(this_week_start.strftime("%Y-%m-%d"))
        #print(date_list)
        start_d = date_list[date_list.index < this_week_start.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == 'mon':
        this_mon_start =  datetime(td.year, td.month, 1)
        start_d = date_list[date_list.index < this_mon_start.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == 'quart':
        month = (td.month - 1) - (td.month - 1) % 3 + 1
        this_quarter_start = datetime(td.year, month, 1)
        start_d = date_list[date_list.index < this_quarter_start.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == 'ytd':
        this_year_start = datetime(td.year, 1, 1)
        start_d = date_list[date_list.index < this_year_start.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    else:
        print("find_cur_start - NotImplementedError")

    return start_d

def find_last_start(td, date_list, inter):
    td = datetime.strptime(td, "%Y-%m-%d")
    start_d = None
    if inter == '1w':
        last_1w = td - relativedelta(weeks=1)
        start_d = date_list[date_list.index <= last_1w.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == '2w':
        last_2w = td  - relativedelta(weeks=2)
        start_d = date_list[date_list.index <= last_2w.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == '1m':
        last_1m = td - relativedelta(months=1)
        start_d = date_list[date_list.index <= last_1m.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == '2m':
        last_2m = td  - relativedelta(months=2)
        start_d = date_list[date_list.index <= last_2m.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == '3m':
        last_3m = td  - relativedelta(months=3)
        start_d = date_list[date_list.index <= last_3m.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == '6m':
        last_6m = td  - relativedelta(months=6)
        start_d = date_list[date_list.index <= last_6m.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    elif inter == '1y':
        last_1y = td  - relativedelta(years=1)
        start_d = date_list[date_list.index <= last_1y.strftime("%Y-%m-%d")]
        start_d = start_d.index.tolist()[-1].strftime("%Y-%m-%d")
    else:
        print("find_cur_start - NotImplementedError")

    return start_d

def find_start_end_m(td, date_list, inter):
    td = datetime.strptime(td, "%Y-%m-%d")
    month = int(inter)
    s = datetime(td.year, month, 1)
    e = datetime(td.year, month, calendar.monthrange(td.year, month)[1])
    start_d = date_list[date_list.index < s.strftime("%Y-%m-%d")].index.tolist()[-1].strftime("%Y-%m-%d")
    end_d = date_list[date_list.index <= e.strftime("%Y-%m-%d")].index.tolist()[-1].strftime("%Y-%m-%d")
    return start_d,end_d

def find_start_end_y(td, date_list, inter):
    td = datetime.strptime(td, "%Y-%m-%d")
    year = int(inter)
    s = datetime(year, 1, 1)
    e = datetime(year, 12, 31)
    if date_list.index.tolist()[0] > s:
        start_d = None
    else:
        start_d = date_list[date_list.index < s.strftime("%Y-%m-%d")].index.tolist()[-1].strftime("%Y-%m-%d")
    end_d = date_list[date_list.index <= e.strftime("%Y-%m-%d")].index.tolist()[-1].strftime("%Y-%m-%d")
    return start_d,end_d



class IndexYieldModel:
    def __init__(self):
        pass

    @staticmethod
    def get_index_yields(index_list, calc_date, interval_list):
        #0.默认取近5年的历史行情
        EARLY_D = datetime.strptime(calc_date, "%Y-%m-%d")  - relativedelta(years=5)
        #1. 获取所有的index id对应的所有历史行情
        index_list = index_list.split(',')
        interval_list = interval_list.split(',')
        index_mkt_data = qa.QA_fetch_index_day_adv(index_list, EARLY_D.strftime("%Y-%m-%d"), calc_date)
        #index_mkt_data.show()
        #2. 计算不同区间增长率
        res = pd.DataFrame(columns=('index_id', 'calc_date', 'index_yields'))
        for inx_id in index_list:
            mkt_data = index_mkt_data.select_code(inx_id)
            mkt_data = mkt_data.data.reset_index(level=[1])
            inx_yields = {}
            for inter in interval_list:
                if inter.startswith('cur'):
                    #print(mkt_data.index.levels[0])
                    start_d = find_cur_start(calc_date, mkt_data, inter.split('_')[-1])
                    end_d = mkt_data.index.tolist()[-1].strftime("%Y-%m-%d")
                    #print(start_d)
                    #print(end_d)
                elif inter.startswith('last'):
                    start_d = find_last_start(calc_date, mkt_data, inter.split('_')[-1])
                    end_d = mkt_data.index.tolist()[-1].strftime("%Y-%m-%d")
                    #print(start_d)
                    #print(end_d)
                elif inter.startswith('m'):
                    start_d, end_d = find_start_end_m(calc_date, mkt_data, inter.split('_')[-1])
                    #print(start_d)
                    #print(end_d)
                elif inter.startswith('y'):
                    start_d, end_d = find_start_end_y(calc_date, mkt_data, inter.split('_')[-1])
                    #print(start_d)
                    #print(end_d)
                else:
                    print("Not Support Interval")
                    continue

                if start_d is not None:
                    inx_yields[inter] = mkt_data.loc[end_d]['close'] / mkt_data.loc[start_d]['close'] - 1
                    #print(inx_yields)
                    #print(inx_yield['inter'])
                else:
                    inx_yields[inter] = None
            
            res = res.append({
                'index_id':  inx_id,
                'calc_date': end_d,
                'index_yields':inx_yields
                }, ignore_index=True)

        print(res)
        return  json.loads(dumps(res.to_dict(orient='records')), parse_constant=trans)

#IndexYieldModel.get_index_yields("000300,000852,399006,000688,159920,513130,513500,513300", "2023-05-25", "m_1,m_2,m_3,m_4,m_5,cur_td,cur_week,cur_mon,cur_quart,cur_ytd,y_2022,y_2021,last_1w,last_2w,last_1m,last_2m,last_3m,last_6m,last_1y")