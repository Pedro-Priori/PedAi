import streamlit as st
import pandas as pd
import sqlite3
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard PedAI | FICR",
    page_icon="📊",
    layout="wide"
)

# --- ESTILO PERSONALIZADO (Identidade FICR) ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #003366; /* Azul FICR */
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #FFCC00; /* Dourado FICR */
        padding: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE CARREGAMENTO DE DADOS ---
def carregar_dados():
    # Caminho do banco de dados (assume que está na mesma pasta)
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        return None

    conn = sqlite3.connect(db_path)
    
    # Query SQL para cruzar Pedidos -> Itens -> Produtos -> Vendedores
    # Isso permite saber qual bairro vendeu mais!
    query = """
    SELECT 
        p.id AS pedido_id,
        p.data_criacao,
        p.total,
        p.status,
        prod.nome AS produto,
        vendedor.username AS vendedor,
        vendedor.local AS bairro
    FROM pedidos_pedido p
    JOIN pedidos_itempedido i ON p.id = i.pedido_id
    JOIN loja_produto prod ON i.produto_id = prod.id
    JOIN utilizadores_usuario vendedor ON prod.vendedor_id = vendedor.id
    WHERE p.status != 'cancelado'
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Converte data para formato datetime
    if not df.empty:
        df['data_criacao'] = pd.to_datetime(df['data_criacao'])
        
    return df

# --- INTERFACE DO DASHBOARD ---

st.markdown('<div class="main-header">📊 Dashboard Analítico PedAI</div>', unsafe_allow_html=True)
st.markdown("Visão estratégica de vendas e movimentação por bairro.")
st.markdown("---")

df = carregar_dados()

if df is None:
    st.error("❌ Erro: Não encontrei o arquivo 'db.sqlite3'. Certifique-se de rodar este script na pasta do projeto.")
elif df.empty:
    st.warning("⚠️ O banco de dados está vazio ou não há vendas concluídas. Faça alguns pedidos no site para ver os gráficos!")
else:
    # --- FILTROS LATERAIS ---
    st.sidebar.header("Filtros")
    bairros_disponiveis = df['bairro'].unique()
    bairros_selecionados = st.sidebar.multiselect("Filtrar por Bairro", bairros_disponiveis, default=bairros_disponiveis)
    
    # Aplica filtro
    df_filtrado = df[df['bairro'].isin(bairros_selecionados)]

    # --- 1. INDICADORES (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_vendas = df_filtrado['total'].sum()
    qtd_pedidos = df_filtrado['pedido_id'].nunique()
    ticket_medio = total_vendas / qtd_pedidos if qtd_pedidos > 0 else 0
    top_bairro = df_filtrado.groupby('bairro')['total'].sum().idxmax() if not df_filtrado.empty else "N/A"

    col1.metric("💰 Faturamento Total", f"R$ {total_vendas:.2f}")
    col2.metric("🧾 Pedidos Realizados", qtd_pedidos)
    col3.metric("🏷️ Ticket Médio", f"R$ {ticket_medio:.2f}")
    col4.metric("📍 Local + Forte", top_bairro)

    st.markdown("---")

    # --- 2. GRÁFICOS ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader(" Movimentação por Local (R$)")
        # Agrupa vendas por local
        vendas_bairro = df_filtrado.groupby('bairro')['total'].sum().sort_values(ascending=True)
        st.bar_chart(vendas_bairro, color="#003366") # Azul FICR

    with col_right:
        st.subheader(" Top Vendedores")
        vendas_vendedor = df_filtrado.groupby('vendedor')['total'].sum().sort_values(ascending=True)
        st.bar_chart(vendas_vendedor, color="#FFCC00") # Dourado FICR

    # --- 3. DADOS BRUTOS ---
    with st.expander("🔎 Ver Tabela Detalhada de Vendas"):
        st.dataframe(df_filtrado)
        
    st.caption("Dados atualizados em tempo real do banco de dados Django.")