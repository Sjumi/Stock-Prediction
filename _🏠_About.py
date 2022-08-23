import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

logo = Image.open('data/stockcode.jpg')

st.markdown(""" <style> .font {
font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
</style> """, unsafe_allow_html=True)
st.title('저희와 함께 반포자이로 가시죠.')    

st.markdown('<p class="font">Hello!\n\n저희는 **반포자이까지 한걸음** 입니다.\n\n저희는 *부족한 투자 지식*으로 인한 *투자손실*을 예방하고자 내일의 **주가를 예측** 해 보는 사이트입니다.\n\n**재미로** 봐주시기 바랍니다.</p>', unsafe_allow_html=True)
st.markdown('투자하시기 전에 [유의사항](https://map-jo-final-project---about-cmvol8.streamlitapp.com/%EF%B8%8F_Caution)을 꼭 읽어주시길 바랍니다!')
image = Image.open('data/stockcode.jpg')
st.image(image, width=800, caption= 'The Great GATSBY')
