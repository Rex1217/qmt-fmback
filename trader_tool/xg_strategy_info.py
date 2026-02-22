import pandas as pd
import json
import requests
import os
class xg_strategy_info:
    '''
    小果策略交易系统
    读取策略商城的交易信号
    http://120.78.132.143:8023/
    '''
    def __init__(self,url='http://120.78.132.143',port='8023',password='123456',strategy_id='6'):
        '''
        小果数据api，支持qmt,本地
        url服务器网页
        port端口
        password授权码
        strategy_id策略id
        '''
        self.url=url
        self.port=port
        self.password=password
        self.strategy_id=strategy_id
        self.path=os.path.dirname(os.path.abspath(__file__))
    def get_strategy_trader_info(self,data_type='持股数据'):
        '''
        读取策略的交易信号
        data_type=持股数据/账户数据/买入股票记录/卖出股票记录/交易记录/自定义交易股票池
        '''
        try:
            url='{}:{}/_dash-update-component'.format(self.url,self.port)
            headers={'Content-Type':'application/json'}
            data={
                "output":"xg_bond_data_maker_table_{}.data@a0ff4c7fd0a4afa1c2ef593dc2a34992".format(self.strategy_id),
                "outputs":{"id":"xg_bond_data_maker_table_{}".format(self.strategy_id),
                "property":"data@a0ff4c7fd0a4afa1c2ef593dc2a34992"},
                "inputs":[{"id":"password","property":"value","value":self.password},
                {"id":"xg_bond_data_data_type","property":"value","value":data_type},
                {"id":"xg_bond_data_end_date","property":"date","value":"2025-01-30"},
                {"id":"xg_bond_data_run","property":"value","value":"运行"},
                {"id":"xg_bond_data_down_data","property":"value","value":"不下载数据"}],
                "changedPropIds":["xg_bond_data_data_type.value"]}
            res=requests.post(url=url,data=json.dumps(data),headers=headers)
            text=res.json()
            df=pd.DataFrame(text['response']['xg_bond_data_maker_table_{}'.format(self.strategy_id)]['data'])
            return df
        except Exception as e:
            print(e,self.strategy_id,'有问题********')
if __name__=='__main__':
    models=xg_strategy_info(url='http://120.78.132.143',port='8023',password='123456',strategy_id='6')
    df=models.get_strategy_trader_info(data_type='持股数据')
    print(df)
