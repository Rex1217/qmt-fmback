import pandas as pd
import requests
import json


#可转债数据
class bond_cov_data_ths:
    def __init__(self):
        pass
    def get_cov_bond_hist_data(self,stock='113016',start='20100101',end='20500101',limit='10000',
                                data_type='D',fqt='1',count=8000):
        '''
        可转债历史数据
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
        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
        klt=data_dict[data_type]
        try:
            params={
                'secid':'1.{}'.format(stock),
                'klt':klt,
                'fqt':fqt,
                'lmt':limit,
                'start':start,
                'end':end,
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                'ut':'f057cbcbce2a86e2866ab8877db1d059',
                'forcect':'1'
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
            #data1['累计涨跌幅']=data1['涨跌幅'].cumsum()
            return data1
        except:
            params={
                    'secid':'0.{}'.format(stock),
                    'klt':klt,
                    'fqt':fqt,
                    'start':start,
                    'lmt':limit,
                    'end':end,
                    'iscca': '1',
                    'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8',
                    'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64',
                    'ut':'f057cbcbce2a86e2866ab8877db1d059',
                    'forcect':'1'
            }
            url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
            res = requests.get(url=url, params=params)
            text = res.json()
            json_text =text
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
            
    def get_cov_bond_spot(self,stock='113016'):
        '''
        获取可转债实时数据
        '''
        try:
            params={
                'cb':'jQuery35107788691587529397_1680967733868',
                'secid':'1.{}'.format(stock),
                'forcect':'1',
                'invt': '2',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f59,f60,f108,f152,f154,f161,f168,f169,f170,f262,f264,f265,f266,f267,f424,f426,f427,f428,f429,f432',
                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                '_': '1680967733870',
            }
            url='https://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text[41:len(res.text)-2]
            json_text=json.loads(text)['data']
            data_dict={}
            data_dict['最新价']=json_text['f43']/1000
            data_dict['最高价']=json_text['f44']/1000
            data_dict['最低价']=json_text['f45']/1000
            data_dict['今开']=json_text['f46']/1000 
            data_dict['总手']=json_text['f47']
            data_dict['金额']=json_text['f48']
            #data_dict['量比']=json_text['f50']/100
            data_dict['外盘']=json_text['f49']
            data_dict['涨停价']=json_text['f51']/1000
            data_dict['跌停价']=json_text['f52']/1000
            data_dict['涨停收盘价']=json_text['f60']/1000
            data_dict['涨跌幅']=json_text['f170']/100
            data_dict['证券代码']=json_text['f262']
            data_dict['名称']=json_text['f264']
            data_dict['溢价率']=json_text['f428']/100
            return data_dict
        except:
            
            params={
                    'cb':'jQuery35107788691587529397_1680967733868',
                    'secid':'0.{}'.format(stock),
                    'forcect':'1',
                    'invt': '2',
                    'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f59,f60,f108,f152,f154,f161,f168,f169,f170,f262,f264,f265,f266,f267,f424,f426,f427,f428,f429,f432',
                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                    '_': '1680967733870',
            }
            url='https://push2.eastmoney.com/api/qt/stock/get?'
            res=requests.get(url=url,params=params)
            text=res.text[41:len(res.text)-2]
            json_text=json.loads(text)['data']
            data_dict={}
            data_dict['最新价']=json_text['f43']/1000
            data_dict['最高价']=json_text['f44']/1000
            data_dict['最低价']=json_text['f45']/1000
            data_dict['今开']=json_text['f46']/1000 
            data_dict['总手']=json_text['f47']
            data_dict['金额']=json_text['f48']
            #data_dict['量比']=json_text['f50']/100
            data_dict['外盘']=json_text['f49']
            data_dict['涨停价']=json_text['f51']/1000
            data_dict['跌停价']=json_text['f52']/1000
            data_dict['涨停收盘价']=json_text['f60']/1000
            data_dict['涨跌幅']=json_text['f170']/100
            data_dict['证券代码']=json_text['f262']
            data_dict['名称']=json_text['f264']
            data_dict['溢价率']=json_text['f428']/100
            return data_dict
            
    
   
    def get_cov_bond_spot_trader_data(self,stock='123018'):
        '''
        控制住实时数据
        '''
        try:
            url='https://push2.eastmoney.com/api/qt/stock/details/get?'
            params={
                #'cb': 'jQuery3510784161408794853_1689866980183',
                'secid': '0.{}'.format(stock),
                'forcect': '1',
                'invt': '2',
                'pos': '-10000',
                'iscca': '1',
                'fields1': 'f1,f2,f3,f4,f5',
                'fields2': 'f51,f52,f53,f54,f55',
                'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                '_': '1689866980185'
            }
            res=requests.get(url=url,params=params)
            text=res.json()
            df=pd.DataFrame(text['data']['details'])
            df.columns=['数据']
            all_df=[]
            for i in df['数据']:
                all_df.append(i.split(','))
            data=pd.DataFrame(all_df)
            data.columns=['时间','价格','成交量','单数','性质']
            def select_stock(x):
                if x=='2':
                    return '买盘'
                elif x=='1':
                    return '卖盘'
                else:
                    return x
            data['性质']=data['性质'].apply(select_stock)
            data['价格']=data['价格'].astype(float)
            data['时间']=data['时间'].apply(lambda x :int(str(x).replace(':','')))
            data=data[data['时间']>=92100]
            data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
            data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
            return data
        except:
            
            url='https://push2.eastmoney.com/api/qt/stock/details/get?'
            params={
                    #'cb': 'jQuery3510784161408794853_1689866980183',
                    'secid': '1.{}'.format(stock),
                    'forcect': '1',
                    'invt': '2',
                    'pos': '-10000',
                    'iscca': '1',
                    'fields1': 'f1,f2,f3,f4,f5',
                    'fields2': 'f51,f52,f53,f54,f55',
                    'ut': 'f057cbcbce2a86e2866ab8877db1d059',
                    '_': '1689866980185'
            }
            res=requests.get(url=url,params=params)
            text=res.json()
            df=pd.DataFrame(text['data']['details'])
            df.columns=['数据'] 
            all_df=[]
            for i in df['数据']:
                all_df.append(i.split(','))
            data=pd.DataFrame(all_df)
            data.columns=['时间','价格','成交量','单数','性质']
            def select_stock(x):
                    if x=='2':
                        return '买盘'
                    elif x=='1':
                        return '卖盘'
                    else:
                        return x
            data['性质']=data['性质'].apply(select_stock)
            data['价格']=data['价格'].astype(float)
            data['时间']=data['时间'].apply(lambda x :int(str(x).replace(':','')))
            data=data[data['时间']>=92500]
            data['涨跌幅']=(data['价格'].pct_change()*100).cumsum()
            data['实时涨跌幅']=data['涨跌幅']-data['涨跌幅'].shift(1)
            return data
           
   