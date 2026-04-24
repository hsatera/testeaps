import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Avaliação APS", layout="wide")

# Estabelece conexão com o Google Sheets usando as Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🩺 Avaliação de Conhecimentos: Atenção Primária")
st.markdown("---")

tab_quiz, tab_dash = st.tabs(["📝 Responder Questionário", "📊 Painel de Resultados"])

# --- ABA 1: O QUESTIONÁRIO ---
with tab_quiz:
    st.info("Responda às questões abaixo. Suas respostas são anônimas e ajudam a compor as estatísticas da turma.")
    
    with st.form(key="form_aps", clear_on_submit=True):
        
        st.markdown("### 1. Evolução Histórica")
        st.write("Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno referente à organização de “serviços médicos e anexos”, em resposta a requisição do Ministro da Saúde. O relatório apresentava um conceito integrado de centros de saúde e serviços domiciliares. Os centros de saúde seriam primários e secundários, onde o nível primário coordenaria a assistência a partir de médicos e outros profissionais em contato direto com a comunidade.")
        q1 = st.text_input("A qual relatório se refere o texto?", key="q1")
        
        st.divider()

        st.markdown("### 2. Marcos Internacionais")
        st.write("Em 1978, representantes de diversos países reuniram-se na União Soviética, em uma conferência internacional organizada pela Organização Mundial da Saúde e pelo UNICEF. O encontro resultou em um documento que estabeleceu a Atenção Primária à Saúde como estratégia central para alcançar melhores níveis de saúde global, tendo como lema “Saúde para todos no ano 2000” e defendendo princípios como equidade, participação comunitária e ações intersetoriais.")
        q2 = st.text_input("A qual documento o texto se refere?", key="q2")

        st.divider()
        
        st.markdown("### Atributos da APS (PCATool)")
        st.caption("Identifique o atributo essencial da APS (Longitudinalidade, Coordenação, Acesso ou Integralidade):")

        q4 = st.text_input("4. Quando você vai ao serviço de saúde, é o mesmo médico ou enfermeiro que atende você todas as vezes?")
        q5 = st.text_input("5. O médico ou enfermeiro sabe quais foram os resultados da consulta com o especialista ou no serviço especializado?")
        q6 = st.text_input("6. O serviço de saúde fica aberto pelo menos algumas noites de dias úteis até às 20 horas?")
        q7 = st.text_input("7. O serviço de saúde oferece procedimentos como remoção de verrugas ou outros pequenos procedimentos cirúrgicos?")

        st.divider()

        st.markdown("### 8. Equipes de Saúde")
        q8 = st.text_input("Qual o profissional que diferencia uma equipe de AB tradicional (eAB) e de uma Equipe de Saúde da Família?")

        enviar = st.form_submit_button("Enviar Respostas")

    if enviar:
        # Lógica de validação baseada nas palavras-chave do doc
        def validar(entrada, gabarito):
            return 1 if gabarito.lower() in entrada.lower() else 0

        nova_linha = pd.DataFrame([{
            "Relatorio_Dawson": validar(q1, "Dawson"),
            "Alma_Ata": validar(q2, "Alma"),
            "Longitudinalidade": validar(q4, "Longitudinalidade"),
            "Coordenacao": validar(q5, "Coordenação") or validar(q5, "Cuidado"),
            "Acesso": validar(q6, "Acesso") or validar(q6, "Contato"),
            "Integralidade": validar(q7, "Integralidade"),
            "ACS": validar(q8, "ACS") or validar(q8, "Agente")
        }])

        try:
            # Tenta ler dados existentes para concatenar
            try:
                dados_atuais = conn.read()
            except:
                dados_atuais = pd.DataFrame()

            df_final = pd.concat([dados_atuais, nova_linha], ignore_index=True)
            conn.update(data=df_final)
            st.success("Respostas salvas com sucesso na planilha!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao salvar na planilha: {e}")

# --- ABA 2: RESULTADOS ---
with tab_dash:
    st.subheader("📊 Resultados Consolidados (Histórico)")
    try:
        df_historico = conn.read()
        if not df_historico.empty:
            st.metric("Total de Respondentes", len(df_historico))
            
            # Gráfico de barras com a soma de acertos
            acertos = df_historico.sum().reset_index()
            acertos.columns = ['Questão/Tema', 'Total de Acertos']
            st.bar_chart(data=acertos, x='Questão/Tema', y='Total de Acertos')
            
            st.write("**Dados Brutos (Anonimizados)**")
            st.dataframe(df_historico)
        else:
            st.info("Aguardando as primeiras respostas para exibir estatísticas.")
    except Exception as e:
        st.warning("Ainda não foi possível carregar os dados. Certifique-se de que a planilha possui cabeçalhos.")
