import requests
import json
import pandas as pd
class joinquant_data:
	def __init__(self,url='http://101.34.65.108',
		port=8888,
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
if __name__=='__main__':
	'''
	数据
	'''
	api=joinquant_data()
	df=api.get_user_data(data_type='实时数据')
	print(df)
	