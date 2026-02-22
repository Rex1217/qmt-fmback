import datetime
import time
import pandas as pd
import execjs
import os
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
from lxml import html
from tqdm import tqdm
from datetime import datetime
class jsl_data_xg:
    '''
    获取集思录数据
    '''
    def __init__(self,user, password):
        filename = 'encode_jsl.txt'
        self.user=user
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
        path = os.path.dirname(os.path.abspath(__file__))
        self.full_path = os.path.join(path, filename)
        self.headers = {
            'Host': 'www.jisilu.cn', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
            'Cache-Control': 'no-cache', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'Origin': 'https://www.jisilu.cn', 'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Referer': 'https://www.jisilu.cn/login/',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'
        }
        self.session=''
    def decoder(self,text): # 加密用户名和密码
        with open(self.full_path, 'r', encoding='utf8') as f:
            source = f.read()

        ctx = execjs.compile(source)
        key = '397151C04723421F'
        return ctx.call('jslencode', text, key)
    def login(self,): # 登录
        session = requests.Session()
        url = 'https://www.jisilu.cn/account/ajax/login_process/'
        username = self.decoder(self.user)
        jsl_password = self.decoder(self.password)
        data = {
                'return_url': 'https://www.jisilu.cn/',
                'user_name': username,
                'password': jsl_password,
                'net_auto_login': '1',
                '_post_type': 'ajax',
        }

        js = session.post(
            url=url,
            headers=self.headers,
            data=data,
            )
        ret = js.json()
        if ret.get('errno') == 1:
            print('集思录登录成功 账户 {}'.format(self.user))
            self.session=session
            return session
        else:
            print('集思录登录失败 账户 {}'.format(self.user))
            return ''   
    
    def get_convert_bond_detail(self,stock='113672'):
        '''
        获取仔细数据
        '''
        
        url='https://www.jisilu.cn/data/convert_bond_detail/{}'.format(stock)
        r = self.session.get(
            url=url,
            headers=self.headers,
        )
        ret = r.text
        columns=['正股总市值(亿)','正股流通市值(亿)','网上中签率','正股价','正股PB','正股PE','正股ROE']
        value_list=[]
        with open(r'{}\text.html'.format(self.path),'w+',encoding='utf-8') as f:
            f.write(ret)
        data=pd.DataFrame()

        with open(r'{}\text.html'.format(self.path), 'r', encoding='utf-8') as file:
            content = file.read()
        #使用Beautifulsoup解析
        soup = BeautifulSoup(content, features='lxml')
        table=soup.find_all('table')
        for tr in table:
            tr=tr.find_all('tr')
            for td in tr:
                for i in td:
                    j=str(i)
                    if '<span class="font_16">' in j:
                        for m in i:
                            for p in m:
                                if '<div class="bond_nm">' in str(p):
                                    data['可转债名称']=[p.text.split(' ')[0].replace('\n','')]
                                    data['可转债代码']=[p.text.split(' ')[1]]
                                elif '<div class="stock_nm">' in str(p):
                                    data['正股名称']=[p.text.split('正股')[-1].split(' ')[0]]
                                    data['正股代码']=[p.text.split(' ')[1].replace('\n','')]
                                elif '<div class="stock_indu">' in str(p):
                                    p=p.text.split(' id="industry_new" target="_cblist"')[-1].split('</a>')[0][3:]
                                    data['一级行业']=p.split('-')[0]
                                    data['二级行业']=p.split('-')[1]
                                    data['三级行业']=p.split('-')[2]

                    elif 'class="jisilu_subtitle" colspan="2"' in j:
                        text=i.text
                        if '转股价值' in text:
                            data[text.split(' ')[0]]=[text.split(' ')[1]]
                        else:
                            data[text.split(' ')[0]]=[text.split(' ')[-1]]
                    elif 'id="issue_dt"' in j:
                        text=i.text
                        data['起息日']=text
                    elif 'id="list_dt"' in j:
                        text=i.text
                        data['上市日']=text
                    elif 'id="maturity_dt"' in j:
                        text=i.text
                        data['到期日']=text
                    elif 'id="year_term"' in j:
                        text=i.text
                        data['剩余年限']=text
                    elif 'id="convert_dt"' in j and 'nowrap=""' in j:
                        text=i.text
                        data['转股起始日']=text
                    elif 'id="next_put_dt"' in j and 'nowrap=""' in j:
                        text=i.text
                        data['回售起算日']=text
                    elif 'id="next_put_dt"' in j:
                        text=i.text
                        data['最后交易日']=text
                    elif 'id="convert_dt"' in j:
                        text=i.text
                        data['最后转股日']=text
                    elif 'id="convert_price"' in j:
                        text=i.text
                        data['转股价']=text
                    elif 'id="put_price"' in j:
                        text=i.text
                        data['回售价']=text
                    elif 'id="redeem_price"' in j:
                        text=i.text
                        data['到期赎回价']=text
                    elif 'id="convert_cd"' in j:
                        text=i.text
                        data['转股代码']=text
                    elif 'id="repo_cd"' in j:
                        text=i.text
                        data['质押代码']=text
                    elif 'id="apply_cd"' in j:
                        text=i.text
                        data['申购代码']=text
                    elif 'id="ration_cd"' in j:
                        text=i.text
                        data['配售代码']=text
                    elif 'id="orig_iss_amt"' in j:
                        text=i.text
                        data['发行规模(亿)']=text
                    elif 'id="lck_iss_amt"' in j:
                        text=i.text
                        data['限售规模(亿)']=text
                    elif 'id="curr_iss_amt"' in j:
                        text=i.text
                        data['剩余规模(亿)']=text
                    elif 'id="cvt_rt"' in j:
                        text=i.text
                        data['已转股比例']=text
                    elif 'id="convert_amt_ratio2"' in j:
                        text=i.text
                        data['转债市值占比']=text
                    elif 'id=""' in j:
                        text=i.text
                        data['正股总市值(亿)']=text
                    elif 'id="convert_amt_ratio"' in j:
                        text=i.text
                        data['转债流通市值占比']=text
                    elif 'id="ration"' in j:
                        text=i.text
                        data['每股配售']=text
                    elif 'id="convert_value"' in j:
                        text=i.text
                        data['股东配售率']=text
                    elif 'id="province"' in j:
                        text=i.text
                        data['地域']=text
                    elif 'id="issuer_rating_cd"' in j:
                        text=i.text
                        data['主体评级']=text
                    elif 'id="rating_cd"' in j:
                        text=i.text
                        data['债券评级']=text
                    elif 'id="repo_discount_rt"' in j:
                        text=i.text
                        data['折算率']=text
                    elif 'id="fund_rt"' in j:
                        text=i.text
                        data['机构持仓']=text
                    elif 'id="bond_md"' in j:
                        text=i.text
                        data['税前修正久期']=text
                    elif 'id="bond_incr20"' in j:
                        text=i.text
                        data['20日涨幅']=text
                    elif 'id="stock_incr20"' in j:
                        text=i.text
                        data['正股20日涨幅']=text
                    elif 'id="bond_stdevry"' in j:
                        text=i.text
                        data['年化波动率']=text
                    elif 'id="volatility_rate"' in j:
                        text=i.text
                        data['正股年化波动率']=text
                    elif 'id="bond_bias20"' in j:
                        text=i.text
                        data['20日BIAS']=text
                    elif 'id="正股20日BIAS"' in j:
                        text=i.text
                        data['stock_bias20']=text
                    elif 'id="force_redeem_price"' in j:
                        text=i.text
                        data['强赎触发价']=text
                    elif 'id="redeem_status"' in j:
                        text=i.text
                        data['强赎天计数']=text
                    elif 'id="threshold_value"' in j:
                        text=i.text
                        data['下修触发价']=text
                    elif 'id="adjust_condition"' in j:
                        text=i.text
                        data['下修天计数']=text
                    elif 'id="put_convert_price"' in j:
                        text=i.text
                        data['回售触发价']=text
                    elif 'id="put_status"' in j:
                        text=i.text
                        data['回售天计数']=text
                    elif 'id="estimate_put_dt"' in j:
                        text=i.text
                        data['预估回售日']=text
                    elif 'id="left_put_year"' in j:
                        text=i.text
                        data['回售剩余年限']=text
                    elif 'id="put_ytm_rt"' in j:
                        text=i.text
                        data['回售税前收益']=text
                    elif 'id="put_ytm_rt_tax"' in j:
                        text=i.text
                        data['回售税后收益']=text
                    elif 'id="bond_value"' in j:
                        text=i.text
                        data['纯债价值']=text
                    elif 'id="option_value"' in j:
                        text=i.text
                        data['期权价值']=text
                    elif 'id="theory_value"' in j:
                        text=i.text
                        data['理论价值']=text
                    elif 'id="deviation_degree"' in j:
                        text=i.text
                        data['理论偏离度']=text
                    elif 'id="guarantor"' in j:
                        text=i.text
                        data['担保']=text
                    elif 'id="adjust_tc"' in j:
                        text=i.text
                        data['下修条款']=text
                    elif 'id="redeem_tc"' in j:
                        text=i.text
                        data['强赎条款']=text
                    elif 'id="unadj_logs"' in j:
                        text=i.text
                        data['不强赎历史']=text
                    elif 'id="put_tc"' in j:
                        text=i.text
                        data['回售条款']=text
                    elif 'id="cpn_desc"' in j:
                        text=i.text
                        data['利率']=text
                    elif 'id="税前YTM"' in j:
                        text=i.text
                        data['ytm_formula']=text
                    elif 'class="data_val"' in j and 'class="jisilu_title"' not in j and 'id' not in j:
                        value_list.append(i.text)
                    else:
                        pass
            for value,column in zip(value_list,columns):
                data[column]=[value]     
        return data
    def adjust_data(x):
        x=str(x)
        if '%' in x:
            return x.replace('%','')
        else:
            return x
    def get_all_connect_data(self) :
        '''
        获取全部合并数据
        '''     
        data=pd.DataFrame() 
        df=self.get_conv_data_jsl()
        stock_list=df['转债代码'].tolist()
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            try:
                df=self.get_convert_bond_detail(stock=stock)
                data=pd.concat([data,df],ignore_index=True)
            except Exception:
                print('{}获取有问题'.format(stock))
        for columns in data.columns.tolist():
            data[columns]=data[columns].replace('-',0)
        for columns in data.columns.tolist():
            try:
                data[columns]=data[columns].apply(lambda x: float(str(x).split('%')[0]) if '%' in str(x) else x)
            except:
                pass
        
        return data
    def get_conv_data_jsl(self):
        """
        可转债列表
        """
        rename_dict = {
            'bond_id': '转债代码',
            'bond_nm': '转债名称',
            'bond_py': '转债拼音',
            'price': '最新价',
            'increase_rt': '涨跌幅',
            'stock_id': '正股代码',
            'stock_nm': '正股名称',
            'stock_py': '正股拼音',
            'sprice': '正股最新价',
            'sincrease_rt': '正股涨跌幅',
            'pb': '市净率',
            'convert_price': '转股价',
            'convert_value': '转股价值',
            'convert_dt': '距离转股天数',
            'premium_rt': '转股溢价率',
            'bond_premium_rt': '纯债溢价率',
            'dblow': '双低',
            'adjust_condition': '下修状态',
            'sw_cd': '申万行业',
            'market_cd': '市场代码',
            'list_dt': '上市日期',
            'bond_value': '纯债价值',
            'rating_cd': '外部评级',
            'option_value': '期权价值',
            'put_convert_price': '回售触发价',
            'force_redeem_price': '强赎触发价',
            'convert_amt_ratio': '转债市占比',
            'fund_rt': '机构持仓',
            'maturity_dt': '转股截止日期',
            'year_left': '剩余年限',
            'curr_iss_amt': '剩余市值(亿)',
            'volume': '成交额(万)',
            'svolume': '正股成交额',
            'turnover_rt': '换手率',
            'ytm_rt': '到期收益率(税前)',
            'put_ytm_rt': '回售收益',
            'last_time': '下载时间',
            'qstatus': '停牌提示',
            'sqflag': 'sqflag',
            'pb_flag': 'PB提示',
            'adj_cnt': '下修次数',
            'adj_scnt': '成功次数',
            'convert_price_valid': '转股生效',
            'convert_price_tips': '下修提示',
            'convert_cd_tip': '转股提示',
            'ref_yield_info': '转债提示',
            'adjusted': 'adjusted',
            'orig_iss_amt': '发行规模',
            'price_tips': '价格提示',
            'redeem_dt': '强赎日期',
            'real_force_redeem_price': '强赎价格',
            'option_tip': '期权提示',
            'unadj_cnt': '不下修次数',
            'adjust_remain_days': '下修剩余天数',
            'icons': '强赎提示',
            'theory_value': '理论价值',
            'deviation_degree': '理论偏离度',
            'short_estimate_put_dt': '预估回售日',
            'left_put_year': '回售剩余年限',
            'put_ytm_rt_tax': '回售税后收益',
            'volatility_rate': '正股年化波动率', 
        }
        ts = int(time.time() * 1000)
        url = f'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={ts}'
        data = {
            'fprice': '',
            'tprice': '',
            'curr_iss_amt': '',
            'volume': '',
            'svolume': '',
            'premium_rt': '',
            'ytm_rt': '',
            'rating_cd': '',
            'is_search': 'N',
            'btype': '',
            'listed': 'Y',
            'qflag': 'N',
            'sw_cd': '',
            'bond_ids': '',
            'rp': '50',
            'page': '0'
        }
        res = self.session.post(
            url=url,
            headers=self.headers,
            data=json.dumps(data)
        )
        data = res.json()
        data_list = []
        for item in data['rows']:
            data_list.append(item['cell'])
        df = pd.DataFrame(data_list)
        # 过滤退债
        df = df[df['price_tips'].str.contains('全价') & ~df['bond_nm'].str.contains('退债')]
        df.rename(columns=rename_dict, inplace=True)
        # 过滤停牌
        df = df[df['停牌提示'] != '03']
        today = datetime.today()
        df['上市日期'] = pd.to_datetime(df['上市日期'])
        df['上市天数'] = today - df['上市日期']
        return df
if __name__=='__main__':
    models=jsl_data_xg('19985619215','')
    models.login()
    print(models.get_convert_bond_detail(stock='123219'))
    df=models.get_all_connect_data()
    print(df)
    df.to_excel(r'数据.xlsx')