import requests
import json
import openpyxl as op
import os
import pandas as pd
#biqunat跟单
class biquant_data:
    def __init__(self,account='outside',password='0',notebook_id='3e1b61ea-c340-11eb-aca8-9a8e001243a4'):
        '''
        account账户,
        password密码
        '''
        self.account=account
        self.password=password
        self.notebook_id=notebook_id
    def login(self):
        """
        模拟登录
        """
        # 登陆页面(拿cookie)
        url='https://bigquant.com/bigapis/auth/v1/auth/login'
        data={"payload":{"username":self.account,"password":self.password},"auth_name":"UserPass"}
        res=requests.post(url=url,data=json.dumps(data))
        text1=res.json()
        code=text1['code']
        if code==0:
            print('biquant登录成功'.format(self.account,self.password))
            text=res.cookies.get_dict()
            text=str(text).replace('{','').replace('}','').replace(':','=')
            text=text.replace("'",'')
            text=text.replace('""','')
            text=text.replace(',',';')
            headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'cookie':text
            }
            f = open(r'headers.txt', 'w+')
            f.write(str(headers))
            f.close()
            return  True
        else:
            print('账户{}密码{} 登录不成功'.format(self.account,self.password))
            return  False
    def get_headers(self):
        '''
        获取请求头
        :return:
        '''
        f = open(r'headers.txt',)
        comm=f.readline()
        f.close()
        headers=eval(comm)
        return headers
    def get_planned_order(self):
        '''
        获取计划交易数据
        '''
        headers=self.get_headers()
        params={
            'owner':self.account,
            'notebook_id':self.notebook_id,
            'limit': '1'
        }
        url='https://bigquant.com/bigwebapi/algo_info/planned_order?'
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        message=text['message']
        if message=='SUCCESSED':
            print('获取计划交易数据成功headers可用')
            df=pd.DataFrame(text['data']['planned_order_lists'][0])
            columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
            df.columns=columns
            return df
        else:
            print('获取计划交易数据失败headers不可用程序获取')
            self.login()
            headers=self.get_headers()
            params={
                'owner':self.account,
                'notebook_id':self.notebook_id,
                'limit': '1'
            }
            url='https://bigquant.com/bigwebapi/algo_info/planned_order?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='SUCCESSED':
                print('获取计划交易数据成功headers可用')
                df=pd.DataFrame(text['data']['planned_order_lists'][0])
                columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
                df.columns=columns
                return df
            else:
                print('获取计划交易不成功,重新登录')
    def get_position(self):
        '''
        获取持股数据
        '''
        headers=self.get_headers()
        params={
            'owner':self.account,
            'notebook_id':self.notebook_id,
            'limit': '1'
        }
        url='https://bigquant.com/bigwebapi/algo_info/position?'
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        message=text['message']
        if message=='SUCCESSED':
            print('获取计划交易数据成功headers可用')
            df=pd.DataFrame(text['data']['positions_lists'][0])
            columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
            #df.columns=columns
            return df
        else:
            print('获取计划交易数据失败headers不可用程序获取')
            self.login()
            headers=self.get_headers()
            params={
                'owner':self.account,
                'notebook_id':self.notebook_id,
                'limit': '1'
            }
            url='https://bigquant.com/bigwebapi/algo_info/position?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='SUCCESSED':
                print('获取计划交易数据成功headers可用')
                df=pd.DataFrame(text['data']['positions_lists'][0])
                columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
                #df.columns=columns
                return df
            else:
                print('获取计划交易不成功,重新登录')

    def get_transaction(self):
        '''
        获取交易详情
        '''
        headers=self.get_headers()
        params={
            'owner':self.account,
            'notebook_id':self.notebook_id,
            'limit': '1'
        }
        url='https://bigquant.com/bigwebapi/algo_info/transaction?'
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        message=text['message']
        if message=='SUCCESSED':
            print('获取计划交易数据成功headers可用')
            df=pd.DataFrame(text['data']['transactions_lists'][0])
            columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
            #df.columns=columns
            return df
        else:
            print('获取计划交易数据失败headers不可用程序获取')
            self.login()
            headers=self.get_headers()
            params={
                'owner':self.account,
                'notebook_id':self.notebook_id,
                'limit': '1'
            }
            url='https://bigquant.com/bigwebapi/algo_info/transaction?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='SUCCESSED':
                print('获取计划交易数据成功headers可用')
                df=pd.DataFrame(text['data']['transactions_lists'][0])
                columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
                #df.columns=columns
                return df
            else:
                print('获取计划交易不成功,重新登录')
#
    def get_sold_transaction(self):
        '''
        获取卖出详情
        '''
        headers=self.get_headers()
        params={
            'owner':self.account,
            'notebook_id':self.notebook_id,
            'limit': '1000'
        }
        url='https://bigquant.com/bigwebapi/algo_info/sold_transaction?'
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        message=text['message']
        if message=='SUCCESSED':
            print('获取计划交易数据成功headers可用')
            df=pd.DataFrame(text['data']['slod_transactions_lists'][0])
            columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
            #df.columns=columns
            return df
        else:
            print('获取计划交易数据失败headers不可用程序获取')
            self.login()
            headers=self.get_headers()
            params={
                'owner':self.account,
                'notebook_id':self.notebook_id,
                'limit': '1'
            }
            url='https://bigquant.com/bigwebapi/algo_info/sold_transaction?'
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            message=text['message']
            if message=='SUCCESSED':
                print('获取计划交易数据成功headers可用')
                df=pd.DataFrame(text['data']['slod_transactions_lists'])
                columns=['委托数量','代码','交易类型','时间','交易时间','调整数量','调整因子','名称','价格','持有比率']
                #df.columns=columns
                return df
            else:
                print('获取计划交易不成功,重新登录')
   
#bigqunat跟单
if __name__=='__main__':
    a=biquant_data()
    a.login()
    print(a.get_position())
    print(a.get_planned_order())
    print(a.get_transaction())