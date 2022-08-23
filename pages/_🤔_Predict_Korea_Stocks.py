# 코사인 유사도 코드출처 : https://teddylee777.github.io/pandas/cos-sim-stock

import FinanceDataReader as fdr
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime
from PIL import Image

st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Predict Korea Stocks 📊")

st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
st.markdown('<p class="font"> Predict Tomorrow\'s Korea Stocks!</p>', unsafe_allow_html=True)

st.header('국내주식 종목의 주가를 예측해 보세요 📈')


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
if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'Symbol']
    data = fdr.DataReader(code_num)
    with st.spinner('Predicting...'):
        if data.shape[0] >= 60:
            startdate = (datetime.datetime.now()-datetime.timedelta(days=31)).strftime('%Y-%m-%d')
            enddate = datetime.datetime.now().strftime('%Y-%m-%d')
            data_ = data.loc[startdate:enddate]
            close = data_['Close']
            base = (close - close.min()) / (close.max() - close.min())
            window_size = len(base)
            next_date = 5
            moving_cnt = len(data) - window_size - next_date - 1
            def cosine_similarity(x, y):
                return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

            sim_list = []

            for i in range(moving_cnt):
                target = data['Close'].iloc[i:i+window_size]
                target = (target - target.min()) / (target.max() - target.min())
                cos_similarity = cosine_similarity(base, target)
                sim_list.append(cos_similarity)

            top = pd.Series(sim_list).sort_values(ascending=False).head(1).index[0]

            idx=top
            target = data['Close'].iloc[idx:idx+window_size+next_date]
            target = (target - target.min()) / (target.max() - target.min())

            fig = plt.figure(figsize=(20,5))
            plt.plot(base.values, label='base', color='grey')
            plt.plot(target.values, label='target', color='orangered')
            plt.xticks(np.arange(len(target)), list(target.index.strftime('%Y-%m-%d')), rotation=45)
            plt.axvline(x=len(base)-1, c='grey', linestyle='--')
            plt.axvspan(len(base.values)-1, len(target.values)-1, facecolor='ivory', alpha=0.7)
            plt.legend()
            st.pyplot(fig)

            period=5
            preds = data['Change'][idx+window_size: idx+window_size+period]
            cos = round(float(pd.Series(sim_list).sort_values(ascending=False).head(1).values), 2)
            st.markdown(f'현재 주식 상황과 **{cos} %** 유사한 시기의 주식 상황입니다.')
            future = round(preds.mean()*100, 2)
            if future > 0:
                st.markdown(f'위의 주식 상황을 바탕으로 앞으로 5일동안 **{Name}** 주식은 평균 **{future}%** 상승할 것으로 보입니다.')
            elif future < 0:
                st.markdown(f'위의 주식 상황을 바탕으로 앞으로 5일동안 **{Name}** 주식은 평균 **{future}%** 하락할 것으로 보입니다.')

            pred = preds[0]
            predict = data['Close'].tail(1).values * pred #8월 17일꺼에 떨어질 확률 곱하면 0.1이면 1000원 일 때 100원으로 계산 됨. -0.1이면 -100으로 계산 됨
            yesterday_close = data['Close'].tail(1).values #8월 17일꺼


            if pred > 0:
                plus_money = yesterday_close + predict
                plus_money = format(int(plus_money), ',')
                st.markdown(f'내일 **{Name}** 주식은 **{round(pred*100,2)} %** 상승할 예정이고, 주가는 **{plus_money}원**으로 예상됩니다.')
            elif pred < 0:
                minus_money = yesterday_close + predict
                minus_money = format(int(minus_money), ',')
                st.markdown(f'내일 **{Name}** 주식은 **{round(pred*100,2)} %** 하락할 예정이고, 주가는 **{minus_money}원**으로 예상됩니다.')
            else:
                st.markdown(f'내일 **{Name} 주식은 변동이 없을 것으로 예상됩니다.')
        elif data.shape[0] < 60:
            st.markdown(f'**{Name}**은 최근에 상장한 주식으로 예상됩니다.')
            st.markdown('예측할 데이터가 부족합니다.')
            st.markdown('충분한 데이터가 모일 때까지 조금만 기다려 주세요.')
            st.markdown('그때 다시 만나요~')

            image = Image.open('data/waitplease.png')
            st.image(image, width=500)
        st.success('Done!')

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')
