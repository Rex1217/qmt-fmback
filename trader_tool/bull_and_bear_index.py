import akshare as ak
import pandas as pd  # 导入Pandas库，用于数据处理
import numpy as np  # 导入NumPy库，用于数值计算
class bull_and_bear_index:
    def __init__(self,df,switch_all_signals = True, rsiPeriod=14,rsiThresholdHigh = 66, rsiDifference = 4,
            rsiLookback = 3,rsiThresholdLow = 30,lookback_piv = 24,cooldownPeriod = 25, minVolume = 7000,
            show_zigzag = False,switch_overheat = False,showPivotPoints = False,showLevels = False):
        '''
        牛熊指标
        '''
        # 示例数据
        # self.df 应包含 'close', 'open', 'high', 'low', 'volume' 等列
        # self.df = pd.read_csv('your_data.csv')  # 假设从CSV文件读取数据
        # 参数设置
        self.df=df
        self.switch_all_signals=switch_all_signals  # 开关所有信号
        self.rsiPeriod=rsiPeriod # RSI周期设置为14
        self.rsiThresholdHigh=rsiThresholdHigh   # RSI高阈值设置为66
        self.rsiDifference=rsiDifference  # RSI差值设置为4
        self.rsiLookback=rsiLookback  # RSI回溯期设置为3
        self.rsiThresholdLow=rsiThresholdLow  # RSI低阈值设置为30
        self.lookback_piv=lookback_piv   # 枢轴回溯期设置为24
        self.cooldownPeriod=cooldownPeriod   # 冷却期设置为25
        self.minVolume =minVolume # 最小成交量设置为7000
        self.show_zigzag=show_zigzag # Zig Zag显示开关
        self.switch_overheat=switch_overheat   # 过热冷却枢轴开关
        self.showPivotPoints=showPivotPoints   # 显示枢轴点开关
        self.showLevels=showLevels  # 显示过热水平线开关

        # RSI 和 MACD 计算
        self.df['RSI'] = self.RSI(self.df['close'],self.rsiPeriod)  # 计算RSI指标
        self.df['MACD'], self.df['MACD_signal'], self.df['MACD_hist'] = self.MACD(self.df['close'],12, 26,9)
    def RET(self,S,N=1):  
        #返回序列倒数第N个值,默认返回最后一个
        return np.array(S)[-N] 
    def SMA(self,S, N, M=1):       #中国式的SMA,至少需要120周期才精确 (雪球180周期)    alpha=1/(1+com)    
        return pd.Series(S).ewm(alpha=M/N,adjust=False).mean().values           #com=N-M/M
    def MAX(sel,S1,S2): 
        #序列max 
        return np.maximum(S1,S2)  
    def ABS(self,S):  
        #返回N的绝对值    
        return np.abs(S) 
    def EMA(self,S,N):             #指数移动平均,为了精度 S>4*N  EMA至少需要120周期     alpha=2/(span+1)    
        return pd.Series(S).ewm(span=N, adjust=False).mean().values    
    def REF(self,S, N=1):          #对序列整体下移动N,返回序列(shift后会产生NAN)    
        return pd.Series(S).shift(N).values  
    def RSI(self,CLOSE,N1=14):
        '''
        RSI
        '''  
        LC=self.REF(CLOSE,1)
        RSI1=self.SMA(self.MAX(CLOSE-LC,0),N1,1)/self.SMA(self.ABS(CLOSE-LC),N1,1)*100
        return RSI1
    def MACD(self,CLOSE,SHORT=12,LONG=26,MID=9):
        '''
        平滑异同平均线
        输出DIF:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
        输出DEA:DIF的MID日指数移动平均
        输出平滑异同平均线:(DIF-DEA)*2,COLORSTICK
        '''
        DIF=self.EMA(CLOSE,SHORT)-self.EMA(CLOSE,LONG)
        DEA=self.EMA(DIF,MID)
        MACD=(DIF-DEA)*2
        return DIF,DEA,MACD
    # LeleCalculation函数
    def LeleCalculation(self, bars, length):  # 定义LeleCalculation函数，计算特定信号
        bullIndex = np.zeros(len(self.df))  # 初始化牛市索引为0
        bearIndex = np.zeros(len(self.df))  # 初始化熊市索引为0
        result = np.zeros(len(self.df))  # 初始化结果数组为0
        
        for i in range(4, len(self.df)):  # 遍历数据，从第5个元素开始
            bullIndex[i] = bullIndex[i-1] + 1 if self.df['close'].iloc[i] > self.df['close'].iloc[i-4] else bullIndex[i-1]  # 计算牛市索引
            bearIndex[i] = bearIndex[i-1] + 1 if self.df['close'].iloc[i] < self.df['close'].iloc[i-4] else bearIndex[i-1]  # 计算熊市索引
            
            if bullIndex[i] > bars and self.df['close'].iloc[i] < self.df['open'].iloc[i] and self.df['high'].iloc[i] >= self.df['high'].rolling(length).max().iloc[i]:  # 判断牛市信号
                bullIndex[i] = 0  # 重置牛市索引
                result[i] = -1  # 设置结果为-1，表示牛市信号
            elif bearIndex[i] > bars and self.df['close'].iloc[i] > self.df['open'].iloc[i] and self.df['low'].iloc[i] <= self.df['low'].rolling(length).min().iloc[i]:  # 判断熊市信号
                bearIndex[i] = 0  # 重置熊市索引
                result[i] = 1  # 设置结果为1，表示熊市信号
        return result  # 返回计算结果
    # 计算OverheatSignal
    def OverheatSignal(self, bars=10, length=40):
        '''
        计算OverheatSignal
        '''
        self.df['OverheatSignal'] = self.LeleCalculation(bars, length)  # 计算过热信号
        self.df['highOverheat'] = np.where(self.df['OverheatSignal'] == -1, self.df['high'], np.nan)  # 设置高过热信号
        self.df['lowOverheat'] = np.where(self.df['OverheatSignal'] == 1, self.df['low'], np.nan)  # 设置低过热信号

        # 计算阻力和支撑水平
        self.df['resistanceLevel'] = np.nan  # 初始化阻力水平为NaN
        self.df['supportLevel'] = np.nan  # 初始化支撑水平为NaN

        for i in range(1, len(self.df)):  # 遍历数据，从第2个元素开始
            self.df['resistanceLevel'].iloc[i] = self.df['high'].iloc[i] if self.df['close'].iloc[i] < self.df['open'].iloc[i] and self.df['OverheatSignal'].iloc[i] else self.df['resistanceLevel'].iloc[i-1]  # 计算阻力水平
            self.df['supportLevel'].iloc[i] = self.df['low'].iloc[i] if self.df['close'].iloc[i] > self.df['open'].iloc[i] and self.df['OverheatSignal'].iloc[i] else self.df['supportLevel'].iloc[i-1]  # 计算支撑水平
    # Main Trigger 计算
    def calculate_triggers(self,bars=10, length=40):  # 定义计算触发器的函数
        '''
        Main Trigger 计算
        '''
        self.OverheatSignal(bars,length)
        lastMainTrigger = None  # 初始化上一个主要触发器为None
        lastSubTrigger = None  # 初始化上一个次要触发器为None
        lastMainTriggerLow = None  # 初始化上一个低主要触发器为None
        lastSubTriggerLow = None  # 初始化上一个低次要触发器为None
        self.df['mainTriggerHigh'] = False  # 初始化主要高触发器为False
        self.df['subTriggerHigh'] = False  # 初始化次要高触发器为False
        self.df['mainTriggerLow'] = False  # 初始化主要低触发器为False
        self.df['subTriggerLow'] = False  # 初始化次要低触发器为False
        for i in range(1, len(self.df)):  # 遍历数据，从第2个元素开始
            rsiConditionHigh1 = self.df['RSI'].iloc[i] > self.rsiThresholdHigh and self.df['RSI'].iloc[i] < self.df['RSI'].rolling(3).max().iloc[i] - self.rsiDifference  # 计算RSI高条件1
            rsiConditionHigh = rsiConditionHigh1 and self.df['RSI'].iloc[i - self.rsiLookback] > self.rsiThresholdHigh  # 计算RSI高条件

            macdConditionHigh = self.df['MACD_hist'].iloc[i] > 0 and self.df['MACD_hist'].iloc[i] < self.df['MACD_hist'].iloc[i - 1]  # 计算MACD高条件

            mainTriggerHighRaw = rsiConditionHigh and macdConditionHigh and self.df['volume'].iloc[i] >= self.minVolume  # 计算主要高触发器的原始条件
            self.df['mainTriggerHigh'].iloc[i] = mainTriggerHighRaw and (lastMainTrigger is None or (i - lastMainTrigger > self.cooldownPeriod))  # 设置主要高触发器

            if self.df['mainTriggerHigh'].iloc[i]:  # 如果主要高触发器被触发
                lastMainTrigger = i  # 更新上一个主要触发器的位置

            subTriggerHighRaw = self.df['RSI'].iloc[i] > (self.rsiThresholdHigh - 5) and macdConditionHigh and self.df['volume'].iloc[i] >= self.minVolume  # 计算次要高触发器的原始条件
            self.df['subTriggerHigh'].iloc[i] = subTriggerHighRaw and (lastSubTrigger is None or (i - lastSubTrigger > self.cooldownPeriod))  # 设置次要高触发器

            if self.df['subTriggerHigh'].iloc[i]:  # 如果次要高触发器被触发
                lastSubTrigger = i  # 更新上一个次要触发器的位置

            rsiConditionLow1 = self.df['RSI'].iloc[i] < self.rsiThresholdLow and self.df['RSI'].iloc[i] > self.df['RSI'].rolling(3).min().iloc[i] + self.rsiDifference  # 计算RSI低条件1
            rsiConditionLow = rsiConditionLow1 and self.df['RSI'].iloc[i - self.rsiLookback] < self.rsiThresholdLow  # 计算RSI低条件

            macdConditionLow = self.df['MACD_hist'].iloc[i] < 0 and self.df['MACD_hist'].iloc[i] > self.df['MACD_hist'].iloc[i - 1]  # 计算MACD低条件

            mainTriggerLowRaw = rsiConditionLow and macdConditionLow and self.df['volume'].iloc[i] >= self.minVolume  # 计算主要低触发器的原始条件
            self.df['mainTriggerLow'].iloc[i] = mainTriggerLowRaw and (lastMainTriggerLow is None or (i - lastMainTriggerLow > self.cooldownPeriod))  # 设置主要低触发器

            if self.df['mainTriggerLow'].iloc[i]:  # 如果主要低触发器被触发
                lastMainTriggerLow = i  # 更新上一个主要低触发器的位置

            subTriggerLowRaw = self.df['RSI'].iloc[i] < (self.rsiThresholdLow + 5) and macdConditionLow and self.df['volume'].iloc[i] >= self.minVolume  # 计算次要低触发器的原始条件
            self.df['subTriggerLow'].iloc[i] = subTriggerLowRaw and (lastSubTriggerLow is None or (i - lastSubTriggerLow > self.cooldownPeriod))  # 设置次要低触发器

            if self.df['subTriggerLow'].iloc[i]:  # 如果次要低触发器被触发
                lastSubTriggerLow = i  # 更新上一个次要触发器的位置
    def get_cacal_rsult(self,bars=10, length=40):
        self.calculate_triggers(bars,length)  # 计算触发器

        # 打印信号列
        self.df=self.df[['mainTriggerHigh', 'subTriggerHigh', 'mainTriggerLow', 'subTriggerLow', 'resistanceLevel', 'supportLevel']] # 打印信号和水平
        return self.df
if __name__=='__main__':
    df=ak.stock_zh_a_daily(symbol='sh600171',start_date='20210101',end_date='20500101')
    models=bull_and_bear_index(df)
    print(models.get_cacal_rsult())

