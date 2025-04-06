import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# 全国の主要都市と対応する city code（気象庁のAPIより取得）
city_code_list = {
    "札幌": "016010",
    "青森": "020010",
    "仙台": "040010",
    "東京": "130010",
    "横浜": "140010",
    "新潟": "150010",
    "金沢": "170010",
    "名古屋": "230010",
    "大阪": "270000",
    "広島": "340010",
    "高知": "390010",
    "福岡": "400010",
    "熊本": "430010",
    "那覇": "471010",
}

city_code_index = "東京"  # デフォルトの都市

st.title("お天気アプリ ☀️🌧️")
st.write("調べたい地域を選んでください。")

city_code_index = st.selectbox("地域を選んでください。", city_code_list.keys())
city_code = city_code_list[city_code_index]

st.write("選択中の地域: " + city_code_index)

# APIリクエスト
url = "https://weather.tsukumijima.net/api/forecast/city/" + city_code
response = requests.get(url)
weather_json = response.json()
now_hour = datetime.now().hour

# 現在の時間帯に応じた降水確率を取得
if 0 <= now_hour < 6:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T00_06']
elif 6 <= now_hour < 12:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T06_12']
elif 12 <= now_hour < 18:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T12_18']
else:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T18_24']

st.write("現在の降水確率 : " + weather_now)

# 3日分の降水確率をDataFrameにまとめて表示
df1 = pd.DataFrame(weather_json['forecasts'][0]['chanceOfRain'], index=["今日"])
df2 = pd.DataFrame(weather_json['forecasts'][1]['chanceOfRain'], index=["明日"])
df3 = pd.DataFrame(weather_json['forecasts'][2]['chanceOfRain'], index=["明後日"])
df = pd.concat([df1, df2, df3])
st.dataframe(df)

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        .css-1rs6os.edgvbvh3 {display: none;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
