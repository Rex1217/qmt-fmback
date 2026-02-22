import requests
import pandas as pd
import json
from trader_tool.dfcf_etf_data import dfcf_etf_data
from tqdm import tqdm
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
from trader_tool.stock_data import stock_data
class etf_subscription:
    def __init__(self):
        '''
        ETF 申购
        '''
        self.dfcf_etf_data=dfcf_etf_data()
        self.stock_data=stock_data()
    def get_sh_fund_info(self,stock='513100'):
        '''
        获取上海基金的信息
        '''
        params={
            #'jsonCallBack': 'jsonpCallback94504258',
            'isPagination': 'false',
            'FUNDID2': stock,
            'sqlId': 'COMMON_SSE_CP_JJLB_ETFJJGK_GGSGSHQD_JBXX_C',
            #'_': '1736475617247',
        }
        url='https://query.sse.com.cn/commonQuery.do?'
        headers={
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'connection':'keep-alive',
            'host':'query.sse.com.cn',
            'referer':'https://www.sse.com.cn/',
            'sec-ch-ua':'"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'script',
            'sec-fetch-mode':'no-cors',
            'sec-fetch-site':'same-site',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        df=pd.DataFrame(text['result'])
        columns=['净值','交易日','_','最小申购赎回(万份)',
                '_','赎回上限(万份)','前一交易日','_',
                "基金公司",'_','_','_','_',
                '_','前最小申购,赎回单位净值','基金代码','_',
                "_",'申购上限(万份)']
        df.columns=columns
        del df['_']
        for i in df.columns.tolist():
            df[i]=df[i].apply(lambda x: str(x).replace('￥',''))
        df['申购上限(万份)']=df['申购上限(万份)'].apply(lambda x: 100000000000000000000000 if x=='无' else x)
        df['赎回上限(万份)']=df['赎回上限(万份)'].apply(lambda x: 100000000000000000000000 if x=='无' else x)
        df['赎回上限(万份)']=pd.to_numeric(df['赎回上限(万份)'])
        df['申购上限(万份)']=pd.to_numeric(df['申购上限(万份)'])
        df['最小申购赎回(万份)']=pd.to_numeric(df['最小申购赎回(万份)'])
        df['净值']=pd.to_numeric(df['净值'])
        df['赎回上限(万份)']=df['赎回上限(万份)']/10000
        df['申购上限(万份)']=df['申购上限(万份)']/10000
        df['最小申购赎回(万份)']=df['最小申购赎回(万份)']/10000
        df['申购资金']=df['最小申购赎回(万份)']*df['净值']*1.2
        return df
    def get_all_sh_fund_info(self,stock_list=['513100']):
        '''
        获取全部上海基金的信息
        '''
        all_df=self.dfcf_etf_data.get_all_etf_data_1()
        all_df['基金代码']= all_df['基金代码'].astype(str)
        #选择上海的基金
        all_df['交易市场']=all_df['基金代码'].apply(lambda x: '上海' if str(x)[0]=='5' else '深圳')
        all_df=all_df[['基金代码','基金名称','价格','前收盘价','溢价率','交易市场','涨跌幅','成交量']]
        all_df=all_df[all_df['交易市场']=='上海']
        all_df['选择']=all_df['基金代码'].apply(lambda x: '是' if x in stock_list else '不是')
        all_df= all_df[all_df['选择']=='是']
        data=pd.DataFrame()
        stock_list=all_df['基金代码'].tolist()
        if len(stock_list)>0:
            for  i in tqdm(range(len(stock_list))):
                    stock=stock_list[i]
                    try:
                        stock=str(stock)
                        df=self.get_sh_fund_info(stock=stock)
                        data=pd.concat([data,df],ignore_index=True)
                    
                    except Exception as e:
                        print(e,'{}基金基本信息有问题'.format(stock))
                    
            result=pd.merge(all_df,data,on='基金代码')
            result['前收盘价']=pd.to_numeric(result['前收盘价'])
            result['净值']=pd.to_numeric(result['净值'])
            result['前一溢价率']=((result['前收盘价']-result['净值'])/result['净值'])*100
            result=result[['交易日','基金代码','基金名称','价格','前收盘价','前一溢价率','溢价率',
                        '赎回上限(万份)','申购上限(万份)','最小申购赎回(万份)','申购资金']]
            return result
        else:
            return data
    def get_all_sh_fund_data(self):
        '''
        获取全部上海的数据
        '''
        all_df=self.dfcf_etf_data.get_all_etf_data_1()
        all_df['基金代码']= all_df['基金代码'].astype(str)
        #选择上海的基金
        all_df['交易市场']=all_df['基金代码'].apply(lambda x: '上海' if str(x)[0]=='5' else '深圳')
        all_df=all_df[['基金代码','基金名称','价格','前收盘价','溢价率','交易市场','涨跌幅','成交量']]
        all_df=all_df[all_df['交易市场']=='上海']
        stock_list=all_df['基金代码'].tolist()
        result=self.get_all_sh_fund_info(stock_list=stock_list)
        return result
    def get_sh_wp_fund_info(self):
        '''
        获取上海外盘
        '''
        all_df=self.dfcf_etf_data.get_all_etf_data_1()
        all_df['基金代码']= all_df['基金代码'].astype(str)
        select_list=['纳斯达克','纳指','标普','道琼斯','美国','法国',
                     '德国','印度','沙特','亚太','日本','日经']
        data=pd.DataFrame()
        for select in select_list:
            all_df['选择']=all_df['基金名称'].apply(lambda x: '是' if select in x else '不是')
            df1=all_df[all_df['选择']=='是']
            data=pd.concat([data,df1])
        stock_list=data['基金代码'].tolist()
        result=self.get_all_sh_fund_info(stock_list=stock_list)
        return result
    def get_sz_fund_info(self,stock='159941',date='20250110'):
        '''
        获取深圳基金的信息
        '''
        url='https://reportdocs.static.szse.cn/files/text/etf/ETF{}{}.txt?'.format(stock,date)
        res=requests.get(url=url)
        text=res.text
        text=text.split('-------------------------------------------------------------------------------------------------------------------------------------------------------')
        data_dict={}
        for i in text:
            i=i.replace('\r\n','').replace('\r','').replace('\n','').lstrip().rstrip()
            j=i.replace(' ',',').replace('：,,',':').split(',')
            for m in j:
                if ':' in m:
                    n=m.split(':')
                    data_dict[n[0]]=[n[-1]]
        df=pd.DataFrame(data_dict)
        df['当天净赎回的基金份额上限']=df['当天净赎回的基金份额上限'].apply(lambda x: 100000000000000000000000 if x=='不设上限' else x)
        df['最小申购、赎回单位']=df['最小申购、赎回单位'].apply(lambda x: 100000000000000000000000 if x=='不设上限' else x)
        df['当天净申购的基金份额上限']=df['当天净申购的基金份额上限'].apply(lambda x: 100000000000000000000000 if x=='不设上限' else x)
        data=pd.DataFrame()
        data['净值']=[float(df['基金份额净值'].tolist()[-1].replace('元',''))]
        data['交易日']=[date]
        data['最小申购赎回(万份)']=[float(str(df['最小申购、赎回单位'].tolist()[-1]).replace('份',''))/10000]
        data['赎回上限(万份)']=[float(str(df['当天净赎回的基金份额上限'].tolist()[-1]).replace('份',''))/10000]
        data['前一交易日']=[date]
        data['基金公司']=[df['基金管理公司名称'].tolist()[-1]]
        data['前最小申购,赎回单位净值']=[float(df['最小申购、赎回单位资产净值'].tolist()[-1].replace('元',''))]
        data['基金代码']=[df['基金代码'].tolist()[-1]]
        data['申购上限(万份)']=[float(str(df['当天净申购的基金份额上限'].tolist()[-1]).replace('份',''))/10000]
        data['申购资金']=data['最小申购赎回(万份)']*data['净值']*1.2
        return data
    def get_all_sz_fund_info(self,stock_list=['159941'],date='20250110'):
        '''
        获取全部深圳基金的信息
        '''
        all_df=self.dfcf_etf_data.get_all_etf_data_1()
        all_df['基金代码']= all_df['基金代码'].astype(str)
        #选择上海的基金
        all_df['交易市场']=all_df['基金代码'].apply(lambda x: '上海' if str(x)[0]=='5' else '深圳')
        all_df=all_df[['基金代码','基金名称','价格','前收盘价','溢价率','交易市场','涨跌幅','成交量']]
        all_df=all_df[all_df['交易市场']=='深圳']
        all_df['选择']=all_df['基金代码'].apply(lambda x: '是' if x in stock_list else '不是')
        all_df= all_df[all_df['选择']=='是']
        data=pd.DataFrame()
        stock_list=all_df['基金代码'].tolist()
        if len(stock_list)>0:
            for  i in tqdm(range(len(stock_list))):
                    stock=stock_list[i]
                    try:
                        stock=str(stock)
                        df=self.get_sz_fund_info(stock=stock,date=date)
                        data=pd.concat([data,df],ignore_index=True)
                    
                    except Exception as e:
                        print(e,'{}基金基本信息有问题'.format(stock))
                    
                    
            result=pd.merge(all_df,data,on='基金代码')
            result['前收盘价']=pd.to_numeric(result['前收盘价'])
            result['净值']=pd.to_numeric(result['净值'])
            result['前一溢价率']=((result['前收盘价']-result['净值'])/result['净值'])*100
            result=result[['交易日','基金代码','基金名称','价格','前收盘价','前一溢价率','溢价率',
                        '赎回上限(万份)','申购上限(万份)','最小申购赎回(万份)','申购资金']]
            return result
        else:
            return data
    def get_all_sz_fund_data(self):
        '''
        获取全部深圳的数据
        '''
        date=self.stock_data.get_trader_date_list()[-1]
        date=''.join(str(date).split('-'))
        all_df=self.dfcf_etf_data.get_all_etf_data_1()
        all_df['基金代码']= all_df['基金代码'].astype(str)
        #选择上海的基金
        all_df['交易市场']=all_df['基金代码'].apply(lambda x: '上海' if str(x)[0]=='5' else '深圳')
        all_df=all_df[['基金代码','基金名称','价格','前收盘价','溢价率','交易市场','涨跌幅','成交量']]
        all_df=all_df[all_df['交易市场']=='深圳']
        stock_list=all_df['基金代码'].tolist()
        result=self.get_all_sz_fund_info(stock_list=stock_list,date=date)
        return result
    def get_sz_wp_fund_info(self):
        '''
        获取深圳外盘
        '''
        date=self.stock_data.get_trader_date_list()[-1]
        date=''.join(str(date).split('-'))
        all_df=self.dfcf_etf_data.get_all_etf_data_1()
        all_df['基金代码']= all_df['基金代码'].astype(str)
        select_list=['纳斯达克','纳指','标普','道琼斯','美国','法国',
                     '德国','印度','沙特','亚太','日本','日经']
        data=pd.DataFrame()
        for select in select_list:
            all_df['选择']=all_df['基金名称'].apply(lambda x: '是' if select in x else '不是')
            df1=all_df[all_df['选择']=='是']
            data=pd.concat([data,df1])
        stock_list=data['基金代码'].tolist()
        result=self.get_all_sz_fund_info(stock_list=stock_list,date=date)
        return result
    def get_all_maker_wp_fund_data(self):
        '''
        获取全市场外盘的数据
        '''
        data=pd.DataFrame()
        df_sz=self.get_sz_wp_fund_info()
        df_sh=self.get_sh_wp_fund_info()
        data=pd.concat([data,df_sh],ignore_index=True)
        data=pd.concat([data,df_sz],ignore_index=True)
        data=data.sort_values(by='溢价率',ascending=True)
        return data
    def get_all_maker_fund_data(self):
        '''
        获取全市场的数据
        '''
        data=pd.DataFrame()
        df_sz=self.get_all_sz_fund_data()
        df_sh=self.get_all_sh_fund_data()
        data=pd.concat([data,df_sh],ignore_index=True)
        data=pd.concat([data,df_sz],ignore_index=True)
        data=data.sort_values(by='溢价率',ascending=True)
        return data
if __name__=='__main__':
    data=etf_subscription()
    df=data.get_all_maker_wp_fund_data()
    print(df)
    df.to_excel(r'数据.xlsx')
   



