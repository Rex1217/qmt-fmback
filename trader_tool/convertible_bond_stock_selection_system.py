import pandas as pd
import json
import os
import requests
class convertible_bond_stock_selection_system:
    def __init__(self,url='http://120.78.132.143',port=8023,password='123456'):
        '''
        可转债选股系统
        url服务器网页
        port端口
        password授权码
        '''
        self.url=url
        self.port=port
        self.password=password
        self.path=os.path.dirname(os.path.abspath(__file__))
    def get_user_info(self):
        '''
        获取用户信息
        '''
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"bond_trader_models_table_1.data@25956d89597d08e2116ebf2664b9ff75",
            "outputs":{"id":"bond_trader_models_table_1","property":"data@25956d89597d08e2116ebf2664b9ff75"},
            "inputs":[{"id":"bond_trader_models_password","property":"value","value":self.password},
            {"id":"bond_trader_models_data_type","property":"value","value":"代码"},
            {"id":"bond_trader_models_text","property":"value","value":""},
            {"id":"bond_trader_models_run","property":"value","value":"运行"},
            {"id":"bond_trader_models_down_data","property":"value","value":"不下载数据"}],"changedPropIds":["bond_trader_models_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['bond_trader_models_table_1']['data'])
        return df
    def get_convertible_bond_stock_selection_system(self,text=''):
        '''
        获取选股的结果
        '''
        user=self.get_user_info()
        print(user)
        print('开始分析*************************************')
        url='{}:{}/_dash-update-component'.format(self.url,self.port)
        headers={'Content-Type':'application/json'}
        data={
            "output":"bond_trader_models_table.data@25956d89597d08e2116ebf2664b9ff75",
            "outputs":{"id":"bond_trader_models_table","property":"data@25956d89597d08e2116ebf2664b9ff75"},
            "inputs":[{"id":"bond_trader_models_password","property":"value","value":"123456"},
            {"id":"bond_trader_models_data_type","property":"value","value":"代码"},
            {"id":"bond_trader_models_text","property":"value","value":"{}".format(text)},
            {"id":"bond_trader_models_run","property":"value","value":"运行"},
            {"id":"bond_trader_models_down_data","property":"value","value":"不下载数据"}],"changedPropIds":["bond_trader_models_run.value"]}
        res=requests.post(url=url,data=json.dumps(data),headers=headers)
        text=res.json()
        df=pd.DataFrame(text['response']['bond_trader_models_table']['data'])
        return df
if __name__=='__main__':
    '''
    获取数据
    '''
    text={
    "可转债溢价率设置":"可转债溢价率设置",
    "数据源模式说明":"服务器/自定义 自定义自己直接导入禄得选股的结果，放在自定义数据，支持盘中，盘后选股交易",
    "数据源":"服务器",
    "更新数据模式说明":"手动/自动",
    "更新数据模式":"自动",
    "服务器":"http://120.78.132.143",
    "端口":"8023",
    "授权码":"123456",
    "是否测试":"否",
    "是否数据没有更新的情况下更新":"是",
    "强制赎回设置":"************************",
    "是否剔除强制赎回":"是",
    "距离强制赎回天数":0,
    "排除上市天数":3,
    "是否排除ST":"是",
    "市场说明":["沪市主板","深市主板","创业板","科创板"],
    "排除市场":[],
    "行业说明":"查询行业表**********,混合排除不区分一二三级行业",
    "排除行业":[],
    "企业类型说明":["民营企业","地方国有企业","中央国有企业","外资企业","中外合资经营企业","集体企业"],
    "排除企业类型":[],
    "排除地域说明":["陕西", "山西", "山东", "河南", "新疆", "安徽", "西藏", "海南", "湖北", "河北", 
    "福建", "广西", "内蒙古", "浙江", "江西", "江苏", "上海", "贵州", "黑龙江", "湖南", "甘肃",
    "宁夏", "云南", "天津", "广东", "四川", "北京", "辽宁", "重庆"],
    "排除地域":[],
    "排除外部评级说明":["AAA", "AA+", "AA", "AA-", "A+", "A", "A-",
    "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC", "CC"],
    "排除外部评级":["B","B-","CCC","CC"],
    "排除三方评级说明":["1", "2", "3", "4+", "4", "4-", "5+", "5", "5-", "6+", "6",
     "6-", "7+", "7", "7-", "8+", "8", "8-", "9", "10"],
    "排除三方评级":["10","9","8"],
    "添加排除因子":"排除因子设置************************",
    "全部的排除因子打分因子,必须选择可以计算的":["开盘价", "最高价", "最低价", "最新价", "涨跌幅", "5日涨跌幅",
    "正股最高价", "正股最低价", "正股最新价", "正股涨跌幅", "正股5日涨跌幅", "成交量(手)", 
    "成交额(万)", "年化波动率", "正股年化波动率", "股息率", "转股价值", "转股溢价率", "理论转股溢价率",
    "修正转股溢价率", "纯债价值", "纯债溢价率", "期权价值", "理论价值", "理论偏离度", "双低",
    "剩余规模(亿)", "剩余市值(亿)", "换手率", "市净率", "市盈率_ttm", "市销率_ttm", "正股流通市值(亿)",
    "正股总市值（亿）", "资产负债率", "转债市占比", "上市天数", "转股截止日", "剩余年限", 
    "到期收益率(税前)", "强赎触发比例", "外部评级", "三方评级", "企业类型", "地域", "一级行业", "二级行业", "三级行业"],
    "因子计算符号说明":"大于,小于,大于排名%,小于排名%,空值,排除是相反的,大于是小于",
    "排除因子":["最新价","最新价","转股溢价率","剩余规模(亿)"],
    "因子计算符号":["大于","小于","大于","大于"],
    "因子值":[130,100,0.3,8],
    "打分因子设置":"*************************************************",
    "打分因子说明":"正相关：因子值越大得分越高；负相关：因子值越大得分越低,",
    "打分因子":["转股溢价率","最新价","剩余规模(亿)"],
    "因子相关性":["负相关","负相关","负相关"],
    "因子权重":[1,1,1],
    "持有限制":10,
    "持股限制":10,
    "策略轮动设置":"策略轮动设置************************,轮动都按排名来",
    "轮动方式说明":"每天/每周/每月/特别时间",
    "轮动方式":"每天",
    "说明":"每天按自定义函数运行",
    "每周轮动是说明":"每周比如0是星期一,4是星期五**********",
    "每周轮动时间":0,
    "每月轮动是说明":"必须是交易日,需要自己每个月自动输入**********",
    "每月轮动时间":["2024-02-29","2024-02-29","2024-02-29","2024-02-29","2024-02-29","2024-02-29","2024-02-29"],
    "特定时间说明":"特别的应该交易日",
    "特定时间":["2024-02-23","2024-02-24","2024-02-25","2024-02-26","2024-02-27"],
    "轮动规则设置":"轮动规则设置88888888**********排名",
    "买入排名前N":10,
    "持有排名前N":10,
    "跌出排名卖出N":10,
    "买入前N":10,
    "自定义因子模块":"自定义因子模块设置***********************",
    "是否开启自定义因子":"否",
    "自定义因子":{
    "5日收益":"return_5()",
    "均线金叉":"ma_gold_fork()",
    "macd金叉":"macd_gold_fork()"}
}
    models=convertible_bond_stock_selection_system()
    df=models.get_convertible_bond_stock_selection_system(text=text)
    print(df)
    
    