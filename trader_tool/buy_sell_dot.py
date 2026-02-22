import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from finta import TA
import mplfinance as mpf
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
class buy_sell_dot:
    '''
    大智慧BS买卖点
    '''
    def __init__(self,df):
        '''
        买线:EMA(C,2);
        卖线:EMA(SLOPE(C,21)*20+C,42);
        BU:=CROSS(买线,卖线);
        SEL:=CROSS(卖线,买线);DRAWICON(BU,L,7);DRAWICON(SEL,H,8);
        输出买线:收盘价的2日指数移动平均
        输出卖线:收盘价的21日线性回归斜率*20+收盘价的42日指数移动平均
        BU赋值:买线上穿卖线
        SEL赋值:卖线上穿买线
        当满足条件BU时,在最低价位置画7号图标
        当满足条件SEL时,在最高价位置画8号图标
        '''
        self.df=df
    def get_hist_data(self):
        '''
        获取历史数据
        '''
        df=self.df
        return df
    def EMA(self,S,N):             #指数移动平均,为了精度 S>4*N  EMA至少需要120周期     alpha=2/(span+1)    
        return pd.Series(S).ewm(span=N, adjust=False).mean().values  
    def CROSS(self,S1, S2):                     #判断向上金叉穿越 CROSS(MA(C,5),MA(C,10))  判断向下死叉穿越 CROSS(MA(C,10),MA(C,5))   
        return np.concatenate(([False], np.logical_not((S1>S2)[:-1]) & (S1>S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226
    def SLOPE(self,S=[1,2,3,4,5,6],N=3):
        slopes = []
        for i in range(len(S) - N + 1):
            x = np.arange(N)
            y = S[i:i+N]
            slope, _ = np.polyfit(x, y, 1)
            slopes.append(slope)
        #对其数据
        for i in range(N-1):
            slopes.insert(0,None)
        return slopes
    def params_tdx_func(self,C):
        '''
        解析通达信函数
        买线:EMA(C,2);
        卖线:EMA(SLOPE(C,21)*20+C,42);
        BU:=CROSS(买线,卖线);
        SEL:=CROSS(卖线,买线);DRAWICON(BU,L,7);DRAWICON(SEL,H,8);
        '''
        买线=self.EMA(C,2)
        df=pd.DataFrame()
        df['C']=C.tolist()
        SLOPE=pd.Series(self.SLOPE(C,21))*20
        df['SLOPE']=SLOPE
        df['value']= df['SLOPE']+df['C']
        value=df['value']
        卖线=self.EMA(value,42)
        BU=self.CROSS(买线,卖线)
        SEL=self.CROSS(卖线,买线)
        return BU,SEL
    def get_cacal_result(self):
        '''
        获取计算的结果
        '''
        df=self.get_hist_data()
        C=df['close']
        buy,sell=self.params_tdx_func(C=C)
        df['buy']=buy
        df['sell']=sell
        return df
    def show_params_result(self):
        '''
        显示分析的结果
        '''
        df=self.get_cacal_result()
        #拆分买卖点
        buy_list=[]
        sell_list=[]
        for price,dot in zip(df['close'],df['buy']):
            if dot==True:
                buy_list.append(price)
            else:
                buy_list.append(None)
        for price,dot in zip(df['close'],df['sell']):
            if dot==True:
                sell_list.append(price)
            else:
                sell_list.append(None)
        df['买点']=buy_list
        df['卖点']=sell_list
        df1=df 
        df1.index=df1['date']
        df1=df1.sort_index()
        macd = TA.MACD(df1)
        boll = TA.BBANDS(df1)
        rsi = TA.RSI(df1)
        df1.rename(columns={'date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                            'volume': 'Volume'}, inplace=True)
        # 时间格式转换
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False
        df1['Date'] = pd.to_datetime(df1['Date'])
        # 出现设置索引
        df1.set_index(['Date'], inplace=True)
        # 设置股票颜
        mc = mpf.make_marketcolors(up='r', down='g', edge='i')
        # 设置系统
        s = mpf.make_mpf_style(marketcolors=mc)
        add_plot = [mpf.make_addplot(macd['MACD'], panel=1, color='r',title='MACD'),
                    mpf.make_addplot(macd['SIGNAL'], panel=1, color='y'),
                    mpf.make_addplot(df1['卖点'],panel=0,color='g',type='scatter',marker='v',markersize=60),
                    mpf.make_addplot(df1['买点'],panel=0,color='r',type='scatter',marker='^',markersize=60),
                    ]
        # 绘制股票图，5，10，20日均线
        mpf.plot(df1, type='candle',mav=(5, 10, 20), style=s,addplot=add_plot,title='BS buy sell dot'),
        plt.show()
if __name__=='__main__':
    models=buy_sell_dot(df='')
    print(models.show_params_result())
    

    
    
 