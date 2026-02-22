import pandas as pd
import json
import requests
import os
class xg_trader_api:
    '''
    小果交易api
    '''
    def __init__(self,url='http://127.0.0.1',port=8050,password='123456'):
        '''
        小果交易api
        url服务器网页
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
    def get_user_info(self):
        '''
        获取用户信息
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"trader_table_1.data@b40ab3b3ad3b940c92d37efd243a0f5f",
            "outputs":{"id":"trader_table_1","property":"data@b40ab3b3ad3b940c92d37efd243a0f5f"},
            "inputs":[{"id":"trader_password","property":"value","value":self.password},
            {"id":"trader_data_type","property":"value","value":"代码"},
            {"id":"trader_text","property":"value","value":"df=trader.position()\ndf.to_csv(r'{}\\数据\\{}数据.csv')\n                \n                "},
            {"id":"trader_run","property":"value","value":"运行"},
            {"id":"trader_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['trader_table_1']['data'])
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
        data={"output":"trader_table.data@b40ab3b3ad3b940c92d37efd243a0f5f",
            "outputs":{"id":"trader_table","property":"data@b40ab3b3ad3b940c92d37efd243a0f5f"},
            "inputs":[{"id":"trader_password","property":"value","value":self.password},
            {"id":"trader_data_type","property":"value","value":"代码"},
            {"id":"trader_text","property":"value","value":func},
            {"id":"trader_run","property":"value","value":"运行"},
            {"id":"trader_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['trader_table']['data'])
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
    def balance(self):
        '''
        获取持股
        '''
        func="""
        df=trader.balance()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def position(self):
        '''
        获取持股
        '''
        func="""
        df=trader.position()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def today_entrusts(self):
        '''
        当日委托
        '''
        func="""
        df=trader.today_entrusts()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def today_trades(self):
        '''
        当日成交
        '''
        func="""
        df=trader.today_trades()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def buy(self,security='600111', price=16.5, amount=100):
        '''
        买入
        '''
        func="""
        trader.buy(security="{}",price={},amount={})
        """.format(security,price,amount)+"""\n
        df=pd.DataFrame()
        df['操作']=['buy']
        df['security']=[{}]
        df['price']=[{}]
        df['amount']=[{}]
        """.format(security,price,amount)+"""\n
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def sell(self,security='600111', price=16.5, amount=100):
        '''
        卖出
        '''
        func="""
        trader.sell(security="{}",price={},amount={})
        """.format(security,price,amount)+"""\n
        df=pd.DataFrame()
        df['操作']=['sell']
        df['security']=[{}]
        df['price']=[{}]
        df['amount']=[{}]
        """.format(security,price,amount)+"""\n
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
if __name__=='__main__':
    '''
    交易api
    '''
    trader=xg_trader_api()
    info,df=trader.buy()
    print(df)

