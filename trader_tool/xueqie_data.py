import pandas as pd
import requests
import json
class xueqie_data:
    def __init__(self,cookie='cookiesu=241715400714727; device_id=a3ef10a376ef5247ffa076b3f60cda63; smidV2=20240511121735f94708a388b3849549dd32f49888adb60042a1a6f570c88a0; remember=1; xq_is_login=1; u=1342909666; s=cb127hrtpz; bid=f1b5e01be977a7023f9ec859cdf24ad4_lw1xly5z; __utmz=1.1715421398.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=8d2185ec88fc34490976cbe2eb4caf7d6961e32e; xqat=8d2185ec88fc34490976cbe2eb4caf7d6961e32e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEzNDI5MDk2NjYsImlzcyI6InVjIiwiZXhwIjoxNzE5MTk1Mzc4LCJjdG0iOjE3MTY2MDMzNzgxMjIsImNpZCI6ImQ5ZDBuNEFadXAifQ.Sjy6h4gQ8nX3P1QvfN8d1jaozlDCQ_z4fPU1gnU97hmcEbDlAQE9tZ5_SAB2uVHJgUvmXEKKlHPWhNHnipI404hz5I0AxAXAod1nAAXUu9xyRlpN5HvISph3snFPInKOrDYas6Pf7mtunhHXHvdiCtt0j__P2hOyA0VevN3Mqc34a6NJDh2yftTIXWpDVAI03hHo1izuEuA9Reld-7OX8H_KGfFGbIN0frJFfvR_KiTadHK_hJK4LafSetP71-RC1qgouIcB2Eb4tS_IANZ8G-ETk9Y-6DW2_SwffzEUiCNscRvGmzCMy9XPWA5413QphlGdfbgk2rN7enArOVx3Cw; xq_r_token=d8d877c6634c1dccc7472835539149f69c6f9f70; Hm_lvt_1db88642e346389874251b5a1eded6e3=1716392246,1716473979,1716554527,1716603379; acw_tc=276077ab17166051880926379e31d55708918c25a7b1b7778b05ec078e0cb6; __utma=1.694453535.1715421398.1715524198.1716605549.4; __utmc=1; __utmt=1; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=yLJiLZESXni8VXn3zlUOJUOfp16pud99AQIv/v5OtCn72W3NDQ3kBY3tY4OxOBlzf3eoH+ByDMs2DcwGjEhdMw%3D%3D; __utmb=1.2.10.1716605549; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1716605925',
    assembly_id='ZH3345503'):
        '''
       聚宽跟单
        cookie 用户的cookie
        assembly_id组合的id
        '''
        self.cookie=cookie
        self.assembly_id=assembly_id
    def get_headers(self):
        '''
        获取请求头
        '''
        headers={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br, zstd',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection':'keep-alive',
            'Cookie':self.cookie,
            'Host':'xueqiu.com',
            'Referer':'https://xueqiu.com/P/ZH3223683',
            'Sec-Ch-Ua':'"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':"Windows",
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            'X-Requested-With':'XMLHttpRequest'
        }
        return headers
    def get_the_latest_move(self,rb_id=''):
        '''
        获取最近调仓
        https://xueqiu.com/cubes/rebalancing/show_origin.json?rb_id=164306198&cube_symbol=ZH3223683
        '''
        url='https://xueqiu.com/cubes/rebalancing/show_origin.json?'
        headers=self.get_headers()
        params={
            'rb_id':rb_id,
            'cube_symbol':self.assembly_id
        }
        try:
            res=requests.get(url=url,headers=headers,params=params)
            text=res.json()
            stats=text['rebalancing']['status']
            if stats=='success':
                print('最近获取数据成功')
                result=text['rebalancing']['rebalancing_histories']
                df=pd.DataFrame(result)
                df['updated_at']=pd.to_datetime(df['updated_at'],unit='ms')
                return df
            else:
                print(text)
                print('最近获取数据失败检查cookie')
                df=pd.DataFrame()
                return df
        except Exception as e:
            print(e)
            df=pd.DataFrame()
            return df
    def get_hist_move(self):
        '''
        获取历史调仓
        https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH3223683&count=20&page=1
        '''
        url='https://xueqiu.com/cubes/rebalancing/history.json?'
        headers=self.get_headers()
        params={
            'cube_symbol':self.assembly_id,
            'count': '50',
            'page': '1',
        }
        try:
            res=requests.get(url=url,headers=headers,params=params)
            text=res.json()
            df=pd.DataFrame(text['list'])
            data=pd.DataFrame()
            for i in df['rebalancing_histories']:
                df1=pd.DataFrame(i)
                data=pd.concat([data,df1],ignore_index=True)
            return data
        except Exception as e:
            print(e,'cookie过期检查')
            df=pd.DataFrame()
            return df

if __name__=='__main__':
    '''
    获取数据
    '''
    trader=xueqie_data()
    df=trader.get_hist_move()
    print(df)
    df.to_excel(r'数据.xlsx')
    
    