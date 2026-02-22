import pandas as pd
import json
import requests
import os
class xg_bond_data_down:
    '''
    小果金融数据库
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
    def xg_bond_data_down(self,date='2024-09-09'):
        '''
        获取可转债数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"xg_bond_data_maker_table.data@a0ff4c7fd0a4afa1c2ef593dc2a34992",
            "outputs":{"id":"xg_bond_data_maker_table","property":"data@a0ff4c7fd0a4afa1c2ef593dc2a34992"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"xg_bond_data_data_type","property":"value","value":"实时数据"},
            {"id":"xg_bond_data_end_date","property":"date","value":date},
            {"id":"xg_bond_data_run","property":"value","value":"运行"},
            {"id":"xg_bond_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["xg_bond_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['xg_bond_data_maker_table']['data'])
        return df
if __name__=='__main__':
    api=xg_bond_data_down(url='http://120.78.132.143',port=8023,password='123456')
    df=api.xg_bond_data_down(date='2025-02-09')
    print(df)
