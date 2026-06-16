import streamlit as st
from supabase import create_client
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(
    page_title="Quiz APS - Supabase",
    layout="wide"
)

SENHA_DASHBOARD = "Aps123"

# =====================================================
# CONEXÃO SUPABASE
# =====================================================
@st.cache_resource
def init_supabase():
    url = st.secrets["connections"]["supabase"]["url"]
    key = st.secrets["connections"]["supabase"]["key"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error(f"Erro ao conectar ao Supabase: {e}")
    st.stop()

# =====================================================
# FUNÇÃO DE VALIDAÇÃO
# =====================================================
def validar(entrada, termos):
    if not entrada:
        return 0

    entrada = entrada.lower()

    for termo in termos:
        if termo.lower() in entrada:
            return 1

    return 0

# =====================================================
# TÍTULO
# =====================================================
st.title("🩺 PRÉ-TESTE - OFICINA APS - MD436")

tab_quiz, tab_dash = st.tabs(
    ["📝 Responder", "📊 Resultados"]
)

# =====================================================
# QUIZ
# =====================================================
with tab_quiz:

    with st.form(
        key="form_aps",
        clear_on_submit=True
    ):

        st.markdown("## 1. Evolução Histórica")

        st.write("""
        Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno
        referente à organização de serviços médicos e anexos.

        O relatório apresentava um conceito integrado de centros de saúde e serviços
        domiciliares.
        """)

        q1 = st.text_input(
            "A qual relatório se refere o texto?"
        )

        st.divider()

        st.markdown("## 2. Marcos Internacionais")

        st.write("""
        Em 1978, representantes de diversos países reuniram-se em uma conferência
        organizada pela OMS e UNICEF.

        O encontro resultou em um documento que estabeleceu a Atenção Primária à Saúde
        como estratégia central para alcançar melhores níveis de saúde global.
        """)

        q2 = st.text_input(
            "A qual documento o texto se refere?"
        )

        st.divider()

        st.markdown("## 3. Atributos Essenciais da APS")

        st.caption(
            "Correlacione cada pergunta com apenas um atributo essencial da APS."
        )

        q3 = st.text_input(
            "Quando você vai ao serviço de saúde, é o mesmo médico ou enfermeiro que atende você todas as vezes?"
        )

        q4 = st.text_input(
            "O médico ou enfermeiro sabe quais foram os resultados da consulta com o especialista ou no serviço especializado?"
        )

        q5 = st.text_input(
            "O serviço de saúde fica aberto pelo menos algumas noites de dias úteis até às 20 horas?"
        )

        q6 = st.text_input(
            "O serviço de saúde oferece procedimentos como remoção de verrugas ou outros pequenos procedimentos cirúrgicos?"
        )

        st.divider()

        st.markdown("## 4. Equipes de Saúde")

        q7 = st.text_input(
            "Qual profissional diferencia uma equipe de AB tradicional (eAB) de uma Equipe de Saúde da Família?"
        )

        enviar = st.form_submit_button(
            "Enviar Respostas"
        )

    if enviar:

        dados = {
            "relatorio_dawson": validar(
                q1,
                ["dawson"]
            ),

            "alma_ata": validar(
                q2,
                ["alma", "alma-ata", "alma ata"]
            ),

            "longitudinalidade": validar(
                q3,
                ["longitudinalidade"]
            ),

            "coordenacao": validar(
                q4,
                ["coordenação", "coordenacao"]
            ),

            "acesso_primeiro_contato": validar(
                q5,
                [
                    "acesso",
                    "primeiro contato",
                    "contato"
                ]
            ),

            "integralidade": validar(
                q6,
                ["integralidade"]
            ),

            "acs": validar(
                q7,
                [
                    "acs",
                    "agente comunitário",
                    "agentecomunitario",
                    "agente"
                ]
            )
        }

        dados["total"] = sum(dados.values())

        try:

            supabase.table(
                "respostas_aps"
            ).insert(
                dados
            ).execute()

            st.success(
                f"✅ Respostas enviadas! Nota: {dados['total']}/7"
            )

            st.balloons()

        except Exception as e:

            st.error(
                f"❌ Erro ao enviar: {e}"
            )

# =====================================================
# DASHBOARD PROTEGIDO POR SENHA
# =====================================================
with tab_dash:

    st.subheader("🔒 Área Restrita")

    senha = st.text_input(
        "Digite a senha para acessar os resultados",
        type="password"
    )

    if senha != SENHA_DASHBOARD:

        if senha != "":
            st.error("Senha incorreta.")

        st.info("Digite a senha para visualizar o painel.")
        st.stop()

    st.success("Acesso autorizado.")

    st.subheader("📊 Painel de Resultados")

    try:

        resposta = (
            supabase
            .table("respostas_aps")
            .select("*")
            .execute()
        )

        if resposta.data:

            df = pd.DataFrame(
                resposta.data
            )

            st.metric(
                "Total de respostas",
                len(df)
            )

            if "total" in df.columns:

                st.metric(
                    "Média Geral",
                    round(
                        df["total"].mean(),
                        2
                    )
                )

                st.metric(
                    "Percentual Médio",
                    f"{round(df['total'].mean()/7*100,1)}%"
                )

            questoes = [
                "relatorio_dawson",
                "alma_ata",
                "longitudinalidade",
                "coordenacao",
                "acesso_primeiro_contato",
                "integralidade",
                "acs"
            ]

            st.markdown("### Acertos por Questão")

            dados_chart = (
                df[questoes]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                dados_chart
            )

            st.markdown("### Dados Brutos")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "Nenhuma resposta cadastrada."
            )

    except Exception as e:

        st.error(
            f"Erro ao carregar dados: {e}"
        )
