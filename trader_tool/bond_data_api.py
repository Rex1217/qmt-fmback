import pandas as pd
import json
import requests
class bond_data_api:
    def __init__(self):
        pass
    def get_login(self):
        '''
        模拟登录
        '''
        data={"username":"",
            "password":""}
        url='https://qisisay.com/prod-api/login'
        headers={
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'connection':'keep-alive',
            'content-length':'39',
            'content-type':'application/json;charset=UTF-8',
            
            'istoken':'false',
            'origin':'https://qisisay.com',
            'referer':'https://qisisay.com/login?redirect=%2Findex',
            'sec-ch-ua':'"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }
            
        res=requests.post(data=json.dumps(data),url=url,headers=headers)
        text=res.json()
        print(text)
        stats=text['msg']
        if stats=='操作成功':
            print(stats,'登录成功')
            self.token=text['token']
        else:
            print(text)
            self.token=''
        print(res.text)
        return self.token
    def get_bond_now_5_factor(self,max=150,min=100):
        '''
        获取新可转债新5因子数据
        '''
        url='https://qisisay.com/prod-api/kzz/jsl1/ffwn?max={}&min={}'.format(max,min)
        res=requests.get(url=url)
        text=res.json()
        df=pd.DataFrame(text['data'])
        df.columns=['调整条件','可转债代码','可转债名称',"bond_nm_fg","纯债溢价率","cap_mv_rate",
            "转股价值","剩余规模","剩余市值","双低","基金持仓","id","涨跌幅","premium_rt","价格",
            "价格比例","评分","redeem_price_ratio","redeem_remain_days","redeem_status",
            "sincrease_rt","股票名称",'股票行业',"市值","换手率","更新时间","股票波动率",
            "成交量","剩余年限"]
        return df 

if __name__=='__main__':
    api=bond_data_api()
    print(api.get_bond_now_5_factor())