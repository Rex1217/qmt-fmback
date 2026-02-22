from qmt_trader.unification_data_qmt import unification_data_qmt
from xgtrader.unification_data_ths import unification_data_ths
class unification_data:
    def __init__(self,trader_tool='qmt',data_api='qmt'):
        self.qmt_trader=trader_tool
        self.data_api=data_api
    def get_unification_data(self):
        if self.qmt_trader=='qmt':
            return unification_data_qmt(data_api=self.data_api)
        else:
            return unification_data_ths()
    