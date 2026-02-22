import os
import pandas as pd
class xg_tdx:
    '''
    小果通达信自选股操作模型
    作者微信15117320079
    '''
    def __init__(self,path=r'E:\tdx\T0002\blocknew'):
            '''
            小果通达信自选股操作模型
            '''
            self.path=path

    def read_all_tdx_stock(self):
        '''
        读取全部的通达信板块
        '''
        try:
            all_path=os.listdir(r'{}'.format(self.path))
        except Exception as e:
            print(e,'通达信板块文件不存在')
            all_path=[]
        return all_path
    def creat_tdx_user_def_stock(self,name='CS_1'):
        '''
        建立通达信自定义自选股模块
        '''
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            print('{} 通达信自选股模块已经存在不建立'.format(name))
        else:
            with open(path, 'w', encoding='gbk') as file:
                file.writelines('')
                print('{} 通达信自选股板块建立成功'.format(name))
    def del_tdx_user_def_stock(self,name='CS'):
        '''
        删除自定义股票池板块
        '''
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            os.remove(path=path)
            print('自定义模块{}删除成功'.format(name))
        else:
            print(name_1,'不存在')
    def adjust_stock(self,stock='600031.SH'):
        '''
        调整代码
        '''
        if stock[:3] in ['600','601','603','605','688','689',
                             ] or stock[:2] in ['11','51','58']:
            stock="1{}".format(stock)
        else:
            stock="0{}".format(stock)
        return stock
    def read_tdx_stock(self,name='CS'):
        '''
        读取通达信板块成分股
        '''
        path="{}\{}.blk".format(self.path,name)
        try:
            stock_list=[]
            with open(r'{}'.format(path)) as p:
                com=p.readlines()
                for stock in com:
                    if len(stock)>=6:
                        stock=stock.replace("\n", "")
                        stock_list.append(stock)
            df=pd.DataFrame()
            df['证券代码']=stock_list
        except Exception as e:
            print(e,'通达信路径有问题可能不存在',path)
            df=pd.DataFrame()
        return df 
    def read_tdx_stock_uer_def_path(self,path=''):
        '''
        读取通达信板块成分股自定义路径
        '''
        try:
            stock_list=[]
            with open(r'{}'.format(path)) as p:
                com=p.readlines()
                for stock in com:
                    if len(stock)>=6:
                        stock=stock.replace("\n", "")
                        stock_list.append(stock)
            df=pd.DataFrame()
            df['证券代码']=stock_list
        except Exception as e:
            print(e,'通达信路径有问题可能不存在',path)
            df=pd.DataFrame()
        return df 
    def add_tdx_stock(self,name='CS',stock='000001'):
        '''
        把股票添加到通达信自选股
        '''
        stock=self.adjust_stock(stock)
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            pass
        else:
            self.creat_tdx_user_def_stock(name=name)
            print(name,'自选股不存在建立')
        df=self.read_tdx_stock(name=name)
        if df.shape[0]>0:
            stock_list=df['证券代码'].tolist()
        else:
            print('{}自定义没有数据'.format(name))
            stock_list=[]
        if stock in stock_list:
            print('{} 在自选股{} 不添加'.format(stock,name))
        else:
            stock_list.append(stock)
            with open(path, 'w', encoding='gbk') as file:
                for stock in stock_list:
                    file.writelines(str(stock)+'\n')
                    print('{} 添加到自选股{}成功'.format(stock,name))
        
            
    def add_tdx_stock_list(self,name='CS',user_stock_list=['000001']):
        '''
        批量添加股票池到自选股
        '''
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            pass
        else:
            self.creat_tdx_user_def_stock(name=name)
            print(name,'自选股不存在建立')
        df=self.read_tdx_stock(name=name)
        if df.shape[0]>0:
            stock_list=df['证券代码'].tolist()
        else:
            print('{}自定义没有数据'.format(name))
            stock_list=[]
        for stock in user_stock_list:
            stock=self.adjust_stock(stock)
            if stock in stock_list:
                print('{} 在自选股{} 不添加'.format(stock,name))
            else:
                stock_list.append(stock)
        with open(path, 'w', encoding='gbk') as file:
            for stock in stock_list:
                file.writelines(str(stock)+'\n')
                print('{} 添加到自选股{}成功'.format(stock,name))
    def del_tdx_stock(self,name='CS',stock='000001'):
        '''
        删除通达信自选股成分股
        '''
        stock=self.adjust_stock(stock)
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            df=self.read_tdx_stock(name=name)
            if df.shape[0]>0:
                stock_list=df['证券代码'].tolist()
            else:
                print('{}自定义没有数据'.format(name))
                stock_list=[]
            if len(stock_list)>0:
                if stock in stock_list:
                    stock_list.remove(stock)
                    print('{} 删除自选股{}成功'.format(stock,name))
                else:
                    print('{}不在{}自选股不能删除'.format(stock,name))
            else:
                print('{} 自选股没有数据'.format(name))
            with open(path, 'w', encoding='gbk') as file:
                for stock in stock_list:
                    file.writelines(str(stock)+'\n')
        else:
            print('{} 自选股不存在'.format(name))
    def del_tdx_stock_list(self,name='CS',user_stock_list=['000001']):
        '''
        批量删除通达信自选股成分股
        '''
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            df=self.read_tdx_stock(name=name)
            if df.shape[0]>0:
                stock_list=df['证券代码'].tolist()
            else:
                print('{}自定义没有数据'.format(name))
                stock_list=[]
            if len(stock_list)>0:
                for stock in user_stock_list:
                    stock=self.adjust_stock(stock)
                    if stock in stock_list:
                        stock_list.remove(stock)
                        print('{} 删除自选股{}成功'.format(stock,name))
                    else:
                        print('{}不在{}自选股不能删除'.format(stock,name))
            else:
                print('{} 自选股没有数据'.format(name))
            with open(path, 'w', encoding='gbk') as file:
                for stock in stock_list:
                    file.writelines(str(stock)+'\n')
                    print('{} 从板块{}删除成功'.format(stock,name))
        else:
            print('{} 自选股不存在'.format(name))
            
    def del_all_tdx_stock(self,name='CS'):
        '''
        清空通达信自选股股票
        '''
        name_1='{}.blk'.format(name)
        path="{}\{}.blk".format(self.path,name)
        all_path=self.read_all_tdx_stock()
        if name_1 in all_path:
            stock_list=[]
            with open(path, 'w', encoding='gbk') as file:
                for stock in stock_list:
                    file.writelines(str(stock)+'\n')
            print('{}全部板块内容清空成功'.format(name))
        else:
            print('{} 自选股不存在'.format(name))
if __name__=='__main__':
    tdx=xg_tdx(path=r'E:\tdx\T0002\blocknew')
    df=tdx.add_tdx_stock_list(name='QMT')
    print(df)
    



    
