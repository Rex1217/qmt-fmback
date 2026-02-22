from trader_tool.unification_data import unification_data
from trader_tool.trader_frame import trader_frame
import pandas as pd 
import time
import datetime
import schedule
import json
from trader_tool.base_func import base_func
import os
from trader_tool.joinquant_data import joinquant_data
from trader_tool.seed_trader_info import seed_trader_info
from qmt_trader.xtquant import xtdata
import math
import numpy as np 
from trader_tool.decode_trader_password import decode_trader_password
class joinquant_trader:
    def __init__(self,
                trader_tool='ths',
                exe='C:/同花顺软件/同花顺/xiadan.exe',
                tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',
                qmt_account_type='STOCK',
                data_api='qmt'):
        '''
        法玛全天候趋势回归动量指数风控策略
        作者:法码量化
        微信:xms_quants1
        时间:20260123
        系统放在桌面一级目录就可以
        '''
        print('################################################################################################')
        print("""
            风险告知书,代码开源,自己使用风险自担，和作者无关，代码只用于学习研究使用,不做交易参考,运行请仔细研究源代码,模拟盘测试
            请在使用前仔细阅读下述内容
            1、数据、计算、程序等力求但不保证绝对正确，不排除技术故障，因此带来的风险需自行承担。
            2、回测数据仅代表历史，不代表未来收益，仅供参考。
            3、请在使用前，充分学习和掌握，操作不当造成的后果需自行承担。
            4、提供内容仅作为交流，不代表开通证券账户必然提供该服务。
            5、程序化交易不代表一定能赚钱，旨在讨论、交流和学习一种更为科学的交易方式，请做好预期管理。
            6、部分内容整理自互联网或得到作者授权转载分享，所述内容不代表个人观点，仅供参考学习。
            7、建议投资者务必确认自身风险承受能力及投资目标,不推荐投资目标不相符的投资者参与。
            8、智能交易可能因系统、通讯等原因无法正常使用或无法按照您的设置价格发出委托指令及完成成交，最终成交价格及数量以交易所、登记结算机构等记录为准。请密切关注交易回报情况及条件单设置情况。
            9、提供内容仅供参考，不构成对委托指令成交的承诺，不构成投资建议，不构成收益或避免损失的承诺。请您务必仔细阅读相关风险提示及协议，了解各类智能交易功能的区别及不同风险，审慎决策是否使用相关功能。
            10、所有内容仅供参考学习，均在模拟盘的环境下使用，请充分掌握后使用，实盘使用风险请自行承担。
              
            """)
        print('################################################################################################')
        self.data_api=data_api
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.trader_tool=trader_tool
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
        order_frame=trader_frame(
            trader_tool=self.trader_tool,
            exe=self.exe,
            tesseract_cmd=self.tesseract_cmd,
            qmt_path=self.qmt_path,
            qmt_account=self.qmt_account,
            qmt_account_type=self.qmt_account_type,
            )
        self.trader=order_frame.get_trader_frame()
        data=unification_data(trader_tool=self.trader_tool,data_api=self.data_api)
        self.data=data.get_unification_data()
        self.path=os.path.dirname(os.path.abspath(__file__))
    def connact(self):
        '''
        链接交易
        '''
        try:
            self.trader.connect()
            return True
        except Exception as e:
            print("运行错误:",e)
            print('{}连接失败'.format(self.trader_tool))
            return False
    def save_data(self):
        try:
            account=self.trader.balance()
            account.to_excel(r'{}/账户数据/账户数据.xlsx'.format(self.path))
            print(account)
            position=self.trader.position()
            position.to_excel(r'{}/持股数据/持股数据.xlsx'.format(self.path))
            print(position)
        except Exception as e:
            print(e,'检测qmt账户,路径是不是对的')
    def get_index_hist_data(self,stock='000001.SH'):
        '''
        读取指数数据
        '''
        #下载历史数据作为备用
        xtdata.download_history_data(
            stock_code=stock,
            period='1d',
            start_time='20210101',
            end_time='20500101')
        xtdata.subscribe_quote(stock_code=stock,
                period='1d',
                start_time='20210101',
                end_time='20500101',
                count=-1)
        df=xtdata.get_market_data_ex(stock_list=[stock],
                period='1d',
                start_time='20210101',
                end_time='20500101',
                count=-1)
        df=df[stock]
        return df
    def get_trader_stock(self):
        '''
        获取交易股票池
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df=pd.DataFrame()
        st_name=text['策略名称']
        try:
            df['证券代码']=text['股票池']
            df['名称']=text['股票池名称']
            df['投资备注']=st_name+'B'+df['证券代码']
        except Exception as e:
            print(e,'股票池获取有问题')
        return df
    def MOM(self,etf='518800'):
        '''
        计算动量
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        df=pd.DataFrame()
        n=text['动量天数']
        r_line=text['风险控制线']
        index_stock=text['指数代码']
        index_line=text['指数风控线']
        index_trader_stock=text['指数风控标的']
        stock=etf
        df=self.data.get_hist_data_em(
            stock=stock,
            start_date='20210101',
            end_date='20500101',
        )
        df=df[-n:]
        df['line']=df['close'].rolling(r_line).mean()
        df=df[-n:]
        y = np.log(df['close'].values)
        n = len(y)  
        x = np.arange(n)
        weights = np.linspace(1,2, n)  # 线性增加权重
        slope, intercept = np.polyfit(x, y, 1, w=weights)
        annualized_returns = math.pow(math.exp(slope), 250) - 1
        residuals = y - (slope * x + intercept)
        weighted_residuals = weights * residuals**2
        r_squared = 1 - (np.sum(weighted_residuals) / np.sum(weights * (y - np.mean(y))**2))
        last_price=df['close'].tolist()[-1]
        last_line=df['line'].tolist()[-1]
        #指数数据
        index_df=self.get_index_hist_data(stock=index_stock)
        index_df['index_line']=index_df['close'].rolling(index_line).mean()
        
        close_list=df['close'].tolist()
        last_price=close_list[-1]
        pre_price=close_list[0]
        score=((last_price-pre_price)/pre_price)*100
        last_line=df['line'].tolist()[-1]
        #指数风险分析
        last_index=index_df['close'].tolist()[-1]
        last_index_line=index_df['index_line'].tolist()[-1]
        if last_index<last_index_line and stock in index_trader_stock:
            print(stock,'触发指数风控卖出************')
            score=-100
        else:
            if last_price<last_line:
                score=-100
            else:
                score=score = annualized_returns * r_squared
        return score
    def get_rank(self,etf_pool=["518880","513100",
        "159915"]):
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        score_list = []
        min_value=text['最小动量']
        max_value=text['最大动量']
        for etf in etf_pool:
            score = self.MOM(etf)
            score_list.append(score)
        df = pd.DataFrame(index=etf_pool, data={'score':score_list})
        df = df.sort_values(by='score', ascending=False)
        df['证券代码']=df.index.tolist()
        name_dict=dict(zip(text['股票池'],text['股票池名称']))
        df['名称']=df['证券代码'].apply(lambda x: name_dict.get(x,x))
        df=df[['证券代码','名称','score']]
        print('今日动量计算排行***************')
        print(df)
        df = df[(df['score'] > min_value) & (df['score'] <= max_value)] #安全区间，动量过高过低都不好
        rank_list = list(df.index)
        if len(rank_list) == 0:
            rank_list=[] #如果全部都小于最小动量，那么空仓或者买《国债、银华日历、黄金》避险
        return rank_list
    def check_is_sell(self,stock='562310',amount=100):
        '''
        检查是否可以卖出
        '''
        position=self.trader.position()
        if position.shape[0]>0:
            position=position[position['证券代码']==stock]
            if position.shape[0]>0:
                position=position[position['股票余额']>=10]
                if position.shape[0]>0:
                    hold_amount=position['股票余额'].tolist()[-1]
                    av_amount=position['可用余额'].tolist()[-1]
                    if av_amount>=amount and amount>=10:
                        return True
                    elif av_amount< amount and av_amount>=10:
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False
    def check_is_buy(self,stock='513100.SH',amount=100,price=1.3):
        '''
        检查是否可以买入
        '''
        account=self.trader.balance()
        #可以使用的现金
        av_cash=account['可用金额'].tolist()[-1]
        value=amount*price
        if av_cash>=value:
            return True
        else:
            return False
    def adjust_amount(self,stock='',amount=''):
        '''
        调整数量
        '''           
        if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['11','12']:
            amount=math.floor(amount/10)*10
        else:
            amount=math.floor(amount/100)*100
        return amount
    def check_not_trader_data(self):
        '''
        #检查单子是不是委托了
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        st_name=text['策略名称']
        now_dat=str(datetime.datetime.now())[:10]
        trader_log=self.trader.today_entrusts()
        if trader_log.shape[0]>0:
            trader_log['策略']=trader_log['委托备注'].apply(lambda x: str(x)[:len(st_name)])
            trader_log=trader_log[trader_log['策略']==st_name]
            if trader_log.shape[0]>0:
                maker_list=trader_log['委托备注'].tolist()
            else:
                maker_list=[]
        else:
            maker_list=[]
        return maker_list
    def get_price(self,stock='513100'):
        '''
        获取价格
        '''
        price=self.data.get_spot_data(stock=stock)['最新价']
        return price
    def get_position(self):
        '''
        读取隔离的持股数据
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        is_open=text['是否开启策略隔离']
        stock_list=text['股票池']
        position=self.trader.position()
        if position.shape[0]>0:
            if is_open=='是':
                print('开启策略隔离******************')
                position['证券代码']=position['证券代码'].astype(str)
                position['隔离']=position['证券代码'].apply(lambda x: '是' if x in stock_list else '不是')
                position=position[position['隔离']=='是']
            else:
                position=position
                print('不开启策略隔离******************')
        else:
            position=position
        return position


    # 交易
    def trade(self):
        '''
        运行交易函数
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        maker_list=self.check_not_trader_data()
        if self.check_is_trader_date_1():
            #获取动量最高的N个ETF
            target_num =text['买入数量']
            trader_type=text['交易模式']
            value=text['下单值']
            etf_pool=text['股票池']
            st_name=text['策略名称']
            target_list = self.get_rank(etf_pool)[:target_num]
            # 卖出    
            position=self.get_position()
            account=self.trader.balance()
            if position.shape[0]>0:
                position=position[position['股票余额']>=10]
                if position.shape[0]>0:
                    position['证券代码']=position['证券代码'].astype(str)
                    hold_list=position['证券代码'].tolist()
                    av_amount_dict=dict(zip(position['证券代码'],position['可用余额']))
                else:
                    hold_list=[]
                    av_amount_dict={}
            else:
                hold_list=[]
                av_amount_dict={}
            for stock in hold_list:
                price=self.get_price(stock)
                if stock not in target_list:
                    if trader_type=='数量':
                        amount=value
                    elif trader_type=='金额':
                        amount=value/price
                        amount=self.adjust_amount(stock,amount)
                    elif trader_type=='百分比':
                        total=account['总资产']
                        value=total*value
                        amount=value/price
                        amount=self.adjust_amount(stock,amount)
                    else:
                        amount=0
                    av_amount=av_amount_dict.get(stock,0)
                    if av_amount>=10:
                        if av_amount>=amount:
                            amount=amount
                        else:
                            amount=av_amount
                    else:
                        amount=0
                    
                    if self.check_is_sell(stock=stock,amount=amount) and amount>=10:
                        maker='{}{}{}'.format(st_name,'S',stock)
                        if maker not in maker_list:
                            self.trader.sell(
                                security=stock,
                                amount=amount,
                                price=price,
                                strategy_name=maker,
                                order_remark=maker)
                            msg="""
                                策略:法玛全天候绝对动量指数风控策略,
                                交易类型:卖出,
                                股票:"{}",
                                数量:"{}",
                                价格:"{}",
                                时间:"{}"
                                """.format(stock,amount,price,datetime.datetime.now())
                            self.seed_trader_data(msg=msg)
                            #注意这个卖出了要移除持股,不然无法买入
                            try:
                                hold_list.remove(stock)
                            except Exception as e:
                                print(e,stock,'移除持股有问题******')
                            #卖出等待30秒充分的等待卖单成交
                            time.sleep(30)
                        else:
                            print(maker,'已经卖出委托不在下单')
                    else:
                        print(stock,'卖出不了')
                else:
                    print(stock,'卖出在动量排名继续持有')
            # 买入
            for stock in target_list:
                if stock not in hold_list:
                    price=self.get_price(stock)
                    if trader_type=='数量':
                        amount=value
                    elif trader_type=='金额':
                        amount=value/price
                        amount=self.adjust_amount(stock,amount)
                    elif trader_type=='百分比':
                        total=account['总资产']
                        value=total*value
                        amount=value/price
                        amount=self.adjust_amount(stock,amount)
                    else:
                        amount=0
                    if self.check_is_buy(stock=stock,amount=amount,price=price) and amount>=10:
                        maker='{}{}{}'.format(st_name,'B',stock)
                        if maker not in maker_list:
                            self.trader.buy(
                                security=stock,
                                amount=amount,
                                price=price,
                                strategy_name=maker,
                                order_remark=maker)
                            msg="""
                                策略:法玛全天候绝对动量指数风控策略,
                                交易类型:买入,
                                股票:"{}",
                                数量:"{}",
                                价格:"{}",
                                时间:"{}"
                                """.format(stock,amount,price,datetime.datetime.now())
                            self.seed_trader_data(msg=msg)
                        else:
                            print(maker,'已经买入委托不在下单')
                    else:
                        print(stock,'买入不了')
                else:
                    print(stock,'买入在动量排名继续持有')
        else:
            print('{} 目前不是交易时间'.format(datetime.datetime().now()))
    def check_is_trader_date_1(self):
        '''
        检测是不是交易时间
        '''
        with open('{}/分析配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        trader_time=text['交易时间段']
        start_date=text['交易开始时间']
        end_date=text['交易结束时间']
        start_mi=text['开始交易分钟']
        jhjj=text['是否参加集合竞价']
        if True:
            if jhjj=='是':
                jhjj_time=15
            else:
                jhjj_time=30
            loc=time.localtime()
            tm_hour=loc.tm_hour
            tm_min=loc.tm_min
            wo=loc.tm_wday
            if wo<=trader_time:
                if tm_hour>=start_date and tm_hour<=end_date:
                    if tm_hour==9 and tm_min<jhjj_time:
                        return False
                    elif tm_min>=start_mi:
                        return True
                    else:
                        return False
                else:
                    return False    
            else:
                print('周末')
                return False
    def seed_trader_data(self,msg='test'):
        '''
        发送交易信号
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        seed_type=text['通知发送方式']
        sender_email =text['发送QQ']
        receiver_email =text['接收QQ']
        password =text['QQ掩码']
        dd_token_list=text['钉钉token']
        wx_token_list=text['企业微信token']
        api=seed_trader_info(
            seed_type=seed_type,
            sender_email=sender_email,
            receiver_email=receiver_email,
            password=password,
            dd_token_list=dd_token_list,
            wx_token_list=wx_token_list
            )
        api.seed_trader_info(msg=msg)
    def trader_log(self):
        '''
        日志输出
        '''
        with open('{}/策略配置.json'.format(self.path),'r+',encoding='utf-8') as f:
            com=f.read()
        st_text=json.loads(com)
        date_list=st_text['调仓时间']
        if self.check_is_trader_date_1():
            print('{} 策略的调仓时间是{} 等待时间调仓****************************'.format(datetime.datetime.now(),date_list))
        else:
            print('{} 目前不是交易时间'.format(datetime.datetime.now()))
if __name__=='__main__':
    '''
    法玛全天候趋势回归动量指数风控策略
    '''
    with open('分析配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    with open('策略配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    st_text=json.loads(com)
    trader_tool=text['交易系统']
    exe=text['同花顺下单路径']
    tesseract_cmd=text['识别软件安装位置']
    qmt_path=text['qmt路径']
    qmt_account=text['qmt账户']
    qmt_account_type=text['qmt账户类型']
    data_api=text['交易数据源']
    date_list=st_text['调仓时间']
    trader=joinquant_trader(
        trader_tool=trader_tool,
        exe=exe,
        tesseract_cmd=tesseract_cmd,
        qmt_path=qmt_path,
        qmt_account=qmt_account,
        qmt_account_type=qmt_account_type,
        data_api=data_api)
    trader.connact()
    if True:
        #3秒运行一次
        schedule.every(0.05).minutes.do(trader.trader_log)
        for date in date_list:
            schedule.every().day.at('{}'.format(date)).do(trader.trade)
            print('策略调仓时间定时在{} 等待交易***********************************'.format(date))
        while True:
            schedule.run_pending()
            time.sleep(1)
    
                    


