import requests
import pandas as pd
import json
class xueqiu_assembly:
    def __init__(self,cookie='cookiesu=241715400714727; device_id=a3ef10a376ef5247ffa076b3f60cda63; remember=1; xq_is_login=1; u=1342909666; s=cb127hrtpz; bid=f1b5e01be977a7023f9ec859cdf24ad4_lw1xly5z; xq_a_token=8d2185ec88fc34490976cbe2eb4caf7d6961e32e; xqat=8d2185ec88fc34490976cbe2eb4caf7d6961e32e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjEzNDI5MDk2NjYsImlzcyI6InVjIiwiZXhwIjoxNzE5MTk1Mzc4LCJjdG0iOjE3MTY2MDMzNzgxMjIsImNpZCI6ImQ5ZDBuNEFadXAifQ.Sjy6h4gQ8nX3P1QvfN8d1jaozlDCQ_z4fPU1gnU97hmcEbDlAQE9tZ5_SAB2uVHJgUvmXEKKlHPWhNHnipI404hz5I0AxAXAod1nAAXUu9xyRlpN5HvISph3snFPInKOrDYas6Pf7mtunhHXHvdiCtt0j__P2hOyA0VevN3Mqc34a6NJDh2yftTIXWpDVAI03hHo1izuEuA9Reld-7OX8H_KGfFGbIN0frJFfvR_KiTadHK_hJK4LafSetP71-RC1qgouIcB2Eb4tS_IANZ8G-ETk9Y-6DW2_SwffzEUiCNscRvGmzCMy9XPWA5413QphlGdfbgk2rN7enArOVx3Cw; xq_r_token=d8d877c6634c1dccc7472835539149f69c6f9f70; Hm_lvt_1db88642e346389874251b5a1eded6e3=1717120878,1717230932,1717317518,1717469934; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1717470263'):
        '''
        控制雪球组合
        '''
        self.cookie=cookie
    def get_headers(self):
        '''
        获取请求头
        '''
        headers={
            'Accept-Encoding':'gzip, deflate, br, zstd',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie':self.cookie,
            'Origin':'https://xueqiu.com',
            'Priority':'u=1, i',
            'Referer':'https://xueqiu.com/',
            'Sec-Ch-Ua':'"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':"Windows",
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        return headers
    def get_all_user_assembly(self):
        '''
        获取全部的自己的组合
        '''
        data={
            'size': '1000',
            'category': '3',
            'pid': '-120',
        }
        url='https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?'
        headers=self.get_headers()
        try:
            res=requests.get(url=url,params=data,headers=headers)
            text=res.json()
            error_code=text['error_code']
            error_description=text['error_description']
            if error_code==0:
                print('获取全部的组合成功')
                df=pd.DataFrame(text['data']['stocks'])
                return True,df
            else:
                print('获取全部的组合失败')
                print(error_code,error_description)
                return False,''
        except Exception as e:
            print(e)
            print('获取全部的组合失败')
            return False,''
if __name__=='__main__':
    models=xueqiu_assembly()
    print(models.get_all_user_assembly())
