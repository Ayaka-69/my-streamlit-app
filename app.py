import streamlit as st # 小文字に修正
from openai import OpenAI

st.title("AI勉強計画アシスタント")

# APIキーの設定
API_KEY=st.secrets["HUGGINGFACE_API_KEY"])

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {API_KEY}"}

# モデルの初期化
if "hugginhface_model" not in st.session_state:
    st.session_state["huggingface_model"] = "gpt-4o-mini"

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 過去のメッセージ（ユーザーとAI両方）を画面に表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を受け付ける
if prompt := st.chat_input("勉強したい内容や目標を教えてください！"):
    # 1. ユーザーの入力を履歴に追加して画面に表示
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AIの返答を生成
    with st.chat_message("assistant"):
        messages_to_send = [
            {"role": "system", "content": "You are a professional study planner. Please create a detailed and encouraging study plan based on the user's request. Respond in Japanese."}
        ] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]
        ]

        response = client.chat.completions.create(
            model=st.session_state["huggingface_model"],
            messages=messages_to_send
        )
        
        answer = response.choices[0].message.content
        
        # 3. 先に履歴（session_state）に保存してから、画面に表示する（これで画面更新時も消えなくなります）
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.markdown(answer)

