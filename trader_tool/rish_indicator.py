import ffn
import empyrical
import pandas as pd
import numpy as np
import empyrical
import akshare as ak
from finta import TA
import mplfinance as mpf
class rish_indicator:
    '''
    股票风险
    '''
    def __init__(self,df='',factor_df=''):
        '''
        股票风险
        '''
        self.df=df
        self.factor_df=factor_df
    def simple_returns(self,n=100):
        result=empyrical.simple_returns(self.df['close'])
        return result
    #累计回报
    def cum_returns(self,n=100):
        result=empyrical.cum_returns(self.df['close'][-n:].pct_change())
        return result
    #累计最终回报
    def cum_returns_final(self,n=100):
        result=empyrical.cum_returns_final(self.df['close'][-n:].pct_change())
        return result
    #转换回报率，比如转成Can be 'weekly', 'monthly', or 'yearly'.
    def agg_returns(self,n=100):
        result=empyrical.aggregate_returns(self.df['close'][-n:].pct_change(),'weekly')
        return result
    #最大回测
    def max_drawdown(self,n=100):
        result=empyrical.max_drawdown(self.df['close'][-n:].pct_change())
        return result
    #滚动最大回撤
    def roll_max_drawdown(self,n=100):
        #第二个参数为周期
        result=empyrical.roll_max_drawdown(self.df['close'][-n:].pct_change(),window=5)
        return result
    #年回报率
    def anaun_returns(self,n=100):
        result=empyrical.annual_return(self.df['close'][-n:].pct_change())
        return result
    #复合年增长率
    def year_grath_ratio(self,n=100):
        result=empyrical.cagr(self.df['close'][-n:].pct_change())
        return result
    #年波动率
    def anaual_vol(self,n=100):
        result=empyrical.annual_volatility(self.df['close'][-n:].pct_change())
        return result
    #滚动年波动率
    def roll_annual_vol(self,n=100):
        result=empyrical.roll_annual_volatility(self.df['close'][-n:].pct_change(),window=5)
        return result
    #omega比例
    def omega_ratio(self,n=100):
        result=empyrical.omega_ratio(self.df['close'][-n:].pct_change())
        return result
    #夏普比例
    def sharpe_ratio(self,n=100):
        result=empyrical.sharpe_ratio(self.df['close'][-n:].pct_change())
        return result
    #短期比例
    def sortion_ratio(self,n=100):
        result=empyrical.sortino_ratio(self.df['close'][-n:].pct_change())
        return result
    #下行风险
    def downsode_risk(self,n=100):
        result=empyrical.downside_risk(self.df['close'][-n:].pct_change())
        return result
    #超额夏普比率
    def excess_sharpe(self,n=100):
        result=empyrical.excess_sharpe(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算股票a和b
    def alpha_beta(self,n=100):
        #第一个为计算股票，第二个为参考股票
        result=empyrical.alpha_beta(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算滚动的a和b
    def roll_alpha_bate(self,n=100):
        result=empyrical.roll_alpha_beta(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change(),window=5)
        return result
    #计算年华a和b
    def alpha_bate_year(self,n=100):
        result=empyrical.alpha_beta_aligned(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算股票a
    def alpha(self,n=100):
        result=empyrical.alpha(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        print(result,'888888888888')
        return result
    #年华aipha
    def aipha_year(self,n=100):
        result=empyrical.alpha_aligned(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算股票beta
    def beta(self,n=100):
        result=empyrical.beta(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算图片年化b
    def beta_year(self,n=100):
        result=empyrical.beta_aligned(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算滚动b
    def roll_bate(self,n=100):
        result=empyrical.roll_beta(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change(),window=5)
        return result
    #收益率log可决系数
    def log_liner_r(self,n=100):
        result=empyrical.stability_of_timeseries(self.df['close'][-n:].pct_change())
        return result
    #计算股票95%在险价值
    def var_in(self,n=100):
        result=empyrical.tail_ratio(self.df['close'][-n:].pct_change())
        return result
    #计算股票吸引比例
    def capturn_ratio(self,n=100):
        result=empyrical.capture(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #b下降脆弱性
    def b_down_heuristic(self,n=100):
        result=empyrical.beta_fragility_heuristic(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #股票b年化下降脆弱性
    def b_down_heuristic_year(self,n=100):
        result=empyrical.beta_fragility_heuristic_aligned(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算股票在险价值和es
    def var_and_es_values(self,n=100):
        result=empyrical.gpd_risk_estimates(self.df['close'][-n:].pct_change())
        return result
    #计算股票股票年化在险价值和es
    def var_and_es_values_year(self,n=100):
        result=empyrical.gpd_risk_estimates_aligned(self.df['close'][-n:].pct_change())
        return result
    #计算参考回报为正捕获比例
    def up_capturn(self,n=100):
        result=empyrical.up_capture(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算参考回报为正滚动捕获比例
    def roll_up_capturn(self,n=100):
        result=empyrical.roll_up_capture(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change(),window=5)
        return result
    #计算参考回报为负捕获回报率
    def down_capturn(self,n=100):
        result=empyrical.down_capture(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算参考回报为负滚动捕获回报率
    def roll_down_capturn(self,n=100):
        result=empyrical.roll_down_capture(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算a和b在参考为正捕获比例
    def a_and_b_up_capturn(self,n=100):
        result=empyrical.up_alpha_beta(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算a和b在参考为负捕获比例
    def a_and_b_down_capturn(self,n=100):
        result=empyrical.down_alpha_beta(self.df['close'][-n:].pct_change(),self.factor_df['close'][-n:].pct_change())
        return result
    #计算股票条件在险价值
    def condition_var(self,n=100):
        result=empyrical.conditional_value_at_risk(self.df['close'][-n:].pct_change())
        return result
    


