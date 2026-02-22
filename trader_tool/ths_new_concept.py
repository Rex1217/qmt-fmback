import requests
import json
import pandas as pd
from datetime import datetime
import time
import time
import yagmail
import json
import random
import schedule
from datetime import  timedelta
class ths_new_concept:
    def __init__(self):
        '''
        同花顺新概念
        '''
        pass
    def date_to_unix_timestamp_ms(self,date='2024-02-27'):
        '''
        '''
        # 创建一个 datetime 对象，表示特定的时间
        text=date.split('-')
        year=int(text[0])
        moth=int(text[1])
        daily=int(text[-1])
        import datetime
        date_time = datetime.datetime(year, moth, daily, 0, 0, 0)

        # 转换为 Unix 时间戳（秒）
        unix_timestamp = time.mktime(date_time.timetuple())

        # 转换为 Unix 时间戳（毫秒）
        unix_timestamp_ms = int(unix_timestamp * 1000)

        return unix_timestamp_ms
    def seed_emial_qq_1(self,text='交易完成'):
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text1=json.loads(com)
        try:
            password=text1['qq掩码']
            seed_qq=text1['发送qq']
            yag = yagmail.SMTP(user='{}'.format(seed_qq), password=password, host='smtp.qq.com')
            m = text1['接收qq']
            text = text
            yag.send(to=m, contents=text, subject='邮件')
            print('邮箱发生成功')
        except:
            print('qq发送失败可能用的人多')
    def seed_dingding(self,msg='买卖交易成功,',access_token_list=['ab5d0a609429a786b9a849cefd5db60c0ef2f17f2ec877a60bea5f8480d86b1b']):
        access_token=random.choice(access_token_list)
        url='https://oapi.dingtalk.com/robot/send?access_token={}'.format(access_token)
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "text",  # 发送消息类型为文本
            "at": {
                #"atMobiles": reminders,
                "isAtAll": False,  # 不@所有人
            },
            "text": {
                "content": msg,  # 消息正文
            }
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        text=r.json()
        errmsg=text['errmsg']
        if errmsg=='ok':
                print('钉钉发生成功')
                return text
        else:
            print(text)
            return text
    def seed_wechat(self, msg='买卖交易成功,', access_token_list=[]):
        access_token=random.choice(access_token_list)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + access_token
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "text",  # 发送消息类型为文本
            "at": {
                # "atMobiles": reminders,
                "isAtAll": False,  # 不@所有人
            },
            "text": {
                "content": msg,  # 消息正文
            }
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        text = r.json()
        errmsg = text['errmsg']
        if errmsg == 'ok':
            print('wechat发生成功')
            return text
        else:
            print(text)
            return text
    def seed_emial_qq(self,text='交易完成,'):
        '''
        发生交易通知
        '''
        msg=text
        msg+=','
        with open('分析配置.json','r+',encoding='utf-8') as f:
            com=f.read()
        text=json.loads(com)
        access_token_list=text['钉钉账户token']
        seed_type=text['发送方式']
        if seed_type=='qq':
            self.seed_emial_qq_1(text=msg)
        elif seed_type=='微信':
            access_token_list_wx=text['微信账户token']
            self.seed_wechat(msg=msg,access_token_list=access_token_list_wx)
        else:
            self.seed_dingding(msg=msg,access_token_list=access_token_list)
    def get_individual_stocks_add_concept(self,date='2024-02-28'):
        '''
        获取个股添加的概念
        '''
        date=self.date_to_unix_timestamp_ms(date=date)
        data={"page_num":1,"page_size":100,"concept":"all","date":date,"tab_type":"all"}
        url='https://dq.10jqka.com.cn/fuyao/concept_express/concept_trends/v1/list'
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        status_code=text['status_code']
        if status_code==0:
            try:
                print('获取成功')
                df=pd.DataFrame(text['data']['concept_trends']['list'])
                df['concept']=df['concept'].apply(lambda x:x['name'])
                df['code']=df['stock'].apply(lambda x:x['code'])
                df['name']=df['stock'].apply(lambda x:x['name'])
                df['created_at']=pd.to_datetime(df['created_at'],unit='ms')
                df['发送状态']='未发送'
                return df
            except:
                df=pd.DataFrame()
                print('没有数据')
                return df
        else:
            df=pd.DataFrame()
            print('没有数据')
            return df
    def cacal_date(self,date='2024-02-29'):
        # 假设给定的时间是 "2022-01-01 12:00:00"
        given_time = date+' 12:00:00'
        # 将给定的时间转换为 datetime 对象
        dt = datetime.strptime(given_time, "%Y-%m-%d %H:%M:%S")
        # 减去一天的时间
        result = dt - timedelta(days=1)
        # 输出结果
        return str(result)[:10]
    def seed_info(self):
        '''
        发送信息
        '''
        date=str(datetime.now())[:10]
        date1=str(datetime.now())[:18]
        df=self.get_individual_stocks_add_concept(date=date)
        seed_log=pd.read_excel(r'发送记录.xlsx')
        try:
            columns=['reason','concept','created_at','news_url','code','name','发送状态']
            seed_log=seed_log[columns]
        except:
            pass
        if df.shape[0]>0:
            if seed_log.shape[0]>0:
                log_list=seed_log['reason'].tolist()
            else:
                log_list=[]
            i=0
            for reason,concept,created_at,news_url,code,name in zip(df['reason'],df['concept'],
                                    df['created_at'],df['news_url'],df['code'],df['name']):
                if reason in log_list:
                    print('{} {}已经发送'.format(datetime.now(),name))
                    text=''
                    text+='发现新增概念!\n'
                    text+='股票名称:{} {}\n'.format(name,code)
                    text+='新添加概念名称:{}\n'.format(concept)
                    text+='概念解析:{}\n'.format(reason)
                    text+='内容链接:{}\n'.format(news_url)
                    text+='建立时间:{}\n'.format(created_at)
                    text+='发送时间:{}\n'.format(date1)
                    print(text)
                else:
                    text=''
                    text+='发现新增概念!\n'
                    text+='股票名称:{} {}\n'.format(name,code)
                    text+='新添加概念名称:{}\n'.format(concept)
                    text+='概念解析:{}\n'.format(reason)
                    text+='内容链接:{}\n'.format(news_url)
                    text+='建立时间:{}\n'.format(created_at)
                    text+='发送时间:{}\n'.format(date1)
                    self.seed_emial_qq(text=text)
                    print(text)
                    df1=df[i:i+1]
                    df1['发送状态']='已经发送'
                    seed_log=pd.concat([seed_log,df1])
                    seed_log.to_excel(r'发送记录.xlsx')
                    i+=1
        else:
            print('{}没有新数据'.format(datetime.now()))
    def seed_info_test(self):
        '''
        发送信息
        '''
        date=str(datetime.now())[:10]
        date1=str(datetime.now())[:18]
        df=self.get_individual_stocks_add_concept(date=date)
        seed_log=pd.read_excel(r'发送记录.xlsx')
        try:
            columns=['reason','concept','created_at','news_url','code','name','发送状态']
            seed_log=seed_log[columns]
        except:
            pass
        if df.shape[0]>0:
            if seed_log.shape[0]>0:
                log_list=seed_log['reason'].tolist()
            else:
                log_list=[]
            i=0
            for reason,concept,created_at,news_url,code,name in zip(df['reason'],df['concept'],
                                    df['created_at'],df['news_url'],df['code'],df['name']):
                if reason in log_list:
                    print('{} {}已经发送'.format(datetime.now(),name))
                    text=''
                    text+='发现新增概念!\n'
                    text+='股票名称:{} {}\n'.format(name,code)
                    text+='新添加概念名称:{}\n'.format(concept)
                    text+='概念解析:{}\n'.format(reason)
                    text+='内容链接:{}\n'.format(news_url)
                    text+='建立时间:{}\n'.format(created_at)
                    text+='发送时间:{}\n'.format(date1)
                    self.seed_emial_qq(text=text)
                    print(text)
                else:
                    text=''
                    text+='发现新增概念!\n'
                    text+='股票名称:{} {}\n'.format(name,code)
                    text+='新添加概念名称:{}\n'.format(concept)
                    text+='概念解析:{}\n'.format(reason)
                    text+='内容链接:{}\n'.format(news_url)
                    text+='建立时间:{}\n'.format(created_at)
                    text+='发送时间:{}\n'.format(date1)
                    self.seed_emial_qq(text=text)
                    print(text)
                    df1=df[i:i+1]
                    df1['发送状态']='已经发送'
                    seed_log=pd.concat([seed_log,df1])
                    seed_log.to_excel(r'发送记录.xlsx')
                    i+=1
        else:
            print('{}没有新数据'.format(datetime.now()))
if __name__:
    with open('分析配置.json','r+',encoding='utf-8') as f:
        com=f.read()
    text=json.loads(com)
    models=ths_new_concept()
    print('开始程序*************************')
    test=text['是否测试发生']
    if test=='是':
        models.seed_info_test()
    else:
        seed_time=text['循环发生时间']
        print('每{}分钟推送一次****************'.format(seed_time))
        schedule.every(seed_time).minutes.do(models.seed_info)
        while True:
            schedule.run_pending()
            time.sleep(1)
        
