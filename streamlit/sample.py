import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# タイトル
st.title("My Sample")

# 文字列
st.write("Good morning")

# Table
st.table(
    pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
)

# markdown
st.markdown("# Markdown documents")


# グラフ
animals = ["giraffes", "orangutans", "monkeys", "a", "b"]
populations = [20, 14, 23, 80, 90]

fig = go.Figure(data=[go.Bar(x=animals, y=populations)])

fig.update_layout(
    xaxis=dict(
        tickangle=0, title_text="Animal", title_font={"size": 20}, title_standoff=25
    ),
    yaxis=dict(title_text="Populations", title_standoff=25),
    title="Title",
)

st.plotly_chart(fig, use_container_width=True)


df = pd.read_csv("data/backup.csv")


df = df[df["price"] < 100]["prefectre"]
# データフレーム
st.dataframe(df)


# plotly
# st.plotly_chart(fig, width, height, use_container_width=True or Flase)

# bokeh
# st.bokeh_chart(fig, use_container_width=True or Flase)
