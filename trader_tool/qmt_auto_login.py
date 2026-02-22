import time
import pyautogui as pa
import pywinauto as pw
import schedule
import yagmail
import requests
import json
import random
from datetime import datetime
class qmt_auto_login:
    '''
    qmt自动登录
    '''
    def __init__(self,connect_path = r'D:\国金证券QMT交易端\bin.x64\XtItClient.exe',
                user = '',
                password = '',
                seed_type='qq',
                seed_qq='1752515969@qq.com',
                qq_paasword='jgyhavzupyglecaf',
                access_token_list=['1029762153@qq.com']):
        '''
        connect_path qmt安装路径
        user股票账户
        password密码
        seed_type发送方式 wx微信,qq qq,dd钉钉
        seed_qq发送qq
        qq_paasword QQ掩码
        access_token_list账户token
        特别在提醒，在服务器运行的qmt，退出服务器需要点击文件夹下面的退出保持链接bat退出服务器
        '''
        self.connect_path=connect_path
        self.user=user
        self.password=password
        self.app = None
        self.seed_type=seed_type
        self.access_token_list=access_token_list
        self.seed_qq=seed_qq
        self.qq_paasword=qq_paasword
    def seed_dingding(self,msg='买卖交易成功,',access_token_list=['ab5d0a609429a786b9a849cefd5db60c0ef2f17f2ec877a60bea5f8480d86b1b']):
        '''
        发送钉钉
        '''
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
    def get_seed_qq_test(self,text='交易完成',seed_qq='1752515969@qq.com',qq_paasword='jgyhavzupyglecaf',re_qq='1029762153@qq.com'):
        '''
        发送qq，可以自己给自己发
        text发送内容，支持表格文字
        see_qq发送QQ
        qq_pasword发送qq的掩码
        re_qq接收信息QQ
        '''
        try:
            yag = yagmail.SMTP(user=seed_qq, password=qq_paasword, host='smtp.qq.com')
            text = text
            yag.send(to=re_qq, contents=text, subject='邮件')
            print('qq发送完成')
        except:
            print('qq发送失败')
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
    def seed_info(self,text=''):
        '''
        发送信息
        '''
        
        if self.seed_type=='qq':
            self.get_seed_qq_test(text=text,seed_qq=self.seed_qq,qq_paasword=self.qq_paasword,
                                  re_qq=self.access_token_list[-1])
        elif self.seed_type=='wx':
            self.seed_wechat(msg=text,access_token_list=self.access_token_list)
        elif self.seed_type=='dd':
            self.seed_dingding(msg=text,access_token_list=self.access_token_list)
        else:
            self.get_seed_qq_test(text=text,seed_qq=self.seed_qq,qq_paasword=self.qq_paasword,
                                  re_qq=self.access_token_list[-1])
    def send_vx_msg(self,msg):
        print(msg)
    def login(self):
        test_app = pw.application.Application(backend="uia")
        try:
            # 获取test.exe的process id
            proc_id = pw.application.process_from_module("XtItClient.exe")
            print('proc_id:', proc_id)

            # 关联应用程序进程
            self.app = test_app.connect(process=proc_id)
            self.app.top_window().dump_tree()
            self.app.kill()
        except Exception:
            pass
        # if app is None:
        self.app = pw.Application(backend='uia').start(self.connect_path, timeout=10)
        time.sleep(5)
        self.app.top_window()
        time.sleep(5)
        pa.typewrite(self.user)
        time.sleep(1)
        pa.hotkey('tab')
        time.sleep(1)
        pa.typewrite(self.password)
        time.sleep(1)
        pa.hotkey('enter')
        time.sleep(3)
        # 判断是否成功 WindowSpecification
        login_window = self.app.window_(title="国金证券QMT交易端 1.0.0.29456", control_type="Pane")
        try:
            login_window.wait('visible', timeout=1)
            text='{} qmt登录失败'.format(datetime.now())
            self.seed_info(text=text)
            self.send_vx_msg('登录失败！')
        except (pw.findwindows.ElementNotFoundError, pw.timings.TimeoutError):
            text='{} qmt登录成功'.format(datetime.now())
            self.seed_info(text=text)
            print('登录成功！')
    def kill(self):
        '''
        退出程序
        '''
        self.app.kill()
if __name__=='__main__':
    models=qmt_auto_login(connect_path = r'D:\国金证券QMT交易端\bin.x64\XtItClient.exe',
                user = '',
                password = '',
                seed_type='qq',
                seed_qq='1752515969@qq.com',
                qq_paasword='jgyhavzupyglecaf',
                access_token_list=['1029762153@qq.com'])
    test='True'
    if test=='True':
        print('测试登录')
        models.login()
        models.kill()
    else:
        #定时登录
        schedule.every().day.at('{}'.format('09:10')).do(models.login)
        #定时退出
        schedule.every().day.at('{}'.format('15:3')).do(models.kill)
    while True:
        schedule.run_pending()
        time.sleep(1)
    