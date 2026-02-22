import pyautogui as pg
import time
import os
import shutil
import schedule
from trader_tool.stock_data import stock_data
import pandas as pd
class lude_spot_data:
    def __init__ (self,down_path=r'C:\Users\lxg123456\Downloads'):
        '''
        禄得实时数据
        '''
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.down_path=down_path
        self.stock_data=stock_data()
    def check_is_trader_date_1(self):
        '''
        检测是不是交易时间
        '''
        trader_time=4
        start_date=9
        end_date=24
        start_mi=0
        jhjj='否'
        if jhjj=='是':
            jhjj_time=15
        else:
            jhjj_time=30
        loc=time.localtime()
        tm_hour=loc.tm_hour
        tm_min=loc.tm_min
        wo=loc.tm_wday
        if wo<=trader_time:
            if tm_hour>=start_date and tm_hour<=end_date:
                if tm_hour==9 and tm_min<jhjj_time:
                    return False
                elif tm_min>=start_mi:
                    return True
                else:
                    return False
            else:
                return False    
        else:
            print('周末')
            return False
    def get_position(self):
        '''
        获取目前鼠标的位置
        '''
        x,y=pg.position()
        print(x,y)
        return x,y
    def click_spot_select(self,x=852,y=413):
        '''
        点击盘中选股
        '''
        pg.click(x=x,y=y)
    def after_disk_selection(self,x=709,y=417):
        '''
        盘后选择
        '''
        pg.click(x=x,y=y)
    def down_table(self,x=572,y=418):
        '''
        点击下载表格
        '''
        pg.click(x=x,y=y)
    def delete_folder_contents(self):
        folder_path=self.down_path
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print('{}删除成功'.format(item))
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print('{}删除成功'.format(item))
            else:
                print(item,'文件夹为空')
    def get_spot_select_stock_data(self):
        '''
        获取盘中选股结果
        '''
        #检查是否是交易时间
        print('开始下载盘中数据')
        if self.check_is_trader_date_1():
            #删除全部下载数据
            self.delete_folder_contents()
            time.sleep(10)
            #点击盘中选股
            now_date=self.stock_data.get_trader_date_list()[-1]
            self.click_spot_select()
            time.sleep(15)
            #点击下载数据
            self.down_table()
            time.sleep(5)
            all_path=os.listdir(self.down_path)
            if len(all_path)>0:
                df=pd.read_csv(r'{}\{}'.format(self.down_path,all_path[0]))
                df['交易日期']=now_date
                print(df)
                #保持数据
                df.to_excel(r'数据.xlsx')
                self.delete_folder_contents()
            else:
                print('{}没有文件'.format(self.down_path))
                df=pd.DataFrame() 
        else:
            print('目前不是交易时间')
    def get_after_disk_selection_data(self):
        '''
        获取盘后选股结果
        '''
        #检查是否是交易时间
        print('开始下载盘后数据')
        if self.check_is_trader_date_1():
            #删除全部下载数据
            self.delete_folder_contents()
            time.sleep(5)
            #点击盘中选股
            now_date=self.stock_data.get_trader_date_list()[-1]
            self.after_disk_selection()
            time.sleep(10)
            #点击下载数据
            self.down_table()
            time.sleep(5)
            all_path=os.listdir(self.down_path)
            if len(all_path)>0:
                df=pd.read_csv(r'{}\{}'.format(self.down_path,all_path[0]))
                df['交易日期']=now_date
                print(df)
                #保持数据
                df.to_excel(r'数据.xlsx')
                self.delete_folder_contents()
            else:
                print('{}没有文件'.format(self.down_path))
                df=pd.DataFrame() 
        else:
            print('目前不是交易时间')
    
if __name__=='__main__':
    models=lude_spot_data()
    time.sleep(5)
    models.get_spot_select_stock_data()
    schedule.every(2).minutes.do(models.get_spot_select_stock_data)
    schedule.every().day.at('18:30').do(models.get_after_disk_selection_data)
    schedule.every().day.at('19:30').do(models.get_after_disk_selection_data)
    schedule.every().day.at('20:30').do(models.get_after_disk_selection_data)
    schedule.every().day.at('21:30').do(models.get_after_disk_selection_data)
    while True:
        schedule.run_pending()
        time.sleep(1)
    