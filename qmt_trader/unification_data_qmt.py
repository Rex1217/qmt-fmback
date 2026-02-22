#统一数据源
#需要打开qmt
from .qmt_data import qmt_data
from .stock_data_qmt import stock_data_qmt
from .bond_cov_data_qmt import bond_cov_data_qmt
from .etf_fund_data_qmt import etf_fund_data_qmt
import requests
class  unification_data_qmt:
    def __init__(self,data_api='qmt'):
        '''
        统一数据源
        data_type=其他/qmt/tdx
        '''
        self.data_api=data_api
        self.stock_data=stock_data_qmt(data_api=self.data_api)
        self.bond_cov_data=bond_cov_data_qmt(data_api=self.data_api)
        self.etf_fund_data=etf_fund_data_qmt(data_api=self.data_api)
        
    def select_data_type(self,stock='600031'):
        '''
        选择数据类型
        '''
        stock=str(stock)[:6]
        if stock[:3] in ['110','113','128','127','123','117'] or stock[:2] in ['11','12']:
            return 'bond'
        elif stock[:3] in ['502','501'] or stock[:2] in ['16','15','51','50','56','58'] or stock[:1] in ['5']:
            return 'fund'
        else:
            return 'stock'
    def adjust_stock(self,stock='600031.SH'):
        '''
        调整代码
        '''
        if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
            stock=stock.upper()
        else:
            if stock[:3] in ['110','113','118','510','519',
                            "900",'200'] or stock[:2] in ['11','51','60','68'] or stock[:1] in ['5']:
                stock=stock+'.SH'
            else:
                stock=stock+'.SZ'
        return stock
    def get_hist_data_em(self,stock='600031.SH',start_date='20210101',end_date='20500101',data_type='D',limit=10000000):
        '''
        获取历史数据
         获取股票数据
        start_date=''默认上市时间
        - ``1`` : 分钟
            - ``5`` : 5 分钟
            - ``15`` : 15 分钟
            - ``30`` : 30 分钟
            - ``60`` : 60 分钟
            - ``101`` : 日
            - ``102`` : 周
            - ``103`` : 月
        fq=0股票除权
        fq=1前复权
        fq=2后复权
        '''
        stock=str(stock)[:6]
        code_type=self.select_data_type(stock=stock)
        if code_type=='stock':
            df=self.stock_data.get_stock_hist_data_em(stock=stock,start_date=start_date,
                                                          end_date=end_date,data_type=data_type)
        elif code_type=='fund':
            df=self.etf_fund_data.get_ETF_fund_hist_data(stock=stock,end=end_date,
                                                             limit=limit,data_type=data_type)
        else:
            df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,end=end_date,
                                                             data_type=data_type,limit=1000000)
        return df
    def get_spot_data(self,stock='600031.SH'):
        '''
        获取实时数据
        '''
        stock=str(stock)[:6]
        code_type=self.select_data_type(stock=stock)
        if code_type=='stock':
            df=self.stock_data.get_stock_spot_data(stock=stock)
        elif code_type=='fund':
            df=self.etf_fund_data.get_etf_fund_spot_data(stock=stock)
        else:
            df=self.bond_cov_data.get_cov_bond_spot(stock=stock)
        return df
    def get_spot_trader_data(self,stock='600031.SH'):
        '''
        获取实时交易数据3秒一次
        '''
        stock=str(stock)[:6]
        code_type=self.select_data_type(stock=stock)
        if code_type=='stock':
            df=self.stock_data.get_stock_all_trader_data(stock=stock)
        elif code_type=='fund':
            df=self.etf_fund_data.get_etf_spot_trader_data(stock=stock)
        else:
            df=self.bond_cov_data.get_cov_bond_spot_trader_data(stock=stock)
        return df
    
    def get_national_debt_spot_data(self,stock='131810'):
        '''
        获取国债实盘盘口数据
        '''
        if str(stock)[:3] in ['131']:
            maker='0'
        else:
            maker='1'
        secid='{}.{}'.format(maker,stock)
        params={
            'invt': '2',
            'fltt': '1',
            #cb: jQuery35103912037352847286_1705635267482
            'fields': 'f58,f734,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f171,f47,f86,f292,f19,f39,f20,f40,f17,f531,f18,f15,f16,f13,f14,f11,f12,f37,f38,f35,f36,f33,f34,f31,f32,f48,f50,f161,f49,f191,f192,f71,f264,f263,f262,f267,f265,f268,f706,f700,f701,f703,f154,f704,f702,f705,f721,f51,f52,f301',
            'secid':secid,
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'wbp2u': '|0|1|0|web',
            #_: 1705635267483
        }
        url='https://push2.eastmoney.com/api/qt/stock/get?'
        res=requests.get(url=url,params=params)
        text=res.json()
        data=text['data']
        result={}
        result['买一']=data['f19']/1000
        result['买一量']=data['f20']
        result['买二']=data['f17']/1000
        result['买二量']=data['f18']
        result['买三']=data['f15']/1000
        result['买三量']=data['f16']
        result['买四']=data['f14']/1000
        result['买四量']=data['f15']
        result['买五']=data['f11']/1000
        result['买五量']=data['f12']
        result['卖一']=data['f39']/1000
        result['卖一量']=data['f40']
        result['卖二']=data['f37']/1000
        result['卖二量']=data['f38']
        result['卖三']=data['f35']/1000
        result['卖三量']=data['f36']
        result['卖四']=data['f33']/1000
        result['卖四量']=data['f34']
        result['卖五']=data['f31']/1000
        result['卖五量']=data['f32']
        return result



        

        