"""
ORCA INTERIORES SAAS - Versão 5.0 Fábrica
Sistema de Orçamento com Preços Reais de Fábrica
Calibrado para R$ 9.000 base
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Importar módulos locais
from auth_manager import AuthManager
from file_analyzer import FileAnalyzer
from orcamento_engine import OrcamentoEngineFabricaFinal

# Configuração da página
st.set_page_config(
    page_title="Orca Interiores - Orçamento de Marcenaria",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para design premium
st.markdown("""
<style>
    /* Tema principal */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header premium */
    .header-container {
        background: linear-gradient(90deg, #2E8B57, #4682B4);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Cards premium */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #2E8B57;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2E8B57;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Botões premium */
    .stButton > button {
        background: linear-gradient(90deg, #2E8B57, #4682B4);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(46,139,87,0.3);
    }
    
    /* Sidebar premium */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Upload area */
    .uploadedFile {
        border: 2px dashed #2E8B57;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: rgba(46,139,87,0.05);
    }
    
    /* Alertas customizados */
    .alert-success {
        background: linear-gradient(90deg, #d4edda, #c3e6cb);
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(90deg, #d1ecf1, #bee5eb);
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Tabs premium */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2E8B57, #4682B4);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""
    
    # Inicializar gerenciadores
    auth_manager = AuthManager()
    
    # Verificar autenticação
    if 'usuario_logado' not in st.session_state:
        mostrar_tela_login(auth_manager)
    else:
        usuario = st.session_state.usuario_logado
        mostrar_aplicacao_principal(auth_manager, usuario)

def mostrar_tela_login(auth_manager):
    """Tela de login limpa e profissional"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏠 Orca Interiores</h1>
        <p class="header-subtitle">Sistema Profissional de Orçamento de Marcenaria</p>
        <p class="header-subtitle">✨ Preços Baseados em Fábrica Real ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centralizar formulário
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Acesso ao Sistema")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_btn = st.form_submit_button("🚀 Entrar", use_container_width=True)
            
            with col_btn2:
                registro_btn = st.form_submit_button("📝 Registrar", use_container_width=True)
        
        # Processar login
        if login_btn:
            if email and senha:
                usuario = auth_manager.fazer_login(email, senha)
                if usuario:
                    st.session_state.usuario_logado = usuario
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos")
            else:
                st.warning("⚠️ Preencha email e senha")
        
        # Processar registro
        if registro_btn:
            if email and senha:
                if auth_manager.criar_usuario(email, senha):
                    st.success("✅ Usuário criado com sucesso! Faça login.")
                else:
                    st.error("❌ Erro ao criar usuário")
            else:
                st.warning("⚠️ Preencha email e senha")
        
        # Informações dos planos
        st.markdown("---")
        st.markdown("### 💎 Planos Disponíveis")
        
        col_plan1, col_plan2, col_plan3 = st.columns(3)
        
        with col_plan1:
            st.markdown("""
            **🥉 Básico**
            - 10 orçamentos/mês
            - Análise básica
            - R$ 49/mês
            """)
        
        with col_plan2:
            st.markdown("""
            **🥈 Profissional**
            - 50 orçamentos/mês
            - IA avançada
            - R$ 149/mês
            """)
        
        with col_plan3:
            st.markdown("""
            **🥇 Empresarial**
            - Ilimitado
            - Suporte premium
            - R$ 299/mês
            """)

def mostrar_aplicacao_principal(auth_manager, usuario):
    """Interface principal da aplicação"""
    
    # Header com informações do usuário
    st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">🏠 Orca Interiores</h1>
        <p class="header-subtitle">Bem-vindo, {usuario['email']} | Plano: {usuario['plano'].title()}</p>
        <p class="header-subtitle">🏭 Sistema Calibrado com Preços Reais de Fábrica</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar com configurações
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")
        
        # Logout
        if st.button("🚪 Sair", use_container_width=True):
            del st.session_state.usuario_logado
            st.rerun()
        
        st.markdown("---")
        
        # Configurações de orçamento
        st.markdown("### 🔧 Configurações do Orçamento")
        
        material = st.selectbox(
            "📦 Material",
            ["mdf_18mm", "mdf_15mm", "compensado_18mm", "compensado_15mm", "melamina_18mm", "melamina_15mm"],
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        complexidade = st.selectbox(
            "⚙️ Complexidade",
            ["simples", "media", "complexa", "premium"],
            index=1,
            format_func=lambda x: x.title()
        )
        
        qualidade_acessorios = st.selectbox(
            "🔩 Qualidade dos Acessórios",
            ["comum", "premium"],
            format_func=lambda x: x.title()
        )
        
        margem_lucro = st.slider(
            "💰 Margem de Lucro (%)",
            min_value=0,
            max_value=100,
            value=30,
            step=5,
            help="Sua margem sobre o preço de fábrica"
        )
        
        st.markdown("---")
        
        # Informações do sistema
        st.markdown("### 📊 Sistema de Preços")
        st.info("""
        🏭 **Base:** Preços reais de fábrica
        
        📈 **Sua margem:** Controlável
        
        🎯 **Resultado:** Máxima competitividade
        """)
    
    # Área principal
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload", "📊 Resultados", "📈 Gráficos", "📄 Relatório"])
    
    with tab1:
        mostrar_area_upload()
    
    with tab2:
        if 'analise' in st.session_state and 'orcamento' in st.session_state:
            mostrar_resultados(st.session_state.analise, st.session_state.orcamento, material, complexidade, qualidade_acessorios, margem_lucro)
        else:
            st.info("📤 Faça upload de um arquivo 3D para ver os resultados")
    
    with tab3:
        if 'orcamento' in st.session_state:
            mostrar_graficos(st.session_state.orcamento)
        else:
            st.info("📊 Faça upload de um arquivo 3D para ver os gráficos")
    
    with tab4:
        if 'orcamento' in st.session_state:
            mostrar_relatorio(st.session_state.orcamento)
        else:
            st.info("📄 Faça upload de um arquivo 3D para gerar o relatório")

def mostrar_area_upload():
    """Área de upload de arquivos"""
    
    st.markdown("### 📤 Upload de Arquivo 3D")
    
    # Instruções
    st.markdown("""
    <div class="alert-info">
        <strong>📋 Instruções:</strong><br>
        • Formatos aceitos: OBJ, DAE, STL, PLY<br>
        • Tamanho máximo: 500MB<br>
        • <strong>IMPORTANTE:</strong> Use apenas móveis de marcenaria (sem paredes, pisos, eletrodomésticos)<br>
        • Nomeie os objetos corretamente no SketchUp para melhor precisão da IA
    </div>
    """, unsafe_allow_html=True)
    
    # Upload
    arquivo_upload = st.file_uploader(
        "Selecione seu arquivo 3D",
        type=['obj', 'dae', 'stl', 'ply'],
        help="Arraste e solte ou clique para selecionar"
    )
    
    if arquivo_upload is not None:
        # Mostrar informações do arquivo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">📁</p>
                <p class="metric-label">Nome: {arquivo_upload.name}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            tamanho_mb = arquivo_upload.size / (1024 * 1024)
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{tamanho_mb:.1f}MB</p>
                <p class="metric-label">Tamanho</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            tipo = arquivo_upload.name.split('.')[-1].upper()
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{tipo}</p>
                <p class="metric-label">Formato</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Botão de análise
        if st.button("🔍 Analisar Arquivo", use_container_width=True):
            with st.spinner("🤖 Analisando arquivo com IA..."):
                try:
                    # Salvar arquivo temporariamente
                    with open(f"temp_{arquivo_upload.name}", "wb") as f:
                        f.write(arquivo_upload.getbuffer())
                    
                    # Analisar arquivo
                    analyzer = FileAnalyzer()
                    analise = analyzer.analisar_arquivo_3d(f"temp_{arquivo_upload.name}")
                    
                    if analise:
                        st.session_state.analise = analise
                        
                        # Calcular orçamento
                        engine = OrcamentoEngineFabricaFinal()
                        configuracoes = {
                            'material': st.session_state.get('material', 'mdf_18mm'),
                            'complexidade': st.session_state.get('complexidade', 'media'),
                            'qualidade_acessorios': st.session_state.get('qualidade_acessorios', 'comum'),
                            'margem_lucro': st.session_state.get('margem_lucro', 30)
                        }
                        
                        orcamento = engine.calcular_orcamento_completo(analise, configuracoes)
                        
                        if orcamento:
                            st.session_state.orcamento = orcamento
                            
                            st.markdown("""
                            <div class="alert-success">
                                <strong>✅ Análise concluída com sucesso!</strong><br>
                                Vá para a aba "Resultados" para ver o orçamento detalhado.
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Erro ao calcular orçamento")
                    else:
                        st.error("❌ Erro ao analisar arquivo")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

def mostrar_resultados(analise, orcamento, material, complexidade, qualidade_acessorios, margem_lucro):
    """Mostra resultados do orçamento"""
    
    # Recalcular se configurações mudaram
    configuracoes_atuais = {
        'material': material,
        'complexidade': complexidade,
        'qualidade_acessorios': qualidade_acessorios,
        'margem_lucro': margem_lucro
    }
    
    if (not hasattr(st.session_state, 'configuracoes_anteriores') or 
        st.session_state.configuracoes_anteriores != configuracoes_atuais):
        
        engine = OrcamentoEngineFabricaFinal()
        orcamento = engine.calcular_orcamento_completo(analise, configuracoes_atuais)
        st.session_state.orcamento = orcamento
        st.session_state.configuracoes_anteriores = configuracoes_atuais
    
    if not orcamento:
        st.error("❌ Erro ao calcular orçamento")
        return
    
    resumo = orcamento['resumo']
    
    # Métricas principais
    st.markdown("### 💰 Resumo do Orçamento")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">R$ {resumo['valor_final']:,.2f}</p>
            <p class="metric-label">💰 Valor Final</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{resumo['area_total_m2']:.1f} m²</p>
            <p class="metric-label">📐 Área Total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{len(orcamento['componentes'])}</p>
            <p class="metric-label">📦 Componentes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{resumo['margem_lucro_pct']:.0f}%</p>
            <p class="metric-label">📈 Margem</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Breakdown de custos
    st.markdown("### 🔍 Breakdown de Custos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏭 Base de Fábrica")
        st.markdown(f"**Material:** R$ {resumo['custo_material']:,.2f}")
        st.markdown(f"**Painéis Extras:** R$ {resumo['custo_paineis_extras']:,.2f}")
        st.markdown(f"**Montagem:** R$ {resumo['custo_montagem']:,.2f} (Não inclusa)")
        st.markdown(f"**Subtotal Fábrica:** R$ {resumo['custo_base_fabrica']:,.2f}")
    
    with col2:
        st.markdown("#### 💰 Sua Margem")
        st.markdown(f"**Margem ({resumo['margem_lucro_pct']:.0f}%):** R$ {resumo['valor_lucro']:,.2f}")
        st.markdown(f"**TOTAL FINAL:** R$ {resumo['valor_final']:,.2f}")
        
        # Comparação com mercado
        if 'valor_mercado_estimado' in resumo:
            economia = resumo.get('economia_cliente', 0)
            st.markdown(f"**Preço Mercado:** R$ {resumo['valor_mercado_estimado']:,.2f}")
            st.markdown(f"**Economia Cliente:** R$ {economia:,.2f}")
    
    # Componentes detalhados
    st.markdown("### 📦 Componentes Detalhados")
    
    componentes_df = []
    for comp in orcamento['componentes']:
        componentes_df.append({
            'Nome': comp['nome'],
            'Tipo': comp['tipo'].title(),
            'Área (m²)': f"{comp['area_m2']:.2f}",
            'Preço/m²': f"R$ {comp['preco_por_m2']:,.2f}",
            'Custo Total': f"R$ {comp['custo_total']:,.2f}",
            'IA Confiança': f"{comp.get('ia_confianca', 0):.1%}" if comp.get('ia_confianca') else "N/A"
        })
    
    if componentes_df:
        df = pd.DataFrame(componentes_df)
        st.dataframe(df, use_container_width=True)

def mostrar_graficos(orcamento):
    """Mostra gráficos do orçamento"""
    
    st.markdown("### 📊 Análise Visual")
    
    engine = OrcamentoEngineFabricaFinal()
    graficos = engine.gerar_graficos(orcamento)
    
    if graficos:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'distribuicao' in graficos:
                st.plotly_chart(graficos['distribuicao'], use_container_width=True)
        
        with col2:
            if 'comparacao' in graficos:
                st.plotly_chart(graficos['comparacao'], use_container_width=True)
        
        if 'componentes' in graficos:
            st.plotly_chart(graficos['componentes'], use_container_width=True)

def mostrar_relatorio(orcamento):
    """Mostra relatório detalhado"""
    
    st.markdown("### 📄 Relatório Detalhado")
    
    engine = OrcamentoEngineFabricaFinal()
    relatorio = engine.gerar_relatorio_detalhado(orcamento)
    
    # Mostrar relatório
    st.text_area("Relatório Completo", relatorio, height=400)
    
    # Botão de download
    st.download_button(
        label="📥 Baixar Relatório",
        data=relatorio,
        file_name=f"orcamento_orca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )
    
    # Exportar JSON
    json_data = json.dumps(orcamento, indent=2, ensure_ascii=False, default=str)
    st.download_button(
        label="📥 Baixar JSON",
        data=json_data,
        file_name=f"orcamento_orca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main()

