# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo da app (Interface Streamlit)

# Imports
import os
import streamlit as st

# Variável de ambiente
# Evita um comportamento indesejado do Hugging Face Tokenizers quando usado dentro de aplicações que executam várias threads em paralelo,
# como Streamlit, FastAPI ou Jupyter.
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Garante que caminhos relativos (ex: 'dados/produtos.json' e 'img/...') sejam resolvidos a partir da pasta do projeto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importa a classe responsável pela geração de embeddings
from src.embeddings import EmbeddingModel

# Importa a classe responsável pelo banco de dados vetorial
from src.vector_db import VectorDB

# Importa a classe responsável pela interação com o modelo de linguagem
from src.llm_service import LLMService

# Configuração Inicial da Aplicação Streamlit
st.set_page_config(
    page_title="Engenharia de Dados para IA - Data Science Academy",  # Título que aparece na aba do navegador
    page_icon="🤖",                      # Ícone (emoji) que aparece na aba do navegador
    layout="wide",                      # Define o layout da página para usar a largura total da tela
    initial_sidebar_state="expanded",   # Garante que a sidebar (menu lateral) comece aberta
)

# Estilização customizada (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Reduz o espaço vazio no topo da página */
    .block-container {
        padding-top: 2rem;
    }

    /* Fundo em degradê para o app inteiro */
    .stApp {
        background: linear-gradient(160deg, #0F172A 0%, #14224a 45%, #0B1220 100%);
    }

    /* Bolhas de chat mais suaves */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        border: 1px solid #1E293B;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
        padding: 0.5rem 0.25rem;
    }

    /* Esconde a barra de rolagem da sidebar (a rolagem continua funcionando em telas menores) */
    section[data-testid="stSidebar"] * {
        scrollbar-width: none;
    }
    section[data-testid="stSidebar"] *::-webkit-scrollbar {
        display: none;
    }

    /* Imagem do produto com cantos arredondados */
    div[data-testid="stExpander"] img {
        border-radius: 10px;
    }

    /* Botões (normal e link): gradiente azul + sombra + brilho espelhado no topo */
    .stButton > button,
    .stLinkButton > a {
        position: relative;
        overflow: hidden;
        border-radius: 999px;
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.3rem;
        background: linear-gradient(180deg, #2C5282 0%, #1A365D 100%);
        box-shadow:
            0 4px 14px rgba(59, 130, 246, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
        transition: all 0.2s ease;
    }

    /* Faixa de "reflexo" na metade superior do botão (efeito espelhado) */
    .stButton > button::before,
    .stLinkButton > a::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 50%;
        background: linear-gradient(180deg, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }

    .stButton > button:hover,
    .stLinkButton > a:hover {
        color: white;
        background: linear-gradient(180deg, #2B6CB0 0%, #2C5282 100%);
        box-shadow:
            0 6px 20px rgba(59, 130, 246, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    .stButton > button:active,
    .stLinkButton > a:active {
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)


# Carrega os recursos pesados uma única vez (modelo de embeddings, banco vetorial e serviço de LLM)
@st.cache_resource(show_spinner="Carregando modelo de embeddings e conectando ao Qdrant...")
def load_resources():
    return EmbeddingModel(), VectorDB(), LLMService()

embed_model, db, llm_service = load_resources()


# Verifica se a coleção existe e quantos produtos estão indexados
def dsa_total_indexado():
    if not db.client.collection_exists(db.collection_name):
        return 0
    return db.client.count(db.collection_name).count


# Exibe os produtos recuperados: imagem à esquerda e informações + link à direita
def dsa_exibe_produtos(produtos):
    for prod in produtos:
        with st.expander(f"{prod['name']} - R$ {prod['price']}"):

            col_img, col_info = st.columns([1, 2])

            # Imagem do produto (somente se o campo existir no payload e o arquivo estiver na pasta img)
            with col_img:
                imagem = prod.get('image')
                if imagem and os.path.isfile(imagem):
                    st.image(imagem, width="stretch")
                else:
                    st.caption("🖼️ Imagem indisponível")

            # Informações do produto e link para a loja
            with col_info:
                st.markdown(f"**Marca:** {prod['brand']}")
                st.markdown(f"**Categoria:** {prod.get('category', 'N/A')}")
                st.markdown(f"**Descrição:** {prod['description']}")
                if prod.get('link'):
                    st.link_button("🛒 Ver produto na loja", prod['link'])


# Exibe o resultado em duas colunas: recomendação da IA à esquerda e produtos recuperados à direita
def dsa_exibe_resultado(recomendacao, produtos):
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("💡 Recomendação da IA")
        st.markdown(recomendacao)

    with col2:
        st.subheader("📦 Produtos Recuperados (Contexto)")
        dsa_exibe_produtos(produtos)


# Títulos
st.markdown("""
<div style="text-align:center; padding: 0.5rem 0 1.5rem 0;">
    <h1 style="margin-bottom:0;">🤖 Consultor de Compras Inteligente</h1>
    <p style="color:#94A3B8; font-size:0.95rem; margin-top:0.3rem;">
        Sistema de Recomendação · Engenharia de Dados para IA · Data Science Academy
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Sobre este sistema", expanded=True):
    st.markdown("""
    Este sistema utiliza **Busca Semântica + Filtros de Metadados (Hybrid Search)** para recomendar
    produtos eletrônicos com base na sua necessidade.
    - Modelo de Embeddings: `all-MiniLM-L6-v2` (Hugging Face)
    - Modelo de LLM: `openai/gpt-oss-120b` (Groq)
    - Banco Vetorial com filtros de payload (categoria, marca e preço): `Qdrant`
    - Fonte de Dados: `JSON` (dados/produtos.json)
    """)

with st.expander("💡 Sugestões de Solicitação", expanded=False):
    st.markdown("""
    - Preciso de um notebook bom para trabalhar em viagens
    - Quero um console para jogar com meus amigos
    - Qual fone é melhor para usar no avião?
    - Procuro uma caixa de som para levar à praia

    **Teste os filtros:** selecione a categoria `Áudio` e pergunte por um notebook.
    """)


# --- Sidebar: Filtros de Metadados ---
with st.sidebar:

    st.header("🔎 Filtros")

    # Define as categorias disponíveis para filtragem
    categorias = ["Todas", "Games", "Notebooks", "Áudio"]

    # Define as marcas disponíveis para filtragem
    marcas = ["Todas", "Sony", "Microsoft", "Apple", "Dell", "JBL"]

    filter_category = st.selectbox("Categoria", categorias)
    filter_brand = st.selectbox("Marca", marcas)
    price_range = st.slider("Faixa de Preço (R$)", 0, 10000, (0, 10000))

    st.markdown("---")

    st.info(
        "Aviso: IA pode gerar respostas imprecisas, incompletas ou erradas. "
        "Sempre verifique informações críticas antes de confiar totalmente no resultado."
    )

    st.markdown(
        """
        <div style="background-color:#1A365D; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
            <h3 style="color:white; margin:0; font-weight:bold;">Dúvidas?</h3>
            <p style="color:white; margin:0; font-weight:bold; font-size:0.7rem; white-space:nowrap;">aline.abm97@gmail.com</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Área Principal: Chat ---

# Inicializa histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores (incluindo os produtos recuperados em cada resposta)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("products"):
            dsa_exibe_resultado(message["content"], message["products"])
        else:
            st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("O que você está procurando hoje? (ex: notebook para viagens, console, fone...)"):

    # 1. Adiciona pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gera resposta usando Busca Semântica + Filtros + LLM
    context_products = []

    with st.chat_message("assistant"):

        if dsa_total_indexado() == 0:
            answer = "⚠️ O catálogo ainda não foi indexado. Execute `python dsa_ingestao.py` antes de usar a app."
            st.markdown(answer)

        else:
            with st.spinner("Processando vetores e aplicando filtros..."):

                # Etapa A: Converte a consulta em embedding e busca no Qdrant com filtros de metadados
                query_vector = embed_model.get_embedding(prompt)
                search_results = db.search(query_vector = query_vector,
                                           category = filter_category,
                                           brand = filter_brand,
                                           price_min = price_range[0],
                                           price_max = price_range[1],
                                           limit = 3)

            if not search_results:
                answer = "❌ Nenhum produto encontrado com esses filtros e termos."
                st.markdown(answer)

            else:
                # Extrai os payloads dos resultados retornados
                context_products = [hit.payload for hit in search_results]

                with st.spinner("IA gerando recomendação..."):

                    # Etapa B: Geração da recomendação (RAG)
                    answer = llm_service.generate_recommendation(prompt, context_products)

                # Exibe a recomendação da IA e os produtos recuperados em duas colunas
                dsa_exibe_resultado(answer, context_products)

    # 3. Adiciona resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": answer, "products": context_products})


# Fim
