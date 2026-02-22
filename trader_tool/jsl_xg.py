# -*- coding: utf-8 -*-
import pandas as pd
import requests
import execjs
import time
import json
from datetime import datetime
import os
class jsl_xg:
    def __init__(self,user, password):
        '''
        获取集思录数据
        '''
        self.user=user
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.session=''
        self.headers = {
        'Host': 'www.jisilu.cn', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
        'Cache-Control': 'no-cache', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Origin': 'https://www.jisilu.cn', 'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Referer': 'https://www.jisilu.cn/login/',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'}
    def decoder(self,text):
        with open(r'{}\jsl.js'.format(self.path), 'r', encoding='utf8') as f:
            source = f.read()
        js = execjs.compile(source)
        key = '397151C04723421F'
        return js.call('encode', text, key)
    def login(self,):
        #user='J583812153 ', password='azalea1126'
        self.session = requests.Session()
        url = 'https://www.jisilu.cn/account/ajax/login_process/'
        username = self.decoder(self.user)
        password = self.decoder(self.password)
        data = {
            'return_url': 'https://www.jisilu.cn/',
            'user_name': username,
            'password': password,
            'net_auto_login': '1',
            '_post_type': 'ajax',
        }
        res = self.session.post(
            url=url,
            headers=self.headers,
            data=data,
        )
        data = res.json()
        if data.get('errno') == 1:
            print('集思录登录成功')
            return self.session
        else:
            raise ValueError('集思录登录失败')


#_session = login()


    def get_conv_data_jsl(self):
        """
        可转债列表
        """
        rename_dict = {
            'bond_id': '转债代码',
            'bond_nm': '转债名称',
            'bond_py': '转债拼音',
            'price': '最新价',
            'increase_rt': '涨跌幅',
            'stock_id': '正股代码',
            'stock_nm': '正股名称',
            'stock_py': '正股拼音',
            'sprice': '正股最新价',
            'sincrease_rt': '正股涨跌幅',
            'pb': '市净率',
            'convert_price': '转股价',
            'convert_value': '转股价值',
            'convert_dt': '距离转股天数',
            'premium_rt': '转股溢价率',
            'bond_premium_rt': '纯债溢价率',
            'dblow': '双低',
            'adjust_condition': '下修状态',
            'sw_cd': '申万行业',
            'market_cd': '市场代码',
            'list_dt': '上市日期',
            'bond_value': '纯债价值',
            'rating_cd': '外部评级',
            'option_value': '期权价值',
            'put_convert_price': '回售触发价',
            'force_redeem_price': '强赎触发价',
            'convert_amt_ratio': '转债市占比',
            'fund_rt': '机构持仓',
            'maturity_dt': '转股截止日期',
            'year_left': '剩余年限',
            'curr_iss_amt': '剩余市值(亿)',
            'volume': '成交额(万)',
            'svolume': '正股成交额',
            'turnover_rt': '换手率',
            'ytm_rt': '到期收益率(税前)',
            'put_ytm_rt': '回售收益',
            'last_time': '下载时间',
            'qstatus': '停牌提示',
            'sqflag': 'sqflag',
            'pb_flag': 'PB提示',
            'adj_cnt': '下修次数',
            'adj_scnt': '成功次数',
            'convert_price_valid': '转股生效',
            'convert_price_tips': '下修提示',
            'convert_cd_tip': '转股提示',
            'ref_yield_info': '转债提示',
            'adjusted': 'adjusted',
            'orig_iss_amt': '发行规模',
            'price_tips': '价格提示',
            'redeem_dt': '强赎日期',
            'real_force_redeem_price': '强赎价格',
            'option_tip': '期权提示',
            'unadj_cnt': '不下修次数',
            'adjust_remain_days': '下修剩余天数',
            'icons': '强赎提示',
            'theory_value': '理论价值',
            'deviation_degree': '理论偏离度',
            'short_estimate_put_dt': '预估回售日',
            'left_put_year': '回售剩余年限',
            'put_ytm_rt_tax': '回售税后收益',
            'volatility_rate': '正股年化波动率', 
        }
        ts = int(time.time() * 1000)
        url = f'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={ts}'
        data = {
            'fprice': '',
            'tprice': '',
            'curr_iss_amt': '',
            'volume': '',
            'svolume': '',
            'premium_rt': '',
            'ytm_rt': '',
            'rating_cd': '',
            'is_search': 'N',
            'btype': '',
            'listed': 'Y',
            'qflag': 'N',
            'sw_cd': '',
            'bond_ids': '',
            'rp': '50',
            'page': '0'
        }
        res = self.session.post(
            url=url,
            headers=self.headers,
            data=json.dumps(data)
        )
        data = res.json()
        data_list = []
        for item in data['rows']:
            data_list.append(item['cell'])
        df = pd.DataFrame(data_list)
        # 过滤退债
        df = df[df['price_tips'].str.contains('全价') & ~df['bond_nm'].str.contains('退债')]
        df.rename(columns=rename_dict, inplace=True)
        # 过滤停牌
        df = df[df['停牌提示'] != '03']
        today = datetime.today()
        df['上市日期'] = pd.to_datetime(df['上市日期'])
        df['上市天数'] = today - df['上市日期']
        return df

    def check_redeem_status(self,df,text):
        """
        已满足强赎条件
        公告提示强赎
        公告实施强赎
        公告到期赎回
        已公告强赎
        """
        if type(text) is list:
            return
        if type(text) is dict:
            _ = text.get('G', None)
            if _ is not None:
                if '不提前赎回' in _:
                    return '公告不强赎'
            _ = text.get('R', None)
            if _ is not None:
                if '到期赎回价' in _:
                    return '公告到期赎回'
                elif '赎回价' in _:
                    return '已公告强赎'
                else:
                    pass

        df['赎回状态'] = df['强赎提示'].apply(self.check_redeem_status)
        return df


    def get_adjust_data_jsl(self,):
        """
        可转债下修
        """
        url = 'https://www.jisilu.cn/webapi/cb/adjust/'
        res = self.session.get(url)
        json_data = res.json()
        data_dict = json_data['data']
        df = pd.DataFrame.from_dict(data_dict)
        return df


    def get_redeem_data_jsl(self,):
        """
        可转债强赎
        """
        url = 'https://www.jisilu.cn/webapi/cb/redeem/'
        res = self.session.get(url)
        json_data = res.json()
        data_dict = json_data['data']
        df = pd.DataFrame.from_dict(data_dict)
        return df


if __name__ == '__main__':
    models=jsl_xg(user='J583812153 ', password='azalea1126')
    models.login()
    df=models.get_conv_data_jsl()
    print(df)
    df.to_excel(r'数据.xlsx')
