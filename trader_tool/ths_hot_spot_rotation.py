import pandas as pd
import json
import requests
class ths_hot_spot_rotation:
    def __init__(self):
        '''
        热点轮动
        '''
    def get_hist_hot_spot_rotation(self,type='行业板块',field='涨跌幅'):
        '''
        获取历史数据
        '''
        type_dict={'概念板块':'con','行业板块':"industry"}
        field_dict={'涨跌幅':'zf','5日涨跌幅':'zf5','上涨比例':"riseRate",'涨停家数':"riseLimCnt","主力流入":"zljlr"}
        url="https://eq.10jqka.com.cn/pick/block/block_hotspot/hotspot/v1/hot_block_list?"
        params={
            'type': type_dict[type],
            'field':field_dict[field],
        }
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }
        res=requests.get(url=url,params=params,headers=headers)
        text=res.json()
        status_msg=text['status_msg']
        data=pd.DataFrame()
        if status_msg=='ok':
            df=pd.DataFrame(text['data']['data_list'])
            df.index=df['date']
            df1=df.T
            df2=df1.drop(index='date')
            columns=df2.columns.tolist()
            for column in columns:
                df3=df2[column]
                df4=pd.DataFrame(df3)
                df5=pd.DataFrame(df4[column][0])
                try:
                    df5['info']=df5['name']+df5['info'].apply(lambda x:x[field_dict[field]])
                except:
                    df5['info']=df5['name']+df5['info'].apply(lambda x:x['zf'])
                data[column]=df5['info']
            return data
        else:
            data=pd.DataFrame()
            return data  
if __name__=='__main__':
    models=ths_hot_spot_rotation()
    df=models.get_hist_hot_spot_rotation(type='概念板块')
    df.to_excel(r'数据.xlsx')
    print(df)