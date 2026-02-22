import pandas as pd
import requests 
import json
class microc_stock_data:
    '''
    微盘股数据
    '''
    def __init__(self) -> None:
        '''
        微盘股数据
        '''
        pass
    def get_stock_hist_data_em(self,start_date='20210101',end_date='20500101',data_type='D',fq=1,count=1000000):
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
        data_dict = {'1': '1', '5': '5', '15': '15', '30': '30', '60': '60', 'D': '101', 'W': '102', 'M': '103'}
        params={
            'secid': '90.BK1158',
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': data_dict[data_type],
            'fqt':fq ,
            'beg': start_date,
            'end': end_date,
            'smplmt': '460',
            'lmt': count
            
        }
        headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
        url='https://push2his.eastmoney.com/api/qt/stock/kline/get?'
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        df = pd.DataFrame(text['data']['klines'])
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
    def stock_sector_fund_flow_summary(self,indicator= "今日") :
        """
        成分股
        """
        symbol='BK1158'
        data=pd.DataFrame()
        for pn in [1,2]:
            url = "https://push2.eastmoney.com/api/qt/clist/get"
            if indicator == "今日":
                params = {
                    "fid": "f62",
                    "po": "1",
                    "pz": "200",
                    "pn": pn,
                    "np": "1",
                    "fltt": "2",
                    "invt": "2",
                    "fs": f"b:{symbol}",
                    "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
                }
                r = requests.get(url, params=params)
                data_json = r.json()
                temp_df = pd.DataFrame(data_json["data"]["diff"])
                temp_df.reset_index(inplace=True)
                temp_df["index"] = temp_df["index"] + 1
                temp_df.rename(
                    columns={
                        "index": "序号",
                        "f12": "代码",
                        "f14": "名称",
                        "f2": "最新价",
                        "f3": "今天涨跌幅",
                        "f62": "今日主力净流入-净额",
                        "f184": "今日主力净流入-净占比",
                        "f66": "今日超大单净流入-净额",
                        "f69": "今日超大单净流入-净占比",
                        "f72": "今日大单净流入-净额",
                        "f75": "今日大单净流入-净占比",
                        "f78": "今日中单净流入-净额",
                        "f81": "今日中单净流入-净占比",
                        "f84": "今日小单净流入-净额",
                        "f87": "今日小单净流入-净占比",
                    },
                    inplace=True,
                )
                temp_df = temp_df[
                    [
                        "序号",
                        "代码",
                        "名称",
                        "最新价",
                        "今天涨跌幅",
                        "今日主力净流入-净额",
                        "今日主力净流入-净占比",
                        "今日超大单净流入-净额",
                        "今日超大单净流入-净占比",
                        "今日大单净流入-净额",
                        "今日大单净流入-净占比",
                        "今日中单净流入-净额",
                        "今日中单净流入-净占比",
                        "今日小单净流入-净额",
                        "今日小单净流入-净占比",
                    ]
                ]
                temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
                temp_df["今天涨跌幅"] = pd.to_numeric(temp_df["今天涨跌幅"], errors="coerce")
                temp_df["今日主力净流入-净额"] = pd.to_numeric(
                    temp_df["今日主力净流入-净额"], errors="coerce"
                )
                temp_df["今日主力净流入-净占比"] = pd.to_numeric(
                    temp_df["今日主力净流入-净占比"], errors="coerce"
                )
                temp_df["今日超大单净流入-净额"] = pd.to_numeric(
                    temp_df["今日超大单净流入-净额"], errors="coerce"
                )
                temp_df["今日超大单净流入-净占比"] = pd.to_numeric(
                    temp_df["今日超大单净流入-净占比"], errors="coerce"
                )
                temp_df["今日大单净流入-净额"] = pd.to_numeric(
                    temp_df["今日大单净流入-净额"], errors="coerce"
                )
                temp_df["今日大单净流入-净占比"] = pd.to_numeric(
                    temp_df["今日大单净流入-净占比"], errors="coerce"
                )
                temp_df["今日中单净流入-净额"] = pd.to_numeric(
                    temp_df["今日中单净流入-净额"], errors="coerce"
                )
                temp_df["今日中单净流入-净占比"] = pd.to_numeric(
                    temp_df["今日中单净流入-净占比"], errors="coerce"
                )
                temp_df["今日小单净流入-净额"] = pd.to_numeric(
                    temp_df["今日小单净流入-净额"], errors="coerce"
                )
                temp_df["今日小单净流入-净占比"] = pd.to_numeric(
                    temp_df["今日小单净流入-净占比"], errors="coerce"
                )
            data=pd.concat([data,temp_df],ignore_index=True)
        return data
if __name__=='__main__':
    data=microc_stock_data()
    print(data.get_stock_hist_data_em())
    print(data.stock_sector_fund_flow_summary())
