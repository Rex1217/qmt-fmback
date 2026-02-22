try:
    from . import pyML
except Exception as e:
    print(e)
    from .. import pyML
from typing import Tuple,Union,Iterable,Optional
import numpy as np

def ATR(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=20)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''均幅指标（ATR）是取一定时间周期内的股价波动幅度的移动平均值
:CLOSE-收盘价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N-周期[整数]
返回(MTR,ATR)元组
:MTR-N周期的平均真实波幅
:ATR-平均真实波幅的N周期平均值'''
    return pyML.ATR(CLOSE,HIGH,LOW,N)
    
def STD(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''计算一组数据的N日估算标准差，N可以为序列值'''
    return pyML.STD(S,SN)

def BOLL(CLOSE:Iterable,N:int=20)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:
    '''计算布林带,N取值2-999,只能为常数
:CLOSE-收盘价[序列值]
返回值为(UB,MID,LB)元组(分别指上轨、中轨、下轨)'''
    return pyML.BOLL(CLOSE,N)

def BOLL_M(CLOSE:Iterable,N:int=20)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:
    '''计算布林带(传统版),N取值2-999,只能为常数
:CLOSE-收盘价[序列值]
返回值为(UB,MID,LB)元组(分别指上轨、中轨、下轨)'''
    return pyML.BOLL_M(CLOSE,N)

def WINNER(HIGH:Iterable,LOW:Iterable,VOL:Iterable,Turnrate:Iterable,price,avg:Union[Iterable,str]='hlavg')->Optional[np.ndarray]:
    '''计算某价位的盈利盘比例
:HIGH-最高价[序列值]
:LOW-最低价[序列值]  
:VOL-成交量[序列值]，单位是手，万股等不重要,只要统一就行
:Turnrate[换手率]：取值范围0-1，注意50%的换手应写作0.5
   *换手率由于流通股变动问题，故不能简单使用“成交量/流通股”的方式计算，这也是本函数保留输入换手率的原因
:price-某价格的盈利比例中的价格，可以是具体数值（如：99.98），也可以是序列（如收盘价、开盘价等）
:avg-三角分部顶点:默认取每日最高价和最低价的平均值，某些算法中使用“成交额/成交量”的计算方法
   *使用“成交额/成交量”的计算方法的话，注意这个平均位置也要复权，否则会出现平均位置出现在当日最高价和最低价之外的情况
返回一组获利比例的序列值，范围0-1，如0.1即当前股价的盈利比例为10%
   *此函数专用于T+1交易，不适用于可转债或者非日线周期等换手率超过100的情况
    '''
    return pyML.WINNER(HIGH,LOW,VOL,Turnrate,price,avg)

def COST(HIGH:Iterable,LOW:Iterable,VOL:Iterable,Turnrate:Iterable,winpercent:Iterable,radio:float=0.01,avg:Union[Iterable,str]='hlavg')->Optional[np.ndarray]:
    '''计算某盈利比例对应的股价
:HIGH-最高价[序列值]
:LOW-最低价[序列值]  
:VOL-成交量[序列值]，单位是手，万股等不重要,只要统一就行
:Turnrate[换手率]：取值范围0-1，注意50%的换手应写作0.5
   *换手率由于流通股变动问题，故不能简单使用“成交量/流通股”的方式计算，这也是本函数保留输入换手率的原因 
:winpercent-指定获利比例，应为0-100之间的数值（如winpercent=90,即返回盈利90%的股价）
:avg-三角分部顶点:默认取每日最高价和最低价的平均值，某些算法中使用“成交额/成交量”的计算方法
   *使用“成交额/成交量”的计算方法的话，注意这个平均位置也要复权，否则会出现平均位置出现在当日最高价和最低价之外的情况
:radio-精确度：如股票等使用0.01，ETF，Reits等使用0.001
返回一组指定获利比例的股价。
   *此函数专用于T+1交易，不适用于可转债或者非日线周期等换手率超过100的情况'''
    return pyML.COST(HIGH,LOW,VOL,Turnrate,winpercent,radio,avg)

def BACKSET(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''属于未来函数,将当前位置到若干周期前的数据设为True
:S-输入序列值，不为0则置为True,为0则置为False
:N-设为True的周期数，可以为序列值，当前周期为True才会往前设置
返回值:向前置True后的序列，dtype=np._bool'''
    return pyML.BACKSET(S,SN)

def REF(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''引用SN个周期前的数据
:S-源数据
:SN-向前引用的周期数，可以为序列值，SN可以包含负数
返回值：向前引用SN个周期的数值后的序列'''
    return pyML.REF(S,SN)

def POW(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回S的N次幂
:S-源数据
:SN-计算幂的次数，可以为序列值
返回值：计算后的序列'''
    return pyML.POW(S,SN)
	

def INTPART(S:Iterable)->Optional[np.ndarray]:
    '''返回沿A绝对值减小方向最接近的整数'''
    return pyML.INTPART(S)

def EMA(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:		#SN是序列值未处理
    '''返回X的SN日平滑移动平均,SN可以为序列值'''
    return pyML.EMA(S,SN)

def SMA(S:Iterable,N:Union[Iterable[int],int],M:int=1)->Optional[np.ndarray]:
    '''返回X的N日移动平均,M为权重，N可以为序列值，M为常量'''
    return pyML.SMA(S,N,M)
	

def SLOPE(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回线性回归斜率,SN支持变量'''
    return pyML.SLOPE(S,SN)


def HHV(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回SN周期内S最高值,SN=0则从第一个有效值开始，SN可以序列值'''
    return pyML.HHV(S,SN)


def LLV(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回SN周期内S最低值,SN=0则从第一个有效值开始，SN可以序列值'''
    return pyML.LLV(S,SN)

def MA(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回S的SN日简单移动平均,SN可以为序列值'''
    return pyML.MA(S,SN)


def AVEDEV(S:Iterable,SN)->Optional[np.ndarray]:
    '''返回S的SN日平均绝对偏差,SN可以为序列值'''
    return pyML.AVEDEV(S,SN)


def CCI(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=14)->Optional[np.ndarray]:
    '''CCI顺势指标
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N-周期[常量]
返回CCI的数值'''
    return pyML.CCI(CLOSE,HIGH,LOW,N)


def KDJ(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=9,M1:int=3,M2:int=3)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:
    '''KDJ随机指标
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N,M1,M2-周期[常量]
返回(K,D,J)元组'''
    return pyML.KDJ(CLOSE,HIGH,LOW,N,M1,M2)

def MACD(CLOSE:Iterable,SHORT:int=12,LONG:int=26,MID:int=9,bit:int=2)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]: #bit为保留小数的位数，取值不等于2或3时则输出全部小数
    '''MACD异同移动平均线
:CLOSE-收盘报价[序列值]
:SHORT,LONG,MID-周期[常量]
:bit-保留的小数位数
返回(DIF,DEA,MACD)元组'''
    return pyML.MACD(CLOSE,SHORT,LONG,MID,bit)
	

def WR(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=10,N1:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]: 
    '''WR威廉指标
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N,N1-周期[常量]
返回(WR1,WR2)元组，WR1、WR2即N和N1周期的威廉指标数值'''
    return pyML.WR(CLOSE,HIGH,LOW,N,N1)
	

def SUM(S:Iterable,SN)->Optional[np.ndarray]:
    '''统计SN周期中S的总和,若SN=0则从第一个有效值开始，SN可以为序列值'''
    return pyML.SUM(S,SN)
	
			
def BARSLAST(S:Iterable)->Optional[np.ndarray]:
    '''返回上一次条件成立到当前的周期数'''
    return pyML.BARSLAST(S)
	
def BARSCOUNT(S:Iterable)->Optional[np.ndarray]:
    '''返回第一个有效数据到当前的间隔周期数'''
    return pyML.BARSCOUNT(S)

def BETWEEN(S1:Iterable,S2:Iterable,S3:Iterable)->Optional[np.ndarray]:
    '''BETWEEN(S1,S2,S3)表示S1处于S2和S3之间时返回1(S2<=S1<=S3或S3<=S1<=S2),否则返回0'''
    return pyML.BETWEEN(S1,S2,S3)

def COUNT(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''统计N周期中满足X条件的周期数,若N<=0则从第一个有效值开始.'''
    return pyML.COUNT(S,SN)

def WMA(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回S的SN日加权移动平均,SN可以为序列值'''
    return pyML.WMA(S,SN)

def MFI(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,VOL:Iterable,N:int=14)->Optional[np.ndarray]:
    '''MFI资金流量指标
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:VOL-交易量[序列值]
:N-周期[常量]
返回值：MFI数值'''
    return pyML.MFI(CLOSE,HIGH,LOW,VOL,N)

def TRIX(CLOSE:Iterable,N:int=12,M:int=9)->Optional[np.ndarray]:
    '''TRIX三重指数平滑平均线,属于中长线指标
:CLOSE-收盘报价[序列值]
:N,M-周期[常量]
返回值：(TRIX,MATRIX)元组,MATRIX为TRIX的N日平均'''
    return pyML.TRIX(CLOSE,N,M)

def BARSLASTCOUNT(S:Iterable)->Optional[np.ndarray]:
    '''返回连续满足S条件的周期数。'''
    return pyML.BARSLASTCOUNT(S)

def FILTER(S:Iterable,SN)->Optional[np.ndarray]:
    '''过滤连续出现的信号：S满足条件后,将其后SN周期内的数据置为0,SN可以是变量。'''
    return pyML.FILTER(S,SN)

def BIAS(CLOSE:Iterable,N1:int=6,N2:int=12,N3:int=24)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:
    '''BIAS乖离率指标
:CLOSE-收盘价[序列值]
:N1,N2,N3-周期[常量]
返回值:(BIAS1,BIAS2,BIAS3)元组，即收盘价的N1/N2/N3日乖离率'''
    return pyML.BIAS(CLOSE,N1,N2,N3)

def BIAS_QL(CLOSE:Iterable,N:int=6,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''BIAS乖离率(传统版)指标
:CLOSE-收盘价[序列值]
:N,M-周期[常量]
返回值:(BIAS,BIASMA)元组
:BIAS-收盘价的N日乖离率
:BIASMA:乖离率的M日均值'''
    return pyML.BIAS_QL(CLOSE,N,M)

def EXIST(S:Iterable,N:int)->Optional[np.ndarray]:
    '''返回在N个交易周期内是否存在S位True的值，N为常量'''
    return pyML.EXIST(S,N)

def BBI(CLOSE:Iterable,M1:int=3,M2:int=6,M3:int=12,M4:int=24)->Optional[np.ndarray]:
    '''BBI多空均线指标
:CLOSE-收盘价[序列值]
:M1,M2,M3,M4-周期[常量]
返回值:BBI数值'''
    return pyML.BBI(CLOSE,M1,M2,M3,M4)

def DIFF(S:Iterable)->Optional[np.ndarray]:
    '''返回前一个值减后一个值的数值'''
    return pyML.DIFF(S)

def VALUEWHEN(COND:Iterable,S:Iterable)->Optional[np.ndarray]:
    '''当COND条件成立时,取X的当前值,否则取VALUEWHEN的上个值'''
    return pyML.VALUEWHEN(COND,S)

def VR(CLOSE:Iterable,VOL:Iterable,N:int=26,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''VR成交量变异率指标
:CLOSE-收盘价[序列值]
:VOL-成交量[序列值]
:N,M-周期[常量]
返回值：(VR,MAVR)元组，MAVR为VR的M日均值'''
    return pyML.VR(CLOSE,VOL,N,M)

def RSI(CLOSE:Iterable,N1:int=6,N2:int=12,N3:int=24)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:
    '''RSI相对强弱指标
:CLOSE-收盘价[序列值]
:N1,N2,N3-3个周期[常量]
返回值：(RSI1,RSI2,RSI3)元组，即根据收盘价计算的3个周期的RSI值'''
    return pyML.RSI(CLOSE,N1,N2,N3)

def LONGCROSS(S1:Iterable,S2:Iterable,N:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''两条线维持一定周期后交叉
:S1,S2-序列值,N-常量或序列值
用法:LONGCROSS(S1,S2,N)表示S1在N周期内都小于S2,本周期从下方向上穿过S2时返回1,否则返回0'''
    return pyML.LONGCROSS(S1,S2,N)

def CROSS(S1:Iterable,S2:Iterable)->Optional[np.ndarray]:
    '''两条线交叉.
用法: CROSS(S1,S2)表示当S1从下方向上穿过S2时返回1,否则返回0'''
    return pyML.LONGCROSS(S1,S2,1)

def KTN(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=20,M:int=10)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:                 #肯特纳交易通道, N选20日，ATR选10日
    '''KTN肯特纳交易通道指标
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N,M-周期[常量]
返回值：(UPPER,MID,LOWER)元组，即通道的上中下三轨'''
    return pyML.KTN(CLOSE,HIGH,LOW,N,M) 

def DMA(S:Iterable,SN:Union[int,Iterable[int]])->Optional[np.ndarray]:
    '''求S的SN周期动态移动平均,SN可以为序列值'''
    return pyML.DMA(S,SN)

def TAQ(HIGH:Iterable,LOW:Iterable,N:int=20)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray]]:
    '''唐安奇通道
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N-周期[常量]
返回值：(UP,MID,DOWN)元组，即通道的上中下三轨'''
    return pyML.TAQ(HIGH,LOW,N)

def BARSSINCEN(S:Iterable,N:int)->Optional[np.ndarray]:
    '''N周期内第一个条件成立到当前的周期数.
用法: BARSSINCEN(S,N):N周期内第一次S不为0到现在的周期数,N为常量'''
    return pyML.BARSSINCEN(S,N)

def LAST(S:Iterable,A:int,B:int)->Optional[np.ndarray]:
    '''LAST(S,A,B):持续存在.
例如:
 LAST(CLOSE>OPEN,10,5) 
 表示从前10日到前5日内一直阳线
 若A为0,表示从第一天开始,B为0,表示到最后日止'''
    return pyML.LAST(S,A,B)

def BRAR(OPEN:Iterable,CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=26)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''BRAR情绪指标
:OPEN-开盘价[序列值]
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N-周期[常量]
返回：(BR,AR)元组'''
    return pyML.BRAR(OPEN,CLOSE,HIGH,LOW,N)

def CONST(S:Iterable)->Optional[np.ndarray]:
    '''返回序列S最后的值组成常量序列'''
    return pyML.CONST(S)

def EMV(HIGH:Iterable,LOW:Iterable,VOL:Iterable,N:int=14,M:int=9)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''EMV简易波动指标
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:VOL-成交量[序列值]
:N,M-周期[常量]
返回值:(EMV,MAEMV)元组,MAEMV为EMV的M日均值'''
    return pyML.EMV(HIGH,LOW,VOL,N,M)

def LLVBARS(S:Iterable,N:int)->Optional[np.ndarray]:
    '''求上一低点到当前的周期数.
用法: LLVBARS(S,N):求N周期内X最低值到当前周期数,N=0表示从第一个有效值开始统计'''
    return pyML.LLVBARS(S,N)

def HHVBARS(S:Iterable,N:int)->Optional[np.ndarray]:
    '''求上一高点到当前的周期数.
用法: HHVBARS(S,N):求N周期内X最高值到当前周期数,N=0表示从第一个有效值开始统计'''
    return  pyML.HHVBARS(S,N)

def OBV(CLOSE:Iterable,VOL:Iterable,N:int=30)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''OBV 能量潮指标
:CLOSE-收盘价[序列值]
:VOL-成交量[序列值]
:N-周期[常量]
返回值:(OBV,MAOBV)元组,MAOBV为OBV的N日均值'''
    return pyML.OBV(CLOSE,VOL,N)
    
def DPO(CLOSE:Iterable,N:int=20,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''DPO 区间震荡线
:CLOSE-收盘价[序列值]
:N,M-周期[常量]
返回值:(DPO,MADPO)元组,MADPO为DPO的M日均值'''
    return pyML.DPO(CLOSE,N,M)

def MTM(CLOSE:Iterable,N:int=12,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''MTM 动量线指标
:CLOSE-收盘价[序列值]
:N,M-周期[常量]
返回值:(MTM,MTMMA)元组,MTMMA为MTM的M日均值'''   
    return pyML.MTM(CLOSE,N,M)

def DMA(CLOSE:Iterable,N1:int=10,N2:int=50,M:int=10)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''DMA 平均差指标
:CLOSE-收盘价[序列值]
:N1,N2,M-周期[常量]
返回值:(DIF,DIFMA)元组,DIFMA为DIF的M日均值'''  
    return pyML.DMA(CLOSE,N1,N2,M)


def DMI(CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=14,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]]:
    '''DMI 趋向指标
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N,M-周期[常量]
返回：(PDI,MDX,ADX,ADXR)元组 '''
    return pyML.DMI(CLOSE,HIGH,LOW,N,M)

def ROC(CLOSE:Iterable,N:int=12,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''ROC 变动率指标
:CLOSE-收盘价[序列值]
:N,M-周期[常量]
返回值:(ROC,MAROC)元组,MAROC为ROC的M日均值'''
    return pyML.ROC(CLOSE,N,M)

def EVERY(S:Iterable,SN:Union[int,Iterable[int]])->Optional[np.ndarray]:
    '''一直存在.表示N日内S一直成立(N应大于0,小于总周期数,N支持变量)'''
    pyML.EVERY(S,SN)

def MASS(HIGH:Iterable,LOW:Iterable,N1:int=9,N2:int=25,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''MASS 梅斯线指标
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N1,N2,M-周期[常量]
返回值:(MASS,MAMASS)元组,MAMASS为MASS的M日均值'''
    return pyML.MASS(HIGH,LOW,N1,N2,M)

def EXPMA(CLOSE:Iterable,M1:int=12,M2:int=50)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''EXPMA 指数平均线指标
:CLOSE-收盘价[序列值]
:N1,M2-周期[常量]
返回值:(EXP1,EXP2)元组,即收盘价的M1,M2日指数移动平均'''
    return pyML.EXPMA(CLOSE,M1,M2)

def PSY(CLOSE:Iterable,N:int=12,M:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''PSY 心理线指标
:CLOSE-收盘价[序列值]
:N,M-周期[常量]
返回值:(PSY,PSYMA)元组,PSYMA为PSY的M日均值'''
    return pyML.PSY(CLOSE,N,M)

def ASI(OPEN:Iterable,CLOSE:Iterable,HIGH:Iterable,LOW:Iterable,N:int=6)->Optional[Tuple[np.ndarray,np.ndarray]]:
    '''ASI 震动升降指标
:OPEN-开盘价[序列值]
:CLOSE-收盘报价[序列值]
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:N-周期[常量]
返回值:(ASI,ASIMA)元组,ASIMA为ASI的N日均值'''
    return pyML.ASI(OPEN,CLOSE,HIGH,LOW,N)

def FORCAST(S:Iterable,SN:Union[Iterable[int],int])->Optional[np.ndarray]:
    '''返回S的线性回归预测值,SN支持变量'''
    return pyML.FORCAST(S,SN)

def ATAN(S)->Union[np.ndarray,float]:
    '''返回S的反正切值'''
    return np.arctan(S)	
def ACOS(S)->Union[np.ndarray,float]: 
    '''返回S的反余弦值'''  
    return np.arccos(S)
def ASIN(S)->Union[np.ndarray,float]:    
    '''返回S的反正弦值'''
    return np.arcsin(S)
def TAN(S)->Union[np.ndarray,float]:
    '''返回S的正切值'''
    return np.arctan(S)	
def COS(S)->Union[np.ndarray,float]:  
    '''返回S的余弦值'''  
    return np.arccos(S)
def SIN(S)->Union[np.ndarray,float]: 
    '''返回S的正弦值'''    
    return np.arcsin(S)
def RD(SN,D:int=3)->Union[np.ndarray,float,int]:   
    '''对SN四舍五入取D位小数''' 
    return np.round(SN,D)        
def RET(S:Iterable,N:int=1): 
    '''返回序列倒数第N个值,默认返回最后一个 '''
    return np.array(S)[-N]      
def ABS(S):
    '''返回S的绝对值'''
    return np.abs(S)           
def MAX(S1,S2): 
    '''序列逐个最大值'''
    return np.maximum(S1,S2)    
def MIN(S1,S2):  
    '''序列逐个最小值'''
    return np.minimum(S1,S2)    
def IF(S,A,B)->np.ndarray:  
    '''根据条件求不同的值.
用法: IF(X,A,B)若X不为0则返回A,否则返回B''' 
    return np.where(S,A,B)      


def getHPoint(S:Iterable,N:int)->Optional[np.ndarray]:
    '''指示当前位置的数据是否是一组数据的高点
:S-输入的数据[序列值]
:N-检测阈值[常量]
返回值为dtype=bool_的数组，True位置即为相对高点位置'''
    return pyML.getLPoint(S,N)

def getLPoint(S:Iterable,N:int)->Optional[np.ndarray]:
    '''指示当前位置的数据是否是一组数据的低点
:S-输入的数据[序列值]
:N-检测阈值[常量]
返回值为dtype=bool_的数组，True位置即为相对低点位置'''
    return pyML.getLPoint(S,N)

def getHLine(S:Iterable,N:int)->Optional[Tuple[np.ndarray,float,float]]:
    '''获取一组数据高点的拟合直线
:S-输入的数据[序列值]
:N-检测阈值[常量]
返回值：(DATA,R2,SLOPE)元组
:DATA-拟合后的高点序列,绘图的话是一条直线
:R2-高点拟合的r-square数值[取值范围0-1，数值越大说明数据拟合度越好]
:SLOPE-拟合后直线的斜率，为正则标识数据越来越大，为负则表示数据越来越小'''
    return pyML.getHLine(S,N)

def getLLine(S:Iterable,N:int)->Optional[Tuple[np.ndarray,float,float]]:
    '''获取一组数据低点的拟合直线
:S-输入的数据[序列值]
:N-检测阈值[常量]
返回值：(DATA,R2,SLOPE)元组
:DATA-拟合后的低点序列,绘图的话是一条直线
:R2-低点拟合的r-square数值[取值范围0-1，数值越大说明数据拟合度越好]
:SLOPE-拟合后直线的斜率，为正则标识数据越来越大，为负则表示数据越来越小'''
    return pyML.getLLine(S,N)

def getBestHLine(S:Iterable,N1:int,N2:int)->Optional[Tuple[np.ndarray,float,float,int]]:
    '''获取一组数据在N取值为N1到N2之间的高点最佳拟合直线
:S-输入的数据[序列值]
:N1,N2-检测阈值[常量],要求N1<N2,即使用函数getHLine(S,N)时N的取值范围
返回值：(DATA,R2,SLOPE,N)元组
:DATA-最佳拟合后的高点序列,绘图的话是一条直线
:R2-高点拟合后的最佳r-square数值[即函数getHLine(S,N)的N值取N1-N2之间所有整数时计算的R2最大值]
:SLOPE-最佳拟合后直线的斜率，为正则标识数据越来越大，为负则表示数据越来越小
:N-最佳拟合时的N值'''
    return pyML.getBestHLine(S,N1,N2)

def getBestLLine(S:Iterable,N1:int,N2:int)->Optional[Tuple[np.ndarray,float,float,int]]:
    '''获取一组数据在N取值为N1到N2之间的低点最佳拟合直线
:S-输入的数据[序列值]
:N1,N2-检测阈值[常量],要求N1<N2,即使用函数getHLine(S,N)时N的取值范围
返回值：(DATA,R2,SLOPE,N)元组
:DATA-最佳拟合后的低点序列,绘图的话是一条直线
:R2-低点拟合后的最佳r-square数值[即函数getHLine(S,N)的N值取N1-N2之间所有整数时计算的R2最大值]
:SLOPE-最佳拟合后直线的斜率，为正则标识数据越来越大，为负则表示数据越来越小
:N-最佳拟合时的N值'''
    return pyML.getBestLLine(S,N1,N2)

def RSRS(HIGH:Iterable,LOW:Iterable,N:int=18,M:int=600)->Optional[np.ndarray]:
    '''RSRS 阻力相对支撑强度指标

:N,M-周期[常量] M默认值值为600，注意输入数据的数量
返回值：计算的RSRS数值，一般在RSRS>0.7时买入，RSRS小于-0.7时卖出'''
    return pyML.RSRS(HIGH,LOW,N,M)

def SAR(HIGH:Iterable,LOW:Iterable,start:int=4,stepstart:int=2,step:int=2,maxstep:int=20)->Optional[np.ndarray]:
    '''SAR 抛物线指标
:HIGH-最高价[序列值]
:LOW-最低价[序列值]
:start:起始统计周期
:stepstart:加速因子参数
:step:加速因子增量
:maxstep:反向临界参数
返回值:SAR值，SAR大于收盘价代表下跌趋势，SAR小于收盘价代表上涨趋势'''
    return pyML.SAR(HIGH,LOW,start,stepstart,step,maxstep)


def SUMBARS(S:Iterable,SN)->Optional[np.ndarray]:
    '''向前累加到指定值到现在的周期数.
:S-数据的一组数据[序列值]
:SN-要达到的数据[常量或序列值]
用法: SUMBARS(S,SN):将S向前累加直到大于等于SN,返回这个区间的周期数,若所有的数据都累加后还不能达到SN,则返回此时前面的总周期数.
返回一组整数'''
    return pyML.SUMBARS(S,SN)


def showMsg(show:bool):
    '''导入模块后是否显示消息，建议使用方法"import fengwo as fw;fw.showMsg(False)"'''
    pyML.showMsg(show)

def time()->float:
    '''返回当前时间，同time.time()，但此函数内部未使用time模块！'''
    return pyML.time()

def getRegId()->str:
    '''返回当前模块的注册Id'''
    return pyML.getRegId()

#以下函数为Windows专用

def binddll(no:int,dllpath:str)->Optional[bool]:
    '''绑定dll文件[Windows系统专用]
:no-要绑定dll文件的函数取值[取值范围：1-10]
:dllpath-要绑定dll文件的路径
成功返回True，失败直接抛出异常'''
    return pyML.binddll(no,dllpath)


def TDXDLL1(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用1号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL1(funcno,ina,inb,inc)

def TDXDLL2(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用2号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL2(funcno,ina,inb,inc)

def TDXDLL3(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用3号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL3(funcno,ina,inb,inc)

def TDXDLL4(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用4号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL4(funcno,ina,inb,inc)

def TDXDLL5(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用5号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL5(funcno,ina,inb,inc)

def TDXDLL6(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用6号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL6(funcno,ina,inb,inc)

def TDXDLL7(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用7号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL7(funcno,ina,inb,inc)

def TDXDLL8(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用9号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL8(funcno,ina,inb,inc)

def TDXDLL9(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用9号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL9(funcno,ina,inb,inc)

def TDXDLL10(funcno:int,ina:Iterable,inb,inc)->Optional[np.ndarray]:
    '''调用10号DLL函数
:funcno-函数号
:ina,inb,inc-输入的3个参数，其中ina必须为序列值
返回值为计算结果的序列'''
    return pyML.TDXDLL10(funcno,ina,inb,inc)