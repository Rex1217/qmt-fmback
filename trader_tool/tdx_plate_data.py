import pandas as pd
import json
from struct import unpack
import os
class tdx_plate_data:
    '''
    通达信板块数据
    '''
    def __init__(self,path='E:/tdx'):
        '''
        自定义模型
        path 通达信的目录
        风格板块、概念板块、指数板块，分别对应的文件为block_fg.dat；block_gn.dat；block_zs.dat，
        '''
        DATAPATH = r'{}/T0002/hq_cache/'.format(path)
        self.path=DATAPATH
    def read_tdx_trader_stock(self,path=r'C:\new_tdx\T0002\blocknew\BUY.blk'):
        '''
        读取通达信板块自选股交易
        '''
        try:
            stock_list=[]
            with open(r'{}'.format(path),'r+') as f:
                com=f.readlines()
            for i in com:
                i=i.strip()
                if len(str(i))>0:
                    stock_list.append(i)
            df=pd.DataFrame()
            df['证券代码']=stock_list
            df['证券代码']=df['证券代码'].apply(lambda x:str(x)[-6:]+'.SH' if str(x)[0]=='1' else str(x)[-6:]+'.SZ')
            return df
        except:
            print('路径有问题{}'.format(path))
            df=pd.DataFrame()
            return df
    
    def read_file_loc(self,file_name, splits):
        with open(file_name, 'r') as f:
            buf_lis = f.read().split('\n')
        return [x.split(splits) for x in buf_lis[:-1]]

    def get_block_zs_tdx_loc(self,block='hy'):
        """
        读取本地通达信板块
        block板块名称
        """
        buf_line = self.read_file_loc(self.path+'tdxzs3.cfg', '|')

        mapping = {'hy': '2', 'dq': '3', 'gn': '4', 'fg': '5', 'yjhy': '12', 'zs': '6'}
        df = pd.DataFrame(buf_line, columns=['name', 'code', 'type', 't1', 't2', 'block'])
        dg = df.groupby(by='type')
        #df.to_excel('block.xlsx')
        if (block == 'zs'):
            return df
        temp = dg.get_group(mapping[block]).reset_index(drop=True)
        temp.drop(temp.columns[[2, 3, 4]], axis=1, inplace=True)
        #temp.to_excel('tdxzs3.xlsx', index=False)
        return temp

    def get_block_file(self,block='gn'):
        """ 
        读取板块路径
        block_gn.dat,_fg.dat,_zs.dat
        """

        file_name = f'block_{block}.dat'
        #print(PATH + file_name)
        with open(self.path + file_name, 'rb') as f:
            buff = f.read()

        head = unpack('<384sh', buff[:386])
        blk = buff[386:]
        blocks = [blk[i * 2813:(i + 1) * 2813] for i in range(head[1])]
        bk_list = []
        for bk in blocks:
            name = bk[:8].decode('gbk').strip('\x00')
            num, t = unpack('<2h', bk[9:13])
            stks = bk[13:(12 + 7 * num)].decode('gbk').split('\x00')
            bk_list = bk_list + [[name, block, num, stks]]
        return pd.DataFrame(bk_list, columns=['name', 'tp', 'num', 'stocks'])
    def gn_block(self,blk='gn') :
        '''
        概念板块
        '''
        del_row ={'gn':[],'fg':['', '', ''],'zs':[''],}
        mapping ={'gn': {
        },'fg':{
        },
        'zs':{''

        },}

        bf = self.get_block_file(blk)
        bf.drop(bf[bf['name'].isin(del_row[blk])].index,inplace=True)
        bf['name'] = bf['name'].replace(mapping[blk],regex=True)

        t = self.get_block_zs_tdx_loc(blk)

        if (blk == 'zs'):
            return bf
        del t['block']
        #print(bf)
        #print(t)
        df = pd.merge(t,bf,on='name')
        #print(df)
        return df
    def hy_block(self,blk='hy'):
        '''
        行业板块
        '''
        #begintime = datetime.datetime.now()
        stocklist = self.get_stock_hyblock_tdx_loc()
        #print(stocklist)
        blocklist = self.get_block_zs_tdx_loc(blk)
        #blocklist = blocklist.drop(blocklist[blocklist['name'].str.contains('TDX')].index)
        blocklist['block5'] = blocklist['block']
        #print(blocklist)
        blocklist['num'] = 0
        blocklist['stocks'] = ''
        for i in range(len(blocklist)):
            blockkey = blocklist.iat[i, 2]
            if (len(blockkey) == 5):
                datai = stocklist[stocklist['block5'] == blockkey]  # 根据板块名称过滤
            else:
                datai = stocklist[stocklist['block'] == blockkey]  # 根据板块名称过滤
            # 板块内进行排序填序号
            datai = datai.sort_values(by=['code'], ascending=[True])
            #datai.reset_index(drop=True, inplace=True)
            codelist = datai['code'].tolist()

            blocklist.iat[i, 4] = len(codelist)
            blocklist.iat[i, 5] = str(codelist)
        blocklist = blocklist.drop(blocklist[blocklist['num'] == 0].index)
        #endtime = datetime.datetime.now()
        #print('Cost ' + str((endtime - begintime).seconds) + ' seconds')
        #print(blocklist)
        return blocklist
    def get_stock_hyblock_tdx_loc(self):
        '''
        行业板块
        '''
        buf_line = self.read_file_loc(self.path+'tdxhy.cfg', '|')
        buf_lis = []
        mapping = {'0': 'sz.', '1': 'sh.', '2': 'bj.'}
        for x in buf_line:
            # x[1] = mapping[x[0]] + x[1]
            buf_lis.append(x)

        df = pd.DataFrame(buf_lis, columns=['c0', 'code', 'block', 'c1', 'c2', 'c3'])
        # print(df)
        df.drop(df.columns[[0, 3, 4, 5]], axis=1, inplace=True)

        df = df[(df['block'] != '')]
        # df = df[df.code.str.startswith(('sz','sh'))]
        df['block5'] = df['block']

        #df.to_excel('tdxhy.xlsx', index=False)
        return df
if __name__ == '__main__':
    tdx_plate_data=tdx_plate_data(path='E:/tdx')
    blocks = ['gn','zs', 'fg']
    for block in blocks:
        blocklist = tdx_plate_data.gn_block(block)  # 读取tdx目录下的板块信息 gn, fg, zs
        print(blocklist)
        blocklist.to_excel(block + 'block.xlsx', index=False)
    hyblock = tdx_plate_data.hy_block('hy')
    hyblock.to_excel('hyblock.xlsx', index=False)
    print(hyblock)
        