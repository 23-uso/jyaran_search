#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[2]:


# jyaran.csvを読み込む
jyaran_df = pd.read_csv("jyaran.csv")


# In[3]:


# streamlitの部品設計
st.title("じゃらん")

# フィルタ設定
price_limit = st.slider("最低宿泊価格の上限", min_value=1000, max_value=200000, step=4000, value=10000)
score_limit = st.slider("人気のスコアの下限", min_value=0.0, max_value=5.0, step=1.0, value=5.0)


# In[4]:


# フィルタ処理
filtered_df = jyaran_df[
    (jyaran_df['価格7'] <= price_limit) &
    (jyaran_df['概要'] >= score_limit)
]


# In[5]:


# 散布図の作成 (人気スコア × 最低宿泊価格)
fig = px.scatter(
    filtered_df,
    x='価格7',
    y='概要',
    hover_data=['タイトル', '概要9'],
    title='人気スコアと最低宿泊価格の散布図'
)

st.plotly_chart(fig)


# In[6]:


# 詳細リンクの表示
selected_jyaran = st.selectbox('気になる宿を選んで詳細を確認', filtered_df['タイトル'])

if selected_jyaran:
    url = filtered_df[filtered_df['タイトル'] == selected_jyaran]['タイトルURL'].values[0]
    st.markdown(f"[{selected_jyaran}のページへ移動]({url})",unsafe_allow_html=True)


# In[7]:


sort_key = st.selectbox(
    "ランキング基準を選んでください",
    ("概要", "pop_score", "概要9", "価格7")
)

ascending = True if sort_key == "価格7" else False


# In[8]:


st.subheader(f"{sort_key} による宿ランキング (上位10件)")

ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)

# 必要な列だけ表示
st.dataframe(ranking_df[["タイトル", "価格7", "pop_score", "概要", "概要9"]])


# In[ ]:




