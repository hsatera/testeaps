import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Quiz APS", layout="centered")

# Simulação de Banco de Dados (Em produção, o ideal é usar st.connection ou banco externo)
if 'db' not in st.session_state:
    st.session_state.db = []

st.title("🩺 Quiz: Atenção Primária à Saúde")

# Criação das abas
tab1, tab2 = st.tabs(["Responder Quiz", "Resultados"])

with tab1:
    st.markdown("### Responda às questões abaixo:")
    
    with st.form(key='aps_form', clear_on_submit=True):
        # Questão 1
        q1 = st.text_input("1. A qual relatório se refere o texto de 1920 sobre organização de serviços médicos britânicos?")
        
        # Questão 2
        q2 = st.text_input("2. Qual documento de 1978 estabeleceu a APS como estratégia global (Alma-Ata)?")
        
        # Questão 4 (Atributo)
        q4 = st.text_input("3. Atributo: Quando você vai ao serviço, é o mesmo profissional que te atende sempre?")
        
        # Questão 5 (Atributo)
        q5 = st.text_input("4. Atributo: O profissional sabe os resultados de consultas com especialistas?")
        
        # Questão 6 (Atributo)
        q6 = st.text_input("5. Atributo: O serviço fica aberto até às 20h em dias úteis?")
        
        # Questão 7 (Atributo)
        q7 = st.text_input("6. Atributo: O serviço oferece procedimentos como remoção de verrugas?")
        
        # Questão 8 (Profissional)
        q8 = st.text_input("7. Qual profissional diferencia uma eAB de uma Equipe de Saúde da Família?")

        submit = st.form_submit_button("Enviar Respostas Anônimas")

    if submit:
        # Lógica de Validação (Case Insensitive)
        def check(user_input, target):
            return target.lower() in user_input.lower()

        res = {
            "Relatório Dawson": 1 if check(q1, "Dawson") else 0,
            "Alma-Ata": 1 if check(q2, "Alma") else 0,
            "Longitudinalidade": 1 if check(q4, "Longitudinalidade") else 0,
            "Coordenação": 1 if check(q5, "Coordenação") else 0,
            "Acesso": 1 if check(q6, "Acesso") else 0,
            "Integralidade": 1 if check(q7, "Integralidade") else 0,
            "ACS": 1 if (check(q8, "ACS") or check(q8, "Agente")) else 0
        }
        
        st.session_state.db.append(res)
        st.success("Respostas enviadas com sucesso!")

with tab2:
    st.header("📊 Desempenho da Turma")
    
    if st.session_state.db:
        df = pd.DataFrame(st.session_state.db)
        
        # Gráfico de acertos por questão
        acertos = df.sum().reset_index()
        acertos.columns = ['Questão', 'Total de Acertos']
        
        st.bar_chart(data=acertos, x='Questão', y='Total de Acertos')
        
        st.write(f"**Total de participantes:** {len(df)}")
        st.dataframe(df) # Mostra a tabela de acertos (0 ou 1)
    else:
        st.info("Aguardando as primeiras respostas para gerar estatísticas.")
