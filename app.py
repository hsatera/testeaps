import streamlit as st
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="Quiz APS - Supabase", layout="wide")

# 🔌 Conexão direta com Supabase
url = st.secrets["connections"]["supabase"]["url"]
key = st.secrets["connections"]["supabase"]["key"]

supabase = create_client(url, key)

st.title("🩺 Avaliação de Conhecimentos: APS")

tab_quiz, tab_dash = st.tabs(["📝 Responder", "📊 Resultados"])

# =========================
# 📝 QUIZ
# =========================
with tab_quiz:
    with st.form(key="form_aps", clear_on_submit=True):

        st.markdown("### 1. Evolução Histórica")
        st.write("Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno referente à organização de “serviços médicos e anexos”, em resposta a requisição do Ministro da Saúde. O relatório apresentava um conceito integrado de centros de saúde e serviços domiciliares. Os centros de saúde seriam primários e secundários, onde o nível primário coordenaria a assistência a partir de médicos e outros profissionais em contato direto com a comunidade.")
        q1 = st.text_input("A qual relatório se refere o texto?")

        st.divider()

        st.markdown("### 2. Marcos Internacionais")
        st.write("Em 1978, representantes de diversos países reuniram-se na União Soviética, em uma conferência internacional organizada pela Organização Mundial da Saúde e pelo UNICEF. O encontro resultou em um documento que estabeleceu a Atenção Primária à Saúde como estratégia central para alcançar melhores níveis de saúde global, tendo como lema “Saúde para todos no ano 2000” e defendendo princípios como equidade, participação comunitária e ações intersetoriais.")
        q2 = st.text_input("A qual documento o texto se refere?")

        st.divider()

        # 🔹 Contexto ajustado
        st.markdown("### Atributos da APS (PCATool)")
        st.caption("O PCATool é um instrumento padronizado para avaliar a qualidade da Atenção Primária à Saúde, medindo a presença e o grau de desenvolvimento dos quatro atributos essenciais que configuram uma APS robusta (Starfield). Correlacione as perguntas abaixo com apenas 1 atributo essencial da APS:")

        q4 = st.text_input(
            "4. Quando você vai ao serviço de saúde, é o mesmo médico ou enfermeiro que atende você todas as vezes?"
        )

        q5 = st.text_input(
            "5. O médico ou enfermeiro sabe quais foram os resultados da consulta com o especialista ou no serviço especializado?"
        )

        q6 = st.text_input(
            "6. O serviço de saúde fica aberto pelo menos algumas noites de dias úteis até às 20 horas?"
        )

        q7 = st.text_input(
            "7. O serviço de saúde oferece procedimentos como remoção de verrugas ou outros pequenos procedimentos cirúrgicos?"
        )

        st.divider()

        st.markdown("### 8. Equipes de Saúde")
        q8 = st.text_input("Qual o profissional que diferencia uma equipe de AB tradicional (eAB) e de uma Equipe de Saúde da Família?")

        enviar = st.form_submit_button("Enviar Respostas")

    if enviar:

        def validar(entrada, gabarito):
            return 1 if entrada and gabarito.lower() in entrada.lower() else 0

        dados = {
            "relatorio_dawson": validar(q1, "Dawson"),
            "alma_ata": validar(q2, "Alma"),
            "longitudinalidade": validar(q4, "Longitudinalidade"),
            "coordenacao": validar(q5, "Coordenação"),
            "acesso": validar(q6, "Acesso") or validar(q6, "Contato"),
            "integralidade": validar(q7, "Integralidade"),
            "acs": validar(q8, "ACS") or validar(q8, "Agente")
        }

        try:
            supabase.table("respostas_aps").insert(dados).execute()
            st.success("✅ Enviado com sucesso!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Erro ao enviar: {e}")

# =========================
# 📊 DASHBOARD
# =========================
with tab_dash:
    st.subheader("📊 Painel de Resultados")

    try:
        res = supabase.table("respostas_aps").select("*").execute()

        if res.data:
            df = pd.DataFrame(res.data)

            st.metric("Total de respostas", len(df))

            dados_chart = df.drop(columns=["id", "created_at"], errors="ignore").sum()

            st.bar_chart(dados_chart)

            st.dataframe(df)

        else:
            st.info("Sem dados.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
