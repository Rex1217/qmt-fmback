'''
小果聚宽跟单系统
原理替代,继承聚宽的交易函数类
读取下单类的函数参数把交易数据发送到服务器
把下面的全部源代码复制到聚宽策略的开头就可以
实盘前先模拟盘测试一下数据
'''
import requests
import json
import pandas as pd
url='http://124.220.32.224'
port=8025
#记得把这个改成自己的一个策略一个
password='123456'
class xg_qmt_jq:
    def __init__(self,url='http://124.220.32.224',port=8025,password='123456'):
        '''
        获取服务器数据
        '''
        self.url=url
        self.port=port
        self.password=password
    def get_user_data(self,data_type='用户信息'):
        '''
        获取使用的数据
        data_type='用户信息','实时数据',历史数据','清空实时数据','清空历史数据'
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table.data@63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad",
            "outputs":{"id":"joinquant_trader_table","property":"data@63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad"},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
                    {"id":"joinquant_trader_data_type","property":"value","value":data_type},
                    {"id":"joinquant_trader_text","property":"value","value":"\n               {'状态': 'held', '订单添加时间': 'datetime.datetime(2024, 4, 23, 9, 30)', '买卖': 'False', '下单数量': '9400', '已经成交': '9400', '股票代码': '001.XSHE', '订单ID': '1732208241', '平均成交价格': '10.5', '持仓成本': '10.59', '多空': 'long', '交易费用': '128.31'}\n                "},
                    {"id":"joinquant_trader_run","property":"value","value":"运行"},
                    {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["joinquant_trader_run.value"],"parsedChangedPropsIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
    def send_order(self,result):
        '''
        发送交易数据
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={"output":"joinquant_trader_table.data@63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad",
            "outputs":{"id":"joinquant_trader_table","property":"data@63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad"},
            "inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
                    {"id":"joinquant_trader_data_type","property":"value","value":'实时数据'},
                    {"id":"joinquant_trader_text","property":"value","value":result},
                    {"id":"joinquant_trader_run","property":"value","value":"运行"},
                    {"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["joinquant_trader_run.value"],"parsedChangedPropsIds":["joinquant_trader_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
        return df
#继承类
xg_data=joinquant_trader(url=url,port=port,password=password)
def send_order(result):
    '''
    发送函数
    status: 状态, 一个OrderStatus值
    add_time: 订单添加时间, [datetime.datetime]对象
    is_buy: bool值, 买还是卖，对于期货:
    开多/平空 -> 买
    开空/平多 -> 卖
    amount: 下单数量, 不管是买还是卖, 都是正数
    filled: 已经成交的股票数量, 正数
    security: 股票代码
    order_id: 订单ID
    price: 平均成交价格, 已经成交的股票的平均成交价格(一个订单可能分多次成交)
    avg_cost: 卖出时表示下卖单前的此股票的持仓成本, 用来计算此次卖出的收益. 买入时表示此次买入的均价(等同于price).
    side: 多/空，'long'/'short'
    action: 开/平， 'open'/'close'
    commission交易费用（佣金、税费等）
    '''
    data={}
    data['状态']=str(result.status)
    data['订单添加时间']=str(result.add_time)
    data['买卖']=str(result.is_buy)
    data['下单数量']=str(result.amount)
    data['已经成交']=str(result.filled)
    data['股票代码']=str(result.security)
    data['订单ID']=str(result.order_id)
    data['平均成交价格']=str(result.price)
    data['持仓成本']=str(result.avg_cost)
    data['多空']=str(result.side)
    data['交易费用']=str(result.commission)
    result=str(data)
    xg_data.send_order(result)
    return data
  
def xg_order(func):
    '''
    继承order对象 数据交易函数
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == None:
            return
        send_order(result)
        return result
    return wrapper
def xg_order_target(func):
    '''
    继承order_target对象 百分比
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == None:
            return        
        send_order(result)
        return result
    return wrapper
    
def xg_order_value(func):
    '''
    继承order_value对象 数量
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == None:
            return        
        send_order(result)
        return result
    return wrapper
def xg_order_target_value(func):
    '''
    继承order_target_value对象 数量
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == None:
            return        
        send_order(result)
        return result
    return wrapper
order = xg_order(order)
order_target = xg_order_target(order_target)
order_value = xg_order_value(order_value)
order_target_value = xg_order_target_value(order_target_value)

