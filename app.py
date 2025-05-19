import streamlit as st
import requests
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Receitas Sustentáveis", layout="wide")

# Bootstrap CDN para estilo elegante
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body {
    background-color: #fefcf9;
}
.container-custom {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 0 12px rgba(0,0,0,0.08);
    color: #333;
    font-family: 'Segoe UI', sans-serif;
}
.header-custom {
    text-align: center;
    padding: 2rem;
    background-color: #ffcc00;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.card-answer {
    background-color: #fff8e1;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #ffecb3;
    margin-top: 1rem;
    font-size: 1.1rem;
    line-height: 1.6;
    color: #3e3e3e;
}
</style>
""", unsafe_allow_html=True)

# Título estilizado com Bootstrap
st.markdown("""
<div class="container header-custom">
    <h1 class="display-6">🍲 Receitas Inteligentes a partir do ChatPDF</h1>
    <p class="lead">Descubra receitas sustentáveis e criativas</p>
</div>
""", unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("CHATPDF_API_KEY")
source_id = os.getenv("CHATPDF_SOURCE_ID")

st.sidebar.header("🔎 Consultar Receita no ChatPDF")
pergunta = st.sidebar.text_input("Digite sua pergunta sobre as receitas")

if pergunta and api_key and source_id:
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "sourceId": source_id,
        "messages": [{"role": "user", "content": pergunta}]
    }

    with st.spinner("Consultando o ChatPDF..."):
        response = requests.post("https://api.chatpdf.com/v1/chats/message", headers=headers, json=payload)

    if response.status_code == 200:
        resposta = response.json().get("content", "Sem resposta gerada.")
        st.markdown(f"""
        <div class="container container-custom">
            <h4>📋 Resposta da consulta:</h4>
            <div class="card-answer">{resposta}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Erro ao consultar a API do ChatPDF.")
        st.text(response.text)
else:
    st.markdown("""
    <div class="container container-custom">
       <p class="text-muted">Sua pergunta irá aparecer aqui..</p>
    </div>
    """, unsafe_allow_html=True)
