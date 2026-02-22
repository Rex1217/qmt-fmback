import pywencai
import pandas as pd
from threading import Thread
import akshare as ak
class wencai_threading_data:
    def __init__(self,text='90天趋势向上,有涨停板,非st,人气排行,强势涨停',
                on=['股票简称','代码']):
        '''
        问财经条件选股合并系统，多线程
        问财多条件选股合并,有会员的不用管
        text多条件必须用英文的逗号隔开
        on提取的条件
        '''
        #获取市场股票
        self.text=text
        self.on=on
        self.data=ak.stock_individual_fund_flow_rank()
        self.code_dict=dict(zip(self.data['名称'],self.data['代码']))
        print('获取全市场数据完成###')
        self.data=self.data[['名称','代码']]
        self.data.columns=self.on
        self.query_list=self.text.split(',')
    def get_connect_wencai_data(self,query='90天趋势向上'):
        '''
        问财多条件选股合并,有会员的不用管
        '''
        try:
            df=pywencai.get(query=query,loop=True)[[self.on[0]]]
            df['代码']=df[self.on[0]].apply(lambda x:self.code_dict.get(x,None))
            self.data=pd.merge(self.data, df, how='inner', on=self.on)
            print('提取合并成功 {}'.format(query))
        except Exception as e:
            print(e)
            print('提取合并失败 {}'.format(query))
    def get_all_connect_wencai_data(self):
        '''
        多线程合并数据
        '''
        for query in self.query_list:
                t = Thread(target=self.get_connect_wencai_data, args=(query,))
                t.start()
                #t.join()
                t.join()
    def get_result(self):
        '''
        获取结果
        '''
        return self.data
if __name__=='__main__':
    '''
    测试
    '''
    data=wencai_threading_data(text='90天趋势向上,有涨停板,非st,人气排行')  
    data.get_all_connect_wencai_data()   
    df=data.get_result() 
    print(df)
    df.to_excel(r'数据.xlsx')


