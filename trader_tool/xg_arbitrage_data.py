import requests
import pandas as pd
import json
class xg_arbitrage_data:
    def __init__(self,url='http://120.78.132.143',port='8023',password='123456'):
        '''
        小果套利数据api
        url服务器
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
    def get_atbitrage_analaysis_data(self,date='2024-04-24'):
        '''
        套利分析数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lof_fund_maker_table.data@e3bf7d07ec3deafea65224e2d934f518",
              "outputs":{"id":"lof_fund_maker_table","property":"data@e3bf7d07ec3deafea65224e2d934f518"},
              "inputs":[{"id":"password","property":"value","value":self.password},
              {"id":"lof_fund_data_type","property":"value","value":"套利分析"},
              {"id":"lof_fund_end_date","property":"date","value":date},
              {"id":"lof_fund_name","property":"value","value":"添富核心精选LOF"},
              {"id":"lof_fund_run","property":"value","value":"运行"},
              {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
              "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_all_lof_data(self,date='2024-04-24'):
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
              {"id":"lof_fund_name","property":"value","value":"添富核心精选LOF"},
              {"id":"lof_fund_run","property":"value","value":"运行"},
              {"id":"lof_fund_down_data","property":"value","value":"不下载数据"}],
              "changedPropIds":["lof_fund_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lof_fund_maker_table']['data'])
        return df
    def get_hist_yjl(self,stock='161125',date='2024-04-24',):
        '''
        获取历史溢价率
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        stock_df=self.get_all_lof_data(date=date)
        stock_df['代码']=stock_df['代码'].astype(str)
        stock_dict=dict(zip(stock_df['代码'],stock_df['名称']))
        name=stock_dict.get(stock)
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
    def get_spot_data(self,stock='161125',date='2024-04-24',):
        '''
        获取实时数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        stock_df=self.get_all_lof_data(date=date)
        stock_df['代码']=stock_df['代码'].astype(str)
        stock_dict=dict(zip(stock_df['代码'],stock_df['名称']))
        name=stock_dict.get(stock)
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
    def get_trader_stats(self,stock='161125',date='2024-04-24',):
        '''
        获取交易状态
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        stock_df=self.get_all_lof_data(date=date)
        stock_df['代码']=stock_df['代码'].astype(str)
        stock_dict=dict(zip(stock_df['代码'],stock_df['名称']))
        name=stock_dict.get(stock)
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
    def get_hist_data(self,stock='161125',date='2024-04-24',):
        '''
        获取历史数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        stock_df=self.get_all_lof_data(date=date)
        stock_df['代码']=stock_df['代码'].astype(str)
        stock_dict=dict(zip(stock_df['代码'],stock_df['名称']))
        name=stock_dict.get(stock)
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
    '''
    数据
    '''
    models=xg_arbitrage_data()
    df=models.get_atbitrage_analaysis_data()
    print(df)
