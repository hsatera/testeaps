import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Avaliação APS", layout="wide")

# Inicialização do estado para armazenar respostas (Duração: enquanto o servidor estiver ativo)
if 'historico_respostas' not in st.session_state:
    st.session_state.historico_respostas = []

st.title("🩺 Avaliação de Conhecimentos: Atenção Primária")
st.markdown("---")

# Abas: Responder e Ver Resultados
tab_quiz, tab_dash = st.tabs(["📝 Responder Questionário", "📊 Painel de Resultados"])

# --- ABA 1: O QUESTIONÁRIO ---
with tab_quiz:
    st.info("Responda às questões abaixo. Suas respostas são enviadas de forma anônima.")
    
    with st.form(key="form_aps", clear_on_submit=True):
        
        # Pergunta 1
        st.markdown("### Pergunta 1")
        st.write("Em 1920, um conselho do Ministério da Saúde britânico publicou um relatório interno referente à organização de “serviços médicos e anexos”, em resposta a requisição do Ministro da Saúde. O relatório apresentava um conceito integrado de centros de saúde e serviços domiciliares. Os centros de saúde seriam primários e secundários, onde o nível primário coordenaria a assistência a partir de médicos e outros profissionais em contato direto com a comunidade.")
        q1 = st.text_input("A qual relatório se refere o texto?", key="q1")
        
        st.divider()

        # Pergunta 2
        st.markdown("### Pergunta 2")
        st.write("Em 1978, representantes de diversos países reuniram-se na União Soviética, em uma conferência internacional organizada pela Organização Mundial da Saúde e pelo UNICEF. O encontro resultou em um documento que estabeleceu a Atenção Primária à Saúde como estratégia central para alcançar melhores níveis de saúde global, tendo como lema “Saúde para todos no ano 2000” e defendendo princípios como equidade, participação comunitária e ações intersetoriais.")
        q2 = st.text_input("A qual documento o texto se refere?", key="q2")

        st.divider()
        
        st.markdown("### Atributos da APS (PCATool)")
        st.caption("Correlacione cada uma das perguntas abaixo com os atributos essenciais da Atenção Primária à Saúde.")

        # Pergunta 4
        q4 = st.text_input("4. Quando você vai ao serviço de saúde, é o mesmo médico ou enfermeiro que atende você todas as vezes?", placeholder="Resposta: Qual atributo?")
        
        # Pergunta 5
        q5 = st.text_input("5. O médico ou enfermeiro sabe quais foram os resultados da consulta com o especialista ou no serviço especializado?", placeholder="Resposta: Qual atributo?")
        
        # Pergunta 6
        q6 = st.text_input("6. O serviço de saúde fica aberto pelo menos algumas noites de dias úteis até às 20 horas?", placeholder="Resposta: Qual atributo?")
        
        # Pergunta 7
        q7 = st.text_input("7. O serviço de saúde oferece procedimentos como remoção de verrugas ou outros pequenos procedimentos cirúrgicos?", placeholder="Resposta: Qual atributo?")

        st.divider()

        # Pergunta 8
        st.markdown("### Pergunta 8")
        q8 = st.text_input("Qual o profissional que diferencia uma equipe de AB tradicional (eAB) e de uma Equipe de Saúde da Família?")

        enviar = st.form_submit_button("Enviar Respostas")

    if enviar:
        # Função simples de validação
        def validar(entrada, gabarito):
            # Retorna 1 se a palavra-chave estiver na resposta do usuário
            return 1 if gabarito.lower() in entrada.lower() else 0

        # Processamento
        resultado_atual = {
            "Relatório Dawson": validar(q1, "Dawson"),
            "Alma-Ata": validar(q2, "Alma"),
            "Longitudinalidade": validar(q4, "Longitudinalidade"),
            "Coordenação": validar(q5, "Coordenação"),
            "Acesso": validar(q6, "Acesso") + validar(q6, "Primeiro Contato"), # Aceita ambos
            "Integralidade": validar(q7, "Integralidade"),
            "Profissional (ACS)": validar(q8, "ACS") or validar(q8, "Agente")
        }
        
        # Garante que o Acesso não some 2 pontos se ele escrever os dois nomes
        if resultado_atual["Acesso"] > 1: resultado_atual["Acesso"] = 1

        st.session_state.historico_respostas.append(resultado_atual)
        st.balloons()
        st.success("Respostas registradas com sucesso!")

# --- ABA 2: RESULTADOS ---
with tab_dash:
    if len(st.session_state.historico_respostas) > 0:
        df = pd.DataFrame(st.session_state.historico_respostas)
        
        st.subheader("Estatísticas Gerais")
        col1, col2 = st.columns(2)
        col1.metric("Total de Respondentes", len(df))
        col2.metric("Média de Acertos", f"{(df.mean().mean() * 100):.1f}%")

        st.markdown("---")
        st.subheader("Acertos por Questão/Tema")
        
        # Preparando dados para o gráfico
        resumo = df.sum().sort_values(ascending=True)
        st.bar_chart(resumo, color="#29b5e8")

        with st.expander("Ver tabela de dados brutos (Anônima)"):
            st.write(df)
    else:
        st.warning("Ainda não existem respostas registradas.")
