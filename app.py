import streamlit as st

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Quiz APS",
    layout="wide"
)

def validar(entrada, termos):
    """Retorna ✅ se algum termo esperado estiver contido na resposta."""
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

    # =================================================
    # QUESTÃO 1
    # =================================================

    st.markdown("## 1. Evolução Histórica")

    st.write(
        "Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno que propôs a organização regionalizada dos serviços de saúde e influenciou diversos sistemas de saúde ao redor do mundo."
    )

    q1 = st.text_input(
        "A qual relatório se refere o texto?"
    )

    st.divider()

    # =================================================
    # QUESTÃO 2
    # =================================================

    st.markdown("## 2. Marcos Internacionais")

    st.write(
        "Em 1978, representantes de diversos países reuniram-se em uma conferência internacional organizada pela OMS e UNICEF, defendendo a Atenção Primária à Saúde como estratégia para alcançar saúde para todos."
    )

    q2 = st.text_input(
        "A qual documento o texto se refere?"
    )

    st.divider()

    # =================================================
    # QUESTÃO 3
    # =================================================

    st.markdown("## 3. Atributos Essenciais da APS")

    st.caption(
        "Correlacione cada pergunta do instrumento PCA TOOL de avaliação internacional de APS, com apenas um atributo essencial da Atenção Primária à Saúde."
    )

    q3 = st.text_input(
        "Quando você vai ao serviço de saúde, é o mesmo médico ou enfermeiro que normalmente o atende?"
    )

    q4 = st.text_input(
        "O médico ou enfermeiro sabe quais foram os resultados das consultas realizadas com outros especialistas?"
    )

    q5 = st.text_input(
        "O serviço de saúde fica aberto em horários alternativos, como algumas noites ou finais de semana?"
    )

    q6 = st.text_input(
        "O serviço de saúde realiza pequenos procedimentos, como suturas, remoção de verrugas ou unhas encravadas?"
    )

    st.divider()

    # =================================================
    # QUESTÃO 4
    # =================================================

    st.markdown("## 4. Estratégia Saúde da Família")

    q7 = st.text_input(
        "Qual profissional diferencia uma equipe de Atenção Básica tradicional de uma equipe da Estratégia Saúde da Família?"
    )

    st.divider()

    # =================================================
    # QUESTÃO 5
    # =================================================

    st.markdown("## 5. eMulti")

    q8 = st.radio(
        "Dentre as categorias/especialidades abaixo, qual NÃO faz parte das eMulti (equipes multiprofissionais) na Atenção Primária à Saúde?",
        (
            "Pediatra",
            "Arte educador",
            "Médico de Família e Comunidade",
            "Assistente Social"
        )
    )

    st.divider()

    # =================================================
    # QUESTÃO 6
    # =================================================

    st.markdown("## 6. Saúde Mental")

    q9 = st.text_input(
        "Qual é o nome do processo realizado entre as equipes da Estratégia Saúde da Família e os CAPS AD, CAPS IJ e CAPS III, que promove troca de saberes, apoio técnico-pedagógico, corresponsabilização dos casos e construção compartilhada de Projetos Terapêuticos Singulares?"
    )

    st.divider()

    # =================================================
    # QUESTÃO 7
    # =================================================

    st.markdown("## 7. Política Nacional de Atenção Básica")

    q10 = st.text_input(
        "Segundo a última Política Nacional de Atenção Básica, qual o tamanho preconizado máximo de população adscrita por equipe de Saúde da Família (eSF)?"
    )

    enviar = st.form_submit_button("Enviar")


# =====================================================
# CORREÇÃO
# =====================================================

if enviar:

    resultados = [

        # Q1
        validar(q1, [
            "dawson",
            "relatório dawson",
            "relatorio dawson"
        ]),

        # Q2
        validar(q2, [
            "alma",
            "alma ata",
            "alma-ata"
        ]),

        # Q3
        validar(q3, [
            "longitudinalidade"
        ]),

        # Q4
        validar(q4, [
            "coordenação",
            "coordenacao",
            "coordenação do cuidado",
            "coordenacao do cuidado",
            "coordenação clínica",
            "coordenacao clinica"
        ]),

        # Q5
        validar(q5, [
            "acesso",
            "acesso de primeiro contato",
            "primeiro contato",
            "primeiro acesso",
            "porta de entrada",
            "contato inicial"
        ]),

        # Q6
        validar(q6, [
            "integralidade"
        ]),

        # Q7
        validar(q7, [
            "acs",
            "agente comunitário",
            "agente comunitario",
            "agente comunitário de saúde",
            "agente comunitario de saude"
        ]),

        # Q8
        "✅" if q8 == "Médico de Família e Comunidade" else "❌",

        # Q9
        validar(q9, [
            "matriciamento",
            "apoio matricial"
        ]),

        # Q10
        validar(q10, [
            "3500",
            "3.500",
            "3500 habitantes",
            "3500 pessoas",
            "até 3500",
            "3.500 habitantes"
        ])

    ]

    nota = resultados.count("✅")

    st.success(f"Você acertou **{nota}/10** questões.")

    st.markdown("## Resultado")

    for i, resultado in enumerate(resultados, start=1):
        st.write(f"**Questão {i}:** {resultado}")

    if nota == 10:
        st.balloons()
