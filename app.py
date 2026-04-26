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
        st.write("Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno referente à organização de serviços médicos e anexos...")
        q1 = st.text_input("A qual relatório se refere o texto?")

        st.divider()

        st.markdown("### 2. Marcos Internacionais")
        st.write("Em 1978, representantes de diversos países reuniram-se em uma conferência internacional organizada pela OMS e UNICEF...")
        q2 = st.text_input("A qual documento o texto se refere?")

        st.divider()

        st.markdown("### Atributos da APS (PCATool)")
        q4 = st.text_input("4. Quando você vai ao serviço de saúde, é o mesmo profissional que atende você sempre?")
        q5 = st.text_input("5. O profissional sabe o que aconteceu nas consultas com especialistas?")
        q6 = st.text_input("6. O serviço funciona à noite (até 20h)?")
        q7 = st.text_input("7. Realiza pequenos procedimentos?")

        st.divider()

        st.markdown("### 8. Equipes de Saúde")
        q8 = st.text_input("Qual profissional diferencia eAB de ESF?")

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

            # 🔢 Métricas
            st.metric("Total de respostas", len(df))

            # 📊 Gráfico
            dados_chart = df.drop(columns=["id", "created_at"], errors="ignore").sum()

            st.bar_chart(dados_chart)

            # 📋 Tabela
            st.dataframe(df)

        else:
            st.info("Sem dados ainda.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
