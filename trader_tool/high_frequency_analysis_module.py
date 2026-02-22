from qmt_trader.xtquant import xtdata
from datetime import datetime
import numpy as np
import pandas as pd
class high_frequency_analysis_module:
    def __init__(self,stock='',hist='',tick='',base=''):
        '''
        qmt高频分析模块
        实时tick分析模型
        '''
        self.stock=stock
        self.hist=hist
        self.tick=tick
        self.base=base
    def check_is_up_limit(self):
        '''
        检查是否是涨停
        '''
        askPrice=sum(self.tick['askPrice'])
        if askPrice==0:
            return True
        else:
            return False
    def check_is_down_limit(self):
        '''
        检查是否是跌停
        '''
        askPrice=sum(self.tick['bidPrice'])
        if askPrice==0:
            return True
        else:
            return False
    def get_buy_sell_volume(self):
        '''
        买卖的数量差
        buy-sell
        '''
        tick=self.tick
        volume=sum(tick['bidVol'])-sum(tick['askVol'])
        return volume
    def get_buy_sell_ratio(self):
        '''
        买卖的比例
        '''
        tick=self.tick
        ratio=((sum(tick['bidVol'])-sum(tick['askVol']))/sum(tick['askVol']))/100
        return ratio
    def get_zdf(self):
        '''
        涨跌幅
        '''
        tick=self.tick
        zdf=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
        return zdf
    def get_spot_price(self):
        '''
        获取最新价
        '''
        tick=self.tick
        return tick['lastPrice']

    def get_sealing_ratio(self):
        '''
        封单比率
        '''
        base=self.base
        tick=self.tick
        FloatVolume=base['FloatVolume']
        bidVol=sum(tick['bidVol'])
        return (FloatVolume/bidVol)*100
    def get_pulse_data(self,n=200,zdf=3):
        '''
        3秒一个tick
        10秒上涨3%
        '''
        hist=self.hist
        lastPrice_list=hist['lastPrice'].tolist()[-n:]
        now_zdf=((lastPrice_list[-1]-lastPrice_list[0])/lastPrice_list[0])*100
        print('脉冲涨跌幅{}'.format(now_zdf))
        if  now_zdf>=zdf:
            return True
        else:
            return False
    def get_conditions_pulse_data(self,n1=5,n=200,zdf=3):
        '''
        条件脉冲
        '''
        total_zdf=n1
        tick_zdf=self.get_zdf()
        hist=self.hist
        lastPrice_list=hist['lastPrice'].tolist()[-n:]
        now_zdf=((lastPrice_list[-1]-lastPrice_list[0])/lastPrice_list[0])*100
        print('{} {} 脉冲涨跌幅{} 目前涨跌幅{}'.format(self.stock,datetime.now(),now_zdf,tick_zdf))
        if  now_zdf>=zdf and tick_zdf>total_zdf:
            return True
        else:
            return False
    def check_the_number_of_plate_openings(self):
        '''
        检查开板次数
        上一个tick涨停,下一个tick没有涨停
        '''
        #剔除集合竞价的数据
        hist=self.hist
        hist['date']=hist.index.tolist()
        hist['date']=hist['date'].apply(lambda x: int(str(x)[8:]))
        hist=hist[hist['date']>=92800]
        hist=hist[hist['date']<=145659]
        hist['stats']=hist['askVol'].apply(lambda x:1 if sum(x)==0 else 0)
        hist['开板']=hist['stats']-hist['stats'].shift(1)
        hist['开板']=hist['开板'].apply(lambda x: '是' if x==1 else '不是')
        amount=hist['开板'].tolist().count('是')
        print('{} {} 开板的次数{}'.format(self.stock,datetime.now(),amount))
        return amount-1
    def get_tick_ratio(self,n=3,ratio=1.1):
        '''
        盘口买卖的比例
        '''
        hist=self.hist[-3:]
        hist['bidVol_1']=hist['bidVol'].apply(lambda x: sum(x))
        hist['askVol_1']=hist['askVol'].apply(lambda x: sum(x))
        bidVol_1=hist['bidVol_1'].sum()
        askVol_1=hist['askVol_1'].sum()
        zdf=bidVol_1/askVol_1
        print('{} 最近{} 秒买卖比例{}'.format(self.stock,n*2,zdf))
        if zdf>=ratio:
            return True
        else:
            return False
    def get_firtst_amount(self,n=3):
        '''
        '''
        hist=self.hist
        hist['date']=hist.index.tolist()
        hist['date']=hist['date'].apply(lambda x: int(str(x)[8:]))
        hist=hist[hist['date']>=92800]
        hist['stats']=hist['askVol'].apply(lambda x:1 if sum(x)==0 else 0)
        hist['bidVol_1']=hist['bidVol'].apply(lambda x: sum(x))
        hist['askVol_1']=hist['askVol'].apply(lambda x: sum(x))
        hist['askVol_1']=hist['askVol'].apply(lambda x: sum(x))
        bidVol_1_list=hist['bidVol_1'].tolist()
        hist=hist[hist['stats']==1]
        first=sum(bidVol_1_list[:n])
        return first
    def get_tick_change_analysis(self,limit_amount=50000,limit_time=10,ratio=50,amount=7000):
        '''
        涨停板盘口变化分析
        撤单分析
        '''
        hist=self.hist
        hist['date']=hist.index.tolist()
        hist['date']=hist['date'].apply(lambda x: int(str(x)[8:]))
        hist=hist[hist['date']>=92800]
        hist['stats']=hist['askVol'].apply(lambda x:1 if sum(x)==0 else 0)
        hist['bidVol_1']=hist['bidVol'].apply(lambda x: sum(x))
        hist['askVol_1']=hist['askVol'].apply(lambda x: sum(x))
        bidVol_1_list=hist['bidVol_1'].tolist()
        hist=hist[hist['stats']==1]
        if hist.shape[0]>0:
            #以第一次涨停后最大封单量为基准，封单大幅减少50%
            first=bidVol_1_list[0]
            if hist.shape[0]<=limit_time*20:
                print('{}目前涨停的时间{} 分钟小于{} 分钟不开启撤单1'.format(self.stock,hist.shape[0]/20, limit_time))
            else:
                first_bidVol=bidVol_1_list[limit_time*20]#1#100
                last_bidVol=bidVol_1_list[-1]#1#1
            change_amount=(first_bidVol*ratio)/100#0.5#50
            #封单总数低于7000手撤单
            bidVol=bidVol_1_list[-1]
            #last_bidVol change_amount
            #1，0.5
            #1，50
            #200，0.5
            print('*********************************************************************')
            print('{}目前封单数量{}小于{}结果{},第一次涨停数量{} 大于{} 结果{} 现在封单数量小于{} 分钟的数量{} 结果{}'.format(self.stock,bidVol,amount,bidVol<=amount,first,limit_amount,first>=limit_amount,last_bidVol,limit_time,change_amount,last_bidVol<=change_amount))
            if  (bidVol<=amount or (last_bidVol<=change_amount )) and self.check_is_up_limit():
                
                return True
            else:
                return False
        else:
            print('撤单 {} 不存在涨停'.format(self.stock))
            return False
    
    def BARSLASTCOUNT(self,S):
        '''
        统计连续满足S条件的周期数
        '''                   
        rt = np.zeros(len(S)+1)            # BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数
        for i in range(len(S)): rt[i+1]=rt[i]+1  if S[i] else rt[i+1]
        return rt[1:]
    def REF(self,S, N=1):  
        '''        
        对序列整体下移动N,返回序列(shift后会产生NAN)    
        '''
        return pd.Series(S).shift(N).values  
    def IF(self,S,A,B):   
        '''
        序列布尔判断 return=A  if S==True  else  B
        '''
        return np.where(S,A,B)   
    def AND(self,S1,S2):
        #and
        return np.logical_and(S1,S2)
    def get_check_zt_time(self):
        '''
        检查涨停时间
        '''
        hist=self.hist
        hist['date']=hist.index.tolist()
        hist['date']=hist['date'].apply(lambda x: int(str(x)[8:]))
        hist=hist[hist['date']>=92800]
        hist=hist[hist['date']<=145600]
        hist['stats']=hist['askVol'].apply(lambda x:1 if sum(x)==0 else 0)
        hist['bidVol_1']=hist['bidVol'].apply(lambda x: sum(x))
        hist['askVol_1']=hist['askVol'].apply(lambda x: sum(x))
        hist['涨停时间']=self.BARSLASTCOUNT(self.REF(hist['stats'],1)==1)
        hist['涨停次数']=self.IF(self.AND(self.REF(hist['涨停时间'],1)==0,hist['涨停时间']==1),1,0)
        hist['涨停次数']=hist['涨停次数'].cumsum()
        hist['涨停次数']=self.IF(hist['涨停时间']>0,hist['涨停次数'],0)
        hist['开板次数']= hist['涨停次数']-1
        hist['涨停持续时间']=hist['涨停时间']*3
        return hist
    def get_buy_func_3(self,n=2,time=20,volume=10000,max_is_open=2):
        '''
        "买点3":"涨停时间大于N秒,封单大于N这两种同时出现就可以忽略第一次封单量不够3000的参数买入，这个N是可调的外部参数，像你给我设计的那样",
        "第一次涨停时间大于N秒":3,
        "在次封单大于":10000,
        "总开板次数小于":2,
        n第几次涨停
        time涨停时间
        volume涨停的封单数量
        min_is_open最小的涨停次数
        max_is_open最多的开板次数
        '''
        #检查是否涨停
        if self.check_is_up_limit():
            hist=self.get_check_zt_time()
            hist1=hist[hist['涨停次数']==n-1]
            if hist1.shape[0]>0:
                zt_time=hist1['涨停持续时间'].tolist()[-1]
            else:
                zt_time=0
            is_open=max(hist['开板次数'].tolist())
            zt_volume=hist['bidVol_1'].tolist()[-1]
            if zt_time>=time and zt_volume>=volume and  is_open<=max_is_open:
                return True
            else:
                return False
        else:
            return False  
    def buy_total_amount(self,amount=100000,zdf=9.8):
        '''
        买1档的总金额
        '''
        tick=self.tick
        price=tick['lastPrice']
        total_bidVol=tick['bidVol'][0]
        total_amount=total_bidVol*price
        now_zdf=self.get_zdf()
        if total_amount>=amount and now_zdf>=zdf:
            print(self.stock,'总盘口1档金额{}大于{} 符合要求'.format(total_amount,amount))
            return True
        else:
            print(self.stock,'总盘口1档金额{}小于{} 不符合要求'.format(total_amount,amount))
            return False
    def buy_sell_amount(self,amount=10000):
        '''
        盘口5档买卖的差额
        '''
        tick=self.tick
        price=tick['lastPrice']
        total_bidVol=sum(tick['bidVol'])
        total_askVol=sum(tick['askVol'])
        buy_sell_amount=(total_bidVol-total_askVol)*price
        if buy_sell_amount>=amount:
            print(self.stock,'买入总额{}大于卖出总额{} {} 符合条件'.format(total_bidVol*price,total_askVol*price,buy_sell_amount))
            return True
        else:
            print(self.stock,'买入总额{}小于卖出总额{} {} 不符合条件'.format(total_bidVol*price,total_askVol*price,buy_sell_amount))
            return False
    def cacal_trader_3(self,n=1):
        '''
        封单总量小于流通量的N%
        '''
        tick=self.tick
        price=tick['lastPrice']
        total_bidVol=sum(tick['bidVol'])
        base=self.base
        FloatVolume=base['FloatVolume']
        ratio=(total_bidVol/FloatVolume)*100
        if total_bidVol>0:
            if ratio<=n and self.check_is_up_limit():
                print(self.stock,"撤单3封单总量{} 流通量{} 封单比例{} 小于{}撤单".format(total_bidVol,FloatVolume,ratio,n))
                return True
            else:
                print(self.stock,"撤单3封单总量{} 流通量{} 封单比例{} 大于{}不撤单".format(total_bidVol,FloatVolume,ratio,n))
                return False
        else:
            print(self.stock,"撤单3封单总量{} 可能不是交易日".format(total_bidVol))
            return False

    def cacal_trader_4(self,n=10000):
        '''
        买1金额不小于N，N也是可调，这个做撤单4；
        '''
        tick=self.tick
        price=tick['lastPrice']
        bidVol=tick['bidVol'][0]
        amount=bidVol*price
        if amount>0:
            if amount<=n and self.check_is_up_limit():
                print(self.stock,"撤单4买一的金额{} 小于{} 撤单".format(amount,n))
                return True
            else:
                print(self.stock,"撤单4买一的金额{} 大于{} 不撤单".format(amount,n))
                return False
        else:
            print(self.stock,"撤单4封单总量{} 可能不是交易日".format(amount))
            return False
    def cacal_trader_5(self,time=140000,time_1=15,ratio=2):
        '''
        时间N（14点）之前内涨停，涨停15（N）分钟以后，封单数量小于个股总股本的百分之2（N）就触发撤单
        '''
        tick = self.tick
        hist=self.get_check_zt_time()
        hist=hist[hist['date']<=time]
        base=self.base
        total_bidVol=sum(tick['bidVol'])
        FloatVolume=base['FloatVolume']
        limit_ratio=(total_bidVol/FloatVolume)*100
        if hist.shape[0]>0:
            zt_time=(hist['涨停持续时间'].tolist()[-1])/60
            total_amount=hist['bidVol_1'].tolist()[-1]
            if zt_time>=time_1 and limit_ratio<=ratio and self.check_is_up_limit():
                print(self.stock,'撤单5涨停时间{}大于要求时间{} 封单比例{}小于{} 撤单'.format(zt_time,time_1,limit_ratio,ratio))
                return True
            else:
                print(self.stock,'撤单5涨停时间{} 小于要求时间{} 封单{} 大于{} 不撤单'.format(zt_time,time_1,limit_ratio,ratio))
                return False
        else:
            print(self.stock,'撤单5目前时间超过{}'.format(time_1))
            return False

if __name__=='__main__':
    stock_list=['002965.SZ']
    start_time='20250124'
    end_time='20250124'
    count=-1
    xtdata.subscribe_quote(stock_code=stock_list[-1],period='tick',start_time=start_time,end_time=end_time,count=count)
    hist=xtdata.get_market_data_ex(stock_list=stock_list,period='tick',start_time=start_time,end_time=end_time,count=count)
    hist=hist[stock_list[-1]]
    tick=xtdata.get_full_tick(code_list=[stock_list[0]])
    tick=tick[stock_list[0]]
    base=xtdata.get_instrument_detail(stock_code=stock_list[0])
    print(base)
    print(tick)
    models=high_frequency_analysis_module(hist=hist,tick=tick,base=base)
    df=models.cacal_trader_5()
    print(df)
    
    
