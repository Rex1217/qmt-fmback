import pandas as pd
import json
import requests
from datetime import datetime
class joinquant_trader:
    '''
    聚宽交易
    '''
    def __init__(self,url='http://120.78.132.143',port='8023',password='123456',test=True):
        '''
        url服务器
        port端口
        password授权码
        trader是否直接调用服务器交易
        '''
        self.url=url
        self.port=port
        self.password=password
        self.test=test
    def get_user_info(self):
        '''
        获取用户信息
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table_1.data@f44721d75cb159e250b306f23e48d89d",
            "outputs":{"id":"joinquant_trader_table_1","property":"data@f44721d75cb159e250b306f23e48d89d"},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
            {"id":"joinquant_trader_data_type","property":"value","value":"实时信号"},
            {"id":"joinquant_trader_text","property":"value","value":"\n                date=2023-01-01,security=600031.SH,price=10.8,amount=100,side=long,trader_func=order\n                "},
            {"id":"joinquant_trader_run","property":"value","value":"运行"},
            {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table_1']['data'])
        return df
    def seed_trader_info(self,text='date=2023-01-01,security=600031.SH,price=20,amount=100,side=long,trader_func=order'):
        '''
        发送交易信号
        '''
        print(self.get_user_info())
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table.data@f44721d75cb159e250b306f23e48d89d",
            "outputs":{"id":"joinquant_trader_table","property":"data@f44721d75cb159e250b306f23e48d89d"},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
            {"id":"joinquant_trader_data_type","property":"value","value":"实时信号"},
            {"id":"joinquant_trader_text","property":"value","value":text},
            {"id":"joinquant_trader_run","property":"value","value":"运行"},
            {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
    def get_hist_trader_info(self):
        '''
        获取历史交易数据
        '''
        print(self.get_user_info())
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table.data@f44721d75cb159e250b306f23e48d89d",
            "outputs":{"id":"joinquant_trader_table","property":"data@f44721d75cb159e250b306f23e48d89d"},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
            {"id":"joinquant_trader_data_type","property":"value","value":"历史信号"},
            {"id":"joinquant_trader_text","property":"value","value":"\n                date=2023-01-01,security=600031.SH,price=10.8,amount=100,side=long,trader_func=order\n                "},
            {"id":"joinquant_trader_run","property":"value","value":"运行"},
            {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
            "changedPropIds":["joinquant_trader_data_type.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
    def order(self,context='',security='', amount='', style=None, side='long', pindex=0, close_today=False):
        '''
        security: 标的代码
        amount: 期望的最终数量
        style: 参见OrderStyle, None代表MarketOrder
        side: 'long'/'short'，操作多单还是空单。默认为多单。默认为多单，股票、基金暂不支持开空单。
        pindex: 在使用set_subportfolios创建了多个仓位时，指定subportfolio 的序号, 从 0 开始, 比如 0为 指定第一个 subportfolio, 1 为指定第二个 subportfolio，默认为0。
        close_today: 平今字段，close_today: 平今字段，仅对上海国际能源中心，上海期货交易所，中金所生效，其他交易所将会报错（其他交易所没有区分平今与平昨，均按照先开先平的方法处理）。
        对上海国际能源中心，上海期货交易所，中金所的标的：
        close_today = True, 只平今仓，今仓不足的时候，订单将会被废单。
        close_today = False, 优先平昨仓，昨仓不足部分平今仓
        不管close_today是True还是False，此函数只会产生一个订单，区别在于平仓时的手续费计算，平昨仓使用close_commission对应手续费率，平今仓使用close_today_commission手续费率。
        '''
        if self.test==True:
            price=10
            date=str(datetime.now())
        else:
            price=get_bars(security, count=5, unit='1d', fields=['close'])[-1][0]
            date=get_bars(security, count=5, unit='1d', fields=['date'])[-1][0]
        text='date={},security={},price={},amount={},side={},trader_func=order'.format(date,security,price,amount,side)
        result=self.seed_trader_info(text=text)
        stats=result['数据状态'].tolist()[-1]
        if stats==True:
            print('交易信号发送成功',date,security,price,amount,side,'order')
            return True,date,security,price,amount,side,'order'
        else:
            print('交易信号发送失败',date,security,price,amount,side,'order')
            return False,date,security,price,amount,side,'order'
    
if __name__=='__main__':
    models=joinquant_trader()
    df=models.order()
    

        