import pandas as pd
import numpy as np
import requests
import json
import datetime
import math
import time
import requests
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class seed_trader_info:
	'''
	法码发送交易信号
	作者:xms_quants1
	'''
	def __init__(self,
			seed_type='企业微信',
			sender_email = "1029762153@qq.com",
			receiver_email = "1029762153@qq.com",
			password = "jjfgdhklgguebdje",
			dd_token_list=[''],
			wx_token_list=['']):
		'''
		seed_type发送方式 企业微信,QQ,钉钉
		sender_email发送qq
		password QQ掩码
		receiver_email接受qq
		dd_token_list钉钉机器人token
		wx_token_list 企业微信token
		'''
		self.seed_type=seed_type
		self.sender_email=sender_email
		self.receiver_email=receiver_email
		self.password=password
		self.dd_token_list=dd_token_list
		self.wx_token_list=wx_token_list
	def send_simple_email(self,msg='测试'):
		# 邮件配置
		sender_email = self.sender_email
		receiver_email = self.receiver_email
		password = self.password 
		# 创建邮件内容
		message = MIMEMultipart()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = "交易通知"
			
		# 邮件正文
		body =msg
		message.attach(MIMEText(body, "plain"))
		# 发送邮件
		try:
			# 连接SMTP服务器（以Gmail为例）
			server = smtplib.SMTP("smtp.qq.com", 587)
			server.starttls()  # 启用安全连接
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message.as_string())
			print("邮件发送成功！")
		except Exception as e:
			print(e,'邮箱发送失败')
	def seed_dingding(self,msg='买卖交易成功,'):
		'''
		发送钉钉
		'''
		access_token=random.choice(self.dd_token_list)
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
	def seed_wechat(self, msg='买卖交易成功,'):
		'''
		发送企业微信
		'''
		access_token=random.choice(self.wx_token_list)
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
	def seed_trader_info(self,msg=''):
		'''
		发送信息
		'''
		if self.seed_type=='QQ':
			self.send_simple_email(msg=msg)
		elif self.seed_type=='企业微信':
			self.seed_wechat(msg=msg)
		elif self.seed_type=='钉钉':
			self.seed_dingding(msg=msg)
		else:
			self.send_simple_email(msg=msg)
class xg_jq_data:
	def __init__(self,url='http://124.220.32.224',
		port=8025,
		url_code='63d85b6189e42cba63feea36381da615c31ad8e36ae420ed67f60f3598efc9ad',
		password='123456'):
		'''
		获取服务器数据
		'''
		self.url=url
		self.port=port
		self.url_code=url_code
		self.password=password
	def get_user_data(self,data_type='用户信息'):
		'''
		获取使用的数据
		data_type='用户信息','实时数据',历史数据','清空实时数据','清空历史数据'
		'''
		url='{}:{}/_dash-update-component'.format(self.url,self.port)
		headers={'Content-Type':'application/json'}
		data={"output":"joinquant_trader_table.data@{}".format(self.url_code),
			"outputs":{"id":"joinquant_trader_table","property":"data@{}".format(self.url_code)},
			"inputs":[{"id":"joinquant_trader_password","property":"value","value":self.password},
				{"id":"joinquant_trader_data_type","property":"value","value":data_type},
				{"id":"joinquant_trader_text","property":"value","value":"\n               {'状态': 'held', '订单添加时间': 'datetime.datetime(2024, 4, 23, 9, 30)', '买卖': 'False', '下单数量': '9400', '已经成交': '9400', '股票代码': '001.XSHE', '订单ID': '1732208241', '平均成交价格': '10.5', '持仓成本': '10.59', '多空': 'long', '交易费用': '128.31'}\n                "},
				{"id":"joinquant_trader_run","property":"value","value":"运行"},
				{"id":"joinquant_trader_down_data","property":"value","value":"不下载数据"}],
				"changedPropIds":["joinquant_trader_run.value"],"parsedChangedPropsIds":["joinquant_trader_run.value"]}
		res=requests.post(url=url,data=json.dumps(data),headers=headers)
		text=res.json()
		df=pd.DataFrame(text['response']['joinquant_trader_table']['data'])
		return df