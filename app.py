import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Avaliação APS", layout="wide")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🩺 Avaliação de Conhecimentos: Atenção Primária")
st.markdown("---")

tab_quiz, tab_dash = st.tabs(["📝 Responder Questionário", "📊 Painel de Resultados"])

# -------------------------------
# ABA 1: QUESTIONÁRIO
# -------------------------------
with tab_quiz:
    st.info("Responda às questões abaixo. Suas respostas são anônimas e ajudam a compor as estatísticas da turma.")
    
    with st.form(key="form_aps", clear_on_submit=True):
        
        st.markdown("### 1. Evolução Histórica")
        st.write("Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno referente à organização de “serviços médicos e anexos”.")
        q1 = st.text_input("A qual relatório se refere o texto?")

        st.divider()

        st.markdown("### 2. Marcos Internacionais")
        st.write("Em 1978, uma conferência internacional organizada pela OMS e UNICEF estabeleceu a APS como estratégia central.")
        q2 = st.text_input("A qual documento o texto se refere?")

        st.divider()

        st.markdown("### Atributos da APS (PCATool)")
        st.caption("Identifique o atributo essencial da APS:")

        q4 = st.text_input("4. Mesmo profissional atende você sempre?")
        q5 = st.text_input("5. Profissional sabe do especialista?")
        q6 = st.text_input("6. Serviço abre à noite?")
        q7 = st.text_input("7. Faz pequenos procedimentos?")

        st.divider()

        st.markdown("### 8. Equipes de Saúde")
        q8 = st.text_input("Qual profissional diferencia eAB de ESF?")

        enviar = st.form_submit_button("Enviar Respostas")

    if enviar:
        def validar(entrada, gabarito):
            if not entrada:
                return 0
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
            # 🔹 tenta ler dados existentes
            try:
                dados_atuais = conn.read(worksheet="Sheet1")
                if dados_atuais is None or dados_atuais.empty:
                    dados_atuais = pd.DataFrame(columns=nova_linha.columns)
            except Exception:
                dados_atuais = pd.DataFrame(columns=nova_linha.columns)

            # 🔹 garante mesmas colunas
            for col in nova_linha.columns:
                if col not in dados_atuais.columns:
                    dados_atuais[col] = 0

            df_final = pd.concat([dados_atuais, nova_linha], ignore_index=True)

            # 🔹 grava na planilha
            conn.update(
                worksheet="Sheet1",
                data=df_final
            )

            st.success("Respostas salvas com sucesso!")
            st.balloons()

        except Exception as e:
            st.error(f"Erro ao salvar na planilha: {e}")

# -------------------------------
# ABA 2: DASHBOARD
# -------------------------------
with tab_dash:
    st.subheader("📊 Resultados Consolidados")

    try:
        df_historico = conn.read(worksheet="Sheet1")

        if df_historico is not None and not df_historico.empty:
            st.metric("Total de Respondentes", len(df_historico))

            acertos = df_historico.sum(numeric_only=True).reset_index()
            acertos.columns = ['Questão/Tema', 'Total de Acertos']

            st.bar_chart(acertos, x='Questão/Tema', y='Total de Acertos')

            st.write("### Dados Brutos")
            st.dataframe(df_historico)

        else:
            st.info("Aguardando respostas...")

    except Exception as e:
        st.warning(f"Erro ao carregar dados: {e}")
