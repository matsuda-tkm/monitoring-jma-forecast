import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import streamlit as st
import json
import os

# 認証
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_dict({
    "type": os.environ.get("TYPE"),
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY"),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
    "universe_domain": os.environ.get("UNIVERSE_DOMAIN")
}, scope)
gc = gspread.authorize(credentials)

# データ取得
if 'df' not in st.session_state:
    df = None
    with st.spinner('データを取得しています...'):
        for i in range(40):
            sheet = gc.open_by_key('14ny128TVh9n-9BHNYPEEAsmlqW5fmYUK1TKO4yFTlSw').worksheet(f'data{i}')
            data = sheet.get_all_values()

            # データを整形
            tmp = pd.DataFrame(data[1:], columns=data[0])
            tmp = tmp.replace('', np.nan)
            tmp = tmp.astype({'pop':'float','tempMin':'float','tempMinUpper':'float','tempMinLower':'float','tempMax':'float','tempMaxUpper':'float','tempMaxLower':'float'})
            if tmp.shape[0] == 0:
                break

            # 結合
            if df is None:
                df = tmp
            else:
                df = pd.concat([df,tmp])
    st.session_state.df = df
else:
    df = st.session_state.df


# 地域名と地域コードの対応表
with open('./areaCode.json', 'r', encoding='utf-8') as f:
    areaCode_dict = json.load(f)

# 天気コードと天気の対応表
with open('./weatherCode.json', 'r', encoding='utf-8') as f:
    weatherCode_dict = json.load(f)


#################### 以下、表示 ####################
st.title('気象庁天気予報追跡アプリ')
st.caption('ここに表示されている天気予報は，気象庁が発表したものです．定期的に気象庁の天気予報を取得して保存し，予報対象日時の1週間前から前日までに発表された予報をまとめて表示しています．')

# targetDateを入力(date_input)
targetDate = st.date_input(
    "予報対象日を選択してください",
    value='today',
    min_value=pd.to_datetime(df['targetDate']).min(),
    max_value=pd.to_datetime(df['targetDate']).max()
).strftime('%Y-%m-%d')

# areaを選択(selectbox)
area = st.selectbox(
    '地域を選択してください',
    list(areaCode_dict.keys()),
    index=list(areaCode_dict.keys()).index('京都府')
)

# 抽出
areaCode = areaCode_dict[area]
sub = df[df['targetDate']+df['areaCode'] == targetDate+'T00:00:00+09:00'+areaCode].copy()

# 予報対象日時
cols0 = st.columns(2)
cols0[0].metric(label='予報対象日', value=targetDate)
cols0[1].metric(label='予報対象地域', value=area)

# 天気
st.divider()
st.write('**天気**')
cols = [st.columns(4) for i in range(4)]
for i,(date,weatherCode) in enumerate(zip(sub['reportDatetime'].values,sub['weatherCode'].values)):
    with cols[i//4][i%4]:
        st.write(date[:10] + '(' + date[11:13] + '時)時点')
        if weatherCode is not np.nan:
            st.image(f'https://www.jma.go.jp/bosai/forecast/img/{weatherCode_dict[str(weatherCode)][0]}')

cols1 = st.columns(2)
cols2 = st.columns(2)
sub['reportDatetime'] = pd.to_datetime(sub['reportDatetime'])

# 最低気温
cols1[0].write('**最低気温**')
cols1[0].line_chart(data=sub.dropna(), x='reportDatetime', y=['tempMin','tempMinLower','tempMinUpper'], color=['#0000ff','#a9ceec','#a9ceec'])
# 最高気温
cols1[1].write('**最高気温**')
cols1[1].line_chart(data=sub.dropna(), x='reportDatetime', y=['tempMax','tempMaxLower','tempMaxUpper'], color=['#ff0000','#ffb6c1','#ffb6c1'])
# 信頼度
cols2[0].write('**信頼度**')
cols2[0].line_chart(data=sub.dropna(), x='reportDatetime', y='reliability')
# 降水確率
cols2[1].write('**降水確率**')
cols2[1].area_chart(data=sub.dropna(), x='reportDatetime', y='pop')
