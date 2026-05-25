import streamlit as st
import requests

st.title("📚 AI勉強計画アシスタント")

# StreamlitのSecretsからHugging Faceのキーを読み込む
API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

# 使用するAIモデルを指定
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {API_KEY}"}

prompt = st.text_input("勉強したい内容や目標を教えてください！")

if prompt:
    # AIへの話し掛け方を調整する
    payload = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nあなたは親切な勉強のアシスタントです。日本語で回答してください。<|eot_id|><|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n",
        "parameters": {"max_new_tokens": 500, "return_full_text": False}
    }
    
    with st.spinner("AIが考えています..."):
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # 返ってきたテキストを表示
            st.write(result[0]['generated_text'])
