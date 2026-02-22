import requests
import time
import pandas as pd
import numpy as np
import json
import yagmail
from datetime import datetime
import warnings
#通达信指标
warnings.filterwarnings(action='ignore')
import requests
from finta import TA
from tqdm import tqdm


#股票核心数据
class stock_data_ths:
    def __init__(self,qq='1029762153@qq.com'):
        self.qq=qq
    def get_stock_hist_data_em(self,stock='600031',start_date='20210101',end_date='20500101',data_type='D',count=8000):
        '''
        获取股票数据
        start_date=''默认上市时间
        - ``1`` : 分钟
            - ``5`` : 5 分钟
            - ``15`` : 15 分钟
            - ``30`` : 30 分钟
            - ``60`` : 60 分钟
            - ``101`` : 日
            - ``102`` : 周
            - ``103`` : 月
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        try:
            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
            klt=data_dict[data_type]
            secid='{}.{}'.format(0,stock)
            url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
            params = {
                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'beg': start_date,
                'end': end_date,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'rtntype':end_date,
                'secid': secid,
                'klt':klt,
                'fqt': '1',
                'cb': 'jsonp1668432946680'
            }
            res = requests.get(url=url, params=params)
            text = res.text[19:len(res.text) - 2]
            json_text = json.loads(text)
            df = pd.DataFrame(json_text['data']['klines'])
            df.columns = ['数据']
            data_list = []
            for i in df['数据']:
                data_list.append(i.split(','))
            data = pd.DataFrame(data_list)
            columns = ['date', 'open', 'close', 'high', 'low', 'volume', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
            data.columns = columns
            for m in columns[1:]:
                data[m] = pd.to_numeric(data[m])
            data.sort_index(ascending=True,ignore_index=True,inplace=True)
            return data
        except:
            
            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
            klt=data_dict[data_type]
            secid='{}.{}'.format(1,stock)
            url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?'
            params = {
                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
                    'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                    'beg': start_date,
                    'end': end_date,
                    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                    'rtntype':end_date,
                    'secid': secid,
                    'klt':klt,
                    'fqt': '1',
                    'cb': 'jsonp1668432946680'
            }
            res = requests.get(url=url, params=params)
            text = res.text[19:len(res.text) - 2]
            json_text = json.loads(text)
            df = pd.DataFrame(json_text['data']['klines'])
            df.columns = ['数据']
            data_list = []
            for i in df['数据']:
                data_list.append(i.split(','))
            data = pd.DataFrame(data_list)
            columns = ['date', 'open', 'close', 'high', 'low', 'volume', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
            data.columns = columns
            for m in columns[1:]:
                data[m] = pd.to_numeric(data[m])
            data.sort_index(ascending=True,ignore_index=True,inplace=True)
            return data
            
    def get_stock_all_trader_data(self,stock='600031'):
        '''
        获取股票全部分时交易数据
        备用
        :param stock:
        :return:
        '''
        try:
            market,stock='0',stock
            url='http://push2ex.eastmoney.com/getStockFenShi?'
            params = {
                'pagesize': '10000',#144
                'ut': '7eea3edcaed734bea9cbfc24409ed989',
                'dpt': 'wzfscj',
                'cb': 'jQuery1124032472207483171633_1633697823102',
                'pageindex': '0',
                'id': '{}'.format(stock,market),
                'sort': '1',
                'ft': '1',
                'code': '{}'.format(stock),
                'market': '{}'.format(market),
                '_': '1633697823103'
            }
            res=requests.get(url=url,params=params)
            text=res.text[43:len(res.text)-2]
            json_text=json.loads(text)
            df=pd.DataFrame(json_text['data']['data'])
            columns=['date','价格','成交量','买卖数量']
            df.columns=columns
            df['价格']=df['价格']/1000
            df['close']=df['价格']
            return df
        except:
            
            market,stock='1',stock
            url='http://push2ex.eastmoney.com/getStockFenShi?'
            params = {
                    'pagesize': '10000',#144
                    'ut': '7eea3edcaed734bea9cbfc24409ed989',
                    'dpt': 'wzfscj',
                    'cb': 'jQuery1124032472207483171633_1633697823102',
                    'pageindex': '0',
                    'id': '{}'.format(stock,market),
                    'sort': '1',
                    'ft': '1',
                    'code': '{}'.format(stock),
                    'market': '{}'.format(market),
                    '_': '1633697823103'
            }
            res=requests.get(url=url,params=params)
            text=res.text[43:len(res.text)-2]
            json_text=json.loads(text)
            df=pd.DataFrame(json_text['data']['data'])
            columns=['date','价格','成交量','买卖数量']
            df.columns=columns
            df['价格']=df['价格']/1000
            df['close']=df['价格']
            return df
            
    def get_stock_mi_data_em(self,stock='600031'):
        '''
        获取股票数据
        start_date=''默认上市时间
        - ``1`` : 分钟
            - ``5`` : 5 分钟
            - ``15`` : 15 分钟
            - ``30`` : 30 分钟
            - ``60`` : 60 分钟
            - ``101`` : 日
            - ``102`` : 周
            - ``103`` : 月
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        func="""
            from trader_tool.stock_data import stock_data
            models=stock_data()
            df=models.get_stock_mi_data_em(stock="{}")
            """.format(stock)+"""
            df.to_csv(r'{}\数据\{}数据.csv')
            """
        df=self.xg_data.get_user_def_data(func=func)
        return df
    def seed_emial_qq(self,text='交易完成'):
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        try:
            password=text1['qq掩码']
            seed_qq=text1['发送qq']
            yag = yagmail.SMTP(user='{}'.format(seed_qq), password=password, host='smtp.qq.com')
            m = self.qq
            text = text
            yag.send(to=m, contents=text, subject='邮件')
            print('邮箱发生成功')
        except:
            print('qq发送失败可能用的人多')
    def get_trader_date_list(self):
        '''
        获取交易日历
        :return:
        '''
        df=self.get_stock_hist_data_em()
        date_list=df['date'].tolist()
        return date_list
    def check_is_trader_date(self):
        '''
        检测是不是交易时间
        '''
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        #利用通用时间，不考虑中午不交易
        is_trader=''
        wo=loc.tm_wday
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        if wo<=trader_time:
            if (tm_hour>=start_date) and (tm_hour<=end_date):
                is_trader=True
                return True
            else:
                is_trader=False
                return False
        else:
            print('周末')
            return False
    def check_is_trader_date_1(self):
        '''
        检测是不是交易时间
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        if tm_hour==start_date and tm_min<30:
            is_tradre=False
        elif tm_hour==start_date and tm_min>30:
            is_tradre=True
        elif tm_hour>=start_date and tm_hour<=end_date:
            is_tradre=True
        else:
            is_tradre=False
        #利用通用时间，不考虑中午不交易
        wo=loc.tm_wday
        if wo<=trader_time:
            if (is_tradre) and (tm_hour<=end_date):
                return True
            else:
                return False
        else:
            print('周末')
            return False
    def get_stock_set_bidding(self,stock='600031'):
        '''
        获取股票集合竞价数据
        在集合竞价挂牌使用
        :param stock:
        :return:
        '''
        if stock[0]=='6':
            market='1'
        else:
            market='0'
        def select_data(x):
            if int(x)==1:
                return '卖盘'
            elif int(x)==2:
                return '买盘'
            else:
                return x
        url='http://push2ex.eastmoney.com/getStockFenShi?'
        params = {
            'pagesize': '1000000',#144
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            'dpt': 'wzfscj',
            'cb': 'jQuery1124032472207483171633_1633697823102',
            'pageindex': '0',
            'id': '{}'.format(stock,market),
            'sort': '1',
            'ft': '1',
            'code': '{}'.format(stock),
            'market': '{}'.format(market),
            '_': '1633697823103'
        }
        res=requests.get(url=url,params=params)
        text=res.text[43:len(res.text)-2]
        json_text=json.loads(text)
        df=pd.DataFrame(json_text['data']['data'])
        columns=['时间','价格','成交量','买卖性质']
        df.columns=columns
        df['价格']=df['价格']/1000
        df['时间']=df['时间'].astype(int)
        # 选择集合竞价数据
        df['实时涨跌幅']=df['价格'].pct_change()*100
        spot_data=self.get_stock_spot_data(stock=stock)
        df['昨日收盘价']=spot_data['昨收']
        df['涨跌幅']=((df['价格']-df['昨日收盘价'])/df['昨日收盘价'])*100
        df['实时成交额']=(df['价格']*df['成交量'])*100
        df['流通市值']=spot_data['流通市值']
        df['总市值']=spot_data['总市值']
        df['量比']=spot_data['量比']
        df['实时换手率']=(df['实时成交额']/df['流通市值'])*100
        df['证券代码']=spot_data['证券代码']
        df['股票名称']=spot_data['股票名称']
        #df['累计换手率']=df['实时换手率'].cumsum()
        df['买卖性质']=df['买卖性质'].apply(select_data)
        return df
    def get_stock_spot_data(self,stock='002858'):
        '''
        获取股票实时数据
        '''
        try:
            secid='{}.{}'.format(0,stock)
            params={
                'invt':'2',
                'fltt':'1',
                'cb':'jQuery3510180390237681324_1685191053405',
                'fields':'f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f161,f49,f171,f50,f86,f177,f111,f51,f52,f168,f116,f117,f167,f162,f262',
                'secid': secid,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'wbp2u': '1452376043169950|0|1|0|web',
                '_': '1685191053406',
            }
            url='http://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text
            text=text[40:len(text)-2]
            json_text=json.loads(text)
            data=json_text['data']
            result={}
            result['最新价']=data['f43']/100
            result['最高价']=data['f44']/100
            result['最低价']=data['f45']/100
            result['今开']=data['f46']/100
            result['成交量']=data['f47']
            result['成交额']=data['f48']
            result['量比']=data['f50']/100
            result['涨停']=data['f51']/100
            result['跌停']=data['f52']/100
            result['证券代码']=data['f57']
            result['股票名称'] = data['f58']
            result['昨收']=data['f60']/100
            result['总市值']=data['f116']
            result['流通市值']=data['f117']
            result['换手率']=data['f168']/100
            result['涨跌幅']=data['f170']/100
            return result
        except:
            secid='{}.{}'.format(1,stock)
            params={
                    'invt':'2',
                    'fltt':'1',
                    'cb':'jQuery3510180390237681324_1685191053405',
                    'fields':'f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f161,f49,f171,f50,f86,f177,f111,f51,f52,f168,f116,f117,f167,f162,f262',
                    'secid': secid,
                    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                    'wbp2u': '1452376043169950|0|1|0|web',
                    '_': '1685191053406',
            }
            url='http://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text
            text=text[40:len(text)-2]
            json_text=json.loads(text)
            data=json_text['data']
            result={}
            result['最新价']=data['f43']/100
            result['最高价']=data['f44']/100
            result['最低价']=data['f45']/100
            result['今开']=data['f46']/100
            result['成交量']=data['f47']
            result['成交额']=data['f48']
            result['量比']=data['f50']/100
            result['涨停']=data['f51']/100
            result['跌停']=data['f52']/100
            result['证券代码']=data['f57']
            result['股票名称'] = data['f58']
            result['昨收']=data['f60']/100
            result['总市值']=data['f116']
            result['流通市值']=data['f117']
            result['换手率']=data['f168']/100
            result['涨跌幅']=data['f170']/100
            return result
           
    def get_stock_spot_data_1(self,stock='002858'):
        '''
        获取股票实时数据
        '''
        stock_1=stock
        try:
            stock='0.'+stock
            params={
                'invt':'2',
                'fltt':'1',
                'cb':'jQuery3510180390237681324_1685191053405',
                'fields':'f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f161,f49,f171,f50,f86,f177,f111,f51,f52,f168,f116,f117,f167,f162,f262',
                'secid': stock,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'wbp2u': '1452376043169950|0|1|0|web',
                '_': '1685191053406',
            }
            url='http://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text
            text=text[40:len(text)-2]
            json_text=json.loads(text)
            data=json_text['data']
            result=pd.DataFrame()
            result['股票现价']=[data['f43']/100]
            result['股票最高价']=[data['f44']/100]
            result['股票最低价']=[data['f45']/100]
            result['股票今开']=[data['f46']/100]
            result['股票成交量']=[data['f47']]
            result['股票成交额']=[data['f48']]
            result['股票量比']=[data['f50']/100]
            result['股票涨停']=[data['f51']/100]
            result['股票跌停']=[data['f52']/100]
            result['股票代码']=[data['f57']]
            result['股票名称'] = [data['f58']]
            result['股票昨收']=[data['f60']/100]
            result['股票总市值']=[data['f116']]
            result['股票流通市值']=[data['f117']]
            result['股票动态市盈率']=[data['f162']/100]
            result['股票市净率']=[data['f167']/100]
            result['股票换手率']=[data['f168']/100]
            result['股票涨跌']=[data['f169']/100]
            result['股票涨跌幅']=[data['f170']/100]
            result['股票振幅']=[data['f171']/100]
            return result
        except:
            stock=stock_1
            stock='1.'+stock
            params={
                'invt':'2',
                'fltt':'1',
                'cb':'jQuery3510180390237681324_1685191053405',
                'fields':'f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f161,f49,f171,f50,f86,f177,f111,f51,f52,f168,f116,f117,f167,f162,f262',
                'secid': stock,
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'wbp2u': '1452376043169950|0|1|0|web',
                '_': '1685191053406',
            }
            url='http://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text
            text=text[40:len(text)-2]
            json_text=json.loads(text)
            data=json_text['data']
            result=pd.DataFrame()
            result['股票现价']=[data['f43']/100]
            result['股票最高价']=[data['f44']/100]
            result['股票最低价']=[data['f45']/100]
            result['股票今开']=[data['f46']/100]
            result['股票成交量']=[data['f47']]
            result['股票成交额']=[data['f48']]
            result['股票量比']=[data['f50']/100]
            result['股票涨停']=[data['f51']/100]
            result['股票跌停']=[data['f52']/100]
            result['股票代码']=[data['f57']]
            result['股票名称'] = [data['f58']]
            result['股票昨收']=[data['f60']/100]
            result['股票总市值']=[data['f116']]
            result['股票流通市值']=[data['f117']]
            result['股票动态市盈率']=[data['f162']/100]
            result['股票市净率']=[data['f167']/100]
            result['股票换手率']=[data['f168']/100]
            result['股票涨跌']=[data['f169']/100]
            result['股票涨跌幅']=[data['f170']/100]
            result['股票振幅']=[data['f171']/100]
            return result









