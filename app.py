import streamlit as st
from openai import OpenAI

st.title("AI勉強計画アシスタント")

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# モデルの初期化
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 過去のメッセージを表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を受け付ける
if prompt := st.chat_input("勉強したい内容や目標を教えてください！"):
    # ユーザーの入力を履歴に追加して画面に表示
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの返答を生成して表示
    with st.chat_message("assistant"):
        # システムプロンプト（指示書き）を英語で安全に渡す
        messages_to_send = [
            {"role": "system", "content": "You are a professional study planner. Please create a detailed and encouraging study plan based on the user's request. Respond in Japanese."}
        ] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]
        ]

        # APIを呼び出してテキストとして取得（streamは使わない安全な方法）
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages_to_send
        )
        
        answer = response.choices[0].message.content
        st.markdown(answer)
    
    # AIの返答も履歴に追加
    st.session_state["messages"].append({"role": "assistant", "content": answer})

