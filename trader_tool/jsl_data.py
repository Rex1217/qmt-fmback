# -*- coding: utf-8 -*-
# @File : login.py

import datetime
import time
import pandas as pd
import execjs
import os
import requests
from trader_tool.dfcf_cov_data import dfcf_bond_cov_data
from trader_tool.bond_cov_data import bond_cov_data
filename = 'encode_jsl.txt'

path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(path, filename)

headers = {
    'Host': 'www.jisilu.cn', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
    'Cache-Control': 'no-cache', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
    'Origin': 'https://www.jisilu.cn', 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Referer': 'https://www.jisilu.cn/login/',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'
}


def decoder(text): # 加密用户名和密码
    with open(full_path, 'r', encoding='utf8') as f:
        source = f.read()

    ctx = execjs.compile(source)
    key = '397151C04723421F'
    return ctx.call('jslencode', text, key)


def get_bond_info(session): # 获取行情数据
    ts = int(time.time() * 1000)
    url = 'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={}'.format(ts)
    data={
        'fprice':'' ,
        'tprice':'' ,
        'curr_iss_amt':'' ,
        'volume': '',
        'svolume':'' ,
        'premium_rt': '',
        'ytm_rt':'', 
        'rating_cd':'' ,
        'is_search': 'N',
        'market_cd[]': 'shmb',
        'market_cd[]': 'shkc',
        'market_cd[]': 'szmb',
        'market_cd[]': 'szcy',
        'btype':'' ,
        'listed': 'Y',
        'qflag': 'N',
        'sw_cd': '',
        'bond_ids':'' ,
        'rp': '50',
        'page': '0'
    }
    import json
    r = session.post(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
    ret = r.json()
    result = []
    for item in ret['rows']:
        result.append(item['cell'])
    return result


def login(user, password): # 登录
    session = requests.Session()
    url = 'https://www.jisilu.cn/account/ajax/login_process/'
    username = decoder(user)
    jsl_password = decoder(password)
    data = {
        'return_url': 'https://www.jisilu.cn/',
        'user_name': username,
        'password': jsl_password,
        'net_auto_login': '1',
        '_post_type': 'ajax',
    }

    js = session.post(
        url=url,
        headers=headers,
        data=data,
    )

    ret = js.json()

    if ret.get('errno') == 1:
        print('集思录登录成功 账户 {} 密码{}'.format(user,password))
        return session
    else:
        print('集思录登录失败 账户 {} 密码{}'.format(user,password))
        raise ValueError('登录失败')

def adjust_data(x):
    x=str(x)
    if '%' in x:
        return x.replace('%','')
    else:
        return x
def get_jsl_data(jsl_user='150079',jsl_password='35790'):
    '''
    获取集思录数据
    '''
    if True:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        session = login(jsl_user, jsl_password)
        ret = get_bond_info(session)
        df = pd.DataFrame(ret)
        df = df.reset_index()
        df.rename(
            columns={
                'index': 'index',
                'bond_id': '证券代码', 
                'bond_nm': '可转债名称', 
                'bond_py': 'bond_py', 
                'price': '价格', 
                'increase_rt': '涨跌幅', 
                'stock_id': '正股代码', 
                'stock_nm': '正股名称', 
                'stock_py': 'stock_py', 
                'sprice': '正股价', 
                'sincrease_rt': '正股涨跌', 
                'pb': '正股PB', 
                'convert_price': '转股价', 
                'convert_value': '转股价值', 
                'convert_dt': '转股开始日', 
                'premium_rt': '转股溢价率', 
                'bond_premium_rt': '债底溢价率', 
                'dblow': '双低', 
                'adjust_condition': '下修状态', 
                'sw_cd': '申万', 
                'market_cd': '市场', 
                'btype': 'btype', 
                'list_dt': '上市时间', 
                'owned': 'owned', 
                'hold': 'hold', 
                'bond_value': '纯债价值', 
                'rating_cd': '评级', 
                'option_value': '期权价值', 
                'volatility_rate': '正股年化波动率', 
                'put_convert_price': '回售触发价', 
                'force_redeem_price': '强赎触发价', 
                'convert_amt_ratio': '转债占比', 
                'fund_rt': '机构持仓', 
                'maturity_dt': '到期时间', 
                'year_left': '剩余年限', 
                'curr_iss_amt': '剩余规模', 
                'volume': '成交额', 
                'svolume': '正股成交额', 
                'turnover_rt': '换手率', 
                'ytm_rt': '到期税前收益', 
                'put_ytm_rt': 'put_ytm_rt', 
                'notes': 'notes', 
                'noted':'noted', 
                'last_time': 'last_time', 
                'qstatus': 'qstatus', 
                'sqflag': 'sqflag', 
                'pb_flag': 'pb_flag', 
                'adj_cnt': 'adj_cnt', 
                'adj_scnt': 'adj_scnt', 
                'convert_price_valid': 'convert_price_valid', 
                'convert_price_tips': 'convert_price_tips', 
                'convert_cd_tip': 'convert_cd_tip', 
                'ref_yield_info': 'ref_yield_info', 
                'adjusted': 'adjusted', 
                'orig_iss_amt': '发行规模', 
                'price_tips': 'price_tips', 
                'redeem_dt': 'redeem_dt', 
                'real_force_redeem_price': 'real_force_redeem_price', 
                'option_tip': 'option_tip', 
                'adjust_status': 'adjust_status', 
                'unadj_cnt': 'unadj_cnt', 
                'after_next_put_dt': 'after_next_put_dt', 
                'adjust_remain_days': 'adjust_remain_days', 
                'adjust_orders': 'adjust_orders', 
                'icons': 'icons'
                },inplace=True)
        return df
def get_dfcf_lww_data():
    '''
    东方财富
    '''
    if True:
        models=dfcf_bond_cov_data()
        df=models.bond_cov_comparison()
        df.rename(columns={'转债代码':'证券代码','转债名称':'可转债名称','转债最新价':'价格',
                              '转债涨跌幅':'涨跌幅','正股最新价':"正股价","正股涨跌幅":"正股涨跌"},inplace=True)
        #df['选择']=df['上市日期'].apply(lambda x:'是' if x=='-' else '不是')
        #df=df[df['选择']=='不是']
        df['价格']=df['价格'].replace('-',None)
        df['涨跌幅']=df['涨跌幅'].replace('-',None)
        try:
            print('东方财富可转债数据合并宁稳网数据成功')
            models1=bond_cov_data()
            nww=models1.simple_table()
            nww['可转债名称']=nww['转债名称']
            result=pd.merge(df,nww,on=['可转债名称'])
            result['证券代码']=result['转债代码']
            for i in result.columns.tolist():
                result[i]=result[i].apply(adjust_data)
            for i in result.columns.tolist():
                try:
                    result[i]=pd.to_numeric(result[i])
                except:
                    pass
            return result
        except:
            print('东方财富可转债数据')
            for i in df.columns.tolist():
                try:
                    df[i]=pd.to_numeric(df[i])
                except:
                    pass
            return df
def get_all_cov_bond_data(jsl_user='150079',jsl_password='35790'): # 主函数
    '''
    jsl_user账户名称
    jsl_password账户密码
    '''
    try:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        session = login(jsl_user, jsl_password)
        ret = get_bond_info(session)
        df = pd.DataFrame(ret)
        df = df.reset_index()
        df.rename(
            columns={
                'index': 'index',
                'bond_id': '证券代码', 
                'bond_nm': '可转债名称', 
                'bond_py': 'bond_py', 
                'price': '价格', 
                'increase_rt': '涨跌幅', 
                'stock_id': '正股代码', 
                'stock_nm': '正股名称', 
                'stock_py': 'stock_py', 
                'sprice': '正股价', 
                'sincrease_rt': '正股涨跌', 
                'pb': '正股PB', 
                'convert_price': '转股价', 
                'convert_value': '转股价值', 
                'convert_dt': '转股开始日', 
                'premium_rt': '转股溢价率', 
                'bond_premium_rt': '债底溢价率', 
                'dblow': '双低', 
                'adjust_condition': '下修状态', 
                'sw_cd': '申万', 
                'market_cd': '市场', 
                'btype': 'btype', 
                'list_dt': '上市时间', 
                'owned': 'owned', 
                'hold': 'hold', 
                'bond_value': '纯债价值', 
                'rating_cd': '评级', 
                'option_value': '期权价值', 
                'volatility_rate': '正股年化波动率', 
                'put_convert_price': '回售触发价', 
                'force_redeem_price': '强赎触发价', 
                'convert_amt_ratio': '转债占比', 
                'fund_rt': '机构持仓', 
                'maturity_dt': '到期时间', 
                'year_left': '剩余年限', 
                'curr_iss_amt': '剩余规模', 
                'volume': '成交额', 
                'svolume': '正股成交额', 
                'turnover_rt': '换手率', 
                'ytm_rt': '到期税前收益', 
                'put_ytm_rt': 'put_ytm_rt', 
                'notes': 'notes', 
                'noted':'noted', 
                'last_time': 'last_time', 
                'qstatus': 'qstatus', 
                'sqflag': 'sqflag', 
                'pb_flag': 'pb_flag', 
                'adj_cnt': 'adj_cnt', 
                'adj_scnt': 'adj_scnt', 
                'convert_price_valid': 'convert_price_valid', 
                'convert_price_tips': 'convert_price_tips', 
                'convert_cd_tip': 'convert_cd_tip', 
                'ref_yield_info': 'ref_yield_info', 
                'adjusted': 'adjusted', 
                'orig_iss_amt': '发行规模', 
                'price_tips': 'price_tips', 
                'redeem_dt': 'redeem_dt', 
                'real_force_redeem_price': 'real_force_redeem_price', 
                'option_tip': 'option_tip', 
                'adjust_status': 'adjust_status', 
                'unadj_cnt': 'unadj_cnt', 
                'after_next_put_dt': 'after_next_put_dt', 
                'adjust_remain_days': 'adjust_remain_days', 
                'adjust_orders': 'adjust_orders', 
                'icons': 'icons'
                },inplace=True)
        try:
            df['转债余额']=df['剩余规模']
        except:
            print('转债余额有问题')
        try:
            df['信用']=df['评级']
        except:
            print('信用有问题')
        return df
    except:
        '''
        [
                "序号",
                "转债代码",
                "转债名称",
                "转债最新价",
                "转债涨跌幅",
                "正股代码",
                "正股名称",
                "正股最新价",
                "正股涨跌幅",
                "转股价",
                "转股价值",
                "转股溢价率",
                "纯债溢价率",
                "回售触发价",
                "强赎触发价",
                "到期赎回价",
                "纯债价值",
                "开始转股日",
                "上市日期",
                "申购日期",
            ]
        '''
       
        models=dfcf_bond_cov_data()
        df=models.bond_cov_comparison()
        df.rename(columns={'转债代码':'证券代码','转债名称':'可转债名称','转债最新价':'价格',
                              '转债涨跌幅':'涨跌幅','正股最新价':"正股价","正股涨跌幅":"正股涨跌"},inplace=True)
        #df['选择']=df['上市日期'].apply(lambda x:'是' if x=='-' else '不是')
        #df=df[df['选择']=='不是']
        df['价格']=df['价格'].replace('-',None)
        df['涨跌幅']=df['涨跌幅'].replace('-',None)
        try:
            print('东方财富可转债数据合并宁稳网数据')
            models1=bond_cov_data()
            nww=models1.simple_table()
            nww['证券代码']=nww['转债代码']
            nww['证券代码']=nww['证券代码'].astype(str)
            df['证券代码']=df['证券代码'].astype(str)
            result=pd.merge(nww,df,on=['证券代码'])
            for i in result.columns.tolist():
                result[i]=result[i].apply(adjust_data)
            for i in result.columns.tolist():
                try:
                    result[i]=pd.to_numeric(result[i])
                except:
                    pass
            result=result.fillna(0)
            result['转股溢价率']=result['转股溢价率_x']
            result['转股价值']=result['转股价值_x']
            result['剩余规模']=result['转债余额']
            result['双低']=result['转债价格']+result['转股溢价率']
            df=result
            for i in df.columns.tolist():
                try:
                    df[i]=df[i].replace('-',0)
                except:
                    pass
                try:
                    df[i]=pd.to_numeric(df[i])
                except:
                    pass
            def select_data(x):
                if '天' in x and '年' not in x:
                    result=float(str(x).split('天')[0])
                    result=result/365
                    return result
                elif '年' in x and '天' not in x:
                    result=float(str(x).split('年')[0])
                    return result
                else:
                    year=float(str(x).split('年')[0])
                    daily=float(str(x).split('年')[-1].split('天')[0])/365
                    result=year+daily

            df['剩余年限']=df['剩余年限'].apply(select_data)
            #result['剩余年限']=result['剩余年限'].apply(lambda x:float(str(x).split('年')[0]))
            return df
        except:
            print('东方财富可转债数据')
            df=models.bond_cov_comparison()
            df.rename(columns={'转债代码':'证券代码','转债名称':'可转债名称','转债最新价':'价格',
                              '转债涨跌幅':'涨跌幅','正股最新价':"正股价","正股涨跌幅":"正股涨跌"},inplace=True)
            for i in df.columns.tolist():
                df[i]=df[i].replace('-',None)
                try:
                    df[i]=pd.to_numeric(df[i])
                except:
                    pass
            return df
        