import streamlit as st
import requests

st.title("📚 AI勉強計画アシスタント")

# 1. StreamlitのSecretsからHugging Faceのキーを読み込む
API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

# 2. 無料で使える高性能AI（Llama 3）の接続先を設定
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {API_KEY}"}

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 過去のメッセージを画面に表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を受け付ける
if prompt := st.chat_input("勉強したい内容や目標を教えてください！"):
    # ユーザーの入力を履歴に追加して画面に表示
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # AIへの話し掛け方を調整するデータ
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nあなたは親切な勉強のアシスタントです。日本語で回答してください。<|eot_id|><|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n",
        "parameters": {"max_new_tokens": 500, "return_full_text": False}
    }
    
    # AIの返答を生成
    with st.chat_message("assistant"):
        with st.spinner("AIが考えています..."):
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                answer = result[0]['generated_text']
                st.markdown(answer)
                # AIの返答を履歴に追加
                st.session_state["messages"].append({"role": "assistant", "content": answer})
            else:
                st.error("AIの呼び出しに失敗しました。Secretsの設定やキーを確認してください。")

