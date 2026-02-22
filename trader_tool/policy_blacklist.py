from trader_tool.dfcf_etf_data import dfcf_etf_data
from trader_tool import stock_fund_em
from trader_tool import jsl_data
import pandas as pd
class policy_blacklist:
    def __init__(self):
        '''
        策略黑名单
        '''
        self.dfcf_etf_data=dfcf_etf_data()
    def get_stock_policy_blacklist(self):
        '''
        股票黑名单
        '''
        data=pd.DataFrame()
        bond=jsl_data.get_all_cov_bond_data()
        bond=bond[['转债代码','转债名称']]
        bond.columns=['证券代码','证券名称']
        bond['证券代码']=bond['证券代码'].apply(lambda x:str(x).split('.')[0])
        etf=self.dfcf_etf_data.get_all_etf_data_1()
        etf=etf[['证券代码','基金代码']]
        etf.columns=['证券代码','证券名称']
        etf['证券代码']=etf['证券代码'].apply(lambda x:str(x).split('.')[0])
        data=pd.concat([data,bond],ignore_index=True)
        data=pd.concat([data,etf],ignore_index=True)
        data['证券代码']=data['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x) )
        return data
    def get_etf_policy_blacklist(self):
        '''
        etf黑名单
        '''
        data=pd.DataFrame()
        bond=jsl_data.get_all_cov_bond_data()
        bond=bond[['转债代码','转债名称']]
        bond.columns=['证券代码','证券名称']
        bond['证券代码']=bond['证券代码'].apply(lambda x:str(x).split('.')[0])
        stock=stock_fund_em.stock_individual_fund_flow_rank()
        stock=stock[['代码','名称']]
        stock.columns=['证券代码','证券名称']
        data=pd.concat([data,bond],ignore_index=True)
        data=pd.concat([data,stock],ignore_index=True)
        return data
    def get_bond_policy_blacklist(self):
        '''
        获取可转债黑名单
        '''
        data=pd.DataFrame()
        stock=stock_fund_em.stock_individual_fund_flow_rank()
        stock=stock[['代码','名称']]
        stock.columns=['证券代码','证券名称']
        etf=self.dfcf_etf_data.get_all_etf_data_1()
        etf=etf[['证券代码','基金代码']]
        etf.columns=['证券代码','证券名称']
        etf['证券代码']=etf['证券代码'].apply(lambda x:str(x).split('.')[0])
        data=pd.concat([data,stock],ignore_index=True)
        data=pd.concat([data,etf])
        return data
        


