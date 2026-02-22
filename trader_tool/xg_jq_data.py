import requests
import json
import pandas as pd
url='http://124.220.32.224'
port=8025
#服务器编码
url_code='63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad'
#记得把这个改成自己的一个策略一个
password='123456'
class xg_jq_data:
    def __init__(self,url='http://124.220.32.224',
                 port=8025,
                 url_code=url_code,
                 password='123456'):
        '''
        获取服务器数据
        '''
        self.url=url
        self.port=port
        self.url_code=url_code
        self.password=password
    def get_user_data(self,data_type='用户信息'):
        '''
        获取使用的数据
        data_type='用户信息','实时数据',历史数据','清空实时数据','清空历史数据'
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table.data@{}".format(self.url_code),
            "outputs":{"id":"joinquant_trader_table","property":"data@{}".format(self.url_code)},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
                    {"id":"joinquant_trader_data_type","property":"value","value":data_type},
                    {"id":"joinquant_trader_text","property":"value","value":"\n               {'状态': 'held', '订单添加时间': 'datetime.datetime(2024, 4, 23, 9, 30)', '买卖': 'False', '下单数量': '9400', '已经成交': '9400', '股票代码': '001.XSHE', '订单ID': '1732208241', '平均成交价格': '10.5', '持仓成本': '10.59', '多空': 'long', '交易费用': '128.31'}\n                "},
                    {"id":"joinquant_trader_run","property":"value","value":"运行"},
                    {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["joinquant_trader_run.value"],"parsedChangedPropsIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
    def send_order(self,result):
        '''
        发送交易数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table.data@{}".format(self.url_code),
            "outputs":{"id":"joinquant_trader_table","property":"data@{}".format(self.url_code)},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
                    {"id":"joinquant_trader_data_type","property":"value","value":'实时数据'},
                    {"id":"joinquant_trader_text","property":"value","value":result},
                    {"id":"joinquant_trader_run","property":"value","value":"运行"},
                    {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["joinquant_trader_run.value"],"parsedChangedPropsIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df

    
if __name__=='__main__':
    trader=xg_jq_data(url='http://124.220.32.224',port=8025,password='123456',url_code='63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad')
    df=trader.get_user_data(data_type='实时数据')
    print(df)
    result={'状态': 'held', '订单添加时间': 'datetime.datetime(2024, 4, 23, 9, 30)', '买卖': 'False', '下单数量': '9400', '已经成交': '9400', '股票代码': '600031.XSHE', '订单ID': '1732208241', '平均成交价格': '10.5', '持仓成本': '10.59', '多空': 'long', '交易费用': '128.31'}
    #记得发送类似字典的字符串数据
    result=str(result)
    df=trader.send_order(result)
        