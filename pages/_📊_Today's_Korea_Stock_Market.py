import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Korea Stock Market 📊")

st.markdown(""" <style> .font {
font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font"> Today\'s Korea Stock Market!</p>', unsafe_allow_html=True)

st.header('Korea Stocks 📈')

Stockcode = pd.read_csv('data/Stockcode.csv')
name_list = Stockcode['Name'].tolist()
name_list.insert(0, '')
choice = st.selectbox('검색하실 주식 종목명을 입력해 주세요.',name_list)


for i in range(len(name_list)):
    if choice == name_list[i]:
        choice_name = Stockcode.loc[Stockcode['Name'] == name_list[i], 'Name'].values
        choice_name_to_str =np.array2string(choice_name).strip("[]")
        Name = choice_name_to_str.strip("''")
Stockcode.set_index('Name', inplace=True)
Code_name_list = Stockcode.index.tolist()
with st.spinner('Wait for it...'):
    if Name in Code_name_list:
        code_num = Stockcode.at[Name, 'Symbol']
        df = fdr.DataReader(code_num)
        col1, col2, col3 = st.columns(3)
        col1.metric("현재 주식가격",format(df['Close'].tail(1)[0], ',')+'원', "%d원" %(df['Close'].diff().tail(1)[0]))
        col2.metric("현재 거래량", format(df['Volume'].tail(1)[0], ','),"%.2f%%" %(df['Volume'].pct_change().tail(1)[0] * 100))
        col3.metric("전일 대비 가격", "%d원" %(df['Close'].diff().tail(1)[0]), "%.2f%%" %(df['Change'].tail(1)[0] * 100))

        fig = px.line(df, y='Close', title='{} 종가 Time Series'.format(Name))

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color = 'tomato',
                    decreasing_line_color = 'royalblue',
                    showlegend = False)])

        fig2.update_layout(title='{} Candlestick chart'.format(Name))
        st.plotly_chart(fig2, use_container_width=True)

    elif Name not in Code_name_list:
        st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')