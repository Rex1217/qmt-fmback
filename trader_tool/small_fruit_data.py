import requests
import json
import pandas as pd
class small_fruit_data:
    '''
    小果服务器跟单数据
    '''
    def __init__(self,url='http://127.0.0.1',port='8050',password='123456',url_id='790bbe34b3c77c32afb811e5a47de538330b6effb69e947aec426551906caa9e'):
        '''
        小果服务器跟单数据
        '''
        self.url=url
        self.port=port
        self.password=password
        self.url_id=url_id
    def get_user_info(self):
        '''
        获取用户信息
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"joinquant_trader_table.data@{}".format(self.url_id),
            "outputs":{"id":"joinquant_trader_table","property":"data@{}".format(self.url_id)},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
                    {"id":"joinquant_trader_data_type","property":"value","value":"用户信息"},
                    {"id":"joinquant_trader_run","property":"value","value":"运行"},
                    {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
    def get_trader_data(self,data_type='今日委托'):
        '''
        获取交易数据
        data_type=用户信息/今日成交/今日委托/持股数据/账户数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"joinquant_trader_table.data@{}".format(self.url_id),
            "outputs":{"id":"joinquant_trader_table","property":"data@{}".format(self.url_id)},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
                    {"id":"joinquant_trader_data_type","property":"value","value":data_type},
                    {"id":"joinquant_trader_run","property":"value","value":"运行"},
                    {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
if __name__=='__main__':
    data=small_fruit_data()
    df=data.get_user_info()
    print(df)
    df=data.get_trader_data()
    print(df)
