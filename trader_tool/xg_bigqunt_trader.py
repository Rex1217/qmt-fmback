# 导入系统包 
import os
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pandas as pd
class xg_bigqunt_trader(object):
    """
    小果宽邦bigquant交易信号api
    来自网页改写
    """
    HOST = "https://bigquant.com"
    ACCESS_KEY_HEADER_NAME: str = "X-BigQuant-Access-Key"
    ACCESS_SIGNATURE_HEADER_NAME: str = "X-BigQuant-Signature"
    ACCESS_TIMESTAMP_HEADER_NAME: str = "X-BigQuant-Timestamp"

    def __init__(self, access_key: str, secret_key: str):
        self._access_key = access_key
        self._secret_key = secret_key
        self.account_type_dict ={}
        self.account_id_dict = {}
        self.tradingapiserver_host = os.getenv("TRADINGAPISERVER_HOST")
        self.debug = 1

    def query_papertrading_info(self,strategy_id='ba730553-e42a-4105-84ec-a3c47c7ac7f6') -> Optional[Dict]:
        """获取模拟交易基本信息
        example data:
        {
            'id': 'aec3e784-0724-4d7d-8917-16461b8c5553', 'created_at': '2023-12-07T17:52:43.232000+08:00', 'updated_at': '2023-12-07T17:53:08.416973+08:00',
            'space_id': '00000000-0000-0000-0000-000000000000', 'creator': '6d0130a2-3d94-4f38-97a2-14e1dc9391a4',
            'strategy_name': 'StockRanker-DAI策略-20231206112622', 'strategy_type': '0', 'status': 1, 'account_id': {'10020': '0'},
            'benchmark_instrument': '000300.SH', 'first_benchmark_index': 3572.36, 'first_trading_day': '2023-12-07', 'frequency': '1d',
            'extension': {}, 'source': 'saas', 'strategy_params': {'volume_limit': 1, 'order_price_field_buy': 'open', 'order_price_field_sell': 'close'
        }
        """
        url = f"{self.tradingapiserver_host}/strategies/{strategy_id}"
        params = {'page': 1, 'size': 10}
        if self.tradingapiserver_host:
            url = f"{self.tradingapiserver_host}/strategies/{strategy_id}"
            headers = None
        else:
            url, headers = self.signature_headers(self.HOST, f"/bigapis/trading/v1/strategies/{strategy_id}", self._access_key, self._secret_key, params=params)
        resp = requests.get(url=url, headers=headers, params=params)
        resp_data = resp.json()
        if self.debug:
            #print(f"query_papertrading_info: resp_data={resp_data}")
            pass
        if resp_data["code"] != 0:
            raise Exception(resp_data["message"])
        ret = resp_data.get("data")

        account_id_dict = ret["account_id"]
        account_type = list(account_id_dict.values())[0]
        account_id = list(account_id_dict.keys())[0]
        self.account_type_dict[strategy_id]=account_type
        self.account_id_dict[strategy_id]=account_id
        #print(f"query_papertrading_info: got account_id='{account_type}',\"{account_id}\" by strategy_id={strategy_id}")
        return ret

    def query_papertrading_cash(self,strategy_id='ba730553-e42a-4105-84ec-a3c47c7ac7f6',trading_day='2025-04-17') -> Optional[Dict]:
        """获取模拟交易资金信息
        example data:
        {
            'account_type': '0', 'account_id': '10020', 'trading_day': '2023-06-19', 'currency': 'CNY', 'balance': 109016.71000000006,
            'available': 109016.71000000006, 'frozen_cash': 0.0, 'total_margin': 0.0, 'total_market_value': 407791.0, 'portfolio_value': 516807.71,
            'pre_balance': 101875.81000000006, 'positions_pnl': 12350.64, 'capital_changed': 0.0, 'total_capital_changed': 0.0
        }
        """
        if strategy_id not in list(set(self.account_type_dict.keys())):
            self.query_papertrading_info(strategy_id=strategy_id)
        else:
            pass
        account_type=self.account_type_dict[strategy_id]
        account_id=self.account_id_dict[strategy_id]
        constraints = {"account_type": account_type, "trading_day__gte": trading_day, "trading_day__lte": trading_day}
        params = {'constraints': json.dumps(constraints), 'page': 1, 'size': 10}
        if self.tradingapiserver_host:
            url, headers = f"{self.tradingapiserver_host}/accounts/{account_id}/cash", None
        else:
            url, headers = self.signature_headers(self.HOST, f"/bigapis/trading/v1/accounts/{account_id}/cash", self._access_key, self._secret_key, params=params)
        resp = requests.get(url=url, headers=headers, params=params)
        resp_data = resp.json()
        if self.debug:
            #print(f"query_papertrading_cash: resp_data={resp_data}")
            pass
        if resp_data["code"] != 0:
            raise Exception(resp_data["message"])

        datas = resp_data.get("data").get("items")
        if datas:
            ret = datas[0]
            if "created_at" in ret:
                del ret["created_at"]
            if "id" in ret:
                del ret["id"]
            if "updated_at" in ret:
                del ret["updated_at"]
            return ret
        else:
            return {}

    def query_papertrading_positions(self,strategy_id='ba730553-e42a-4105-84ec-a3c47c7ac7f6', trading_day='2025-04-17') -> List[Dict]:
        """获取模拟交易某日的持仓列表
        example data:
        [{
            'account_type': '0', 'account_id': '10020', 'trading_day': '2023-06-19', 'exchange': 'SZ', 'instrument': '000005.SZ',
            'name': 'ST星源', 'posi_direction': '1', 'current_qty': 17800, 'available_qty': 17800, 'today_qty': 0, 'today_available_qty': 0,
            'cost_price': 1.17, 'last_price': 1.22, 'market_value': 21716.0, 'margin': 0.0, 'position_pnl': 887.92, 'hedge_flag': '1',
            'sum_buy_value': 20826.0, 'sum_sell_value': 0.0, 'commission': 2.08, 'dividend_qty': 0, 'dividend_cash': 0.0,
            'open_date': '2023-06-16', 'open_price': 1.17, 'settlement_price': 0.0, 'hold_days': 2
        }]
        """
        if strategy_id not in list(set(self.account_type_dict.keys())):
            self.query_papertrading_info(strategy_id=strategy_id)
        else:
            pass
        account_type=self.account_type_dict[strategy_id]
        account_id=self.account_id_dict[strategy_id]
        constraints = {"account_type": account_type, "trading_day__gte": trading_day, "trading_day__lte": trading_day}
        params = {'constraints': json.dumps(constraints), 'page': 1, 'size': 3000}
        if self.tradingapiserver_host:
            url, headers = f"{self.tradingapiserver_host}/account_positions/{account_id}/positions", None
        else:
            url, headers = self.signature_headers(self.HOST, f"/bigapis/trading/v1/account_positions/{account_id}/positions", self._access_key, self._secret_key, params=params)
        resp = requests.get(url=url, headers=headers, params=params)
        resp_data = resp.json()
        if resp_data["code"] != 0:
            raise Exception(resp_data["message"])

        list_positions = []
        datas = resp_data.get("data").get("items")
        if datas:
            for pos_data in datas:
                if "created_at" in pos_data:
                    del pos_data["created_at"]
                if "id" in pos_data:
                    del pos_data["id"]
                if "updated_at" in pos_data:
                    del pos_data["updated_at"]
                list_positions.append(pos_data)
        else:
            list_positions=list_positions
        if len(list_positions):
            df=pd.DataFrame(list_positions)
            df=df[[
                'trading_day','instrument','name',
                "cost_price","today_qty",'hold_days',
                "open_price","market_value","position_pnl",
                "profit_ratio"

            ]]
            df.columns=['交易日','证券代码','名称',
                    "成本",'数量','持有天数',
                    "收盘价",'市值','浮动盈亏','收益率%']
            df['收益率%']=df['收益率%']*100
        else:
            df=pd.DataFrame()
        return df
    def query_papertrading_positions_all(self,strategy_id='ba730553-e42a-4105-84ec-a3c47c7ac7f6') -> List[Dict]:
        """获取全部历史的持股
        example data:
        [{
            'account_type': '0', 'account_id': '10020', 'trading_day': '2023-06-19', 'exchange': 'SZ', 'instrument': '000005.SZ',
            'name': 'ST星源', 'posi_direction': '1', 'current_qty': 17800, 'available_qty': 17800, 'today_qty': 0, 'today_available_qty': 0,
            'cost_price': 1.17, 'last_price': 1.22, 'market_value': 21716.0, 'margin': 0.0, 'position_pnl': 887.92, 'hedge_flag': '1',
            'sum_buy_value': 20826.0, 'sum_sell_value': 0.0, 'commission': 2.08, 'dividend_qty': 0, 'dividend_cash': 0.0,
            'open_date': '2023-06-16', 'open_price': 1.17, 'settlement_price': 0.0, 'hold_days': 2
        }]
        """
        if strategy_id not in list(set(self.account_type_dict.keys())):
            self.query_papertrading_info(strategy_id=strategy_id)
        else:
            pass
        account_type=self.account_type_dict[strategy_id]
        account_id=self.account_id_dict[strategy_id]
        constraints = {"account_type": account_type}
        params = {'constraints': json.dumps(constraints), 'page': 1, 'size': 3000}
        if self.tradingapiserver_host:
            url, headers = f"{self.tradingapiserver_host}/account_positions/{account_id}/positions", None
        else:
            url, headers = self.signature_headers(self.HOST, f"/bigapis/trading/v1/account_positions/{account_id}/positions", self._access_key, self._secret_key, params=params)
        resp = requests.get(url=url, headers=headers, params=params)
        resp_data = resp.json()
        if resp_data["code"] != 0:
            raise Exception(resp_data["message"])

        list_positions = []
        datas = resp_data.get("data").get("items")
        if datas:
            for pos_data in datas:
                if "created_at" in pos_data:
                    del pos_data["created_at"]
                if "id" in pos_data:
                    del pos_data["id"]
                if "updated_at" in pos_data:
                    del pos_data["updated_at"]
                list_positions.append(pos_data)
        else:
            list_positions=list_positions
        if len(list_positions):
            df=pd.DataFrame(list_positions)
            df=df[[
                'trading_day','instrument','name',
                "cost_price","today_qty",'hold_days',
                "open_price","market_value","position_pnl",
                "profit_ratio"

            ]]
            df.columns=['交易日','证券代码','名称',
                    "成本",'数量','持有天数',
                    "收盘价",'市值','浮动盈亏','收益率%']
            df['收益率%']=df['收益率%']*100
        else:
            df=pd.DataFrame()
        return df
        

    def query_papertrading_planned_orders(self, strategy_id='ba730553-e42a-4105-84ec-a3c47c7ac7f6', trading_day='2025-04-17') -> List[Dict]:
        """获取模拟交易某日的信号列表
        example data:
        [{
            'creator': '6d0130a2-3d94-4f38-97a2-14e1dc9391a4', 'planned_order_id': '145909290', 'strategy_id': 'aec3e784-0724-4d7d-8917-16461b8c5553',
            'account_type': '0', 'account_id': '10020', 'trading_day': '2023-06-19', 'order_dt': '2023-06-19T15:00:00+08:00', 'exchange': 'SH',
            'instrument': '600767.SH', 'name': '*ST运盛', 'direction': '2', 'offset_flag': '1', 'original_order_qty': 251600, 'order_qty': 251600,
            'order_price': 0.42, 'order_type': 'U', 'order_status': 10, 'status_msg': 'Generated', 'order_params': None, 'order_placed_dt': None,
            'order_key': '', 'entrust_no': '', 'algo_order_id': 0, 'stop_loss_price': 0.0, 'stop_profit_price': 0.0
        }]
        """
        if strategy_id not in list(set(self.account_type_dict.keys())):
            self.query_papertrading_info(strategy_id=strategy_id)
        else:
            pass
        account_type=self.account_type_dict[strategy_id]
        account_id=self.account_id_dict[strategy_id]
        constraints = {
            "account_type": account_type,
            "account_id": account_id,
            "trading_day__gte": trading_day,
            "trading_day__lte": trading_day
        }
        params = {'constraints': json.dumps(constraints), 'page': 1, 'size': 3000}
        if self.tradingapiserver_host:
            url, headers = f"{self.tradingapiserver_host}/planned_order", None
        else:
            url, headers = self.signature_headers(self.HOST, f"/bigapis/trading/v1/planned_order", self._access_key, self._secret_key, params=params)
        resp = requests.get(url=url, headers=headers, params=params)
        resp_data = resp.json()
        if resp_data["code"] != 0:
            raise Exception(resp_data["message"])

        list_planned_orders: List[Dict] = []

        ########
        # For test mock planned orders
        """
        _planned_order = {
            'planned_order_id': '1',
            'strategy_id': self._strategy_id,
            'account_type': '0', 'account_id': '10000',
            'trading_day': trading_day,
            'order_dt': ' '.join([trading_day, "09:31:00"]),
            'exchange': 'SH',
            'instrument': '600900.SH',
            'name': '长江电力',
            'direction': '1',
            'offset_flag': '0',
            'original_order_qty': 600,
            'order_qty': 600,
            'order_price': 23.42,
            'order_type': 'U',
            'order_status': 10,
            'status_msg': 'Generated'
        }
        list_planned_orders.append(_planned_order)
        return list_planned_orders
        """
        ########

        datas = resp_data.get("data").get("items")
        if datas:
            for planned_order in datas:
                if "created_at" in planned_order:
                    del planned_order["created_at"]
                if "id" in planned_order:
                    del planned_order["id"]
                if "updated_at" in planned_order:
                    del planned_order["updated_at"]
                list_planned_orders.append(planned_order)
           
        else:
            list_planned_orders=list_planned_orders
        if len(list_planned_orders):
            df=pd.DataFrame(list_planned_orders)
            
            df=df[['trading_day','instrument','name','original_order_qty','order_price','direction']]
            df.columns=['交易日','证券代码','名称','数量','价格','交易类型']
            df['交易类型']=df['交易类型'].apply(lambda x:'买' if x=='1' else '卖')
        else:
            df=pd.DataFrame()
        return df
    def query_papertrading_planned_orders_all(self, strategy_id='ba730553-e42a-4105-84ec-a3c47c7ac7f6') -> List[Dict]:
        """获取模拟交易全部信号策略
        example data:
        [{
            'creator': '6d0130a2-3d94-4f38-97a2-14e1dc9391a4', 'planned_order_id': '145909290', 'strategy_id': 'aec3e784-0724-4d7d-8917-16461b8c5553',
            'account_type': '0', 'account_id': '10020', 'trading_day': '2023-06-19', 'order_dt': '2023-06-19T15:00:00+08:00', 'exchange': 'SH',
            'instrument': '600767.SH', 'name': '*ST运盛', 'direction': '2', 'offset_flag': '1', 'original_order_qty': 251600, 'order_qty': 251600,
            'order_price': 0.42, 'order_type': 'U', 'order_status': 10, 'status_msg': 'Generated', 'order_params': None, 'order_placed_dt': None,
            'order_key': '', 'entrust_no': '', 'algo_order_id': 0, 'stop_loss_price': 0.0, 'stop_profit_price': 0.0
        }]
        """
        if strategy_id not in list(set(self.account_type_dict.keys())):
            self.query_papertrading_info(strategy_id=strategy_id)
        else:
            pass
        account_type=self.account_type_dict[strategy_id]
        account_id=self.account_id_dict[strategy_id]
        constraints = {
            "account_type": account_type,
            "account_id": account_id,
        }
        params = {'constraints': json.dumps(constraints), 'page': 1, 'size': 3000}
        if self.tradingapiserver_host:
            url, headers = f"{self.tradingapiserver_host}/planned_order", None
        else:
            url, headers = self.signature_headers(self.HOST, f"/bigapis/trading/v1/planned_order", self._access_key, self._secret_key, params=params)
        resp = requests.get(url=url, headers=headers, params=params)
        resp_data = resp.json()
        if resp_data["code"] != 0:
            raise Exception(resp_data["message"])

        list_planned_orders: List[Dict] = []

        ########
        # For test mock planned orders
        """
        _planned_order = {
            'planned_order_id': '1',
            'strategy_id': self._strategy_id,
            'account_type': '0', 'account_id': '10000',
            'trading_day': trading_day,
            'order_dt': ' '.join([trading_day, "09:31:00"]),
            'exchange': 'SH',
            'instrument': '600900.SH',
            'name': '长江电力',
            'direction': '1',
            'offset_flag': '0',
            'original_order_qty': 600,
            'order_qty': 600,
            'order_price': 23.42,
            'order_type': 'U',
            'order_status': 10,
            'status_msg': 'Generated'
        }
        list_planned_orders.append(_planned_order)
        return list_planned_orders
        """
        ########

        datas = resp_data.get("data").get("items")
        if datas:
            for planned_order in datas:
                if "created_at" in planned_order:
                    del planned_order["created_at"]
                if "id" in planned_order:
                    del planned_order["id"]
                if "updated_at" in planned_order:
                    del planned_order["updated_at"]
                list_planned_orders.append(planned_order)
           
        else:
            list_planned_orders=list_planned_orders
        if len(list_planned_orders):
            df=pd.DataFrame(list_planned_orders)
            df=df[['trading_day','instrument','name','original_order_qty','order_price','direction']]
            df.columns=['交易日','证券代码','名称','数量','价格','交易类型']
            df['交易类型']=df['交易类型'].apply(lambda x:'买' if x=='1' else '卖')
        else:
            df=pd.DataFrame()
        return df

    def signature_headers(self,
        host: str,
        path: str,
        access_key: str,
        secret_key: str,
        body: bytes = b"",
        headers: dict = {},
        params: dict = None,
    ) -> Tuple[str, dict]:
        """采用aksk给headers添加签名.
    
        Args:
            host (str): host.
            path (str): 路径.
            access_key (str): ak.
            secret_key (str): sk.
            body (bytes): 请求负载.
            headers (dict, optional): 请求头.
    
        Returns:
            Tuple[str, dict]: url, 请求头.
        """
        import hmac
        
        import time
        from urllib.parse import quote
        url = f"{host}{path}"
        if params:
            url = url + "?" + quote("&".join([f"{k}={v}" for k, v in params.items()]))
        path_encode = path.encode()
        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)
        # 参与签名的消息
        msg = path_encode + body + timestamp.encode()
        signature = hmac.new(secret_key.encode(), msg=msg, digestmod="SHA256").hexdigest()
        
        # 给headers这是签名和时间戳
        headers[self.ACCESS_KEY_HEADER_NAME] = access_key
        headers[self.ACCESS_SIGNATURE_HEADER_NAME] = signature
        headers[self.ACCESS_TIMESTAMP_HEADER_NAME] = timestamp
        return url, headers 
if __name__ == "__main__":
    access_key = ""
    secret_key = ""
    strategy_id = ""
    trading_day = '2025-04-17'  # 假设交易日为当天
    # 初始化 API 对象
    api = xg_bigqunt_trader(access_key, secret_key)
    #先调这个函数获取参数账户类型
    #账户信息
    df=api.query_papertrading_info()
    print(df)
    #账户现金
    df=api.query_papertrading_cash()
    print(df)
    #持股
    df=api.query_papertrading_positions(strategy_id,trading_day)
    print(df)
    #持股全部
    df=api.query_papertrading_positions(strategy_id)
    print(df)
    #交易信号
    df=api.query_papertrading_planned_orders(strategy_id,trading_day)
    print(df)
    #全部交易信号
    df=api.query_papertrading_planned_orders_all(strategy_id)
    print(df)

    