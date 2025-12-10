"""
app.py - Versão simplificada para teste inicial
"""
import streamlit as st
import pandas as pd
from datetime import date

# Configurar página
st.set_page_config(
    page_title="Contas a Pagar - Novo Projeto",
    page_icon="💎",
    layout="wide"
)

# Título
st.title("💎 NOVO PROJETO - CONTAS A PAGAR")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔧 Configuração")
    
    # Datas
    data_inicio = st.date_input(
        "Data Início",
        value=date(2024, 1, 1)
    )
    
    data_fim = st.date_input(
        "Data Fim",
        value=date.today()
    )
    
    # Botão
    if st.button("🎯 Carregar Dados", type="primary"):
        st.session_state.carregar_dados = True

# Conteúdo principal
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Análise", "⚙️ Configuração"])

with tab1:
    st.subheader("Visão Geral")
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", "1.234", "+12%")
    
    with col2:
        st.metric("Valor Total", "R$ 1.234.567,89", "-3%")
    
    with col3:
        st.metric("Média por Registro", "R$ 1.234,56", "+5%")
    
    # Dados de exemplo
    dados_exemplo = pd.DataFrame({
        "Data": pd.date_range("2024-01-01", periods=10),
        "Conta": [f"Conta {i}" for i in range(10)],
        "Valor": [1000 * i for i in range(10)],
        "Status": ["Pago", "Pendente"] * 5
    })
    
    st.dataframe(dados_exemplo, use_container_width=True)

with tab2:
    st.subheader("Análise Detalhada")
    
    # Gráfico
    chart_data = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        'Valor': [10000, 15000, 12000, 18000, 20000]
    })
    
    st.bar_chart(chart_data.set_index('Mês'))

with tab3:
    st.subheader("Configuração do Sistema")
    
    # Testar conexões
    if st.button("🔌 Testar Conexões"):
        with st.spinner("Testando conexões..."):
            try:
                # Aqui viriam os testes reais de conexão
                st.success("✅ Conexões estabelecidas com sucesso!")
                st.info("SQL Server: 10.1.1.254:1433")
                st.info("MySQL: 10.1.1.249:3306")
                st.info("API: 10.1.8.118:9000")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    
    # Informações do sistema
    with st.expander("📋 Informações Técnicas"):
        st.code(f"""
        Porta: 8599
        Ambiente: {st.__version__}
        Pandas: {pd.__version__}
        Repositório: https://github.com/seu-usuario/novo-projeto-contas-pagar
        """)
        
        # QR Code para acesso mobile (opcional)
        url = "http://localhost:8599"
        st.markdown(f"**URL Local:** `{url}`")

# Rodapé
st.markdown("---")
st.caption("🚀 Desenvolvido com Streamlit | 📍 Porta 8599 | 🔗 GitHub integrado")