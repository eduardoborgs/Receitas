import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Consultas em PDF", layout="centered")

# Estilo com CSS inline
st.markdown("""
    <style>
        .main {
            background-color: #f4f4f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .header, .footer {
            text-align: center;
            padding: 1rem;
        }
        
        .footer {
            font-size: 0.8rem;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<div class="header"><h1>Consultas em PDF</h1><p>Interaja com seu documento através da API do ChatPDF</p></div>', unsafe_allow_html=True)

# Campo para pergunta
st.markdown('<div class="main">', unsafe_allow_html=True)

pergunta = st.text_input("O que você deseja perguntar sobre o PDF?")

if pergunta:
    api_key = os.getenv("CHATPDF_API_KEY")
    source_id = os.getenv("CHATPDF_SOURCE_ID")

    if not api_key or not source_id:
        st.error("Verifique se as variáveis CHATPDF_API_KEY e CHATPDF_SOURCE_ID estão definidas no .env")
    else:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "sourceId": source_id,
            "messages": [
                {"role": "user", "content": pergunta}
            ]
        }

        with st.spinner("Consultando..."):
            response = requests.post("https://api.chatpdf.com/v1/chats/message", headers=headers, json=data)

        if response.status_code == 200:
            resposta = response.json()["content"]
            st.success("Resposta:")
            st.write(resposta)
        else:
            st.error("Erro ao consultar o ChatPDF:")
            st.text(response.text)

st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown('<div class="footer">Desenvolvido por Eduardo Borges - LUSS/CTN usando Streamlit e ChatPDF</div>', unsafe_allow_html=True)
