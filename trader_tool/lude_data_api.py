import pandas as pd
import requests 
import json
class lude_data_api:
    def __init__(self,url='http://120.78.132.143',port='8023',password='123456'):
        '''
        手动下载存数据库
        禄得数据api
        url服务器
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
    def get_bond_data(self,date='2024-04-26'):
        '''
        获取可转债数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lude_data_maker_table.data@669dd4696a628d8290353c138057eb97",
            "outputs":{"id":"lude_data_maker_table","property":"data@669dd4696a628d8290353c138057eb97"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lude_data_data_type","property":"value","value":"禄得数据"},
            {"id":"lude_data_end_date","property":"date","value":date},
            {"id":"lude_data_run","property":"value","value":"运行"},
            {"id":"lude_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lude_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lude_data_maker_table']['data'])
        return df
    def get_bond_spot_data(self,date='2024-05-23'):
        '''
        获取可转债实时数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"lude_data_maker_table.data@669dd4696a628d8290353c138057eb97",
            "outputs":{"id":"lude_data_maker_table","property":"data@669dd4696a628d8290353c138057eb97"},
            "inputs":[{"id":"password","property":"value","value":self.password},
            {"id":"lude_data_data_type","property":"value","value":"实时数据"},
            {"id":"lude_data_end_date","property":"date","value":date},
            {"id":"lude_data_run","property":"value","value":"运行"},
            {"id":"lude_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["lude_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['lude_data_maker_table']['data'])
        return df
if __name__=='__main__':
    models=lude_data_api()
    df=models.get_bond_data(date='2024-05-23')
    print(df)
    df=models.get_bond_spot_data(date='2024-05-23')
    print(df)

        
