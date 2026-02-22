import pandas as pd
from tqdm import tqdm
import numpy as np
import json
import numpy as np
import os
from datetime import datetime
import time
import requests
import json
class xms_quant_bond_user_factor_trader:
    def __init__(self,
                data_type='实时数据',
                url='http://124.220.32.224/',
                port='8023',
                text={},
                date='20250114'
                ):
        '''
        西蒙斯可转债量化交易系统   
        作者:西蒙斯量化
        微信:xg_quant
        '''
        print('西蒙斯可转债量化交易系统')
        print('作者:西蒙斯量化,微信:xg_quant')
        self.data_type=data_type
        self.url=url
        self.port=port
        self.text=text
        self.date=date
        self.stats=False
        self.redeem=pd.DataFrame()
    def get_spot_data(self,date='20250711'):
        '''
        获取实时数据表
        '''
        try:
            url='{}:{}/data/实时数据/{}.json?t=1752251108452'.format(self.url,self.port,date)
            res=requests.get(url=url)
            res=res.json()
            df=pd.DataFrame(res)
        except Exception as e:
            print(e,'获取实时数据表有问题')
            df=pd.DataFrame()
        return df
    def get_all_mr_factor_data(self,date='20250711'):
        '''
        获取全部默认因子表
        '''
        try:
            url='{}:{}/data/全部默认因子/{}.json?t=1752251108452'.format(self.url,self.port,date)
            res=requests.get(url=url)
            res=res.json()
            df=pd.DataFrame(res)
        except Exception as e:
            print(e,'全部默认因子有问题')
            df=pd.DataFrame()
        return df
    def get_all_connect_factor_data(self,date='20250711'):
        '''
        获取合成因子表
        '''
        try:
            url='{}:{}/data/合成因子/{}.json?t=1752251108452'.format(self.url,self.port,date)
            res=requests.get(url=url)
            res=res.json()
            df=pd.DataFrame(res)
        except Exception as e:
            print(e,'合成因子有问题')
            df=pd.DataFrame()
        return df
    def select_bond_cov(self,x):
        '''
        选择证券代码
        '''
        if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
            return '是'
        else:
            return '不是'
    def get_shift_data(self,n=1):
        '''
        获取前n天的日期
        '''
        date_str =self.date
        date_obj = pd.to_datetime(date_str, format="%Y%m%d")  # 转换为 pandas Timestamp
        new_date_obj = date_obj - pd.Timedelta(days=n)        # 减少一天
        new_date_str = new_date_obj.strftime("%Y%m%d")        # 转换回字符串
        return new_date_str
    def get_all_factor_data(self):
        '''
        获取可转债全部数据
        '''
        print("获取可转债全部数据************")
        text=self.text
        now_date=self.date
        if self.data_type=='实时数据':
            df=self.get_spot_data(date=now_date)
        elif self.data_type=='全部默认因子':
            df=self.get_all_mr_factor_data(date=now_date)
        elif self.data_type=='合成因子':
            df=self.get_all_connect_factor_data(date=now_date)
        else:
            df=self.get_spot_data(date=now_date)
        if df.shape[0]<=0:
            print(now_date,'获取数据有问题获取前一个交易日数据')
            now_date=self.get_shift_data(n=1)
            print(now_date)
            if self.data_type=='实时数据':
                df=self.get_spot_data(date=now_date)
            elif self.data_type=='全部默认因子':
                df=self.get_all_mr_factor_data(date=now_date)
            elif self.data_type=='合成因子':
                df=self.get_all_connect_factor_data(date=now_date)
            else:
                df=self.get_spot_data(date=now_date)
        else:
            df=df
        if df.shape[0]>0:
            self.stats=True
        else:
            df=pd.DataFrame()
            self.stats=False
        return df
    def get_cacal_factor_base_table(self):
        '''
        计算默认因子
        '''
        print('计算默认因子***********************')
        text=self.text
        is_open=text['是否开启默认因子计算']
        df=self.get_all_factor_data()
        if df.shape[0]>0:
            factor=text['默认因子计算']
            if is_open=='是':
                print('开启计算默认因子***********************')
                factor_name=list(factor.keys())
                if len(factor_name)>0:
                    for name in factor_name:
                        try:
                            print(name,'因子计算完成')
                            func=factor[name]
                            df[name]=eval(func)
                        except Exception as e:
                            print(e,name,'因子计算有问题')
                else:
                    print('没有默认因子需要计算')
            else:
                print('不开启计算默认因子***********************')
        else:
            df=pd.DataFrame()
        return df
    def get_del_qzsh_data(self):
        '''
        剔除强制赎回
        '''
        print('剔除强制赎回')
        text=self.text
        del_select=text['是否剔除强制赎回']
        n=text['满足强制赎回天数']
        df=self.get_cacal_factor_base_table()
        select_list=['强赎登记日','已公告要强赎']
        try:
            if df.shape[0]>0:
                df['强赎']=df['转债提示'].apply(lambda x: '是' if '强赎登记日' in str(x) or '已公告要强赎' in str(x) else '不是')
                df1=df[df['强赎']=='是']
                df2=df[df['强赎']=='不是']
            else:
                df1=pd.DataFrame()
                df2=pd.DataFrame()
        except Exception as e:
            print(e,'剔除强制赎回')
            df1=pd.DataFrame()
            df2=pd.DataFrame()
        self.redeem=df1
        return df2
    def get_n1_n2_daily(self,start_date: str = '2023-12-14') -> int:

        """计算两个日期之间的天数差"""
        end_date=str(datetime.now())[:10]
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return (end - start).days
    def days_excluded_from_market(self):
        '''
        排除上市天数
        '''
        print('排除上市天数')
        text=self.text
        df=self.get_del_qzsh_data()
        try:
            if df.shape[0]>0:
                n=text['排除上市天数']
                df['上市日期']=pd.to_datetime(df['上市日期'],unit='ms')
                df['上市日期']=df['上市日期'].astype(str)
                df['上市天数']=df['上市日期'].apply(lambda x: self.get_n1_n2_daily(str(x)))
                df=df[df['上市天数']>=n]
            else:
                df=df
    
        except Exception as e:
            print(e,'排除上市天数')
            df=df
        return df
    def st_exclusion(self):
        '''
        排除st
        '''
        print('排除st')
        text=self.text
        is_del=text['是否排除ST']
        df=self.days_excluded_from_market()
        try:
            if df.shape[0]>0:
                if is_del=='是':
                    def_list=['ST','st','*ST','*st']
                    df['ST']=df['正股名称'].apply(lambda x: '是' if 'st' in x or 'ST' in x or '*st' in x or '*ST' in x else '不是' )
                    df=df[df['ST']=='不是']
                else:
                    df=df
        except Exception as e:
            print(e,'排除st')
            df=df
        
        return df
    def exclusion_of_market(self):
        '''
        排除市场
        '''
        print("排除市场")
        text=self.text
        exclusion_market_list = []
        del_stock_list=text['排除市场']
        for exclusion_market in del_stock_list:
            if exclusion_market == '沪市主板':
                exclusion_market_list.append(['110','113'])
            elif exclusion_market == '深市主板':
                exclusion_market_list.append(['127','128'])
            elif exclusion_market == '创业板':
                exclusion_market_list.append('123')
            elif exclusion_market == '科创板':
                exclusion_market_list.append('118')
            else:
                pass
        df=self.st_exclusion()
        try:
            if df.shape[0]>0:
                df['market'] = df['转债代码'].apply(lambda x: '排除' if str(x)[:3] in exclusion_market_list  else '不排除')
                df = df[df['market'] == '不排除']
            else:
                df=df
        except Exception as e:
            print(e,'排除市场') 
            df=df
        return df
    def excluded_industry(self):
        '''
        排除行业
        '''
        print('排除行业')
        text=self.text
        del_list=text['排除行业']
        df=self.exclusion_of_market()
        try:
            if df.shape[0]>0:
                industry_list=[]
                data=pd.DataFrame()
                industry_1=df['一级行业'].tolist()
                for i in industry_1:
                    industry_list.append(i)
                industry_2=df['二级行业'].tolist()
                for i in industry_2:
                    industry_list.append(i)
                industry_3=df['三级行业'].tolist()
                for i in industry_3:
                    industry_list.append(i)
                industry_list=list(set(industry_list))
                data['可转债行业']=industry_list
                industry_name=['一级行业','二级行业','三级行业']
                for name in industry_name:
                    df['行业排除']=df[name].apply(lambda x: '是' if x in del_list else '不是')
                    df=df[df['行业排除']=='不是']
            else:
                df=df
        except Exception as e:
            print(e,'排除行业')
            df=df
        
        return df
    def exclusion_of_enterprise(self):
        '''
        排除企业
        '''
        print('排除企业')
        text=self.text
        df=self.excluded_industry()
        return df
    def exclusion_area(self):
        '''
        排除地域
        '''
        print('排除地域')
        text=self.text
        df=self.exclusion_of_enterprise()
        try:
            if df.shape[0]>0:
                del_list=text['排除地域']
                df['排除地域']=df['地域'].apply(lambda x:'是' if str(x) in del_list else '不是')
                df=df[df['排除地域']=='不是']
            else:
                df=df
        except Exception as e :
            print(e,'排除地域')
            df=df
        return df
    def exclusion_of_external_rating(self):
        '''
        排除外部评级
        '''
        print('排除外部评级')
        text=self.text
        df=self.exclusion_area()
        try:
            if df.shape[0]>0:
                del_list=text['排除外部评级']
                df['排除外部评级']=df['主体评级'].apply(lambda x:'是' if str(x) in del_list else '不是')
                df=df[df['排除外部评级']=='不是']
            else:
                df=df
        except Exception as e:
            print(e,'排除外部评级')
        return df
    def tripartite_exclusion(self):
        '''
        排除三方评级
        '''
        print('排除三方评级')
        text=self.text
        df=self.exclusion_of_external_rating()
        try:
            if df.shape[0]>0:
                del_list=text['排除三方评级']
                df['排除三方评级']=df['主体评级'].apply(lambda x:'是' if str(x) in del_list else '不是')
                df=df[df['排除三方评级']=='不是']
            else:
                df=df
        except Exception as e:
            print(e,'排除三方评级')
            df=df
        return df
    def cacal_exclusion_factor(self):
        '''
        计算排除因子
        '''
        print('计算排除因子')
        text=self.text
        df=self.tripartite_exclusion()
        df.to_excel(r'数据.xlsx')
        if df.shape[0]>0:
            factor_list=text['排除因子']
            factor_func_list=text['因子计算符号']
            factor_value_list=text['因子值']
            all_factor_list=df.columns.tolist()
            for factor,func,value in zip(factor_list,factor_func_list,factor_value_list):
                try:
                    if factor in all_factor_list:
                        df[factor]=pd.to_numeric(df[factor])
                        if func=='大于':
                            df=df[df[factor]<=value]
                        elif func=='小于':
                            df=df[df[factor]>=value]
                        elif func=='大于排名%':
                            df=df.sort_values(by=factor,ascending=True)[value:]
                        elif func=='小于排名%':
                            df=df.sort_values(by=factor,ascending=True)[:value]
                        elif func=='空值':
                            df=df
                        else:
                            print('{}未知的计算方式'.format(func))
                       
                    else:
                        print('{}排除因子不在全部的因子表里面全部因子表{}'.format(factor,all_factor_list))
                except Exception as e:
                    print(factor,e,'排除因子计算有问题')
        else:
            df=pd.DataFrame()
        return df
    def cacal_score_factor(self):
        '''
        计算打分因子
        升序从小到大
        降序从大到小
        '''
        print("计算打分因子")
        text=self.text
        df=self.cacal_exclusion_factor()
        if df.shape[0]>0:
            factor_list=text['打分因子']
            factor_cov_list=text['因子相关性']
            factor_weight_list=text['因子权重']
            all_factor_list=df.columns.tolist()
            score_list=[]
            for factor,cov,weight in zip(factor_list,factor_cov_list,factor_weight_list):
                try:
                    if factor in all_factor_list:
                        if cov=='正相关':
                            df[factor]=df[factor]*1
                        elif cov=='负相关':
                            df[factor]=df[factor]*-1
                        else:
                            print('{}未知的相关性'.format(cov))
                        df['{}_得分'.format(factor)]=df[factor].rank(ascending=False)*weight
                        score_list.append('{}_得分'.format(factor))
                    else:
                        print('{}打分因子不在全部的因子表里面全部因子表{}'.format(factor,all_factor_list))
                except Exception as e:
                    print(factor,e,'排除因子打分有问题')
            df['总分']=df[score_list].sum(axis=1).tolist()
            df['排名']=df['总分'].rank( ascending=True)
            df=df.sort_values(by='总分',ascending=True)
        else:
            df=pd.DataFrame()
        return df
    def get_time_rotation(self):
        '''
        轮动方式
        '''
        text=self.text
        now_date=''.join(str(datetime.now())[:10].split('-'))
        now_time=time.localtime()                               
        trader_type=text['轮动方式']                               
        trader_wday=text['每周轮动时间']                               
        moth_trader_time=text['每月轮动时间']
        specific_time=text['特定时间']
        year=now_time.tm_year
        moth=now_time.tm_mon
        wday=now_time.tm_wday
        daily=now_time.tm_mday
        if trader_type=='每天':
            print('轮动方式每天********************************')
            return True
        elif trader_type=='每周':
            if trader_wday==wday:
                return True
            elif trader_wday<wday:
                print('安周轮动 目前星期{} 轮动时间星期{} 目前时间大于轮动时间不轮动'.format(wday+1,trader_wday+1))
                return False
            else:
                print('安周轮动 目前星期{} 轮动时间星期{} 目前时间小于轮动时间不轮动'.format(wday+1,trader_wday+1))
                return False
        elif trader_type=='每月轮动时间':
            stats=''
            for date in moth_trader_time:
                data=''.join(data.split('-'))
                if int(moth_trader_time)==int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间等于轮动时间轮动'.format(now_date,date))
                    stats=True
                    break
                elif int(moth_trader_time)<int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间小于轮动时间轮动'.format(now_date,date))
                    stats=False
                else:
                    print('安月轮动 目前{} 轮动时间{} 目前时间大于轮动时间轮动'.format(now_date,date))
                    stats=False
            return stats
        else:
            #特别时间
            stats=''
            for date in specific_time:
                data=''.join(data.split('-'))
                if int(specific_time)==int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间等于轮动时间轮动'.format(now_date,date))
                    stats=True
                    break
                elif int(specific_time)<int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间小于轮动时间轮动'.format(now_date,date))
                    stats=False
                else:
                    print('安月轮动 目前{} 轮动时间{} 目前时间大于轮动时间轮动'.format(now_date,date))
                    stats=False
            return stats  
    def get_select_result(self):
        '''
        获取选股结果
        '''
        if self.get_time_rotation():
            text=self.text
            select_columns=['转债名称',"转债代码"]
            del_factor=list(set(text['排除因子']))
            score_factor=text['打分因子']
            score_type=text['因子相关性']
            for fcator in del_factor:
                select_columns.append(fcator)
            for fcator in score_factor:
                select_columns.append(fcator)  
            df=self.cacal_score_factor()
            all_columns=df.columns.tolist()
            select_facto=[]
            for columns in select_columns:
                if columns in all_columns:
                    select_facto.append(columns)
            select_facto.append('总分')
            select_facto.append('排名')
            if df.shape[0]>0:
                df=df[select_facto]
                all_columns=df.columns.tolist()
                for factor,cacal_type in zip(score_factor,score_type):
                    if factor in all_columns:
                        if cacal_type=='负相关':
                            df[factor]=df[factor]*-1
                        else:
                            pass
                    else:
                        pass
                df.index=range(0,df.shape[0])
                df=df.drop_duplicates(subset=['转债代码'],keep='last')
            else:
                df=pd.DataFrame()
            stats=self.stats
        else:
            self.stats=False
            df=pd.DataFrame()
        return stats,df,self.redeem
    
if __name__=='__main__':
    '''
    测试
    '''
    with open(r'小果自定义因子选择系统.json',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    table=text['数据表']
    url=text['服务器']
    port=text['端口']
    date=''.join(str(datetime.now())[:10].split('-'))
    data=xms_quant_bond_user_factor_trader(
        data_type=table,
        url=url,
        port=port,
        text=text,
        date=date)
    stats,df,redeem=data.get_select_result()
    print(df)
    print(redeem)
    
    
    