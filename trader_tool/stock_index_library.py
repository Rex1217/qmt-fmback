from trader_tool import tdx_indicator
from finta import TA
from trader_tool.rish_indicator import rish_indicator
from trader_tool.unification_data import unification_data
import empyrical
from tqdm import tqdm
import pandas as pd
from trader_tool.stock_fund_em import stock_fund_em
import numpy as np
class stock_index_library:
    '''
    因子指标库
    '''
    def __init__(self,df='',index_df='',all=True):
        '''
        股票指标库
        df股票数据
        index_df参考数据的
        all返回全部历史的还是特定日期
        date 特定日期
        '''
        self.df=df
        self.index_df=index_df
        self.all=all
        self.rish_indicator=rish_indicator(df=self.df,factor_df=self.index_df)
        self.stock_fund_em=stock_fund_em()
        self.func_name_list=['SMA', 'SMM', 'SSMA', 'EMA', 'DEMA', 'TEMA', 
                             'TRIMA', 'TRIX', 'LWMA', 'VAMA', 'VIDYA', 
                            'ER', 'KAMA', 'ZLEMA', 'WMA', 'HMA', 'EVWMA',
                            'VWAP', 'SMMA', 'ALMA', 'MAMA', 'FRAMA', 'MACD',
                            'PPO', 'VW_MACD', 'EV_MACD', 'MOM', 'ROC', 'VBM',
                            'RSI', 'IFT_RSI', 'SWI', 'DYMI', 'TR', 'ATR', 'SAR',
                            'PSAR', 'BBANDS', 'MOBO', 'BBWIDTH', 'PERCENT_B',
                            'KC', 'DO', 'DMI', 'ADX', 'PIVOT', 'PIVOT_FIB',
                            'STOCH', 'STOCHD', 'STOCHRSI', 'WILLIAMS', 'UO', 
                            'AO', 'MI', 'BOP', 'VORTEX', 'KST', 'TSI', 'TP', 'ADL', 
                            'CHAIKIN', 'MFI', 'OBV', 'WOBV', 'VZO', 'PZO', 'EFI', 'CFI', 
                            'EBBP', 'EMV', 'CCI', 'COPP', 'BASP', 'BASPN', 'CMO', 
                            'CHANDELIER', 'QSTICK', 'TMF', 'WTO', 'FISH', 'ICHIMOKU', 
                            'APZ', 'SQZMI', 'VPT', 'FVE', 'VFI', 'MSD', 'STC', 'EVSTC', 
                            'WILLIAMS_FRACTAL']
    def SMA(self):
        '''
        Simple moving average - rolling mean in pandas lingo. Also known as 'MA'.
        The simple moving average (SMA) is the most basic of the moving averages used for trading.
        '''
        name='SMA'
        result=TA.SMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def SMM(self):
        '''
        Simple moving median, an alternative to moving average. SMA, when used to estimate the underlying trend in a time series,
        is susceptible to rare events such as rapid shocks or other anomalies. A more robust estimate of the trend is the simple moving median over n time periods.
        '''
        name='SMA'
        result=TA.SMM(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def SSMA(self):
        '''
        Smoothed simple moving average.
        '''
        name='SSMA'
        result=TA.SSMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EMA(self):
        '''
        Exponential Weighted Moving Average - Like all moving average indicators, they are much better suited for trending markets.
        When the market is in a strong and sustained uptrend, the EMA indicator line will also show an uptrend and vice-versa for a down trend.
        EMAs are commonly used in conjunction with other indicators to confirm significant market moves and to gauge their validity.
        '''
        name='EMA'
        result=TA.EMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def DEMA(self):
        '''
        Double Exponential Moving Average - attempts to remove the inherent lag associated to Moving Averages
         by placing more weight on recent values. The name suggests this is achieved by applying a double exponential
        smoothing which is not the case. The name double comes from the fact that the value of an EMA (Exponential Moving Average) is doubled.
        To keep it in line with the actual data and to remove the lag the value 'EMA of EMA' is subtracted from the previously doubled EMA.
        Because EMA(EMA) is used in the calculation, DEMA needs 2 * period -1 samples to start producing values in contrast to the period
        samples needed by a regular EMA
        '''
        name='DEMA'
        result=TA.DEMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TEMA(self):
        '''
        Triple exponential moving average - attempts to remove the inherent lag associated to Moving Averages by placing more weight on recent values.
        The name suggests this is achieved by applying a triple exponential smoothing which is not the case. The name triple comes from the fact that the
        value of an EMA (Exponential Moving Average) is triple.
        To keep it in line with the actual data and to remove the lag the value 'EMA of EMA' is subtracted 3 times from the previously tripled EMA.
        Finally 'EMA of EMA of EMA' is added.
        Because EMA(EMA(EMA)) is used in the calculation, TEMA needs 3 * period - 2 samples to start producing values in contrast to the period samples
        needed by a regular EMA.
        '''
        name='TEMA'
        result=TA.TEMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TRIMA(self):
        '''
        Triple exponential moving average - attempts to remove the inherent lag associated to Moving Averages by placing more weight on recent values.
        The name suggests this is achieved by applying a triple exponential smoothing which is not the case. The name triple comes from the fact that the
        value of an EMA (Exponential Moving Average) is triple.
        To keep it in line with the actual data and to remove the lag the value 'EMA of EMA' is subtracted 3 times from the previously tripled EMA.
        Finally 'EMA of EMA of EMA' is added.
        Because EMA(EMA(EMA)) is used in the calculation, TEMA needs 3 * period - 2 samples to start producing values in contrast to the period samples
        needed by a regular EMA.
        '''
        name='TRIMA'
        result=TA.TEMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TRIX(self):
        '''
        The TRIX indicator calculates the rate of change of a triple exponential moving average.
        The values oscillate around zero. Buy/sell signals are generated when the TRIX crosses above/below zero.
        A (typically) 9 period exponential moving average of the TRIX can be used as a signal line.
        A buy/sell signals are generated when the TRIX crosses above/below the signal line and is also above/below zero.

        The TRIX was developed by Jack K. Hutson, publisher of Technical Analysis of Stocks & Commodities magazine,
        and was introduced in Volume 1, Number 5 of that magazine.
        '''
        name='TRIX'
        result=TA.TRIX(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VAMA(self):
        '''
        Volume Adjusted Moving Average
        '''
        name='VAMA'
        result=TA.VAMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VIDYA(self):
        '''
        Vidya (variable index dynamic average) indicator is a modification of the traditional Exponential Moving Average (EMA) indicator.
        The main difference between EMA and Vidya is in the way the smoothing factor F is calculated.
        In EMA the smoothing factor is a constant value F=2/(period+1);
        in Vidya the smoothing factor is variable and depends on bar-to-bar price movements.
        '''
        name='VIDYA'
        result=TA.VIDYA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ER(self):
        '''
        The Kaufman Efficiency indicator is an oscillator indicator that oscillates between +100 and -100, where zero is the center point.
         +100 is upward forex trending market and -100 is downwards trending markets
        '''
        name='ER'
        result=TA.ER(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def KAMA(self):
        '''
        Developed by Perry Kaufman, Kaufman's Adaptive Moving Average (KAMA) is a moving average designed to account for market noise or volatility.
        Its main advantage is that it takes into consideration not just the direction, but the market volatility as well
        '''
        name='KAMA'
        result=TA.KAMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ZLEMA(self):
        '''
        ZLEMA is an abbreviation of Zero Lag Exponential Moving Average. It was developed by John Ehlers and Rick Way.
        ZLEMA is a kind of Exponential moving average but its main idea is to eliminate the lag arising from the very nature of the moving averages
        and other trend following indicators. As it follows price closer, it also provides better price averaging and responds better to price swings
        '''
        name='ZLEMA'
        result=TA.ZLEMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def WMA(self):
        '''
        WMA stands for weighted moving average. It helps to smooth the price curve for better trend identification.
        It places even greater importance on recent data than the EMA does
        '''
        name='WMA'
        result=TA.WMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1] 
    def HMA(self):
        '''
        HMA indicator is a common abbreviation of Hull Moving Average.
        The average was developed by Allan Hull and is used mainly to identify the current market trend.
        Unlike SMA (simple moving average) the curve of Hull moving average is considerably smoother.
        Moreover, because its aim is to minimize the lag between HMA and price it does follow the price activity much closer.
        It is used especially for middle-term and long-term trading.
        '''
        name='HMA'
        result=TA.HMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EVWMA(self):
        '''
        The eVWMA can be looked at as an approximation to the
        average price paid per share in the last n periods.
        '''
        name='EVWMA'
        result=TA.EVWMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VWAP(self):
        '''
        The volume weighted average price (VWAP) is a trading benchmark used especially in pension plans.
        VWAP is calculated by adding up the dollars traded for every transaction (price multiplied by number of shares traded) and then dividing
        by the total shares traded for the day.
        '''
        name='VWAP'
        result=TA.VWAP(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def SMMA(self):
        '''
        The SMMA (Smoothed Moving Average) gives recent prices an equal weighting to historic prices
        '''
        name='SMMA'
        result=TA.SMMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ALMA(self):
        '''
        dataWindow = _.last(data, period)
        size = _.size(dataWindow)
        m = offset * (size - 1)
        s = size / sigma
        sum = 0
        norm = 0
        for i in [size-1..0] by -1
        coeff = Math.exp(-1 * (i - m) * (i - m) / 2 * s * s)
        sum = sum + dataWindow[i] * coeff
        norm = norm + coeff
        return sum / norm
        '''
        name='ALMA'
        result=TA.ALMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MAMA(self):
        '''
        MESA Adaptive Moving Average
        '''
        name='MAMA'
        result=TA.MAMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def FRAMA(self):
        '''
        Fractal Adaptive Moving Average
        Source: http://www.stockspotter.com/Files/frama.pdf
        Adopted from: https://www.quantopian.com/posts/frama-fractal-adaptive-moving-average-in-python
        '''
        name='FRAMA'
        result=TA.FRAMA(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MACD(self):
        '''
        MACD, MACD Signal and MACD difference.
        The MACD Line oscillates above and below the zero line, which is also known as the centerline.
        These crossovers signal that the 12-day EMA has crossed the 26-day EMA. The direction, of course, depends on the direction of the moving average cross.
        Positive MACD indicates that the 12-day EMA is above the 26-day EMA. Positive values increase as the shorter EMA diverges further from the longer EMA.
        This means upside momentum is increasing. Negative MACD values indicates that the 12-day EMA is below the 26-day EMA.
        Negative values increase as the shorter EMA diverges further below the longer EMA. This means downside momentum is increasing.

        Signal line crossovers are the most common MACD signals. The signal line is a 9-day EMA of the MACD Line.
        As a moving average of the indicator, it trails the MACD and makes it easier to spot MACD turns.
        A bullish crossover occurs when the MACD turns up and crosses above the signal line.
        A bearish crossover occurs when the MACD turns down and crosses below the signal line
        '''
        name='MACD'
        result=TA.MACD(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def PPO(self):
        '''
        Percentage Price Oscillator
        PPO, PPO Signal and PPO difference.
        As with MACD, the PPO reflects the convergence and divergence of two moving averages.
        While MACD measures the absolute difference between two moving averages, PPO makes this a relative value by dividing the difference by the slower moving average
        '''
        name='PPO'
        result=TA.PPO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VW_MACD(self):
        '''
        Volume-Weighted MACD" is an indicator that shows how a volume-weighted moving average can be used to calculate moving average convergence/divergence (MACD).
        This technique was first used by Buff Dormeier, CMT, and has been written about since at least 2002
        '''
        name='VW_MACD'
        result=TA.VW_MACD(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EV_MACD(self):
        '''
        Elastic Volume Weighted MACD is a variation of standard MACD,
        calculated using two EVWMA's.
        '''
        name='EV_MACD'
        result=TA.EV_MACD(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MOM(self):
        '''
        Market momentum is measured by continually taking price differences for a fixed time interval.
        To construct a 10-day momentum line, simply subtract the closing price 10 days ago from the last closing price.
        This positive or negative value is then plotted around a zero line
        '''
        name='MOM'
        result=TA.MOM(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VBM(self):
        '''
        The Volatility-Based-Momentum (VBM) indicator, The calculation for a volatility based momentum (VBM)
        indicator is very similar to ROC, but divides by the security’s historical volatility instead.
        The average true range indicator (ATR) is used to compute historical volatility.
        VBM(n,v) = (Close — Close n periods ago) / ATR(v periods)
        '''
        name='VBM'
        result=TA.VBM(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def RSI(self):
        '''
        Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
        RSI oscillates between zero and 100. Traditionally, and according to Wilder, RSI is considered overbought when above 70 and oversold when below 30.
        Signals can also be generated by looking for divergences, failure swings and centerline crossovers.
        RSI can also be used to identify the general trend
        '''
        name='RSI'
        result=TA.RSI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def IFT_RSI(self):
        '''
        Modified Inverse Fisher Transform applied on RSI.
        Suggested method to use any IFT indicator is to buy when the indicator crosses over –0.5 or crosses over +0.5
        if it has not previously crossed over –0.5 and to sell short when the indicators crosses under +0.5 or crosses under –0.5
        if it has not previously crossed under +0.5
        '''
        name='IFT_RSI'
        result=TA.IFT_RSI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def DYMI(self):
        '''
        The Dynamic Momentum Index is a variable term RSI. The RSI term varies from 3 to 30. The variable
        time period makes the RSI more responsive to short-term moves. The more volatile the price is,
        the shorter the time period is. It is interpreted in the same way as the RSI, but provides signals earlier.
        Readings below 30 are considered oversold, and levels over 70 are considered overbought. The indicator
        oscillates between 0 and 100.
        https://www.investopedia.com/terms/d/dynamicmomentumindex.asp
        '''
        name='DYMI'
        result=TA.DYMI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TR(self):
        '''
        True Range is the maximum of three price ranges.
        Most recent period's high minus the most recent period's low.
        Absolute value of the most recent period's high minus the previous close.
        Absolute value of the most recent period's low minus the previous close
        '''
        name='TR'
        result=TA.TR(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ATR(self):
        '''
        Average True Range is moving average of True Range
        '''
        name='ATR'
        result=TA.ATR(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def SAR(self):
        '''
        SAR stands for “stop and reverse,” which is the actual indicator used in the system.
        SAR trails price as the trend extends over time. The indicator is below prices when prices are rising and above prices when prices are falling.
        In this regard, the indicator stops and reverses when the price trend reverses and breaks above or below the indicator
        '''
        name='SAR'
        result=TA.SAR(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def PSAR(self):
        '''
        The parabolic SAR indicator, developed by J. Wells Wilder, is used by traders to determine trend direction and potential reversals in price.
        The indicator uses a trailing stop and reverse method called "SAR," or stop and reverse, to identify suitable exit and entry points.
        Traders also refer to the indicator as the parabolic stop and reverse, parabolic SAR, or PSAR.
        https://www.investopedia.com/terms/p/parabolicindicator.asp
        https://virtualizedfrog.wordpress.com/2014/12/09/parabolic-sar-implementation-in-python/
        '''
        name='PSAR'
        result=TA.PSAR(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def BBANDS(self):
        '''
        Developed by John Bollinger, Bollinger Bands® are volatility bands placed above and below a moving average.
         Volatility is based on the standard deviation, which changes as volatility increases and decreases.
         The bands automatically widen when volatility increases and narrow when volatility decreases.

         This method allows input of some other form of moving average like EMA or KAMA around which BBAND will be formed.
         Pass desired moving average as <MA> argument. For example BBANDS(MA=TA.KAMA(20))
        '''
        name='BBANDS'
        result=TA.BBANDS(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MOBO(self):
        '''
        "MOBO bands are based on a zone of 0.80 standard deviation with a 10 period look-back"
        If the price breaks out of the MOBO band it can signify a trend move or price spike
        Contains 42% of price movements(noise) within bands
        '''
        name='MOBO'
        result=TA.MOBO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def PERCENT_B(self):
        '''
        %b (pronounced 'percent b') is derived from the formula for Stochastics and shows where price is in relation to the bands.
        %b equals 1 at the upper band and 0 at the lower band.
        '''
        name='PERCENT_B'
        result=TA.PERCENT_B(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]

    def KC(self):
        '''
        Keltner Channels [KC] are volatility-based envelopes set above and below an exponential moving average.
        This indicator is similar to Bollinger Bands, which use the standard deviation to set the bands.
        Instead of using the standard deviation, Keltner Channels use the Average True Range (ATR) to set channel distance.
        The channels are typically set two Average True Range values above and below the 20-day EMA.
        The exponential moving average dictates direction and the Average True Range sets channel width.
        Keltner Channels are a trend following indicator used to identify reversals with channel breakouts and channel direction.
        Channels can also be used to identify overbought and oversold levels when the trend is flat
        '''
        name='KC'
        result=TA.KC(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def DO(self):
        '''
        Donchian Channel, a moving average indicator developed by Richard Donchian.
        It plots the highest high and lowest low over the last period time intervals
        '''
        name='DO'
        result=TA.DO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def DMI(self):
        '''
        The directional movement indicator (also known as the directional movement index - DMI) is a valuable tool
         for assessing price direction and strength. This indicator was created in 1978 by J. Welles Wilder, who also created the popular
         relative strength index. DMI tells you when to be long or short.
         It is especially useful for trend trading strategies because it differentiates between strong and weak trends,
         allowing the trader to enter only the strongest trends.
        '''
        name='DMI'
        result=TA.DMI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ADX(self):
        '''
        The A.D.X. is 100 * smoothed moving average of absolute value (DMI +/-) divided by (DMI+ + DMI-). ADX does not indicate trend direction or momentum,
        only trend strength. Generally, A.D.X. readings below 20 indicate trend weakness,
        and readings above 40 indicate trend strength. An extremely strong trend is indicated by readings above 50
        '''
        name='ADX'
        result=TA.ADX(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def PIVOT(self):
        '''
        Pivot Points are significant support and resistance levels that can be used to determine potential trades.
        The pivot points come as a technical analysis indicator calculated using a financial instrument’s high, low, and close value.
        The pivot point’s parameters are usually taken from the previous day’s trading range.
        This means you’ll have to use the previous day’s range for today’s pivot points.
        Or, last week’s range if you want to calculate weekly pivot points or, last month’s range for monthly pivot points and so on
        '''
        name='PIVOT'
        result=TA.PIVOT(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def PIVOT_FIB(self):
        '''
        Fibonacci pivot point levels are determined by first calculating the classic pivot point,
        then multiply the previous day’s range with its corresponding Fibonacci level.
        Most traders use the 38.2%, 61.8% and 100% retracements in their calculations.
        '''
        name='PIVOT_FIB'
        result=TA.PIVOT_FIB(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def STOCH(self):
        '''
        Stochastic oscillator %K
         The stochastic oscillator is a momentum indicator comparing the closing price of a security
         to the range of its prices over a certain period of time.
         The sensitivity of the oscillator to market movements is reducible by adjusting that time
         period or by taking a moving average of the result.
        '''
        name='STOCH'
        result=TA.STOCH(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def STOCHD(self):
        '''
        Stochastic oscillator %D
        STOCH%D is a 3 period simple moving average of %K.
        '''
        name='STOCHD'
        result=TA.STOCHD(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def STOCHRSI(self):
        '''
        StochRSI is an oscillator that measures the level of RSI relative to its high-low range over a set time period.
        StochRSI applies the Stochastics formula to RSI values, instead of price values. This makes it an indicator of an indicator.
        The result is an oscillator that fluctuates between 0 and 1
        '''
        name='STOCHRSI'
        result=TA.STOCHRSI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def WILLIAMS(self):
        '''
        Williams %R, or just %R, is a technical analysis oscillator showing the current closing price in relation to the high and low
         of the past N days (for a given N). It was developed by a publisher and promoter of trading materials, Larry Williams.
         Its purpose is to tell whether a stock or commodity market is trading near the high or the low, or somewhere in between,
         of its recent trading range.
         The oscillator is on a negative scale, from −100 (lowest) up to 0 (highest)
        '''
        name='WILLIAMS'
        result=TA.WILLIAMS(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def UO(self):
        '''
        Ultimate Oscillator is a momentum oscillator designed to capture momentum across three different time frames.
        The multiple time frame objective seeks to avoid the pitfalls of other oscillators.
        Many momentum oscillators surge at the beginning of a strong advance and then form bearish divergence as the advance continues.
        This is because they are stuck with one time frame. The Ultimate Oscillator attempts to correct this fault by incorporating longer
        time frames into the basic formula.
        '''
        name='UO'
        result=TA.UO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]  
    def AO(self):
        '''
        Awesome Oscillator is an indicator used to measure market momentum. AO calculates the difference of a 34 Period and 5 Period Simple Moving Averages.
        The Simple Moving Averages that are used are not calculated using closing price but rather each bar's midpoints.
        AO is generally used to affirm trends or to anticipate possible reversals. 
        '''
        name='AO'
        result=TA.AO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MI(self):
        '''
        Developed by Donald Dorsey, the Mass Index uses the high-low range to identify trend reversals based on range expansions.
        In this sense, the Mass Index is a volatility indicator that does not have a directional bias.
        Instead, the Mass Index identifies range bulges that can foreshadow a reversal of the current trend
        '''
        name='MI'
        result=TA.MI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]

    def BOP(self):
        '''
        Balance Of Power indicator
        '''
        name='BOP'
        result=TA.BOP(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VORTEX(self):
        '''
        The Vortex indicator plots two oscillating lines, one to identify positive trend movement and the other
         to identify negative price movement.
         Indicator construction revolves around the highs and lows of the last two days or periods.
         The distance from the current high to the prior low designates positive trend movement while the
         distance between the current low and the prior high designates negative trend movement.
         Strongly positive or negative trend movements will show a longer length between the two numbers while
         weaker positive or negative trend movement will show a shorter length
        '''
        name='VORTEX'
        result=TA.VORTEX(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def KST(self):
        '''
        Know Sure Thing (KST) is a momentum oscillator based on the smoothed rate-of-change for four different time frames.
        KST measures price momentum for four different price cycles. It can be used just like any momentum oscillator.
        Chartists can look for divergences, overbought/oversold readings, signal line crossovers and centerline crossovers
        '''
        name='KST'
        result=TA.KST(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TSI(self):
        '''
        True Strength Index (TSI) is a momentum oscillator based on a double smoothing of price changes.
        '''
        name='KST'
        result=TA.KST(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    
    def TSI(self):
        '''
        True Strength Index (TSI) is a momentum oscillator based on a double smoothing of price changes
        '''
        name='TSI'
        result=TA.TSI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ADL(self):
        '''
        The accumulation/distribution line was created by Marc Chaikin to determine the flow of money into or out of a security.
        It should not be confused with the advance/decline line. While their initials might be the same, these are entirely different indicators,
        and their uses are different as well. Whereas the advance/decline line can provide insight into market movements,
        the accumulation/distribution line is of use to traders looking to measure buy/sell pressure on a security or confirm the strength of a trend.
        '''
        name='ADL'
        result=TA.ADL(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def CHAIKIN(self):
        '''
        Chaikin Oscillator, named after its creator, Marc Chaikin, the Chaikin oscillator is an oscillator that measures the accumulation/distribution
         line of the moving average convergence divergence (MACD). The Chaikin oscillator is calculated by subtracting a 10-day exponential moving average (EMA)
         of the accumulation/distribution line from a three-day EMA of the accumulation/distribution line, and highlights the momentum implied by the
         accumulation/distribution line.
        '''
        name='CHAIKIN'
        result=TA.CHAIKIN(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MFI(self):
        '''
        The money flow index (MFI) is a momentum indicator that measures
        the inflow and outflow of money into a security over a specific period of time.
        MFI can be understood as RSI adjusted for volume.
        The money flow indicator is one of the more reliable indicators of overbought and oversold conditions, perhaps partly because
        it uses the higher readings of 80 and 20 as compared to the RSI's overbought/oversold readings of 70 and 30
        '''
        name='MFI'
        result=TA.MFI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def OBV(self):
        '''
        On Balance Volume (OBV) measures buying and selling pressure as a cumulative indicator that adds volume on up days and subtracts volume on down days.
        OBV was developed by Joe Granville and introduced in his 1963 book, Granville's New Key to Stock Market Profits.
        It was one of the first indicators to measure positive and negative volume flow.
        Chartists can look for divergences between OBV and price to predict price movements or use OBV to confirm price trends.

        source: https://en.wikipedia.org/wiki/On-balance_volume#The_formula
        '''
        name='OBV'
        result=TA.OBV(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def WOBV(self):
        '''
         Weighted OBV
        Can also be seen as an OBV indicator that takes the price differences into account.
        In a regular OBV, a high volume bar can make a huge difference,
        even if the price went up only 0.01, and it it goes down 0.01
        instead, that huge volume makes the OBV go down, even though
        hardly anything really happened.
        '''
        name='WOBV'
        result=TA.WOBV(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VZO(self):
        '''
        VZO uses price, previous price and moving averages to compute its oscillating value.
        It is a leading indicator that calculates buy and sell signals based on oversold / overbought conditions.
        Oscillations between the 5% and 40% levels mark a bullish trend zone, while oscillations between -40% and 5% mark a bearish trend zone.
        Meanwhile, readings above 40% signal an overbought condition, while readings above 60% signal an extremely overbought condition.
        Alternatively, readings below -40% indicate an oversold condition, which becomes extremely oversold below -60%.
        '''
        name='VZO'
        result=TA.VZO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def PZO(self):
        '''
        The formula for PZO depends on only one condition: if today's closing price is higher than yesterday's closing price,
        then the closing price will have a positive value (bullish); otherwise it will have a negative value (bearish).
        source: http://traders.com/Documentation/FEEDbk_docs/2011/06/Khalil.html
        '''
        name='PZO'
        result=TA.OBV(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EFI(self):
        '''
        Elder's Force Index is an indicator that uses price and volume to assess the power
         behind a move or identify possible turning points.
        '''
        name='EFI'
        result=TA.OBV(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def CFI(self):
        '''
        Cummulative Force Index.
        Adopted from  Elder's Force Index.
        '''
        name='CFI'
        result=TA.CFI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EBBP(self):
        '''
        Bull power and bear power by Dr. Alexander Elder show where today’s high and low lie relative to the a 13-day EMA
        '''
        name='EBBP'
        result=TA.EBBP(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EMV(self):
        '''
        Ease of Movement (EMV) is a volume-based oscillator that fluctuates above and below the zero line.
        As its name implies, it is designed to measure the 'ease' of price movement.
        prices are advancing with relative ease when the oscillator is in positive territory.
        Conversely, prices are declining with relative ease when the oscillator is in negative territory.
        '''
        name='EMV'
        result=TA.EMV(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def CCI(self):
        '''
        Commodity Channel Index (CCI) is a versatile indicator that can be used to identify a new trend or warn of extreme conditions.
        CCI measures the current price level relative to an average price level over a given period of time.
        The CCI typically oscillates above and below a zero line. Normal oscillations will occur within the range of +100 and −100.
        Readings above +100 imply an overbought condition, while readings below −100 imply an oversold condition.
        As with other overbought/oversold indicators, this means that there is a large probability that the price will correct to more representative levels
        '''
        name='CCI'
        result=TA.CCI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def COPP(self):
        '''
        The Coppock Curve is a momentum indicator, 
        it signals buying opportunities when the indicator moved from 
        negative territory to positive territory
        '''
        name='COPP'
        result=TA.COPP(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def BASP(self):
        '''
        BASP indicator serves to identify buying and selling pressure
        '''
        name='BASP'
        result=TA.BASP(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def BASPN(self):
        '''
        Normalized BASP indicator
        '''
        name='BASPN'
        result=TA.BASPN(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def CMO(self):
        '''
        Chande Momentum Oscillator (CMO) - technical momentum indicator invented by the technical analyst Tushar Chande.
        It is created by calculating the difference between the sum of all recent gains and the sum of all recent losses and then
        dividing the result by the sum of all price movement over the period.
        This oscillator is similar to other momentum indicators such as the Relative Strength Index and the Stochastic Oscillator
        because it is range bounded (+100 and -100)
        '''
        name='CMO'
        result=TA.CMO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def CHANDELIER(self):
        '''
        Chandelier Exit sets a trailing stop-loss based on the Average True Range (ATR).

        The indicator is designed to keep traders in a trend and prevent an early exit as long as the trend extends.

        Typically, the Chandelier Exit will be above prices during a downtrend and below prices during an uptrend
        '''
        name='CHANDELIER'
        result=TA.CHANDELIER(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def QSTICK(self):
        '''
        QStick indicator shows the dominance of black (down) or white (up) candlesticks, which are red and green in Chart,
        as represented by the average open to close change for each of past N days
        '''
        name='QSTICK'
        result=TA.QSTICK(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TMF(self):
        '''
        Indicator by Colin Twiggs which improves upon CMF.
        source: https://user42.tuxfamily.org/chart/manual/Twiggs-Money-Flow.html
        '''
        name='TMF'
        result=TA.TMF(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def WTO(self):
        '''
        Wave Trend Oscillator
        source: http://www.fxcoaching.com/WaveTrend/
        '''
        name='WTO'
        result=TA.WTO(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def FISH(self):
        '''
        Fisher Transform was presented by John Ehlers.
         It assumes that price distributions behave like square waves
        '''
        name='FISH'
        result=TA.FISH(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ICHIMOKU(self):
        '''
        The Ichimoku Cloud, also known as Ichimoku Kinko Hyo, is a versatile indicator that defines support and resistance,
        identifies trend direction, gauges momentum and provides trading signals.

        Ichimoku Kinko Hyo translates into “one look equilibrium chart”.
        '''
        name='ICHIMOKU'
        result=TA.ICHIMOKU(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def APZ(self):
        '''
        The adaptive price zone (APZ) is a technical indicator developed by Lee Leibfarth.

        The APZ is a volatility based indicator that appears as a set of bands placed over a price chart.

        Especially useful in non-trending, choppy markets,

        the APZ was created to help traders find potential turning points in the markets.
        '''
        name='APZ'
        result=TA.APZ(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def SQZMI(self):
        '''
        Squeeze Momentum Indicator

        The Squeeze indicator attempts to identify periods of consolidation in a market.
        In general the market is either in a period of quiet consolidation or vertical price discovery.
        By identifying these calm periods, we have a better opportunity of getting into trades with the potential for larger moves.
        Once a market enters into a “squeeze”, we watch the overall market momentum to help forecast the market direction and await a release of market energy.
        '''
        name='SQZMI'
        result=TA.SQZMI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VPT(self):
        '''
        Volume Price Trend
        The Volume Price Trend uses the difference of price and previous price with volume and feedback to arrive at its final form.
        If there appears to be a bullish divergence of price and the VPT (upward slope of the VPT and downward slope of the price) a buy opportunity exists.
        Conversely, a bearish divergence (downward slope of the VPT and upward slope of the price) implies a sell opportunity.
        '''
        name='VPT'
        result=TA.VPT(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def FVE(self):
        '''
        FVE is a money flow indicator, but it has two important innovations: first, the F VE takes into account both intra and
        interday price action, and second, minimal price changes are taken into account by introducing a price threshold
        '''
        name='FVE'
        result=TA.FVE(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def VFI(self):
        '''
         This indicator tracks volume based on the direction of price
        movement. It is similar to the On Balance Volume Indicator.
        For more information see "Using Money Flow to Stay with the Trend",
        and "Volume Flow Indicator Performance" in the June 2004 and
        July 2004 editions of Technical Analysis of Stocks and Commodities.
        '''
        name='VFI'
        result=TA.VFI(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MSD(self):
        '''
         Standard deviation is a statistical term that measures the amount of variability or dispersion around an average.
        Standard deviation is also a measure of volatility. Generally speaking, dispersion is the difference between the actual value and the average value.
        The larger this dispersion or variability is, the higher the standard deviation.
        Standard Deviation values rise significantly when the analyzed contract of indicator change in value dramatically.
        When markets are stable, low Standard Deviation readings are normal.
        Low Standard Deviation readings typically tend to come before significant upward changes in price.
        Analysts generally agree that high volatility is part of major tops, while low volatility accompanies major bottoms
        '''
        name='MSD'
        result=TA.MSD(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def STC(self):
        '''
        The Schaff Trend Cycle (Oscillator) can be viewed as Double Smoothed
        Stochastic of the MACD.

        Schaff Trend Cycle - Three input values are used with the STC:
        – Sh: shorter-term Exponential Moving Average with a default period of 23
        – Lg: longer-term Exponential Moving Average with a default period of 50
        – Cycle, set at half the cycle length with a default value of 10. (Stoch K-period)
        - Smooth, set at smoothing at 3 (Stoch D-period)

        The STC is calculated in the following order:
        EMA1 = EMA (Close, fast_period);
        EMA2 = EMA (Close, slow_period);
        MACD = EMA1 – EMA2.
        Second, the 10-period Stochastic from the MACD values is calculated:
        STOCH_K, STOCH_D  = StochasticFull(MACD, k_period, d_period)  // Stoch of MACD
        STC =  average(STOCH_D, d_period) // second smoothed

        In case the STC indicator is decreasing, this indicates that the trend cycle
        is falling, while the price tends to stabilize or follow the cycle to the downside.
        In case the STC indicator is increasing, this indicates that the trend cycle
        is up, while the price tends to stabilize or follow the cycle to the upside.
        '''
        name='STC'
        result=TA.STC(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def EVSTC(self):
        '''
        Modification of Schaff Trend Cycle using EVWMA MACD for calculation
        '''
        name='EVSTC'
        result=TA.EVSTC(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def WILLIAMS_FRACTAL(self):
        '''
        Williams Fractal Indicator
        Source: https://www.investopedia.com/terms/f/fractal.asp
        '''
        name='WILLIAMS_FRACTAL'
        result=TA.WILLIAMS_FRACTAL(self.df)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    #果仁的因子行情因子
    def open_price(self):
        '''
        开盘价
        '''
        name='open_price'
        result=self.OPEN
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def close_price(self):
        '''
        收盘价
        '''
        name='close_price'
        result=self.CLOSE
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def low_price(self):
        '''
        最低价
        '''
        name='low_price'
        result=self.LOW
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def high_price(self):
        '''
        最高价
        '''
        name='high_price'
        result=self.HIGH
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_0(self):
        '''
        今天的成交额
        '''
        name='amount_0'
        result=self.df['成交额']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_5(self):
        '''
        5日平均成交额
        '''
        name='amount_5'
        result=self.df['成交额'].rolling(window=5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_60(self):
        '''
        60日平均成交额
        '''
        name='amount_60'
        result=self.df['成交额'].rolling(window=20).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_120(self):
        '''
        120日平均成交额
        '''
        name='amount_120'
        result=self.df['成交额'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_120(self):
        '''
        120日平均成交额
        '''
        name='amount_120'
        result=self.df['成交额'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_250(self):
        '''
        250日平均成交额
        '''
        name='amount_250'
        result=self.df['成交额'].rolling(window=250).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amount_N(self,N=10):
        '''
        N日平均成交额
        '''
        name='amount_N'
        result=self.df['成交额'].rolling(window=N).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    
    def volume_0(self):
        '''
        今天的volume
        '''
        name='volume_0'
        result=self.df['volume']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_5(self):
        '''
        5日平均volume
        '''
        name='volume_5'
        result=self.df['volume'].rolling(window=5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_60(self):
        '''
        60日平均volume
        '''
        name='volume_60'
        result=self.df['volume'].rolling(window=20).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_120(self):
        '''
        120日平均volume
        '''
        name='volume_120'
        result=self.df['volume'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_120(self):
        '''
        120日平均volume
        '''
        name='volume_120'
        result=self.df['volume'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_250(self):
        '''
        250日平均volume
        '''
        name='volume_250'
        result=self.df['volume'].rolling(window=250).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_N(self,N=10):
        '''
        N日平均volume
        '''
        name='volume_N'
        result=self.df['volume'].rolling(window=N).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_0(self):
        '''
        今天的涨跌幅
        '''
        name='price_limit_0'
        result=self.df['涨跌幅']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_5(self):
        '''
        5日平均涨跌幅
        '''
        name='price_limit_5'
        result=self.df['涨跌幅'].rolling(window=5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_60(self):
        '''
        60日平均涨跌幅
        '''
        name='price_limit_60'
        result=self.df['涨跌幅'].rolling(window=20).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_120(self):
        '''
        120日平均涨跌幅
        '''
        name='price_limit_120'
        result=self.df['涨跌幅'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_120(self):
        '''
        120日平均涨跌幅
        '''
        name='price_limit_120'
        result=self.df['涨跌幅'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_250(self):
        '''
        250日平均涨跌幅
        '''
        name='price_limit_250'
        result=self.df['涨跌幅'].rolling(window=250).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def price_limit_N(self,N=10):
        '''
        N日平均涨跌幅
        '''
        name='price_limit_N'
        result=self.df['涨跌幅'].rolling(window=N).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def relative_rise_fall_1(self):
        '''
        个股相对指数的涨跌幅1日
        '''
        name='relative_rise_fall_1'
        if self.all==True:
            stock=self.df['涨跌幅'].tolist()[-1]
            index=self.index_df['涨跌幅'].tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅']-stock['index_涨跌幅']
            return name,result
    def relative_rise_fall_5(self):
        '''
        个股相对指数的涨跌幅5日
        '''
        name='relative_rise_fall_5'
        if self.all==True:
            stock=self.df['涨跌幅'].rolling(5).sum().tolist()[-1]
            index=self.index_df['涨跌幅'].rolling(5).sum().tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅'].rolling(5).sum()-stock['index_涨跌幅'].rolling(5).sum()
            return name,result
    def relative_rise_fall_20(self):
        '''
        个股相对指数的涨跌幅20日
        '''
        name='relative_rise_fall_20'
        if self.all==True:
            stock=self.df['涨跌幅'].rolling(20).sum().tolist()[-1]
            index=self.index_df['涨跌幅'].rolling(20).sum().tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅'].rolling(20).sum()-stock['index_涨跌幅'].rolling(20).sum()
            return name,result
    def relative_rise_fall_60(self):
        '''
        个股相对指数的涨跌幅60日
        '''
        name='relative_rise_fall_60'
        if self.all==True:
            stock=self.df['涨跌幅'].rolling(60).sum().tolist()[-1]
            index=self.index_df['涨跌幅'].rolling(60).sum().tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅'].rolling(60).sum()-stock['index_涨跌幅'].rolling(60).sum()
            return name,result
    def relative_rise_fall_120(self):
        '''
        个股相对指数的涨跌幅120日
        '''
        name='relative_rise_fall_120'
        if self.all==True:
            stock=self.df['涨跌幅'].rolling(120).sum().tolist()[-1]
            index=self.index_df['涨跌幅'].rolling(120).sum().tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅'].rolling(120).sum()-stock['index_涨跌幅'].rolling(120).sum()
            return name,result
    def relative_rise_fall_250(self):
        '''
        个股相对指数的涨跌幅60日
        '''
        name='relative_rise_fall_250'
        if self.all==True:
            stock=self.df['涨跌幅'].rolling(250).sum().tolist()[-1]
            index=self.index_df['涨跌幅'].rolling(250).sum().tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅'].rolling(250).sum()-stock['index_涨跌幅'].rolling(250).sum()
            return name,result
    def relative_rise_fall_N(self,N=10):
        '''
        个股相对指数的涨跌幅N日
        '''
        name='relative_rise_fall_N'
        if self.all==True:
            stock=self.df['涨跌幅'].rolling(N).sum().tolist()[-1]
            index=self.index_df['涨跌幅'].rolling(N).sum().tolist()[-1]
            result=stock-index
            return name,result
        else:
            stock_shape=self.df.shape[0]
            index_shape=self.index_df[0]
            if stock_shape>=index_shape:
                stock=self.df[-index_shape:]
            else:
                index=self.index_df[-stock_shape:]
            stock['index_涨跌幅']=index['涨跌幅']
            result=stock['涨跌幅'].rolling(N).sum()-stock['index_涨跌幅'].rolling(N).sum()
            return name,result
    def turnover_rate_0(self):
        '''
        今天的换手率
        '''
        name='turnover_rate_0'
        result=self.df['换手率']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def turnover_rate_5(self):
        '''
        5日平均换手率
        '''
        name='turnover_rate_5'
        result=self.df['换手率'].rolling(window=5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def turnover_rate_60(self):
        '''
        60日平均换手率
        '''
        name='turnover_rate_60'
        result=self.df['换手率'].rolling(window=20).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def turnover_rate_120(self):
        '''
        120日平均换手率
        '''
        name='turnover_rate_120'
        result=self.df['换手率'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def turnover_rate_120(self):
        '''
        120日平均换手率
        '''
        name='turnover_rate_120'
        result=self.df['换手率'].rolling(window=120).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def turnover_rate_250(self):
        '''
        250日平均换手率
        '''
        name='turnover_rate_250'
        result=self.df['换手率'].rolling(window=250).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def turnover_rate_N(self,N=10):
        '''
        N日平均换手率
        '''
        name='turnover_rate_N'
        result=self.df['换手率'].rolling(window=N).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def amplitude(self):
        '''
        股票的振幅
        '''
        name='amplitude'
        result=self.df['振幅']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_orders_net_inflow(self,stock):
        '''
        大单净流入
        '''
        name='large_orders_net_inflow(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['大单净流入-净额']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def single_net_inflow(self,stock):
        '''
        中单净流入
        '''
        name='single_net_inflow(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['中单净流入-净额']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def small_orders_net_inflow(self,stock):
        '''
        小单净流入
        '''
        name='small_orders_net_inflow(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['小单净流入-净额']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def main_net_inflow(self,stock):
        '''
        主力净流入
        '''
        name='main_net_inflow(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['主力净流入-净额']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_single_net_inflow(self,stock):
        '''
        超大单净流入
        '''
        name='large_single_net_inflow(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['超大单净流入-净额']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    




    def large_orders_net_inflow_5(self,stock):
        '''
        大单净流入5日
        '''
        name='large_orders_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def single_net_inflow_5(self,stock):
        '''
        中单净流入5日
        '''
        name='single_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['中单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def small_orders_net_inflow_5(self,stock):
        '''
        小单净流入5日
        '''
        name='small_orders_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['小单净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def main_net_inflow_5(self,stock):
        '''
        主力净流入5日
        '''
        name='main_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['主力净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_single_net_inflow_5(self,stock):
        '''
        超大单净流入5日
        '''
        name='large_single_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['超大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_orders_net_inflow_5(self,stock):
        '''
        大单净流入5日
        '''
        name='large_orders_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def single_net_inflow_5(self,stock):
        '''
        中单净流入5日
        '''
        name='single_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['中单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def small_orders_net_inflow_5(self,stock):
        '''
        小单净流入5日
        '''
        name='small_orders_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['小单净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def main_net_inflow_5(self,stock):
        '''
        主力净流入5日
        '''
        name='main_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['主力净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_single_net_inflow_5(self,stock):
        '''
        超大单净流入5日
        '''
        name='large_single_net_inflow_5(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['超大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    
    def large_orders_net_inflow_20(self,stock):
        '''
        大单净流入20日
        '''
        name='large_orders_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def single_net_inflow_20(self,stock):
        '''
        中单净流入20日
        '''
        name='single_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['中单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def small_orders_net_inflow_20(self,stock):
        '''
        小单净流入20日
        '''
        name='small_orders_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['小单净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def main_net_inflow_20(self,stock):
        '''
        主力净流入20日
        '''
        name='main_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['主力净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_single_net_inflow_20(self,stock):
        '''
        超大单净流入20日
        '''
        name='large_single_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['超大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_orders_net_inflow_20(self,stock):
        '''
        大单净流入20日
        '''
        name='large_orders_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def single_net_inflow_20(self,stock):
        '''
        中单净流入20日
        '''
        name='single_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['中单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def small_orders_net_inflow_20(self,stock):
        '''
        小单净流入20日
        '''
        name='small_orders_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['小单净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def main_net_inflow_20(self,stock):
        '''
        主力净流入20日
        '''
        name='main_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['主力净流入-净额'].rolling(5).mean()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def large_single_net_inflow_20(self,stock):
        '''
        超大单净流入20日
        '''
        name='large_single_net_inflow_20(stock)'
        try:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sh')
        except:
            fund=self.stock_fund_em.stock_individual_fund_flow(stock=stock,market='sz')
        result=fund['超大单净流入-净额'].rolling(5).sum()
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def days_on_market(self):
        '''
        上市天数
        '''
        name='days_on_market'
        result=range(1,self.df.shape[0]+1)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def trading_days(self):
        '''
        交易天数
        '''
        name='trading_days'
        result=range(1,self.df.shape[0]+1)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    #果仁网技术指标,通达信计算指标
    def BIAS_5(self):
        '''
        5日乖离率
        '''
        name='BIAS_5'
        BIAS1,BIAS2,BIAS3=tdx_indicator.BIAS(CLOSE=self.df['close'],N1=6)
        result=pd.Series(BIAS1).tolist()
        if self.all==True:
            return name,result
        else:
            return name,result[-1]
    def BIAS_20(self):
        '''
        20日乖离率
        '''
        name='BIAS_20'
        BIAS1,BIAS2,BIAS3=tdx_indicator.BIAS(CLOSE=self.df['close'],N1=20)
        result=pd.Series(BIAS1).tolist()
        if self.all==True:
            return name,result
        else:
            return name,result[-1]
    def BIAS_60(self):
        '''
        60日乖离率
        '''
        name='BIAS_60'
        BIAS1,BIAS2,BIAS3=tdx_indicator.BIAS(CLOSE=self.df['close'],N1=60)
        result=pd.Series(BIAS1).tolist()
        if self.all==True:
            return name,result
        else:
            return name,result[-1]
    def BIAS_120(self):
        '''
        120日乖离率
        '''
        name='BIAS_120'
        BIAS1,BIAS2,BIAS3=tdx_indicator.BIAS(CLOSE=self.df['close'],N1=120)
        result=pd.Series(BIAS1).tolist()
        if self.all==True:
            return name,result
        else:
            return name,result[-1]
    def BIAS_250(self):
        '''
        250日乖离率
        '''
        name='BIAS_250'
        BIAS1,BIAS2,BIAS3=tdx_indicator.BIAS(CLOSE=self.df['close'],N1=250)
        result=pd.Series(BIAS1).tolist()
        if self.all==True:
            return name,result
        else:
            return name,result[-1]
    def BIAS_N(self,N=10):
        '''
        N日乖离率
        '''
        name='BIAS_N'
        BIAS1,BIAS2,BIAS3=tdx_indicator.BIAS(CLOSE=self.df['close'],N1=N)
        result=pd.Series(BIAS1).tolist()
        if self.all==True:
            return name,result
        else:
            return name,result[-1]
    def volatility_20(self):
        '''
        20日波动率
        '''
        name='volatility_20'
        result=self.df['振幅'].rolling(20).std()*np.sqrt(20)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volatility_60(self):
        '''
        60日波动率
        '''
        name='volatility_60'
        result=self.df['振幅'].rolling(60).std()*np.sqrt(60)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volatility_120(self):
        '''
        120日波动率
        '''
        name='volatility_120'
        result=self.df['振幅'].rolling(120).std()*np.sqrt(120)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volatility_250(self):
        '''
        250日波动率
        '''
        name='volatility_250'
        result=self.df['振幅'].rolling(250).std()*np.sqrt(250)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volatility_N(self,N=10):
        '''
        N日波动率
        '''
        name='volatility_N'
        result=self.df['振幅'].rolling(N).std()*np.sqrt(N)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ma_gold_fork(self,n1=5,n2=10):
        '''
        均线金叉
        '''
        name='ma_gold_fork'
        close=self.df['close']
        result=tdx_indicator.CROSS_UP(tdx_indicator.MA(close,n1),tdx_indicator.MA(close,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def dead_fork(self,n1=5,n2=10):
        '''
        均线死叉
        '''
        name='dead_fork'
        close=self.df['close']
        result=tdx_indicator.CROSS_DOWN(tdx_indicator.MA(close,n1),tdx_indicator.MA(close,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ma_multihead(self,n1=5,n2=10):
        '''
        均线多头
        '''
        name='ma_multihead'
        close=self.df['close']
        result=tdx_indicator.MA(close,n1)-tdx_indicator.MA(close,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x>=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ma_shorts(self,n1=5,n2=10):
        '''
        均线空头
        '''
        name='ma_multihead'
        close=self.df['close']
        result=tdx_indicator.MA(close,n1)-tdx_indicator.MA(close,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x<=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    

    
    def volume_gold_fork(self,n1=5,n2=10):
        '''
        成交量金叉
        '''
        name='volume_gold_fork'
        volume=self.df['volume']
        result=tdx_indicator.CROSS_UP(tdx_indicator.MA(volume,n1),tdx_indicator.MA(volume,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def dead_fork(self,n1=5,n2=10):
        '''
        成交量死叉
        '''
        name='dead_fork'
        volume=self.df['volume']
        result=tdx_indicator.CROSS_DOWN(tdx_indicator.MA(volume,n1),tdx_indicator.MA(volume,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_multihead(self,n1=5,n2=10):
        '''
        成交量多头
        '''
        name='volume_multihead'
        volume=self.df['volume']
        result=tdx_indicator.MA(volume,n1)-tdx_indicator.MA(volume,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x>=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def volume_shorts(self,n1=5,n2=10):
        '''
        成交量空头
        '''
        name='volume_multihead'
        volume=self.df['volume']
        result=tdx_indicator.MA(volume,n1)-tdx_indicator.MA(volume,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x<=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    

    def ema_gold_fork(self,n1=5,n2=10):
        '''
        ema金叉
        '''
        name='ema_gold_fork'
        close=self.df['close']
        result=tdx_indicator.CROSS_UP(tdx_indicator.EMA(close,n1),tdx_indicator.EMA(close,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ema_dead_fork(self,n1=5,n2=10):
        '''
        ema死叉
        '''
        name='ema_dead_fork'
        close=self.df['close']
        result=tdx_indicator.CROSS_DOWN(tdx_indicator.EMA(close,n1),tdx_indicator.EMA(close,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ema_multihead(self,n1=5,n2=10):
        '''
        ema多头
        '''
        name='ema_multihead'
        close=self.df['close']
        result=tdx_indicator.EMA(close,n1)-tdx_indicator.EMA(close,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x>=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ema_shorts(self,n1=5,n2=10):
        '''
        ema空头
        '''
        name='ema_multihead'
        close=self.df['close']
        result=tdx_indicator.EMA(close,n1)-tdx_indicator.EMA(close,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x<=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def macd_dif(self):
        '''
        macd_dif
        '''
        name='macd_dif'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        df=pd.DataFrame()
        df['select']=DIF
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def macd_dea(self):
        '''
        macd_dea
        '''
        name='macd_dea'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        df=pd.DataFrame()
        df['select']=DEA
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def macd_macd(self):
        '''
        macd_macd
        '''
        name='macd_macd'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        df=pd.DataFrame()
        df['select']=MACD
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    


    def macd_gold_fork(self,n1=5,n2=10):
        '''
        macd金叉
        '''
        name='macd_gold_fork'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        result=tdx_indicator.CROSS_UP(tdx_indicator.EMA(DIF,n1),tdx_indicator.EMA(DEA,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def dead_fork(self,n1=5,n2=10):
        '''
        ema死叉
        '''
        name='dead_fork'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        result=tdx_indicator.CROSS_UP(tdx_indicator.EMA(DIF,n1),tdx_indicator.EMA(DEA,n2))
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ema_multihead(self,n1=5,n2=10):
        '''
        ema多头
        '''
        name='ema_multihead'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        result=tdx_indicator.EMA(DIF,n1)-tdx_indicator.EMA(DEA,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x>=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def ema_shorts(self,n1=5,n2=10):
        '''
        ema空头
        '''
        name='ema_multihead'
        close=self.df['close']
        DIF,DEA,MACD=tdx_indicator.MACD(close)
        result=tdx_indicator.EMA(DIF,n1)-tdx_indicator.EMA(DEA,n2)
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x<=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TR(self):
        '''
        三重指数平均线
        '''
        name='TR'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        df=pd.DataFrame()
        df['select']=RIX
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def TRIX(self):
        '''
        三重指数平均线
        '''
        name='TRIX'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        df=pd.DataFrame()
        df['select']=RIX
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def MATRIX(self):
        '''
        移动三重指数平均线
        '''
        name='MATRIX'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        df=pd.DataFrame()
        df['select']=MATRIX
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def matrix_gold_fork(self):
        '''
        三重指数平均线金叉
        '''
        name='matrix_gold_fork'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        result=tdx_indicator.CROSS_UP(RIX,MATRIX)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def matrix_dead_fork(self):
        '''
        三重指数平均线死叉
        '''
        name='matrix_dead_fork'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        result=tdx_indicator.CROSS_DOWN(RIX,MATRIX)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def matrix_multihead(self):
        '''
        matrix_多头
        '''
        name='matrix__multihead'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        result=RIX-MATRIX
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x>=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def matrix_shorts(self):
        '''
        matrix空头
        '''
        name='matrix_multihead'
        close=self.df['close']
        RIX,MATRIX=tdx_indicator.TRIX(close)
        result=RIX-MATRIX
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x<=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def RSV(self):
        '''
        计算KDJ使用到的RSV值，使用后复权价格计算。
        计算公式为 (后复权收盘价 - Min(后复权最低价,9)) / (max(后复权最高价, 9) - min(后复权最低价, 9)) * 100
        '''
        name='RSV'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        result=((close-tdx_indicator.LLV(close,9))/(tdx_indicator.HHV(high,9)-tdx_indicator.LLV(low)))*100
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def kdj_k(self):
        '''
        kdj_k
        '''
        name='kdj_k'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        df=pd.DataFrame()
        df['select']=K
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def kdj_d(self):
        '''
        kdj_d
        '''
        name='kdj_d'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        df=pd.DataFrame()
        df['select']=d
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def kdj_j(self):
        '''
        kdj_j
        '''
        name='kdj_j'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        df=pd.DataFrame()
        df['select']=J
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
        
    def kdj_gold_fork(self):
        '''
        kdj金叉
        '''
        name='kdj_gold_fork'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        result=tdx_indicator.CROSS_UP(K,D)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def kdj_dead_fork(self):
        '''
        kdj死叉
        '''
        name='kdj_dead_fork'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        result=tdx_indicator.CROSS_DOWN(K,D)
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def kdj_multihead(self):
        '''
        kdj_多头
        '''
        name='kdj_multihead'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        result=K-D
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x>=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def kdj_shorts(self):
        '''
        kdj空头
        '''
        name='kdj_shorts'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        K,D,J=tdx_indicator.KDJ(close)
        result=K-D
        df=pd.DataFrame()
        df['select']=result
        df['select']=df['select'].apply(lambda x: True if x<=0 else False)
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def boll_up(self):
        '''
        布林线上线
        '''
        name='boll_up'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        BOLL,UB,LB=tdx_indicator.BOLL(close)
        df=pd.DataFrame()
        df['select']=UB
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def boll_lb(self):
        '''
        布林线下线
        '''
        name='boll_lb'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        BOLL,UB,LB=tdx_indicator.BOLL(close)
        df=pd.DataFrame()
        df['select']=LB
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def boll_boll(self):
        '''
        布林线中线
        '''
        name='boll_boll'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        BOLL,UB,LB=tdx_indicator.BOLL(close)
        df=pd.DataFrame()
        df['select']=BOLL
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def boll_break_up_rail(self):
        '''
        boll线突破上轨
        '''
        name='boll_break_up_rail'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        BOLL,UB,LB=tdx_indicator.BOLL(close)
        df=pd.DataFrame()
        df['select']=close>UB
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def boll_break_lb_rail(self):
        '''
        boll线突破下轨
        '''
        name='boll_break_lb_rail'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        BOLL,UB,LB=tdx_indicator.BOLL(close)
        df=pd.DataFrame()
        df['select']=close<LB
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def BBIC(self):
        '''
        多空指标，等于BBI除以收盘价，BBIC越小股价越强势，BBIC < 1 为多头行情， 
        BBIC>1 为空头行情。BBI等于(N1日均价+N2日均价+N3日均价+N4日均价)/4。
        '''
        name='BBIC'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        BBI=tdx_indicator.BBI(close)
        df=pd.DataFrame()
        df['select']=BBI/close
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    def CCI(self):
        '''
        CCI N日顺势指标，测量股价是否已超出常态分布范围。 
        +100以上为超买区，—100以下为超卖区，+100到—100之间为震荡区。
        '''
        name='CCI'
        close=self.df['close']
        high=self.df['high']
        low=self.df['low']
        CCI=tdx_indicator.CCI(close,high,low)
        df=pd.DataFrame()
        df['select']=CCI
        result=df['select']
        if self.all==True:
            return name,result
        else:
            return name,result.tolist()[-1]
    



        






    


    




        







    def get_all_factor_data(self,stock_list=['600031','600111','000001'],
                            factor_list=['SMA','SMM','SSMA','EMA'],start_date='20210101',
                            end_date='20500101',data_type='D',limit=10000000):
        '''
        获取全部因子
        '''
        if self.all !=True:
            data=pd.DataFrame()
            for i in tqdm(range(len(stock_list))):
                stock=stock_list[i]
                try:
                    value_list=[]
                    
                    hist=self.data.get_hist_data_em(stock=stock,start_date=start_date,
                                                    end_date=end_date,data_type=data_type,limit=limit)
                    self.df=hist
                    for factor in factor_list:
                        try:
                            func='self.{}()'.format(factor)
                            name,value=eval(func)
                            value_list.append([value])
                        except:
                            try:
                                func='self.{}'.format(factor)
                                name,value=eval(func)
                                value_list.append([value])
                            except:
                                name=factor
                                value_list.append([None])
                                print('标的{}最新计算 {}有问题'.format(stock,name))

                    df=pd.DataFrame(value_list)
                    df=df.T
                    df.columns=factor_list
                    df['stock']=stock
                    data=pd.concat([data,df],ignore_index=True)
                except Exception as e:
                    print(e)
            return data
        else:
            data=pd.DataFrame()
            for i in tqdm(range(len(stock_list))):
                stock=stock_list[i]
                try:
                    value_list=[]
                    
                    hist=self.data.get_hist_data_em(stock=stock,start_date=start_date,
                                                    end_date=end_date,data_type=data_type,limit=limit)
                    self.df=hist
                    df=pd.DataFrame()
                    df['date']=hist['date']
                    df['stock']=stock
                    for factor in factor_list:
                        try:
                            func='self.{}()'.format(factor)
                            name,value=eval(func)
                            df[name]=value
                        except:
                            try:
                                func='self.{}'.format(factor)
                                name,value=eval(func)
                                df[name]=value
                            except:
                                name=factor
                                df[name]=None
                                print('标的{}历史计算 {}有问题'.format(stock,name))
                    data=pd.concat([data,df],ignore_index=True)
                except Exception as e:
                    print(e)
            return data
          
                

   
    










    
    
        
        
    
    
