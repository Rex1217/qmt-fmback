#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/3 20:18
Desc: 东方财富-LOF 行情
https://quote.eastmoney.com/center/gridlist.html#fund_lof
https://quote.eastmoney.com/sz166009.html
"""
from functools import lru_cache
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from lxml import etree
class lof_fund_data:
    def __init__(self):
        '''
        lof基金数据
        '''
        pass
    @lru_cache()
    def _fund_lof_code_id_map_em(self) -> dict:
        """
        东方财富-LOF 代码和市场标识映射
        https://quote.eastmoney.com/center/gridlist.html#fund_lof
        :return: LOF 代码和市场标识映射
        :rtype: pandas.DataFrame
        """
        url = "https://2.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "5000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0404,b:MK0405,b:MK0406,b:MK0407",
            "fields": "f12,f13",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_dict = dict(zip(temp_df["f12"], temp_df["f13"]))
        return temp_dict


    def fund_lof_spot_em(self) -> pd.DataFrame:
        """
        东方财富-LOF 实时行情
        https://quote.eastmoney.com/center/gridlist.html#fund_lof
        :return: LOF 实时行情
        :rtype: pandas.DataFrame
        """
        url = "https://88.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "5000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0404,b:MK0405,b:MK0406,b:MK0407",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "_": "1672806290972",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_df.rename(
            columns={
                "f12": "代码",
                "f14": "名称",
                "f2": "最新价",
                "f4": "涨跌额",
                "f3": "涨跌幅",
                "f5": "成交量",
                "f6": "成交额",
                "f17": "开盘价",
                "f15": "最高价",
                "f16": "最低价",
                "f18": "昨收",
                "f8": "换手率",
                "f21": "流通市值",
                "f20": "总市值",
            },
            inplace=True,
        )
        temp_df = temp_df[
            [
                "代码",
                "名称",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "成交量",
                "成交额",
                "开盘价",
                "最高价",
                "最低价",
                "昨收",
                "换手率",
                "流通市值",
                "总市值",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
        temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
        temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
        temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        return temp_df


    def fund_lof_hist_em(self,
        symbol: str = "166009",
        period: str = "daily",
        start_date: str = "19700101",
        end_date: str = "20500101",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        东方财富-LOF 行情
        https://quote.eastmoney.com/sz166009.html
        :param symbol: LOF 代码
        :type symbol: str
        :param period: choice of {'daily', 'weekly', 'monthly'}
        :type period: str
        :param start_date: 开始日期
        :type start_date: str
        :param end_date: 结束日期
        :type end_date: str
        :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
        :type adjust: str
        :return: 每日行情
        :rtype: pandas.DataFrame
        """
        code_id_dict = self._fund_lof_code_id_map_em()
        adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
        period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "klt": period_dict[period],
            "fqt": adjust_dict[adjust],
            "secid": f"{code_id_dict[symbol]}.{symbol}",
            "beg": start_date,
            "end": end_date,
            "_": "1623766962675",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        if not (data_json["data"] and data_json["data"]["klines"]):
            return pd.DataFrame()
        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
        temp_df.columns = [
            "日期",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["日期"])
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        return temp_df


    def fund_lof_hist_min_em(self,
        symbol: str = "166009",
        start_date: str = "1979-09-01 09:32:00",
        end_date: str = "2222-01-01 09:32:00",
        period: str = "5",
        adjust: str = "",
    ) -> pd.DataFrame:
        """
        东方财富-LOF 分时行情
        https://quote.eastmoney.com/sz166009.html
        :param symbol: LOF 代码
        :type symbol: str
        :param start_date: 开始日期时间
        :type start_date: str
        :param end_date: 结束日期时间
        :type end_date: str
        :param period: choice of {"1", "5", "15", "30", "60"}
        :type period: str
        :param adjust: choice of {'', 'qfq', 'hfq'}
        :type adjust: str
        :return: 每日分时行情
        :rtype: pandas.DataFrame
        """
        code_id_dict = self._fund_lof_code_id_map_em()
        adjust_map = {
            "": "0",
            "qfq": "1",
            "hfq": "2",
        }
        if period == "1":
            url = "https://push2his.eastmoney.com/api/qt/stock/trends2/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "ndays": "5",
                "iscr": "0",
                "secid": f"{code_id_dict[symbol]}.{symbol}",
                "_": "1623766962675",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(
                [item.split(",") for item in data_json["data"]["trends"]]
            )
            temp_df.columns = [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "最新价",
            ]
            temp_df.index = pd.to_datetime(temp_df["时间"])
            temp_df = temp_df[start_date:end_date]
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
            temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
            temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
            temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
            return temp_df
        else:
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "klt": period,
                "fqt": adjust_map[adjust],
                "secid": f"{code_id_dict[symbol]}.{symbol}",
                "beg": "0",
                "end": "20500000",
                "_": "1630930917857",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            temp_df = pd.DataFrame(
                [item.split(",") for item in data_json["data"]["klines"]]
            )
            temp_df.columns = [
                "时间",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "振幅",
                "涨跌幅",
                "涨跌额",
                "换手率",
            ]
            temp_df.index = pd.to_datetime(temp_df["时间"])
            temp_df = temp_df[start_date:end_date]
            temp_df.reset_index(drop=True, inplace=True)
            temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
            temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
            temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
            temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
            temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
            temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
            temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
            temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
            temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
            temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
            temp_df["时间"] = pd.to_datetime(temp_df["时间"]).astype(str)
            temp_df = temp_df[
                [
                    "时间",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "涨跌幅",
                    "涨跌额",
                    "成交量",
                    "成交额",
                    "振幅",
                    "换手率",
                ]
            ]
            return temp_df
    def get_lof_fund_info_data(self,stock='501225'):
        '''
        获取ETF基本信息
        '''
        trader_info=self.get_lof_fund_trader_data(stock=stock)
        stats=trader_info['申购状态'].tolist()[-1]
        spot=trader_info['申购起点'].tolist()[-1]
        max_value=trader_info['申购限额'].tolist()[-1]
        stock_1=stock
        headers={
                'Cookie':'cookiesu=241715400714727; device_id=a3ef10a376ef5247ffa076b3f60cda63; remember=1; xq_is_login=1; u=1342909666; s=cb127hrtpz; bid=f1b5e01be977a7023f9ec859cdf24ad4_lw1xly5z; xq_a_token=8d2185ec88fc34490976cbe2eb4caf7d6961e32e; xqat=8d2185ec88fc34490976cbe2eb4caf7d6961e32e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEzNDI5MDk2NjYsImlzcyI6InVjIiwiZXhwIjoxNzE5MTk1Mzc4LCJjdG0iOjE3MTY2MDMzNzgxMjIsImNpZCI6ImQ5ZDBuNEFadXAifQ.Sjy6h4gQ8nX3P1QvfN8d1jaozlDCQ_z4fPU1gnU97hmcEbDlAQE9tZ5_SAB2uVHJgUvmXEKKlHPWhNHnipI404hz5I0AxAXAod1nAAXUu9xyRlpN5HvISph3snFPInKOrDYas6Pf7mtunhHXHvdiCtt0j__P2hOyA0VevN3Mqc34a6NJDh2yftTIXWpDVAI03hHo1izuEuA9Reld-7OX8H_KGfFGbIN0frJFfvR_KiTadHK_hJK4LafSetP71-RC1qgouIcB2Eb4tS_IANZ8G-ETk9Y-6DW2_SwffzEUiCNscRvGmzCMy9XPWA5413QphlGdfbgk2rN7enArOVx3Cw; xq_r_token=d8d877c6634c1dccc7472835539149f69c6f9f70; Hm_lvt_1db88642e346389874251b5a1eded6e3=1716649591,1716706677,1716775334,1716779232; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1716779976',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
            }
        try:
            url='https://stock.xueqiu.com/v5/stock/quote.json?'
            stock='SZ'+stock_1
            params={
                'symbol': stock,
                'extend': 'detail'
            }
            res=requests.get(url=url,params=params,headers=headers)
            text=res.json()
            data=text['data']['quote']
            data_keys=list(data.keys())
            data_value=list(data.values())
            df=pd.DataFrame(data_value)
            df=df.T
            df.columns=data_keys
            #df['套利']=df['premium_rate'].apply(lambda x: '可以套利' if x>=2 else '不可套利')
            df.rename(columns={"code":"代码","volume":"成交量",
                "amount":"成交额","turnover_rate":"换手率","current":"市价","unit_nav":"单位净值","name":"名称",
                "total_shares":"基金份额","premium_rate":"溢价率","market_capital":"资产净值","found_date":"建立时间"},inplace=True)
            df['申购状态']=stats
            df['申购起点']=spot
            df['申购限额']=max_value
            select_columns=['代码',"名称",'市价','溢价率','申购状态','申购起点','申购限额',"单位净值","成交量","成交额",'换手率',"基金份额","资产净值",'建立时间']
            df=df[select_columns]
            df['建立时间']=pd.to_datetime(df['建立时间'],unit='ms')
            return df
        except:
            try:
                url='https://stock.xueqiu.com/v5/stock/quote.json?'
                stock='SH'+stock_1
                params={
                    'symbol': stock,
                    'extend': 'detail'
                }
                res=requests.get(url=url,params=params,headers=headers)
                text=res.json()
                data=text['data']['quote']
                data_keys=list(data.keys())
                data_value=list(data.values())
                df=pd.DataFrame(data_value)
                df=df.T
                df.columns=data_keys
                #df['套利']=df['premium_rate'].apply(lambda x: '可以套利' if x>=2 else '不可套利')
                df.rename(columns={"code":"代码","volume":"成交量",
                    "amount":"成交额","turnover_rate":"换手率","current":"市价","unit_nav":"单位净值","name":"名称",
                    "total_shares":"基金份额","premium_rate":"溢价率","market_capital":"资产净值","found_date":"建立时间"},inplace=True)
                df['申购状态']=stats
                df['申购起点']=spot
                df['申购限额']=max_value
                select_columns=['代码',"名称",'市价','溢价率','申购状态','申购起点','申购限额',"单位净值","成交量","成交额",'换手率',"基金份额","资产净值",'建立时间']
                df=df[select_columns]
                df['建立时间']=pd.to_datetime(df['建立时间'],unit='ms')
                return df
            except:
                df=pd.DataFrame()
                print('{}获取数据有问题'.format(stock))
                return df
    def get_all_lof_fund_info_data(self):
        '''
        获取全部lof基金数据
        '''
        df=self.fund_lof_spot_em()
        data=pd.DataFrame()
        stock_list=df['代码'].tolist()
        for i in tqdm(range(len(stock_list))):
            stock=stock_list[i]
            df=self.get_lof_fund_info_data(stock=stock)
            data=pd.concat([data,df],ignore_index=True)
        return data
    def get_lof_fund_trader_data(self,stock='501225'):
        '''
        获取lof基金的交易数据
        '''
        url='https://fundf10.eastmoney.com/jjfl_{}.html'.format(stock)
        df=pd.read_html(url)
        df1=df[1]
        df2=df[2]
        data=pd.DataFrame()
        try:
            data['申购状态']=[df1[1].tolist()[0]]
            data['申购起点']=[df2[1].tolist()[0]]
            data['申购限额']=[df2[5].tolist()[0]]
        except:
            print("{}数据有问题".format(stock))
            data=pd.DataFrame()
            data['申购状态']=[None]
            data['申购起点']=[None]
            data['申购限额']=[None]
        return data
    def get_hist_yly_data(self,stock='160632'):
        '''
        获取历史溢价率
        '''
        url='https://www.jisilu.cn/data/lof/hist_list/{}?'.format(stock)
        params={
            '___jsl':'LST___t=1710309287496'
        }
        data={
            'rp': '500',
            'page': '1'
        }
        res=requests.post(url=url,params=params,data=data)
        text=res.json()
        df=pd.DataFrame(text['rows'])
        cell=df['cell']
        data_list=[]
        for i in cell:
            data_list.append(list(i.values()))
        df=pd.DataFrame(data_list)
        df.columns=['代码','时间','收盘价','_','净值','_','估值','_','误差',
                    '溢价率','份额(万份)',"份额变得(万份)","份额涨跌幅",'指数涨跌幅']
        del df['_']
        return df
if __name__ == "__main__":
    models=lof_fund_data()
    df=models.fund_lof_spot_em()
    print(df)
    '''
    fund_lof_spot_em_df = models.fund_lof_spot_em()
    print(fund_lof_spot_em_df)
    fund_lof_hist_em_df = models.fund_lof_hist_em(
        symbol="166009",
        period="daily",
        start_date="20000101",
        end_date="20230703",
        adjust="",
    )
    print(fund_lof_hist_em_df)

    fund_lof_hist_qfq_em_df = models.fund_lof_hist_em(
        symbol="166009",
        period="daily",
        start_date="20000101",
        end_date="20230703",
        adjust="qfq",
    )
    print(fund_lof_hist_qfq_em_df)

    fund_lof_hist_em_df = models.fund_lof_hist_em(
        symbol="166009",
        period="daily",
        start_date="20000101",
        end_date="20230703",
        adjust="hfq",
    )
    print(fund_lof_hist_em_df)

    fund_lof_hist_min_em_df = models.fund_lof_hist_min_em(
        symbol="166009",
        period="5",
        adjust="hfq",
        start_date="2023-07-01 09:32:00",
        end_date="2023-07-04 14:40:00",
    )
    print(fund_lof_hist_min_em_df)
    '''
