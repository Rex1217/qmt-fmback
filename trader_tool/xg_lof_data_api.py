import pandas as pd
import json
import requests
import os
class xg_lof_data_api:
    '''
    小果套利数据库api
    '''
    def __init__(self,url='http://120.78.132.143',port=8023,password='123456'):
        '''
        小果金融数据库
        url服务器网页
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
    def get_all_lof_data(self,date='2024-06-07'):
        '''
        获取全部的lof数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"全部lof"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":"标普500LOF"},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_arbitrage_analysis(self,date='2024-06-07'):
        '''
        套利分析
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"套利分析"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":"标普500LOF"},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_arbitrageable_data(self,date='2024-06-07'):
        '''
        获取可以套利的数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"可以套利"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":"标普500LOF"},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_historical_premium_rates(self,stock='164824',date='2024-06-07'):
        '''
        获取历史溢价率
        '''
        all_df=self.get_all_lof_data(date=date)
        all_df['代码']=all_df['代码'].astype(str)
        name_dict=dict(zip(all_df['代码'].tolist(),all_df['名称'].tolist()))
        name=name_dict.get(stock)
        print(name)
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"历史溢价率"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":name},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_spot_data(self,stock='164824',date='2024-06-07'):
        '''
        获取实时数据
        '''
        all_df=self.get_all_lof_data(date=date)
        all_df['代码']=all_df['代码'].astype(str)
        name_dict=dict(zip(all_df['代码'].tolist(),all_df['名称'].tolist()))
        name=name_dict.get(stock)
        print(name)
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"实时数据"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":name},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_trader_stats(self,stock='164824',date='2024-06-07'):
        '''
        获取交易状态
        '''
        all_df=self.get_all_lof_data(date=date)
        all_df['代码']=all_df['代码'].astype(str)
        name_dict=dict(zip(all_df['代码'].tolist(),all_df['名称'].tolist()))
        name=name_dict.get(stock)
        print(name)
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"交易状态"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":name},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_hist_data(self,stock='164824',date='2024-06-07'):
        '''
        获取历史数据
        '''
        all_df=self.get_all_lof_data(date=date)
        all_df['代码']=all_df['代码'].astype(str)
        name_dict=dict(zip(all_df['代码'].tolist(),all_df['名称'].tolist()))
        name=name_dict.get(stock)
        print(name)
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
            "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lof_fund_data_type","property":"value","value":"历史数据"},
            {"id":"lof_fund_end_date","property":"date","value":date},
            {"id":"lof_fund_name","property":"value","value":name},
            {"id":"lof_fund_run","property":"value","value":"运行"},
            {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df

if __name__=='__main__':
    models=xg_lof_data_api()
    df=models.get_arbitrage_analysis(date='2024-06-07')
    print(df)