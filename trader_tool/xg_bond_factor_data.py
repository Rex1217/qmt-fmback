import pandas as pd
import json
import requests
import os
class xg_bond_factor_data:
    '''
    小果可转债因子数据库
    http://101.34.65.108:8023/
    '''
    def __init__(self,url='http://101.34.65.108',
                port='8023',
                url_code='5071dc6e12cd478aa2ab511bbb96abce1f6c0a05a17df9112582acfb29cc3216',

                password='123456'):
        '''
        小果可转债因子数据库
        url服务器网页
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.url_code=url_code
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
    def xg_bond_factor_data(self,date_type='实时数据',date='2024-09-09'):
        '''
        小果可转债因子数据库
        date_type=实时数据/全部默认因子/合成因子
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"xg_bond_data_maker_table.data@{}".format(self.url_code),
            "outputs":{"id":"xg_bond_data_maker_table","property":"data@{}".format(self.url_code)},
            "inputs":[{"id":"password","property":"value","value":self.password},
                    {"id":"xg_bond_data_data_type","property":"value","value":date_type},
                    {"id":"xg_bond_data_end_date","property":"date","value":date},
                    {"id":"xg_bond_data_run","property":"value","value":"运行"},
                    {"id":"xg_bond_data_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["xg_bond_data_run.value"],
                    "parsedChangedPropsIds":["xg_bond_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['xg_bond_data_maker_table']['data'])
        return df
if __name__=='__main__':
    api=xg_bond_factor_data(url='http://124.220.32.224',port='8023',password='123456')
    df=api.xg_bond_factor_data(date_type='实时数据',date='2025-02-09')
    print(df)
    df=api.xg_bond_factor_data(date_type='全部默认因子',date='2025-02-09')
    print(df)
    df=api.xg_bond_factor_data(date_type='合成因子',date='2025-02-09')
    print(df)
    df.to_excel(r'数据.xlsx')
