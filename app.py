import streamlit as str
from supabase import create_client, Client
import pandas as pd

# Configuração da página
st.set_page_config(page_title="📊 Painel de Resultados", layout="wide")

# -------------------------------------------------------------------------
# 1. AUTENTICAÇÃO COM SENHA
# -------------------------------------------------------------------------
def check_password():
    """Retorna True se o usuário inseriu a senha correta."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("📊 Painel de Resultados")
    st.subheader("Acesso Restrito")
    
    password = st.text_input("Digite a senha para acessar o painel:", type="password")
    if st.button("Acessar"):
        if password == "Aps123":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")
    return False

# Só renderiza o painel se a senha estiver correta
if check_password():
    
    # -------------------------------------------------------------------------
    # 2. CONEXÃO COM O SUPABASE (Tratamento do Erro de Conexão)
    # -------------------------------------------------------------------------
    @st.cache_resource
    def init_connection():
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            return create_client(url, key)
        except Exception as e:
            st.error(f"Erro ao inicializar conexão com o Supabase. Verifique os Secrets. Detalhes: {e}")
            return None

    supabase = init_connection()

    # -------------------------------------------------------------------------
    # 3. BUSCA E ORDENAÇÃO DOS DADOS
    # -------------------------------------------------------------------------
    def load_data():
        if supabase is None:
            return pd.DataFrame()
        
        try:
            # Substitua 'nome_da_sua_tabela' pelo nome real da tabela no Supabase
            # Se você já tiver uma coluna de ordem (ex: 'id_questao' ou 'numero'), adicione .order('coluna')
            response = supabase.table("nome_da_sua_tabela").select("*").execute()
            
            df = pd.DataFrame(response.data)
            return df
        except Exception as e:
            st.error(f"Erro ao carregar dados do painel: {e}")
            return pd.DataFrame()

    # Carrega os dados
    df_dados = load_data()

    if not df_dados.empty:
        # CORREÇÃO DA ORDEM DAS QUESTÕES
        # Supondo que a coluna com o nome das questões se chame 'questao' (ex: "Questão 1", "Questão 2")
        # Se a sua coluna tiver outro nome, altere 'questao' abaixo para o nome correto.
        if 'questao' in df_dados.columns:
            # Ordena de forma alfanumérica direta. 
            # Dica: se tiver mais de 10 questões, use números com zero à esquerda (Questão 01, Questão 02) para não quebrar a ordem alfabética.
            df_dados = df_dados.sort_values(by='questao').reset_index(drop=True)
        
        # -------------------------------------------------------------------------
        # 4. EXIBIÇÃO DO PAINEL
        # -------------------------------------------------------------------------
        st.title("📊 Painel de Resultados")
        st.write("Dados carregados com sucesso e ordenados por questão!")
        
        # Exemplo de exibição de dados
        st.dataframe(df_dados, use_container_width=True)
        
        # Botão opcional para deslogar
        if st.sidebar.button("Sair do Painel"):
            st.session_state["password_correct"] = False
            st.rerun()
            
    else:
        st.warning("Nenhum dado encontrado ou conexão indisponível no momento.")
