import streamlit as st
import pandas as pd
import json
import os
import glob
import datetime
import sys

# 添加当前目录到 sys.path 以便导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from 法玛全天候趋势回归动量指数风控策略 import joinquant_trader
try:
    from trader_tool.policy_blacklist import policy_blacklist
except ImportError:
    policy_blacklist = None

st.set_page_config(page_title="量化策略监控面板", layout="wide", page_icon="📈")

st.title("📊 法玛全天候趋势回归动量指数风控策略 - 监控面板")

# Sidebar
st.sidebar.header("⚙️ 控制面板")

def load_config():
    try:
        if os.path.exists('分析配置.json'):
            with open('分析配置.json','r',encoding='utf-8') as f:
                text=json.loads(f.read())
        else:
            st.sidebar.error("缺少 分析配置.json")
            text = None
            
        if os.path.exists('策略配置.json'):
            with open('策略配置.json','r',encoding='utf-8') as f:
                st_text=json.loads(f.read())
        else:
            st.sidebar.error("缺少 策略配置.json")
            st_text = None
            
        return text, st_text
    except Exception as e:
        st.sidebar.error(f"配置文件读取失败: {e}")
        return None, None

text, st_text = load_config()

if st.sidebar.button("🚀 手动执行策略"):
    if text and st_text:
        with st.spinner("正在初始化并执行策略..."):
            try:
                trader_tool=text.get('交易系统')
                exe=text.get('同花顺下单路径')
                tesseract_cmd=text.get('识别软件安装位置')
                qmt_path=text.get('qmt路径')
                qmt_account=text.get('qmt账户')
                qmt_account_type=text.get('qmt账户类型')
                data_api=text.get('交易数据源')
                
                trader = joinquant_trader(
                    trader_tool=trader_tool,
                    exe=exe,
                    tesseract_cmd=tesseract_cmd,
                    qmt_path=qmt_path,
                    qmt_account=qmt_account,
                    qmt_account_type=qmt_account_type,
                    data_api=data_api
                )
                
                if trader.connact():
                    st.info("交易系统连接成功，开始执行策略逻辑...")
                    trader.trade()
                    st.success("策略执行完成！请查看最新日志。")
                else:
                    st.error("连接交易系统失败！请检查配置或终端状态。")
            except Exception as e:
                st.error(f"执行过程中发生错误: {e}")
    else:
        st.error("无法执行策略：配置文件缺失。")

st.sidebar.markdown("---")
st.sidebar.info(f"当前环境: {os.getcwd()}")
st.sidebar.info(f"系统时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 账户资金状况")
    account_file = os.path.join('账户数据', '账户数据.json')
    if os.path.exists(account_file):
        try:
            # 尝试直接读取为DataFrame
            df = pd.read_json(account_file)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            # 如果失败，尝试作为普通JSON读取展示
            try:
                with open(account_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                st.json(data)
            except Exception as e2:
                st.error(f"读取账户数据失败: {e}")
    else:
        st.warning("暂无账户数据文件 (账户数据/账户数据.json)")

with col2:
    st.subheader("📋 当前持仓信息")
    position_file = os.path.join('持股数据', '持股数据.json')
    if os.path.exists(position_file):
        try:
            df = pd.read_json(position_file)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            try:
                with open(position_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                st.json(data)
            except Exception as e2:
                st.error(f"读取持仓数据失败: {e}")
    else:
        st.warning("暂无持仓数据文件 (持股数据/持股数据.json)")

st.markdown("---")

st.subheader("⚠️ 黑名单监控")
if policy_blacklist:
    if st.button("刷新黑名单数据"):
        try:
            with st.spinner("正在获取最新黑名单数据..."):
                bl = policy_blacklist()
                stock_bl = bl.get_stock_policy_blacklist()
                etf_bl = bl.get_etf_policy_blacklist()
                bond_bl = bl.get_bond_policy_blacklist()
                
                tab1, tab2, tab3 = st.tabs(["股票黑名单", "ETF黑名单", "转债黑名单"])
                with tab1:
                    st.dataframe(stock_bl, use_container_width=True)
                with tab2:
                    st.dataframe(etf_bl, use_container_width=True)
                with tab3:
                    st.dataframe(bond_bl, use_container_width=True)
        except Exception as e:
            st.error(f"获取黑名单数据失败: {e}")
    else:
        st.info("点击上方按钮刷新黑名单数据")
else:
    st.warning("未找到 trader_tool.policy_blacklist 模块，无法显示黑名单监控。")

st.markdown("---")
st.subheader("📝 最新策略日志")

# Find latest log file
try:
    # 递归查找所有log文件
    log_files = glob.glob('log/**/*.log', recursive=True)
    if log_files:
        # 按修改时间排序，最新的在前
        latest_log = max(log_files, key=os.path.getctime)
        st.caption(f"日志文件路径: `{latest_log}` (最后修改: {datetime.datetime.fromtimestamp(os.path.getctime(latest_log)).strftime('%Y-%m-%d %H:%M:%S')})")
        
        with open(latest_log, 'r', encoding='utf-8') as f:
            log_content = f.read()
            
        # 显示日志内容，自动滚动到底部
        st.text_area("日志内容", value=log_content, height=500, disabled=True)
    else:
        st.info("log/ 目录下暂无日志文件。")
except Exception as e:
    st.error(f"查找或读取日志文件失败: {e}")

if __name__ == '__main__':
    try:
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
    except ImportError:
        print("请先安装 streamlit: pip install streamlit")
    except Exception as e:
        print(f"启动失败: {e}")
