from xtquant import xtdata
import matplotlib.pyplot as plt
import pandas as pd
class time_sharing_average_qmt:
    def __init__(self,stock='600031.SH',period='tick',start_date='20240812',end_date='20500101',count=-1,jhjj=True):
        '''
        qmt分时均线的计算
        FB:=DATE<>REF(DATE,1);{当根K线的日期不等于前一根K线的日期，这样就确定当天第一根K线的位置}
        T:=BARSLAST(FB);{当天第一根K线距离现在的周期数}
        A1:=SUM(AMO,T+1);{从第一根K线开始累加成交金额}
        V1:=SUM(VOL,T+1)*100;{从第一根K线开始累加成交量，VOL单位为手，乘以100换算为股}
        JJX:A1/V1;{累加成交金额除以累加成交量，得到均价};
        '''
        self.stock=stock
        self.period=period
        self.start_date=start_date
        self.end_date=end_date
        self.count=count
        self.jhjj=jhjj
        xtdata.subscribe_quote(stock_code=self.stock,period=self.period,
                                    start_time=self.start_date,end_time=self.end_date,count=self.count)
    def get_time_sharing_average(self):
        '''
        获取数据
        'time'                  #时间戳
        'lastPrice'             #最新价
        'open'                  #开盘价
        'high'                  #最高价
        'low'                   #最低价
        'lastClose'             #前收盘价
        'amount'                #成交总额
        'volume'                #成交总量
        'pvolume'               #原始成交总量
        'stockStatus'           #证券状态
        'openInt'               #持仓量
        'lastSettlementPrice'   #前结算
        'askPrice'              #委卖价
        'bidPrice'              #委买价
        'askVol'                #委卖量
        'bidVol'                #委买量
        'transactionNum'		#成交笔数
        '''
        self.df=xtdata.get_market_data_ex(stock_list=[self.stock],period=self.period,
                                    start_time=self.start_date,end_time=self.end_date,count=self.count)
        self.df=self.df[self.stock]
        if self.jhjj:
            self.df['select']=self.df.index
            self.df['select']=self.df['select'].apply(lambda x: int(x[-6:-2]))
            self.df=self.df[self.df['select']>=930]
        print(self.df)
        #'amount'                #成交总额
        #'volume'                #成交总量
        #分时
        self.df['sharing_average']=self.df['amount']/self.df['volume']/100
        return self.df
    def plot_show_result(self):
        '''
        展示结果图
        '''
        self.df=self.get_time_sharing_average()
        self.df=self.df[['time','amount','volume','lastPrice','sharing_average']]
        self.df[['lastPrice','sharing_average']].plot(title=self.stock)
        plt.show()
if __name__=='__main__':
    models=time_sharing_average_qmt(stock='600353.SH',period='tick',start_date='20240815',
                                    end_date='20500101',count=-1,jhjj=True)
    models.plot_show_result()
    
