import pandas as pd
import json
import requests
import os
class server_trader_api:
    '''
    服务器交易api
    '''
    def __init__(self,url='http://120.78.132.143',port=8023,password='123456',
                qmt_path='D:/国金QMT交易端模拟/userdata_mini',account='55011917'):
        '''
        服务器交易api
        url服务器网页
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.qmt_path=qmt_path
        self.account=account
    def get_user_info(self):
        '''
        获取用户信息
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"finace_data_table_1.data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0",
            "outputs":{"id":"finace_data_table_1","property":"data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0"},
            "inputs":[{"id":"finace_data_password","property":"value","value":self.password},
            {"id":"finace_data_data_type","property":"value","value":"代码"},
            {"id":"finace_data_text","property":"value","value":"\n                from qmt_trader.qmt_trader import qmt_trader\n                trader=qmt_trader(path= r'D:/国金QMT交易端模拟/userdata_mini',account='55011917',account_type='STOCK')\n                trader.connect()\n                df=trader.position()\n                print(df)\n                df.to_csv(r'{}\\数据\\{}数据.csv')\n                "},
            {"id":"finace_data_run","property":"value","value":"运行"},
            {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["finace_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['finace_data_table_1']['data'])
        return df
    def get_user_def_data(self,func=''):
        '''
        自定义数据获取
        调用数据库
        '''
        text=self.params_func(text=func)
        func=text
        info=self.get_user_info()
        print(info)
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"finace_data_table.data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0",
            "outputs":{"id":"finace_data_table","property":"data@e60ed22f488acd1653d4a92a187c4775d06cc39e4afa58da3bee9c8261dcc6a0"},
            "inputs":[{"id":"finace_data_password","property":"value","value":self.password},
            {"id":"finace_data_data_type","property":"value","value":"代码"},
            {"id":"finace_data_text","property":"value","value":func},
            {"id":"finace_data_run","property":"value","value":"运行"},
            {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["finace_data_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['finace_data_table']['data'])
        return info, df
    def params_func(self,text=''):
        '''
        解析函数
        '''
        data_list=[]
        f=text.split('\n')
        for i in f:
            text=i.strip().lstrip()
            data_list.append(text)
        func='\n'.join(data_list)
        return func
    def position(self):
        '''
        获取持股
        '''
        qmt_path=self.qmt_path

        account=self.account
        func='''
        from qmt_trader.qmt_trader import qmt_trader
        trader=qmt_trader(path= r'{}',account='55011917',account_type='STOCK')
        trader.connect()
        df=trader.position()
        print(df)
        '''.format(self.qmt_path,self.account)+'''df.to_csv(r'{}\数据\{}数据.csv')'''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def balance(self):
        '''
        账户
        '''
        qmt_path=self.qmt_path
        account=self.account
        func='''
        from qmt_trader.qmt_trader import qmt_trader
        trader=qmt_trader(path= r'{}',account='55011917',account_type='STOCK')
        trader.connect()
        df=trader.balance()
        print(df)
        '''.format(self.qmt_path,self.account)+'''df.to_csv(r'{}\数据\{}数据.csv')'''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def today_trades(self):
        '''
        今日成交
        '''
        qmt_path=self.qmt_path

        account=self.account
        func='''
        from qmt_trader.qmt_trader import qmt_trader
        trader=qmt_trader(path= r'{}',account='55011917',account_type='STOCK')
        trader.connect()
        df=trader.today_trades()
        print(df)
        '''.format(self.qmt_path,self.account)+'''df.to_csv(r'{}\数据\{}数据.csv')'''
        info,df=self.get_user_def_data(func=func)
        return info,df
    def today_entrusts(self):
        '''
        今日委托
        '''
        qmt_path=self.qmt_path

        account=self.account
        func='''
        from qmt_trader.qmt_trader import qmt_trader
        trader=qmt_trader(path= r'{}',account='55011917',account_type='STOCK')
        trader.connect()
        df=trader.today_entrusts()
        print(df)
        '''.format(self.qmt_path,self.account)+'''df.to_csv(r'{}\数据\{}数据.csv')'''
        info,df=self.get_user_def_data(func=func)
        return info,df


