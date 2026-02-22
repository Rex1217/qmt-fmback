import pandas as pd
import json
import requests
import os
class xg_financial_database:
    '''
    小果金融数据库
    '''
    def __init__(self,url='http://120.78.132.143',port=8023,password='123456'):
        '''
        小果金融数据库
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
    def get_all_etf_data(self):
        '''
        获取全部的etf数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_all_etf_data()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_bond_etf_data(self):
        '''
        获取债券的etf数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_bond_etf_data()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_sz_sh_etf(self):
        '''
        获取A股ETF数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_sz_sh_etf()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_wp_etf_data(self):
        '''
        获取外盘ETF数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_wp_etf_data()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_sp_etf_data(self):
        '''
        获取商品ETF数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_sp_etf_data()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hot_spot_investment(self):
        '''
        获取ETF热点投资数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_hot_spot_investment()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hot_spot_investment(self):
        '''
        获取ETF热点投资数据
        '''
        func="""
        from trader_tool.dfcf_etf_data import dfcf_etf_data
        data=dfcf_etf_data()
        df=data.get_hot_spot_investment()
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_limit_up_pool(self,date='20240126'):
        '''
        获取涨停板数据
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_limit_up_pool(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_limit_up(self,date=''):
        '''
        冲刺涨停
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_limit_up(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_continuous_limit_pool(self,date='20230925'):
        '''
        连扳
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_continuous_limit_pool(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_open_limit_pool(self,date='20230925'):
        '''
        炸板池
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_open_limit_pool(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_lower_limit_pool(self,date='20230101'):
        '''
        跌停
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_lower_limit_pool(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_block_top_pool(self,date='20230101'):
        '''
        最强风口
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_block_top_pool(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_analysis_block_top_pool(self,date='20240101'):
        '''
        解析最强风口
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_analysis_block_top_pool(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_continuous_limit_up(self,date='20240101'):
        '''
        连扳天梯
        '''
        func="""
        from trader_tool.ths_limitup_data import ths_limitup_data
        data=ths_limitup_data()
        df=data.read_func_data(func="self.get_stock_continuous_limit_up(date={})")
        print(df)
        """.format(date)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_hot_stock_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_hot_stock_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_concept_rot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_stock_concept_rot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_stock_industry_rot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_stock_industry_rot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_etf_hot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_etf_hot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_cov_bond_rot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_cov_bond_rot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_HK_stock_rot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_HK_stock_rot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_US_stock_rot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_US_stock_rot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_futurn_hot_rank(self):
        func="""
        from trader_tool.ths_rq import ths_rq
        models=ths_rq()
        df=models.get_futurn_hot_rank()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def fund_lof_spot_em(self):
        '''
        LOF 实时行情
        '''
        func="""
        from trader_tool.lof_fund_data import lof_fund_data
        models=lof_fund_data()
        df=models.fund_lof_spot_em()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def fund_lof_hist_em(self,
        symbol: str = "166009",
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
        adjust: str = "",):
        '''
        获取lof历史数据
        '''
        func="""
        from trader_tool.lof_fund_data import lof_fund_data
        models=lof_fund_data()
        df=models.fund_lof_hist_em(symbol='{}',
        period='{}',
        start_date='{}',
        end_date='{}',
        adjust='{}')
        print(df)
        """.format(symbol,period,start_date,end_date,adjust)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def fund_lof_hist_min_em(self,
        symbol: str = "166009",
        start_date: str = "1979-09-01 09:32:00",
        end_date: str = "2222-01-01 09:32:00",
        period: str = "5",
        adjust: str = ""):
        '''
        lof分时行情
        '''
        func="""
        from trader_tool.lof_fund_data import lof_fund_data
        models=lof_fund_data()
        df=models.fund_lof_hist_min_em(symbol='{}',
        period='{}',
        start_date='{}',
        end_date='{}',
        adjust='{}')
        print(df)
        """.format(symbol,period,start_date,end_date,adjust)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_lof_fund_info_data(self,stock='501225'):
        '''
        获取ETF基本信息
        '''
        func="""
        from trader_tool.lof_fund_data import lof_fund_data
        models=lof_fund_data()
        df=models.get_lof_fund_info_data(stock='{}')
        """.format(stock)+"""
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
    def get_all_lof_fund_info_data(self):
        '''
        获取全部lof基金数据
        '''
        func="""
        from trader_tool.lof_fund_data import lof_fund_data
        models=lof_fund_data()
        df=models.get_all_lof_fund_info_data()
        print(df)
        df.to_csv(r'{}\数据\{}数据.csv')
        """
        info,df=self.get_user_def_data(func=func)
        return info,df
if __name__=='__main__':
    data=xg_financial_database(password='123456')
    df=data.get_lof_fund_info_data(stock='501025')
    print(df)