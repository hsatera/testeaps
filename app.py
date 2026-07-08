import streamlit as st

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Quiz APS",
    layout="wide"
)

def validar(entrada, termos):
    if not entrada:
        return "❌"

    entrada = entrada.lower().strip()

    for termo in termos:
        if termo.lower() in entrada:
            return "✅"

    return "❌"


# =====================================================
# INTERFACE
# =====================================================

st.title("🩺 PRÉ-TESTE - OFICINA APS - MD436")

with st.form("quiz"):

    st.markdown("## 1. Evolução Histórica")
    st.write(
        "Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno..."
    )
    q1 = st.text_input("A qual relatório se refere o texto?")

    st.divider()

    st.markdown("## 2. Marcos Internacionais")
    st.write(
        "Em 1978, representantes de diversos países reuniram-se em uma conferência..."
    )
    q2 = st.text_input("A qual documento o texto se refere?")

    st.divider()

    st.markdown("## 3. Atributos Essenciais da APS")
    st.caption("Correlacione cada pergunta com apenas um atributo essencial da APS.")

    q3 = st.text_input(
        "Quando você vai ao serviço de saúde, é o mesmo médico ou enfermeiro que o atende?"
    )

    q4 = st.text_input(
        "O médico ou enfermeiro sabe quais foram os resultados da consulta com outros especialistas?"
    )

    q5 = st.text_input(
        "O serviço de saúde fica aberto pelo menos algumas noites ou finais de semana?"
    )

    q6 = st.text_input(
        "O serviço de saúde oferece procedimentos como remoção de verrugas, suturas e pequenos procedimentos?"
    )

    st.divider()

    st.markdown("## 4. Equipes de Saúde")

    q7 = st.text_input(
        "Qual profissional diferencia uma equipe de Atenção Básica tradicional de uma ESF?"
    )

    enviar = st.form_submit_button("Enviar")


# =====================================================
# CORREÇÃO
# =====================================================

if enviar:

    resultados = [
        validar(q1, [
            "dawson",
            "relatório dawson",
            "relatorio dawson"
        ]),

        validar(q2, [
            "alma",
            "alma ata",
            "alma-ata"
        ]),

        validar(q3, [
            "longitudinalidade"
        ]),

        validar(q4, [
            "coordenação",
            "coordenacao",
            "coordenação do cuidado",
            "coordenacao do cuidado",
            "coordenação clínica",
            "coordenacao clinica"
        ]),

        validar(q5, [
            "acesso",
            "acesso de primeiro contato",
            "primeiro contato",
            "primeiro acesso",
            "porta de entrada",
            "contato inicial"
        ]),

        validar(q6, [
            "integralidade"
        ]),

        validar(q7, [
            "acs",
            "agente comunitário",
            "agente comunitario",
            "agente"
        ])
    ]

    nota = resultados.count("✅")

    st.success(f"Você acertou **{nota}/7** questões.")

    st.markdown("## Resultado")

    for i, resultado in enumerate(resultados, start=1):
        st.write(f"**Questão {i}:** {resultado}")

    if nota == 7:
        st.balloons()
