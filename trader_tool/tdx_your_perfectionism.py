from xg_tdx_func.xg_tdx_func import *
import pandas as pd
class tdx_your_perfectionism:
    def __init__(self):
        '''
        通达信十全十美指标
        '''
        pass
    def tdx_your_perfectionism(self,df):
        '''
        自定义十全十美
        填充背景
        DIFF赋值:收盘价的8日指数移动平均-收盘价的13日指数移动平均
        DEA赋值:DIFF的5日指数移动平均
        输出A1:当满足条件DIFF>DEA时,在5和10位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件DIFF<DEA时,在5和10位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        数据分析与运用1赋值:(收盘价-8日内最低价的最低值)/(8日内最高价的最高值-8日内最低价的最低值)*100
        K赋值:数据分析与运用1的3日[1日权重]移动平均
        D赋值:K的3日[1日权重]移动平均
        输出A2:当满足条件K>D时,在10和15位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件K<D时,在10和15位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        LC赋值:1日前的收盘价
        CBA1赋值:(收盘价-LC和0的较大值的5日[1日权重]移动平均)/(收盘价-LC的绝对值的5日[1日权重]移动平均)*100
        CBA2赋值:(收盘价-LC和0的较大值的13日[1日权重]移动平均)/(收盘价-LC的绝对值的13日[1日权重]移动平均)*100
        输出A3:当满足条件CBA1>CBA2时,在15和20位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件CBA1<CBA2时,在15和20位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        数据分析与运用赋值:-(13日内最高价的最高值-收盘价)/(13日内最高价的最高值-13日内最低价的最低值)*100
        指标营地1赋值:数据分析与运用的3日[1日权重]移动平均
        指标营地2赋值:指标营地1的3日[1日权重]移动平均
        输出A4:当满足条件指标营地1>指标营地2时,在20和25位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件指标营地1<指标营地2时,在20和25位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        BBI赋值:(收盘价的3日简单移动平均+收盘价的6日简单移动平均+收盘价的12日简单移动平均+收盘价的24日简单移动平均)/4
        输出A5:当满足条件收盘价>BBI时,在25和30位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件收盘价<BBI时,在25和30位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        MTM赋值:收盘价-1日前的收盘价
        MMS赋值:100*MTM的5日指数移动平均的3日指数移动平均/MTM的绝对值的5日指数移动平均的3日指数移动平均
        MMM赋值:100*MTM的13日指数移动平均的8日指数移动平均/MTM的绝对值的13日指数移动平均的8日指数移动平均
        输出A6:当满足条件MMS>MMM时,在30和35位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件MMS<MMM时,在30和35位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        MAV赋值:(收盘价*2+最高价+最低价)/4
        SK赋值:MAV的13日指数移动平均-MAV的34日指数移动平均
        SD赋值:SK的5日指数移动平均
        空方主力赋值:(-2*(SK-SD))*3.8,画绿色
        多方主力赋值:(2*(SK-SD))*3.8,画红色
        输出A7:当满足条件多方主力>空方主力时,在37和42位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        当满足条件多方主力<空方主力时,在37和42位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        MA11赋值:收盘价的5日简单移动平均
        MA22赋值:1日前的收盘价的5日简单移动平均
        当满足条件MA22>MA11时,在43和48位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        输出A8:当满足条件MA22<=MA11时,在43和48位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        XYZ2赋值:如果月份<12,返回1,否则返回1
        XYZ3赋值:(2*收盘价+最高价+最低价)/4
        XYZ4赋值:34日内最低价的最低值
        XYZ5赋值:34日内最高价的最高值
        主力赋值:(XYZ3-XYZ4)/(XYZ5-XYZ4)*100的13日指数移动平均*XYZ2
        散户赋值:0.667*1日前的主力+0.333*主力的2日指数移动平均
        当满足条件主力<散户时,在49和54位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        输出A9:当满足条件主力>散户时,在49和54位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        输出A10:当满足条件(多方主力>空方主力)AND(MA22<=MA11)AND(主力>散户)时,在56和61位置之间画柱状线,宽度为3,0不为0则画空心柱.,画黄色
        当满足条件(多方主力<空方主力)AND(MA22>MA11)AND(主力<散户)时,在56和61位置之间画柱状线,宽度为3,0不为0则画空心柱.,画青色
        输出A11:当满足条件(多方主力>空方主力)AND(MA22<=MA11)AND(主力>散户)AND(DIFF>DEA)AND(K>D)AND(CBA1>CBA2)AND(指标营地1>指标营地2)AND(收盘价>BBI)AND(MMS>MMM)时,在63和68位置之间画柱状线,宽度为3,0不为0则画空心柱.,画洋红色
        ABC1赋值:收盘价的10日简单移动平均
        ABC2赋值:收盘价的55日简单移动平均
        ABC3赋值:(3日前的收盘价-收盘价)/3日前的收盘价*100>5
        ABC4赋值:ABC3的10日过滤
        ABC5赋值:上次ABC4距今天数
        ABC6赋值:ABC5+2日前的最高价
        ABC7赋值:ABC5+1日前的最高价
        ABC8赋值:ABC5日前的最高价
        ABC9赋值:ABC6和ABC7的较大值
        ABC10赋值:ABC9和ABC8的较大值
        ABC11赋值:(收盘价-1日前的收盘价)/1日前的收盘价*100>5
        ABC12赋值:ABC5<150
        ABC13赋值:(开盘价-ABC10)/ABC10*100<30
        ABC14赋值:(收盘价-ABC5日内最低价的最低值)/ABC5日内最低价的最低值*100<50
        ABC15赋值:(收盘价-5日前的开盘价)/5日前的开盘价*100<30
        ABC16赋值:成交量(手)/成交量(手)的5日简单移动平均<3.5
        ABC17赋值:(收盘价-89日前的收盘价)/89日前的收盘价*100<80
        ABC18赋值:ABC11 AND ABC12 AND ABC13 AND ABC14 AND ABC15 AND ABC16 AND ABC17
        ABC19赋值:ABC18的15日过滤
        ABC20赋值:(收盘价-ABC2)/ABC2<0.1
        ABC21赋值:(收盘价-ABC1)/ABC1<0.3
        ABC22赋值:(ABC20=1 AND ABC21=1)*0.2
        ABC23赋值:(ABC22=0 AND 1日前的ABC22=0.2 AND 1日前的统计10日中满足ABC22=0.2的天数=10=1)*(-0.1)
        ABC24赋值:ABC23=(-0.1)
        ABC25赋值:ABC19 OR ABC24
        ABC27赋值:成交量(手)/1日前的成交量(手)>1.2 AND 收阳线OROSE (最低价>1日前的最高价 AND 收阴线ANDN 成交量(手)/1日前的成交量(手)>1.2)
        ABC28赋值:如果模糊匹配品种代码OR(模糊匹配品种代码ANDDATE>=1200824),返回收盘价>=计算涨停价ANDCLOSE=最高价,否则返回收盘价>=计算涨停价ANDCLOSE=最高价
        共振赋值:ABC25 AND ABC27 AND ABC28 AND 1日前的取反 AND (多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (收盘价>BBI) AND (MMS>MMM)
        当满足条件共振时,在75位置画9号图标
        '''
        CLOSE=df['close']
        OPEN=df['open']
        LOW=df['low']
        HIGH=df['high']
        C=df['close']
        L=df['low']
        H=df['high']
        VOL=df['volume']
        收盘价=df['close']
        data=pd.DataFrame()
        data['date']=df['date']
        #填充背景
        #DRAWGBK(C>1,RGB(0,0,0),RGB(1,1,1),1,0,0);
        #DIFF赋值:收盘价的8日指数移动平均-收盘价的13日指数移动平均
        DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
        DEA=EMA(DIFF,5)
        #输出A1:当满足条件DIFF>DEA时,在5和10位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        '''
        A1=STICKLINE(DIFF>DEA,5,10,2,1),COLORRED;
        #当满足条件DIFF<DEA时,在5和10位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        STICKLINE(DIFF<DEA,5,10,2,1),COLORGREEN;
        '''
        data['A1']=IF(DIFF>DEA,'空红','空绿')
        #数据分析与运用1赋值:(收盘价-8日内最低价的最低值)/(8日内最高价的最高值-8日内最低价的最低值)*100
        数据分析与运用1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
        #K赋值:数据分析与运用1的3日[1日权重]移动平均
        K=SMA(数据分析与运用1,3,1)
        #D赋值:K的3日[1日权重]移动平均
        D=SMA(K,3,1)
        '''
        输出A2:当满足条件K>D时,在10和15位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件K<D时,在10和15位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        A2:STICKLINE(K>D,10,15,2,1),COLORRED;
        STICKLINE(K<D,10,15,2,1),COLORGREEN;
        '''
        data['A2']=IF(K>D,'空红','空绿')
        #LC赋值:1日前的收盘价
        LC=REF(CLOSE,1)
        # CBA1赋值:(收盘价-LC和0的较大值的5日[1日权重]移动平均)/(收盘价-LC的绝对值的5日[1日权重]移动平均)*100
        CBA1=(SMA(MAX(CLOSE-LC,0),5,1))/(SMA(ABS(CLOSE-LC),5,1))*100
        #CBA2赋值:(收盘价-LC和0的较大值的13日[1日权重]移动平均)/(收盘价-LC的绝对值的13日[1日权重]移动平均)*100
        CBA2=(SMA(MAX(CLOSE-LC,0),13,1))/(SMA(ABS(CLOSE-LC),13,1))*100
        ''''
        输出A3:当满足条件CBA1>CBA2时,在15和20位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件CBA1<CBA2时,在15和20位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        A3:STICKLINE(CBA1>CBA2,15,20,2,1),COLORRED;
        STICKLINE(CBA1<CBA2,15,20,2,1),COLORGREEN;
        '''
        data['A3']=IF(CBA1>CBA2,'空红','空绿')
        #数据分析与运用赋值:-(13日内最高价的最高值-收盘价)/(13日内最高价的最高值-13日内最低价的最低值)*100
        数据分析与运用=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
        # 指标营地1赋值:数据分析与运用的3日[1日权重]移动平均
        指标营地1=SMA(数据分析与运用,3,1)
        #指标营地2赋值:指标营地1的3日[1日权重]移动平均
        指标营地2=SMA(指标营地1,3,1)
        '''
        输出A4:当满足条件指标营地1>指标营地2时,在20和25位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件指标营地1<指标营地2时,在20和25位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        A4:STICKLINE(指标营地1>指标营地2,20,25,2,1),COLORRED;
        STICKLINE(指标营地1<指标营地2,20,25,2,1),COLORGREEN;
        '''
        data['A4']=IF(指标营地1>指标营地2,'空红','空绿')
        # BBI赋值:(收盘价的3日简单移动平均+收盘价的6日简单移动平均+收盘价的12日简单移动平均+收盘价的24日简单移动平均)/4
        BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
        '''
        输出A5:当满足条件收盘价>BBI时,在25和30位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件收盘价<BBI时,在25和30位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        A5:STICKLINE(CLOSE>BBI,25,30,2,1),COLORRED;
        STICKLINE(CLOSE<BBI,25,30,2,1),COLORGREEN;
        '''
        data['A5']=IF(CLOSE>BBI,'空红','空绿')
        #MTM赋值:收盘价-1日前的收盘价
        MTM=CLOSE-REF(CLOSE,1)
        # MMS赋值:100*MTM的5日指数移动平均的3日指数移动平均/MTM的绝对值的5日指数移动平均的3日指数移动平均
        MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
        #MMM赋值:100*MTM的13日指数移动平均的8日指数移动平均/MTM的绝对值的13日指数移动平均的8日指数移动平均
        MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
        ''''
        输出A6:当满足条件MMS>MMM时,在30和35位置之间画柱状线,宽度为2,1不为0则画空心柱.,画红色
        当满足条件MMS<MMM时,在30和35位置之间画柱状线,宽度为2,1不为0则画空心柱.,画绿色
        A6:STICKLINE(MMS>MMM,30,35,2,1),COLORRED;
        STICKLINE(MMS<MMM,30,35,2,1),COLORGREEN;
        '''
        data['A6']=IF(MMS>MMM,'空红','空绿')
        # MAV赋值:(收盘价*2+最高价+最低价)/4
        MAV=(C*2+H+L)/4
        #SK赋值:MAV的13日指数移动平均-MAV的34日指数移动平均
        SK=EMA(MAV,13)-EMA(MAV,34)
        #SD赋值:SK的5日指数移动平均
        SD=EMA(SK,5)
        #空方主力赋值:(-2*(SK-SD))*3.8,画绿色
        空方主力=(-2*(SK-SD))*3.8
        #多方主力赋值:(2*(SK-SD))*3.8,画红色
        多方主力=(2*(SK-SD))*3.8
        '''
        输出A7:当满足条件多方主力>空方主力时,在37和42位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        当满足条件多方主力<空方主力时,在37和42位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        A7:STICKLINE(多方主力>空方主力,37,42,2,0),COLORRED;
        STICKLINE(多方主力<空方主力,37,42,2,0),COLORGREEN;
        '''
        data['A7']=IF(多方主力>空方主力,'实红','实绿')
        # MA11赋值:收盘价的5日简单移动平均
        MA11=MA(CLOSE,5)
        #MA22赋值:1日前的收盘价的5日简单移动平均
        MA22=REF(MA(CLOSE,5),1)
        '''
        当满足条件MA22>MA11时,在43和48位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        输出A8:当满足条件MA22<=MA11时,在43和48位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        STICKLINE(MA22>MA11,43,48,2,0),COLORGREEN;
        A8:STICKLINE(MA22<= MA11,43,48,2,0),COLORRED;
        '''
        data['A8']=IF(MA22<MA11,'实红','实绿')
        #XYZ2赋值:如果月份<12,返回1,否则返回1
        XYZ2=IF(1<12,1,1)
        #XYZ3赋值:(2*收盘价+最高价+最低价)/4
        XYZ3=(2*CLOSE+HIGH+LOW)/4
        #XYZ4赋值:34日内最低价的最低值
        XYZ4=LLV(LOW,34)
        #XYZ5赋值:34日内最高价的最高值
        XYZ5=HHV(HIGH,34)
        #主力赋值:(XYZ3-XYZ4)/(XYZ5-XYZ4)*100的13日指数移动平均*XYZ2
        主力=EMA((XYZ3-XYZ4)/(XYZ5-XYZ4)*100,13)*XYZ2
        #散户赋值:0.667*1日前的主力+0.333*主力的2日指数移动平均
        散户=EMA(0.667*REF(主力,1)+0.333*主力,2)
        '''
        当满足条件主力<散户时,在49和54位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        输出A9:当满足条件主力>散户时,在49和54位置之间画柱状线,宽度为2,0不为0则画空心柱.,画红色
        STICKLINE(主力<散户,49,54,2,0),COLORGREEN;
        A9:STICKLINE(主力>散户,49,54,2,0),COLORRED;
        '''
        data['A9']=IF(主力>散户,'实红','实绿')
        '''
        输出A10:当满足条件(多方主力>空方主力)AND(MA22<=MA11)AND(主力>散户)时,在56和61位置之间画柱状线,宽度为3,0不为0则画空心柱.,画黄色
        当满足条件(多方主力<空方主力)AND(MA22>MA11)AND(主力<散户)时,在56和61位置之间画柱状线,宽度为3,0不为0则画空心柱.,画青色
        A10:STICKLINE((多方主力>空方主力) AND(MA22<= MA11) AND (主力>散户) ,56,61,3,0),COLORYELLOW;
        STICKLINE((多方主力<空方主力) AND(MA22>MA11) AND (主力<散户) ,56,61,3,0),COLORCYAN;
        '''
        data['A10']=IF(AND(AND(多方主力>空方主力,MA22<= MA11),主力>散户),'实黄','实青')
        #data['A10_1']=IF(AND(AND(多方主力<空方主力,MA22> MA11),主力>散户),'实青','无')
        # 输出A11:当满足条件(多方主力>空方主力)AND(MA22<=MA11)AND(主力>散户)AND(DIFF>DEA)AND(K>D)AND(CBA1>CBA2)AND(指标营地1>指标营地2)AND(收盘价>BBI)AND(MMS>MMM)时,在63和68位置之间画柱状线,宽度为3,0不为0则画空心柱.,画洋红色
        #A11:STICKLINE((多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (CLOSE>BBI) AND (MMS>MMM),63,68,3,0),COLORMAGENTA;
        #
        data['A11']=IF(AND(AND(AND(AND(AND(AND(AND(AND(多方主力>空方主力,MA22<=MA11),主力>散户),DIFF>DEA),K>D),CBA1>CBA2),指标营地1>指标营地2),收盘价>BBI),MMS>MMM),'实紫','无')
        '''
        ABC1赋值:收盘价的10日简单移动平均
        ABC2赋值:收盘价的55日简单移动平均
        ABC3赋值:(3日前的收盘价-收盘价)/3日前的收盘价*100>5
        ABC4赋值:ABC3的10日过滤
        ABC5赋值:上次ABC4距今天数
        ABC6赋值:ABC5+2日前的最高价
        ABC7赋值:ABC5+1日前的最高价
        ABC8赋值:ABC5日前的最高价
        ABC9赋值:ABC6和ABC7的较大值
        ABC10赋值:ABC9和ABC8的较大值
        ABC11赋值:(收盘价-1日前的收盘价)/1日前的收盘价*100>5
        ABC12赋值:ABC5<150
        ABC13赋值:(开盘价-ABC10)/ABC10*100<30
        ABC14赋值:(收盘价-ABC5日内最低价的最低值)/ABC5日内最低价的最低值*100<50
        ABC15赋值:(收盘价-5日前的开盘价)/5日前的开盘价*100<30
        ABC16赋值:成交量(手)/成交量(手)的5日简单移动平均<3.5
        ABC17赋值:(收盘价-89日前的收盘价)/89日前的收盘价*100<80
        ABC18赋值:ABC11 AND ABC12 AND ABC13 AND ABC14 AND ABC15 AND ABC16 AND ABC17
        ABC19赋值:ABC18的15日过滤
        ABC20赋值:(收盘价-ABC2)/ABC2<0.1
        ABC21赋值:(收盘价-ABC1)/ABC1<0.3
        ABC22赋值:(ABC20=1 AND ABC21=1)*0.2
        ABC23赋值:(ABC22=0 AND 1日前的ABC22=0.2 AND 1日前的统计10日中满足ABC22=0.2的天数=10=1)*(-0.1)
        ABC24赋值:ABC23=(-0.1)
        ABC25赋值:ABC19 OR ABC24
        ABC27赋值:成交量(手)/1日前的成交量(手)>1.2 AND 收阳线OROSE (最低价>1日前的最高价 AND 收阴线ANDN 成交量(手)/1日前的成交量(手)>1.2)
        ABC28赋值:如果模糊匹配品种代码OR(模糊匹配品种代码ANDDATE>=1200824),返回收盘价>=计算涨停价ANDCLOSE=最高价,否则返回收盘价>=计算涨停价ANDCLOSE=最高价
        共振赋值:ABC25 AND ABC27 AND ABC28 AND 1日前的取反 AND (多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (收盘价>BBI) AND (MMS>MMM)
        当满足条件共振时,在75位置画9号图标
        '''
        '''
        ABC1=MA(CLOSE,10)
        ABC2=MA(CLOSE,55)
        ABC3=(REF(CLOSE,3)-CLOSE)/REF(CLOSE,3)*100>5
        ABC4=FILTER(ABC3,10)
        ABC5=BARSLAST(ABC4)
        ABC6=REF(HIGH,ABC5+2)
        ABC7=REF(HIGH,ABC5+1)
        ABC8=REF(HIGH,ABC5)
        ABC9=MAX(ABC6,ABC7)
        ABC10=MAX(ABC9,ABC8)
        ABC11=(CLOSE-REF(CLOSE,1))/REF(CLOSE,1)*100>5
        ABC12=ABC5<150
        ABC13=(OPEN-ABC10)/ABC10*100<30
        ABC14=(CLOSE-LLV(LOW,ABC5))/LLV(LOW,ABC5)*100<50
        ABC15=(CLOSE-REF(OPEN,5))/REF(OPEN,5)*100<30
        ABC16=VOL/MA(VOL,5)<3.5
        ABC17=(CLOSE-REF(CLOSE,89))/REF(CLOSE,89)*100<80
        ABC18=AND(AND(AND(AND(AND(AND(ABC11,ABC12),ABC13),ABC14),ABC15),ABC16),ABC17)
        ABC19=FILTER(ABC18,15)
        ABC20=(CLOSE-ABC2)/ABC2<0.1
        ABC21=(CLOSE-ABC1)/ABC1<0.3
        ABC22=AND(ABC20=1,ABC21=1)*0.2
        REF_ABC22=REF(ABC22,1)==0.2
        '''
        '''
        COUNT_ABC22=ABC22==0.2
        COUNT_ABC22=COUNT(COUNT_ABC22,10)=10
        ABC23=AND(ABC22=0,REF(REF_ABC22,1)) AND REF(COUNT(ABC22=0.2,10)=10,1)=1)*(-0.1)
        ABC24=ABC23=(-0.1)
        ABC25=NOT(ABC19,ABC24)
        ABC27=VOL/REF(VOL,1)>1.2 AND CLOSE>OPEN OR (LOW>REF(HIGH,1) AND OPEN>CLOSE AND VOL/REF(VOL,1)>1.2);
        ABC28=IF(CODELIKE(3) OR (CODELIKE(4) AND DATE>=1200824),CLOSE>=ZTPRICE(REF(CLOSE,1),0.2) AND CLOSE=HIGH,CLOSE>=ZTPRICE(REF(CLOSE,1),0.1) AND CLOSE=HIGH);
        共振:=ABC25 AND ABC27 AND ABC28 AND REF(NOT(ABC28),1) AND (多方主力>空方主力) AND (MA22<= MA11) AND (主力>散户) AND (DIFF>DEA) AND (K>D) AND (CBA1>CBA2) AND (指标营地1>指标营地2) AND (CLOSE>BBI) AND (MMS>MMM);
        DRAWICON(共振,75,9);
        '''
        for i in ['A1','A2','A3','A4','A5','A6']:
            data['{}_1'.format(i)]=data[i].apply(lambda x: 1 if x=='空红' else 0)
        data['六脉神剑']=data[ ['A1_1','A2_1','A3_1','A4_1','A5_1','A6_1']].sum(axis=1)
        for i in ['A1','A2','A3','A4','A5','A6']:
            del data['{}_1'.format(i)]
        for i in ['A7','A8','A9']:
            data['{}_1'.format(i)]=data[i].apply(lambda x: 1 if x=='实红' else 0)
        data['主力']=data[ ['A7_1','A8_1','A9_1']].sum(axis=1)
        for i in ['A7','A8','A9']:
            del data['{}_1'.format(i)]
        data['共振']=data['A11'].apply(lambda x: 1 if x=='实紫' else 0)
        return data