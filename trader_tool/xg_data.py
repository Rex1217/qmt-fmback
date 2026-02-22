import pandas as pd
import json
import requests
import os
import json
import random
class xg_data:
    '''
    小果金融数据库
    '''
    def __init__(self,select_list=['服务器4',"服务器5","服务器6"],random_select=True):
        '''
        小果金融数据库
        url服务器网页
        port端口
        password授权码
        random_select随机选择服务器
        '''
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=text=json.loads(com)
        password=text['数据授权码']
        srever_dict=text['服务器']
        srever_list=list(srever_dict.keys())
        if random_select==True:
            print('随机选择服务器')
            srever=random.choice(srever_list)
            url=srever_dict[srever][0]
            port=srever_dict[srever][-1]
        else:
            print('固定选择服务器')
            srever=random.choice(select_list)
            url=srever_dict[srever][0]
            port=srever_dict[srever][-1]
        print('服务器*****************:{}'.format(srever))
        print('服务器url*****************:{}'.format(url))
        print('服务器端口******************:{}'.format(port))
        print('用户授权码*************************:{}'.format(password))
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
            "output":"finace_data_table_1.data@c28c1f466316fd80f79b58b2e7baab2f",
            "outputs":{"id":"finace_data_table_1","property":"data@c28c1f466316fd80f79b58b2e7baab2f"},
            "inputs":[{"id":"finace_data_password","property":"value","value":"{}".format(self.password)},
            {"id":"finace_data_data_type","property":"value","value":"代码"},
            {"id":"finace_data_text","property":"value","value":"from trader_tool.stock_data import stock_data\nstock_data=stock_data()\ndf=stock_data.get_stock_hist_data_em(stock='600031',start_date='20210101',end_date='20600101',data_type='D',count=8000)\ndf.to_csv(r'{}\\数据\\{}数据.csv')\n                \n                "},
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
        try:
            text=self.params_func(text=func)
            func=text
            info=self.get_user_info()
            print(info)
            url='{}:{}/_dash-update-component'.format(self.url,self.port)
            headers={'Content-Type':'application/json'}
            data={"output":"finace_data_table.data@c28c1f466316fd80f79b58b2e7baab2f",
                "outputs":{"id":"finace_data_table","property":"data@c28c1f466316fd80f79b58b2e7baab2f"},
                "inputs":[{"id":"finace_data_password","property":"value","value":"{}".format(self.password)},
                {"id":"finace_data_data_type","property":"value","value":"代码"},
                {"id":"finace_data_text","property":"value","value":"{}".format(func)},
                {"id":"finace_data_run","property":"value","value":"运行"},
                {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
                "changedPropIds":["finace_data_run.value"]}
            res=requests.post(url=url,data=json.dumps(data),headers=headers)
            text=res.json()
            df=pd.DataFrame(text['response']['finace_data_table']['data'])
            for i in df.columns.tolist():
                try:
                    df[i]=pd.to_numeric(df[i])
                except:
                    pass
            print('服务器数据获取完成第一次*******************')
            return df
        except Exception as e:
            print('第一次失败第二次获取')
            try:
                text=self.params_func(text=func)
                func=text
                info=self.get_user_info()
                print(info)
                url='{}:{}/_dash-update-component'.format(self.url,self.port)
                headers={'Content-Type':'application/json'}
                data={"output":"finace_data_table.data@c28c1f466316fd80f79b58b2e7baab2f",
                    "outputs":{"id":"finace_data_table","property":"data@c28c1f466316fd80f79b58b2e7baab2f"},
                    "inputs":[{"id":"finace_data_password","property":"value","value":"{}".format(self.password)},
                    {"id":"finace_data_data_type","property":"value","value":"代码"},
                    {"id":"finace_data_text","property":"value","value":"{}".format(func)},
                    {"id":"finace_data_run","property":"value","value":"运行"},
                    {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
                    "changedPropIds":["finace_data_run.value"]}
                res=requests.post(url=url,data=json.dumps(data),headers=headers)
                text=res.json()
                df=pd.DataFrame(text['response']['finace_data_table']['data'])
                for i in df.columns.tolist():
                    try:
                        df[i]=pd.to_numeric(df[i])
                    except:
                        pass
                print('服务器数据获取完成*******************')
                return df
            except:
                print('第二次失败第三次获取')
                try:
                    text=self.params_func(text=func)
                    func=text
                    info=self.get_user_info()
                    print(info)
                    url='{}:{}/_dash-update-component'.format(self.url,self.port)
                    headers={'Content-Type':'application/json'}
                    data={"output":"finace_data_table.data@c28c1f466316fd80f79b58b2e7baab2f",
                        "outputs":{"id":"finace_data_table","property":"data@c28c1f466316fd80f79b58b2e7baab2f"},
                        "inputs":[{"id":"finace_data_password","property":"value","value":"{}".format(self.password)},
                        {"id":"finace_data_data_type","property":"value","value":"代码"},
                        {"id":"finace_data_text","property":"value","value":"{}".format(func)},
                        {"id":"finace_data_run","property":"value","value":"运行"},
                        {"id":"finace_data_down_data","property":"value","value":"不下载数据"}],
                        "changedPropIds":["finace_data_run.value"]}
                    res=requests.post(url=url,data=json.dumps(data),headers=headers)
                    text=res.json()
                    df=pd.DataFrame(text['response']['finace_data_table']['data'])
                    for i in df.columns.tolist():
                        try:
                            df[i]=pd.to_numeric(df[i])
                        except:
                            pass
                    print('服务器数据获取完成*******************')
                    return df
                except:
                    print('服务器数据获取失败*******************',e)
                    df=pd.DataFrame()
                    df['数据状态']=[False]
                    return df
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
if __name__=='__main__':
    models=xg_data()
    func="""
    import akshare as ak
    df=ak.stock_rank_cxg_ths()
    print(df)
    df.to_csv(r'{}\数据\{}数据.csv')
    """
    info,df=models.get_user_def_data(func=func)
    print(df)