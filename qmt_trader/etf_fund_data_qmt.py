import pandas as pd
import easyquotation
import requests
import json
import time
import yagmail
from qmt_trader import demjson
from  .qmt_data import qmt_data
from qmt_trader.xtquant import xtdata
from datetime import datetime
class etf_fund_data_qmt:
    def __init__(self,data_api='qmt'):
        '''
        etf基金数据
        '''
        self.qmt_data=qmt_data()
        self.qmt_all_data=self.qmt_data.get_all_data()
        self.data_api=data_api
    def adjust_stock(self,stock='600031.SH'):
        '''
        调整代码
        '''
        if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
            stock=stock.upper()
        else:
            if stock[:3] in ['110','113','118','510','519',
                            "900",'200'] or stock[:2] in ['11','51','60','68'] or stock[:1] in ['5']:
                stock=stock+'.SH'
            else:
                stock=stock+'.SZ'
        return stock
    def get_ETF_fund_hist_data(self,stock='159805',end='20500101',limit='1000000',
                                data_type='D',fqt='1',count=8000):
            '''
            获取ETF基金历史数据
            stock 证券代码
            end结束时间
            limit数据长度
            data_type数据类型：
            1 1分钟
            5 5分钟
            15 15分钟
            30 30分钟
            60 60分钟
            D 日线数据
            W 周线数据
            M 月线数据
            fqt 复权
            fq=0股票除权
            fq=1前复权
            fq=2后复权
            '''
            #qmt数据
            qmt_dict={'1': '1m', '5': '5m', '15': '15m', '30': '30m', '60': '60m', 'D': '1d', 'W': '1d', 'M': '1mon',
                    "tick":'tick','1q':"1q","1hy":"1hy","1y":"1y"}
            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
            if self.data_api=='qmt':
                try:
               
                    start_date='20200101'
                    end_time=end
                    stock_1=self.adjust_stock(stock=stock)
                    period=qmt_dict.get(data_type,'D')
                    subscribe_id=xtdata.subscribe_quote(stock_code=stock_1,period=period,start_time=start_date,end_time=end,count=-1)
                    data=xtdata.get_market_data_ex(stock_list=[stock_1],period=period,start_time=start_date,end_time=end_time,count=-1)
                    data=data[stock_1]
                    if data.shape[0]>0:
                        #['date', 'open', 'close', 'high', 'low', 'volume', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
                        data['date']=data.index.tolist()
                        data['成交额']=data['amount']
                        data['涨跌幅']=data['close'].pct_change()*100
                        data['涨跌额']=data['close']-data['close'].shift(1)
                        xtdata.unsubscribe_quote(subscribe_id)
                        return data
                    else:
                        try:
                            secid='{}.{}'.format(0,stock)
                            klt=data_dict[data_type]
                            params={
                                    'secid':secid,
                                    'klt':klt,
                                    'fqt':fqt,
                                    'lmt':limit,
                                    'end':end,
                                    'iscca': '1',
                                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                                    'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                    'forcect': '1',
                                }
                            url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                            res = requests.get(url=url, params=params)
                            text = res.text
                            json_text = json.loads(text)
                            df = pd.DataFrame(json_text['data']['klines'])
                            df.columns = ['数据']
                            data_list = []
                            for i in df['数据']:
                                data_list.append(i.split(','))
                            data = pd.DataFrame(data_list)
                            columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                                        '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                            data.columns = columns
                            del data['_']
                            for m in columns[1:-3]:
                                data[m] = pd.to_numeric(data[m])
                            data1=data.sort_index(ascending=True,ignore_index=True)
                            return data1
                        except:
                            
                            secid='{}.{}'.format(1,stock)
                            data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
                            klt=data_dict[data_type]
                            params={
                                        'secid':secid,
                                        'klt':klt,
                                        'fqt':fqt,
                                        'lmt':limit,
                                        'end':end,
                                        'iscca': '1',
                                        'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                                        'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                                        'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                        'forcect': '1',
                                }
                            url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                            res = requests.get(url=url, params=params)
                            text = res.text
                            json_text = json.loads(text)
                            df = pd.DataFrame(json_text['data']['klines'])
                            df.columns = ['数据']
                            data_list = []
                            for i in df['数据']:
                                data_list.append(i.split(','))
                            data = pd.DataFrame(data_list)
                            columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                                            '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                            data.columns = columns
                            del data['_']
                            for m in columns[1:-3]:
                                data[m] = pd.to_numeric(data[m])
                            data1=data.sort_index(ascending=True,ignore_index=True)
                            return data1
                
                except Exception as e:
                    print(e,stock_1,'qmt获取基金数据有问题换到东方财富')
                    try:
                        secid='{}.{}'.format(0,stock)
                        
                        klt=data_dict[data_type]
                        params={
                                'secid':secid,
                                'klt':klt,
                                'fqt':fqt,
                                'lmt':limit,
                                'end':end,
                                'iscca': '1',
                                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                                'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                'forcect': '1',
                            }
                        url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                        res = requests.get(url=url, params=params)
                        text = res.text
                        json_text = json.loads(text)
                        df = pd.DataFrame(json_text['data']['klines'])
                        df.columns = ['数据']
                        data_list = []
                        for i in df['数据']:
                            data_list.append(i.split(','))
                        data = pd.DataFrame(data_list)
                        columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                                    '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                        data.columns = columns
                        del data['_']
                        for m in columns[1:-3]:
                            data[m] = pd.to_numeric(data[m])
                        data1=data.sort_index(ascending=True,ignore_index=True)
                        return data1
                    except:
                        
                        secid='{}.{}'.format(1,stock)
                        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
                        klt=data_dict[data_type]
                        params={
                                    'secid':secid,
                                    'klt':klt,
                                    'fqt':fqt,
                                    'lmt':limit,
                                    'end':end,
                                    'iscca': '1',
                                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                                    'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                    'forcect': '1',
                            }
                        url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                        res = requests.get(url=url, params=params)
                        text = res.text
                        json_text = json.loads(text)
                        df = pd.DataFrame(json_text['data']['klines'])
                        df.columns = ['数据']
                        data_list = []
                        for i in df['数据']:
                            data_list.append(i.split(','))
                        data = pd.DataFrame(data_list)
                        columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                                        '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                        data.columns = columns
                        del data['_']
                        for m in columns[1:-3]:
                            data[m] = pd.to_numeric(data[m])
                        data1=data.sort_index(ascending=True,ignore_index=True)
                        return data1
            else:
                try:
                    secid='{}.{}'.format(0,stock)
                    klt=data_dict[data_type]
                    params={
                                'secid':secid,
                                'klt':klt,
                                'fqt':fqt,
                                'lmt':limit,
                                'end':end,
                                'iscca': '1',
                                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                                'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                'forcect': '1',
                            }
                    url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                    res = requests.get(url=url, params=params)
                    text = res.text
                    json_text = json.loads(text)
                    df = pd.DataFrame(json_text['data']['klines'])
                    df.columns = ['数据']
                    data_list = []
                    for i in df['数据']:
                        data_list.append(i.split(','))
                    data = pd.DataFrame(data_list)
                    columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                            '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                    data.columns = columns
                    del data['_']
                    for m in columns[1:-3]:
                        data[m] = pd.to_numeric(data[m])
                    data1=data.sort_index(ascending=True,ignore_index=True)
                    return data1
                except Exception as e:
                    try:
                        secid='{}.{}'.format(1,stock)
                        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
                        klt=data_dict[data_type]
                        params={
                                    'secid':secid,
                                    'klt':klt,
                                    'fqt':fqt,
                                    'lmt':limit,
                                    'end':end,
                                    'iscca': '1',
                                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                                    'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                    'forcect': '1',
                            }
                        url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
                        res = requests.get(url=url, params=params)
                        text = res.text
                        json_text = json.loads(text)
                        df = pd.DataFrame(json_text['data']['klines'])
                        df.columns = ['数据']
                        data_list = []
                        for i in df['数据']:
                            data_list.append(i.split(','))
                        data = pd.DataFrame(data_list)
                        columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                                        '成交额', '振幅', '涨跌幅', '涨跌额', '换手率','_','_','_']
                        data.columns = columns
                        del data['_']
                        for m in columns[1:-3]:
                            data[m] = pd.to_numeric(data[m])
                        data1=data.sort_index(ascending=True,ignore_index=True)
                        return data1
                    except Exception as e:
                        print(e,stock,'东方财富基金数据有问题换到qmt')
                        start_date='20200101'
                        end_time=end
                        stock_1=self.adjust_stock(stock=stock)
                        period=qmt_dict.get(data_type,'D')
                        subscribe_id=xtdata.subscribe_quote(stock_code=stock_1,period=period,start_time=start_date,end_time=end,count=-1)
                        data=xtdata.get_market_data_ex(stock_list=[stock_1],period=period,start_time=start_date,end_time=end_time,count=-1)
                        data=data[stock_1]
                        #['date', 'open', 'close', 'high', 'low', 'volume', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
                        data['date']=data.index.tolist()
                        data['成交额']=data['amount']
                        data['涨跌幅']=data['close'].pct_change()*100
                        data['涨跌额']=data['close']-data['close'].shift(1)
                        xtdata.unsubscribe_quote(subscribe_id)
                        return data
                

                
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
    def seed_emial_qq(self,text='交易完成'):
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        try:
            password=text1['qq掩码']
            yag = yagmail.SMTP(user='1752515969@qq.com', password=password, host='smtp.qq.com')
            m = self.qq
            text = text
            yag.send(to=m, contents=text, subject='邮件')
            print('邮箱发生成功')
        except Exception as e:
            print("运行错误:",e)
            print('qq发送失败可能用的人多')
    
    def get_etf_fund_spot_data(self,stock='159632'):
        '''
        ETF实时数据
        '''
        if self.data_api=='qmt':
            try:
                stock_1=self.adjust_stock(stock=stock)
                tick=xtdata.get_full_tick(code_list=[stock_1])
                tick=tick[stock_1]
                if len(tick)>0:
                    result={}
                    result['证券代码']=stock
                    result['时间']=tick['timetag']
                    result['最新价']=tick['lastPrice']
                    result['今开']=tick['open']
                    result['最高价']=tick['high']
                    result['最低价']=tick['low']
                    result['昨收']=tick['lastClose']
                    result['成交量']=tick['amount']
                    result['成交额']=tick['volume']
                    result['涨跌幅']=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
                    return result
                else:
                    try:
                        stock=str(stock)[:6]
                        secid='{}.{}'.format(0,stock)
                        url='https://push2.eastmoney.com/api/qt/stock/get?'
                        params={
                                    #cb: jQuery3510250885634607382_1693625754740
                                    'secid':secid,
                                    'forcect': '1',
                                    'invt': '2',
                                    'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
                                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                    #_: 1693625754746
                                }
                        res=requests.get(url=url,params=params)
                        text=res.json()['data']
                        result={}
                        if stock[:6]=='164824':
                            result['最新价']=float(text['f43'])/10000
                        else:
                            result['最新价']=float(text['f43'])/1000
                        result['最高价']=text['f44']/1000
                        result['最低价']=text['f45']/1000
                        result['今开']=text['f46']/1000
                        result['金额']=text['f48']
                        result['外盘']=text['f49']
                        result['量比']=text['f50']/100
                        result['涨停价']=text['f51']/1000
                        result['跌停价']=text['f52']/1000
                        result['昨收']=text['f60']/1000
                        result['涨跌']=text['f169']/1000
                        result['内盘']=text['f161']
                        #result['换手率']=text['f168']/100
                        result['涨跌幅']=text['f170']/100
                        return result
                    except:
                        
                        stock=str(stock)[:6]
                        secid='{}.{}'.format(1,stock)
                        url='https://push2.eastmoney.com/api/qt/stock/get?'
                        params={
                                        #cb: jQuery3510250885634607382_1693625754740
                                        'secid':secid,
                                        'forcect': '1',
                                        'invt': '2',
                                        'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
                                        'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                        #_: 1693625754746
                                    }
                        res=requests.get(url=url,params=params)
                        text=res.json()['data']
                        result={}
                        if stock[:6]=='164824':
                            result['最新价']=float(text['f43'])/10000
                        else:
                            result['最新价']=float(text['f43'])/1000
                        result['最高价']=text['f44']/1000
                        result['最低价']=text['f45']/1000
                        result['今开']=text['f46']/1000
                        result['金额']=text['f48']
                        result['外盘']=text['f49']
                        result['量比']=text['f50']/100
                        result['涨停价']=text['f51']/1000
                        result['跌停价']=text['f52']/1000
                        result['昨收']=text['f60']/1000
                        result['涨跌']=text['f169']/1000
                        result['内盘']=text['f161']
                        #result['换手率']=text['f168']/100
                        result['涨跌幅']=text['f170']/100
                        return result
            except Exception as e:
                print(e,stock,'qmt实时数据获取有问题切换到东方财富')
                try:
                    stock=str(stock)[:6]
                    secid='{}.{}'.format(0,stock)
                    url='https://push2.eastmoney.com/api/qt/stock/get?'
                    params={
                                #cb: jQuery3510250885634607382_1693625754740
                                'secid':secid,
                                'forcect': '1',
                                'invt': '2',
                                'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
                                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                #_: 1693625754746
                            }
                    res=requests.get(url=url,params=params)
                    text=res.json()['data']
                    result={}
                    if stock[:6]=='164824':
                        result['最新价']=float(text['f43'])/10000
                    else:
                        result['最新价']=float(text['f43'])/1000
                    result['最高价']=text['f44']/1000
                    result['最低价']=text['f45']/1000
                    result['今开']=text['f46']/1000
                    result['金额']=text['f48']
                    result['外盘']=text['f49']
                    result['量比']=text['f50']/100
                    result['涨停价']=text['f51']/1000
                    result['跌停价']=text['f52']/1000
                    result['昨收']=text['f60']/1000
                    result['涨跌']=text['f169']/1000
                    result['内盘']=text['f161']
                    #result['换手率']=text['f168']/100
                    result['涨跌幅']=text['f170']/100
                    return result
                except:
                    
                    stock=str(stock)[:6]
                    secid='{}.{}'.format(1,stock)
                    url='https://push2.eastmoney.com/api/qt/stock/get?'
                    params={
                                    #cb: jQuery3510250885634607382_1693625754740
                                    'secid':secid,
                                    'forcect': '1',
                                    'invt': '2',
                                    'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
                                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                    #_: 1693625754746
                                }
                    res=requests.get(url=url,params=params)
                    text=res.json()['data']
                    result={}
                    if stock[:6]=='164824':
                        result['最新价']=float(text['f43'])/10000
                    else:
                        result['最新价']=float(text['f43'])/1000
                    result['最高价']=text['f44']/1000
                    result['最低价']=text['f45']/1000
                    result['今开']=text['f46']/1000
                    result['金额']=text['f48']
                    result['外盘']=text['f49']
                    result['量比']=text['f50']/100
                    result['涨停价']=text['f51']/1000
                    result['跌停价']=text['f52']/1000
                    result['昨收']=text['f60']/1000
                    result['涨跌']=text['f169']/1000
                    result['内盘']=text['f161']
                    #result['换手率']=text['f168']/100
                    result['涨跌幅']=text['f170']/100
                    return result
        else:
            try:
                stock=str(stock)[:6]
                secid='{}.{}'.format(0,stock)
                url='https://push2.eastmoney.com/api/qt/stock/get?'
                params={
                                #cb: jQuery3510250885634607382_1693625754740
                                'secid':secid,
                                'forcect': '1',
                                'invt': '2',
                                'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
                                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                #_: 1693625754746
                            }
                res=requests.get(url=url,params=params)
                text=res.json()['data']
                result={}
                if stock[:6]=='164824':
                    result['最新价']=float(text['f43'])/10000
                else:
                    result['最新价']=float(text['f43'])/1000
                result['最高价']=text['f44']/1000
                result['最低价']=text['f45']/1000
                result['今开']=text['f46']/1000
                result['金额']=text['f48']
                result['外盘']=text['f49']
                result['量比']=text['f50']/100
                result['涨停价']=text['f51']/1000
                result['跌停价']=text['f52']/1000
                result['昨收']=text['f60']/1000
                result['涨跌']=text['f169']/1000
                result['内盘']=text['f161']
                #result['换手率']=text['f168']/100
                result['涨跌幅']=text['f170']/100
                return result
            except:
                try:
                    stock=str(stock)[:6]
                    secid='{}.{}'.format(1,stock)
                    url='https://push2.eastmoney.com/api/qt/stock/get?'
                    params={
                                    #cb: jQuery3510250885634607382_1693625754740
                                    'secid':secid,
                                    'forcect': '1',
                                    'invt': '2',
                                    'fields': 'f43,f44,f45,f46,f48,f49,f50,f51,f52,f59,f60,f108,f152,f161,f168,f169,f170',
                                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                                    #_: 1693625754746
                                }
                    res=requests.get(url=url,params=params)
                    text=res.json()['data']
                    result={}
                    if stock[:6]=='164824':
                        result['最新价']=float(text['f43'])/10000
                    else:
                        result['最新价']=float(text['f43'])/1000
                    result['最高价']=text['f44']/1000
                    result['最低价']=text['f45']/1000
                    result['今开']=text['f46']/1000
                    result['金额']=text['f48']
                    result['外盘']=text['f49']
                    result['量比']=text['f50']/100
                    result['涨停价']=text['f51']/1000
                    result['跌停价']=text['f52']/1000
                    result['昨收']=text['f60']/1000
                    result['涨跌']=text['f169']/1000
                    result['内盘']=text['f161']
                    #result['换手率']=text['f168']/100
                    result['涨跌幅']=text['f170']/100
                    return result
                except Exception as e:
                    print(e,stock,'东方财富实时数据获取有问题切换到qmt')
                    stock_1=self.adjust_stock(stock=stock)
                    tick=xtdata.get_full_tick(code_list=[stock_1])
                    tick=tick[stock_1]
                    result={}
                    result['证券代码']=stock
                    result['时间']=tick['timetag']
                    result['最新价']=tick['lastPrice']
                    result['今开']=tick['open']
                    result['最高价']=tick['high']
                    result['最低价']=tick['low']
                    result['昨收']=tick['lastClose']
                    result['成交量']=tick['amount']
                    result['成交额']=tick['volume']
                    result['涨跌幅']=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
                    return result
                
    def get_etf_spot_trader_data(self,stock='159632',limit=600000):
        '''
        ETF实时交易数据3秒一次
        '''
        if self.data_api=='qmt':
            try:
                stock_1=self.adjust_stock(stock=stock)
                period='tick'
                start_date=''.join(str(datetime.now())[:10].split('-'))
                end_time=start_date
                subscribe_id=xtdata.subscribe_quote(stock_code=stock_1,period=period,start_time=start_date,end_time=end_time,count=-1)
                data=xtdata.get_market_data_ex(stock_list=[stock_1],period=period,start_time=start_date,end_time=end_time,count=-1)
                data=data[stock_1]
                if data.shape[0]>0:
                    data['date']=data.index.tolist()
                    data['date']=data['date'].apply(lambda x: str(x)[-6:])
                    data['价格']=data['lastPrice']
                    data['close']=data['lastPrice']
                    data['实时涨跌幅']=data['价格'].pct_change()
                    data['涨跌幅']=((data['close']-data['lastClose'])/data['lastClose'])*100
                    xtdata.unsubscribe_quote(subscribe_id)
                    return data
                else:
                    try:
                        secid='{}.{}'.format(0,stock)
                        url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                        params={
                            #cb: jQuery3510250885634607382_1693625754742
                            'secid':secid,
                            'forcect': '1',
                            'invt': '2',
                            'pos':-limit,
                            'iscca': '1',
                            'fields1': 'f1,f2,f3,f4,f5',
                            'fields2': 'f51,f52,f53,f54,f55',
                            'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                            #_: 1693625754806
                        }
                        res=requests.get(url=url,params=params)
                        text=res.json()['data']['details']
                        data=[]
                        for i in text:
                            data.append(i.split(','))
                        df=pd.DataFrame(data)
                        df.columns=['时间','价格','成交量','未知','买卖盘']
                        df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
                        def select_data(x):
                            if x=='1':
                                return '卖盘'
                            elif x=='2':
                                return '买盘'
                            else:
                                return x
                        df['买卖盘']=df['买卖盘'].apply(select_data)
                        df=df[df['时间']>=92400]
                        df['价格']=pd.to_numeric(df['价格'])
                        df['实时涨跌幅']=(df['价格'].pct_change())*100
                        df['涨跌幅']=df['实时涨跌幅'].cumsum()
                        return df
                    except:
                            
                        secid='{}.{}'.format(1,stock)
                        url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                        params={
                                #cb: jQuery3510250885634607382_1693625754742
                                'secid':secid,
                                'forcect': '1',
                                'invt': '2',
                                'pos':-limit,
                                'iscca': '1',
                                'fields1': 'f1,f2,f3,f4,f5',
                                'fields2': 'f51,f52,f53,f54,f55',
                                'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                                #_: 1693625754806
                        }
                        res=requests.get(url=url,params=params)
                        text=res.json()['data']['details']
                        data=[]
                        for i in text:
                            data.append(i.split(','))
                        df=pd.DataFrame(data)
                        df.columns=['时间','价格','成交量','未知','买卖盘']
                        df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
                        def select_data(x):
                                if x=='1':
                                    return '卖盘'
                                elif x=='2':
                                    return '买盘'
                                else:
                                    return x
                        df['买卖盘']=df['买卖盘'].apply(select_data)
                        df=df[df['时间']>=92400]
                        df['价格']=pd.to_numeric(df['价格'])
                        df['实时涨跌幅']=(df['价格'].pct_change())*100
                        df['涨跌幅']=df['实时涨跌幅'].cumsum()
                        return df
            except Exception as e:
                print(e,stock,'qmt高频数据获取失败切换到东方财富')
                try:
                    secid='{}.{}'.format(0,stock)
                    url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                    params={
                        #cb: jQuery3510250885634607382_1693625754742
                        'secid':secid,
                        'forcect': '1',
                        'invt': '2',
                        'pos':-limit,
                        'iscca': '1',
                        'fields1': 'f1,f2,f3,f4,f5',
                        'fields2': 'f51,f52,f53,f54,f55',
                        'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                        #_: 1693625754806
                    }
                    res=requests.get(url=url,params=params)
                    text=res.json()['data']['details']
                    data=[]
                    for i in text:
                        data.append(i.split(','))
                    df=pd.DataFrame(data)
                    df.columns=['时间','价格','成交量','未知','买卖盘']
                    df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
                    def select_data(x):
                        if x=='1':
                            return '卖盘'
                        elif x=='2':
                            return '买盘'
                        else:
                            return x
                    df['买卖盘']=df['买卖盘'].apply(select_data)
                    df=df[df['时间']>=92400]
                    df['价格']=pd.to_numeric(df['价格'])
                    df['实时涨跌幅']=(df['价格'].pct_change())*100
                    df['涨跌幅']=df['实时涨跌幅'].cumsum()
                    return df
                except:
                        
                    secid='{}.{}'.format(1,stock)
                    url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                    params={
                            #cb: jQuery3510250885634607382_1693625754742
                            'secid':secid,
                            'forcect': '1',
                            'invt': '2',
                            'pos':-limit,
                            'iscca': '1',
                            'fields1': 'f1,f2,f3,f4,f5',
                            'fields2': 'f51,f52,f53,f54,f55',
                            'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                            #_: 1693625754806
                    }
                    res=requests.get(url=url,params=params)
                    text=res.json()['data']['details']
                    data=[]
                    for i in text:
                        data.append(i.split(','))
                    df=pd.DataFrame(data)
                    df.columns=['时间','价格','成交量','未知','买卖盘']
                    df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
                    def select_data(x):
                            if x=='1':
                                return '卖盘'
                            elif x=='2':
                                return '买盘'
                            else:
                                return x
                    df['买卖盘']=df['买卖盘'].apply(select_data)
                    df=df[df['时间']>=92400]
                    df['价格']=pd.to_numeric(df['价格'])
                    df['实时涨跌幅']=(df['价格'].pct_change())*100
                    df['涨跌幅']=df['实时涨跌幅'].cumsum()
                    return df
        else:
            try:
                secid='{}.{}'.format(0,stock)
                url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                params={
                        #cb: jQuery3510250885634607382_1693625754742
                        'secid':secid,
                        'forcect': '1',
                        'invt': '2',
                        'pos':-limit,
                        'iscca': '1',
                        'fields1': 'f1,f2,f3,f4,f5',
                        'fields2': 'f51,f52,f53,f54,f55',
                        'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                        #_: 1693625754806
                }
                res=requests.get(url=url,params=params)
                text=res.json()['data']['details']
                data=[]
                for i in text:
                    data.append(i.split(','))
                df=pd.DataFrame(data)
                df.columns=['时间','价格','成交量','未知','买卖盘']
                df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
                def select_data(x):
                    if x=='1':
                        return '卖盘'
                    elif x=='2':
                        return '买盘'
                    else:
                        return x
                df['买卖盘']=df['买卖盘'].apply(select_data)
                df=df[df['时间']>=92400]
                df['价格']=pd.to_numeric(df['价格'])
                df['实时涨跌幅']=(df['价格'].pct_change())*100
                df['涨跌幅']=df['实时涨跌幅'].cumsum()
                return df
            except: 
                try:
                    secid='{}.{}'.format(1,stock)
                    url='https://push2.eastmoney.com/api/qt/stock/details/get?'
                    params={
                                #cb: jQuery3510250885634607382_1693625754742
                                'secid':secid,
                                'forcect': '1',
                                'invt': '2',
                                'pos':-limit,
                                'iscca': '1',
                                'fields1': 'f1,f2,f3,f4,f5',
                                'fields2': 'f51,f52,f53,f54,f55',
                                'ut': 'f057cbcbce2a86e2866ab8877db1d059'
                                #_: 1693625754806
                    }
                    res=requests.get(url=url,params=params)
                    text=res.json()['data']['details']
                    data=[]
                    for i in text:
                        data.append(i.split(','))
                    df=pd.DataFrame(data)
                    df.columns=['时间','价格','成交量','未知','买卖盘']
                    df['时间']=df['时间'].apply(lambda x:int(''.join(x.split(':'))))
                    def select_data(x):
                        if x=='1':
                            return '卖盘'
                        elif x=='2':
                            return '买盘'
                        else:
                            return x
                    df['买卖盘']=df['买卖盘'].apply(select_data)
                    df=df[df['时间']>=92400]
                    df['价格']=pd.to_numeric(df['价格'])
                    df['实时涨跌幅']=(df['价格'].pct_change())*100
                    df['涨跌幅']=df['实时涨跌幅'].cumsum()
                    return df
                except Exception as e:
                    print(e,stock,'东方财富获取高频数据有问题切换到qmt')
                    stock_1=self.adjust_stock(stock=stock)
                    period='tick'
                    start_date=''.join(str(datetime.now())[:10].split('-'))
                    
                    end_time=start_date
                    subscribe_id=xtdata.subscribe_quote(stock_code=stock_1,period=period,start_time=start_date,end_time=end_time,count=-1)
                    data=xtdata.get_market_data_ex(stock_list=[stock_1],period=period,start_time=start_date,end_time=end_time,count=-1)
                    data=data[stock_1]
                    data['date']=data.index.tolist()
                    data['date']=data['date'].apply(lambda x: str(x)[-6:])
                    data['价格']=data['lastPrice']
                    data['close']=data['lastPrice']
                    data['实时涨跌幅']=data['价格'].pct_change()
                    data['涨跌幅']=((data['close']-data['lastClose'])/data['lastClose'])*100
                    xtdata.unsubscribe_quote(subscribe_id)
                    return data
            
           
    