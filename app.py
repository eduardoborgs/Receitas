import streamlit as st
import requests
import os
from dotenv import load_dotenv
from fpdf import FPDF
import io
import re

st.set_page_config(page_title="Receitas Sustentáveis", layout="wide", initial_sidebar_state="expanded")

custom_css = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Lobster&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

<style>
    body {
        background-color: #FDF5E6;
        font-family: 'Lato', sans-serif;
        color: #4A3B31;
    }

    .container-custom {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
    }

    .header-custom {
        text-align: center;
        padding: 3rem 1.5rem;
        background-color: #6A8A2D;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .header-custom h1 {
        font-family: 'Lobster', cursive;
        color: #FFFFFF;
        font-size: 3.2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.25);
    }

    .header-custom p {
        color: #F0F0F0;
        font-size: 1.25rem;
        margin-top: 0.5rem;
    }

    .card-answer {
        background-color: #FFFBF2;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #EAE0D1;
        margin-top: 1.5rem;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #5C4B42;
        box-shadow: 0 3px 8px rgba(0,0,0,0.07);
    }

    .card-answer h4 {
        font-family: 'Lato', sans-serif;
        font-weight: 700;
        color: #3B2F28;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        border-bottom: 2px solid #6A8A2D;
        padding-bottom: 0.5rem;
    }

    .card-answer h5 {
        font-family: 'Lobster', cursive;
        color: #D16002;
        margin-bottom: 1rem;
        font-size: 1.7rem;
    }
    
    .card-answer p strong {
        color: #4A3B31;
        font-weight: 700;
    }

    .stApp [data-testid="stSidebar"] {
        background-color: #F4EEE5;
        padding: 25px;
        border-right: 1px solid #E0D8CC;
    }
    
    .stApp [data-testid="stSidebar"] button[kind="toolbar"] { 
        color: #4A3B31 !important; 
    }
    .stApp [data-testid="stSidebar"] button[kind="toolbar"] svg {
        fill: #4A3B31 !important; 
    }
    button[title="Open sidebar"] svg { 
        fill: #4A3B31 !important;
    }
    button[title="Close sidebar"] svg { 
        fill: #4A3B31 !important;
    }

    .stApp [data-testid="stSidebar"] .stTextInput label,
    .stApp [data-testid="stSidebar"] .stTextArea label {
        color: #4A3B31 !important;
        font-weight: 700;
        margin-bottom: 8px;
        font-size: 1.05rem;
    }

    .stApp [data-testid="stSidebar"] h2,
    .stApp [data-testid="stSidebar"] h3,
    .stApp [data-testid="stSidebar"] h4,
    .stApp [data-testid="stSidebar"] header {
         color: #6A8A2D;
         font-family: 'Lobster', cursive;
    }

    .stApp [data-testid="stSidebar"] header {
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .stTextInput input[type="text"], .stTextArea textarea {
        border: 1px solid #D3C1B3;
        border-radius: 8px;
        padding: 12px;
        background-color: #fff;
        color: #4A3B31;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
    }
    .stTextInput input[type="text"]:focus, .stTextArea textarea:focus {
        border-color: #6A8A2D;
        box-shadow: 0 0 0 0.2rem rgba(106, 138, 45, 0.25);
    }
    
    .centered-content {
        text-align: center;
        padding: 30px 15px;
    }
    .centered-content img {
        max-width: 350px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.12);
    }
    .centered-content h2 {
        font-family: 'Lobster', cursive;
        color: #4A3B31;
        margin-bottom: 15px;
        font-size: 2rem;
    }
    .text-muted-custom {
        font-size: 1.15rem;
        color: #7A6A5D;
        line-height: 1.6;
    }

    .fa-utensils, .fa-seedling, .fa-receipt, .fa-search, .fa-book-open {
        margin-right: 12px;
        color: inherit;
    }
    
    .header-custom h1 .fa-utensils {
        color: #FFD700;
        font-size: 2.8rem;
    }

    .card-answer h4 .fa-book-open {
        color: #6A8A2D;
    }
    
    .card-answer h5 .fa-receipt {
        color: #D16002;
    }
    
    .stApp [data-testid="stSidebar"] header .fa-search {
        color: #6A8A2D;
    }
    
    .stDownloadButton button {
        background-color: #558B2F;
        color: white !important;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-family: 'Lato', sans-serif;
        width: 100%;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        transition: background-color 0.2s ease;
    }
    .stDownloadButton button:hover {
        background-color: #416B23;
    }
    .stDownloadButton button i {
        margin-right: 8px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

class RecipePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_fill_color(106, 138, 45)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, 'Receitas Sustentáveis', 0, 1, 'C', True)
        self.set_text_color(0, 0, 0)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title_text):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(209, 96, 2)
        try:
            safe_title = title_text.encode('latin-1', 'replace').decode('latin-1')
        except Exception:
            safe_title = "Receita"
        self.multi_cell(0, 10, safe_title, 0, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(6)

    def chapter_body(self, body_text_original):
        self.set_font('Arial', '', 12)
        processed_text = body_text_original.replace('<br>', '\n')
        processed_text = re.sub(r'<strong>(.*?)</strong>', r'\1', processed_text)
        processed_text = re.sub(r'<[^>]+>', '', processed_text)
        try:
            decoded_text = processed_text.encode('latin-1', 'replace').decode('latin-1')
        except UnicodeEncodeError:
            decoded_text = processed_text.encode('utf-8', 'replace').decode('utf-8', 'replace')
        self.multi_cell(0, 8, decoded_text)
        self.ln()

def generate_recipe_pdf_bytes(title, content_original):
    pdf = RecipePDF()
    pdf.add_page()
    pdf.chapter_title(title)
    pdf.chapter_body(content_original)
    pdf_bytearray = pdf.output(dest='B') 
    return bytes(pdf_bytearray)

if 'current_recipe_title' not in st.session_state:
    st.session_state.current_recipe_title = ""
if 'current_recipe_content_original' not in st.session_state:
    st.session_state.current_recipe_content_original = ""
if 'current_recipe_content_html' not in st.session_state:
    st.session_state.current_recipe_content_html = ""
if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None

st.markdown("""
<div class="container header-custom">
    <h1><i class="fas fa-utensils"></i>Receitas Sustentáveis</h1>
    <p class="lead">Descubra receitas criativas e amigas do ambiente!</p>
</div>
""", unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("CHATPDF_API_KEY")
source_id = os.getenv("CHATPDF_SOURCE_ID")

st.sidebar.markdown(f"""<header><i class="fas fa-search"></i>Consultar Receita</header>""", unsafe_allow_html=True)
pergunta = st.sidebar.text_input("Quais ingredientes você tem ou qual receita busca?", placeholder="Ex: bolo de banana com aveia")

if pergunta:
    if not api_key or not source_id:
        st.error("❌ Chave da API ou Source ID não configurados. Verifique as variáveis de ambiente.")
        st.session_state.pdf_bytes = None 
    else:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "sourceId": source_id,
            "messages": [{"role": "user", "content": f"Me forneça a receita para: {pergunta}. Se possível, separe claramente Ingredientes, Modo de Preparo, Tempo de Preparo e Porções."}]
        }

        with st.spinner("Buscando uma receita deliciosa para você... 🍳"):
            response = requests.post("https://api.chatpdf.com/v1/chats/message", headers=headers, json=payload)

        if response.status_code == 200:
            resposta_content_original = response.json().get("content", "Desculpe, não consegui gerar uma resposta no momento.")
            
            temp_title = pergunta.split(',')[0].split(' com ')[0].strip().capitalize()
            if not temp_title or temp_title == pergunta.strip().capitalize():
                 st.session_state.current_recipe_title = f"Receita de {pergunta.strip().capitalize()}"
            else:
                st.session_state.current_recipe_title = f"Receita para: {temp_title}"
            
            st.session_state.current_recipe_content_original = resposta_content_original
            
            formatted_resposta_html = resposta_content_original.replace('\n', '<br>')
            keywords_to_bold = ['Ingredientes:', 'Modo de Preparo:', 'Preparo:', 'Rendimento:', 'Porções:', 'Tempo de Preparo:', 'Dicas:']
            for keyword in keywords_to_bold:
                formatted_resposta_html = formatted_resposta_html.replace(keyword, f'<strong>{keyword}</strong>')
            st.session_state.current_recipe_content_html = formatted_resposta_html
            
            try:
                st.session_state.pdf_bytes = generate_recipe_pdf_bytes(
                    st.session_state.current_recipe_title,
                    st.session_state.current_recipe_content_original 
                )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
                st.session_state.pdf_bytes = None
        else:
            st.error(f"😕 Erro ao consultar a API do ChatPDF (Status: {response.status_code}). Tente novamente mais tarde.")
            st.session_state.current_recipe_title = ""
            st.session_state.current_recipe_content_original = ""
            st.session_state.current_recipe_content_html = ""
            st.session_state.pdf_bytes = None
else:
    if not st.session_state.get('pergunta_anterior_valida', False):
        st.session_state.current_recipe_title = ""
        st.session_state.current_recipe_content_original = ""
        st.session_state.current_recipe_content_html = ""
        st.session_state.pdf_bytes = None

st.session_state.pergunta_anterior_valida = bool(pergunta)

if st.session_state.current_recipe_content_html:
    st.markdown(f"""
    <div class="container-custom"> 
        <div class="card-answer">
            <h4><i class="fas fa-book-open"></i>Sua Receita Personalizada</h4>
            <h5><i class="fas fa-receipt"></i>{st.session_state.current_recipe_title}</h5>
            <p>{st.session_state.current_recipe_content_html}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.pdf_bytes:
        safe_file_name = re.sub(r'[^\w\s-]', '', st.session_state.current_recipe_title.lower()).strip().replace(' ', '_')
        if not safe_file_name: safe_file_name = "receita"
        pdf_file_name = f"{safe_file_name[:50]}_receita.pdf"
        
        st.download_button(
            label="📥 Baixar Receita em PDF",
            data=st.session_state.pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf"
        )
elif not pergunta : 
    initial_image_url = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
    st.markdown(f"""
    <div class="container-custom centered-content">
        <img src="{initial_image_url}" alt="Ingredientes frescos e coloridos">
        <h2><i class="fas fa-seedling" style="color: #6A8A2D;"></i>Bem-vindo(a) ao Receitas Sustentáveis!</h2>
        <p class="text-muted-custom">
            Transforme sobras em delícias e descubra novos sabores! <br>
            Digite na barra lateral os ingredientes que você tem ou a receita que deseja.
            <br><em>Por exemplo: "O que fazer com abobrinha e cenoura?" ou "Receita de torta de legumes".</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---") 
st.markdown("<p style='text-align: center; color: #888; padding-bottom: 20px;'>Feito com Python e Streamlit por Eduardo Borges.</p>", unsafe_allow_html=True)
