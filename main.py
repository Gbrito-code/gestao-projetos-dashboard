import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Configurar o layout da página
st.set_page_config(layout="wide", page_title="Dashboard de Projetos")

# Barra lateral para upload do arquivo
with st.sidebar:
    st.title("Análise de Projetos")
    uploaded_file = st.file_uploader("Coloque o seu arquivo Excel aqui", type=["xlsx"])

# Verificar se o arquivo foi enviado
if uploaded_file is not None:
    # Ler os dados
    df = pd.read_excel(uploaded_file)
    
    # Título do dashboard
    st.title("Dashboard de Projetos")

    # Filtros interativos
    st.sidebar.subheader("Filtros")
    #options=df['Setor'].unique(): Mostra opções únicas encontradas na coluna "Setor".
    #default=df['Setor'].unique(): Por padrão, todos os setores estão selecionados.
    setores = st.sidebar.multiselect("Filtrar por Setor", options=df['Setor'].unique(), default=df['Setor'].unique())
    status = st.sidebar.multiselect("Filtrar por Status", options=df['Status'].unique(), default=df['Status'].unique())
    
    # Aplicar os filtros ao dataframe
    #df['Setor'].isin(setores): Verifica quais linhas têm "Setor" dentro dos setores selecionados no filtro.
    
    df_filtered = df[
        (df['Setor'].isin(setores)) &
        (df['Status'].isin(status))
    ]

    # Exibir métricas principais
    st.subheader("Métricas Resumidas")
    #Divide o espaço em 3 colunas para exibir métricas lado a lado
    col1, col2, col3 = st.columns(3)
    with col1:
        total_orcado = df_filtered['Valor Orçado'].sum()
        #Mostra uma métrica interativa 
        #primeiro argumento: nome  da metrica
        #segundo argumento: Valor formatado como moeda.
        st.metric("Total Orçado", f"R${total_orcado:,.2f}")
    with col2:
        total_negociado = df_filtered['Valor Negociado'].sum()
        st.metric("Total Negociado", f"R${total_negociado:,.2f}")
    with col3:
        #Filtra os projetos com "Status" igual a "Em andamento".
        #Conta quantos projetos tem esse status com len.
        projetos_ativos = len(df_filtered[df_filtered['Status'] == 'Em andamento'])
        st.metric("Projetos Ativos", projetos_ativos)

    # Gráficos com Matplotlib
    st.subheader("Análises Visuais")

    col1, col2 = st.columns(2)

    # Gráfico de barras - Valores por Setor
    with col1:
        st.write("**Distribuição de Valores por Setor**")
        #cria uma figura (fig1) e um eixo (ax1) no Matplotlib.
        #figsize=(6,4) define o tamanho do gráfico em polegadas (lagura x altura)
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        #Agrupa os dados do DataFrame filtrado por Setor e deois selecionar as colunas que vai ser utilizadas
        valores_por_setor = df_filtered.groupby('Setor')[['Valor Orçado', 'Valor Negociado']].sum()
        #.plot(kind='bar) gera um gráfico de barras
        # ax=ax1 - especifica que o gráfico será desenhado no eixo ax1
        valores_por_setor.plot(kind='bar', ax=ax1, color=["#1f77b4", "#ff7f0e"])
        #título do gráfico.
        ax1.set_title("Valores Orçados e Negociados por Setor", fontsize=12)
        #Define o rótulo do eixo Y (vertical), indicando que os valores estão em reais.
        ax1.set_ylabel("Valores (R$)", fontsize=10)
        #Define o rótulo do eixo X (horizontal), que exibe os setores.
        ax1.set_xlabel("Setor", fontsize=10)
        #legend: Adiciona uma legenda explicando as cores das barras.
        #loc="upper right": Posiciona a legenda no canto superior direito do gráfico.
        ax1.legend(["Valor Orçado", "Valor Negociado"], loc="upper right")
        #exibe o gráfico
        st.pyplot(fig1)

    # Gráfico de pizza - Distribuição por Status
    with col2:
        st.write("**Distribuição dos Projetos por Status**")
        #value_counts() - Conta quantos projetos existem para cada valor único na coluna "Status".
        status_count = df_filtered['Status'].value_counts()
        print(status_count)
        #O índice representa os tipos de status
        #Os valores representa o número de projetos
        
        #criando o grafico e definir o tamanho
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        
        #Gera o gráfico de pizza
        ax2.pie(status_count, #Dados do gráfico (quantidade de projetos por status)
                labels=status_count.index, #Define os rótulos como os índices da série (os nomes dos status).
                autopct='%1.1f%%', #Mostra os percentuais diretamente no gráfico (1 casa decimal).
                startangle=90, #Rotaciona o gráfico para que a primeira fatia comece no topo.
                colors=plt.cm.Paired.colors #Usa uma paleta de cores predefinida.
                )
        ax2.set_title("Distribuição de Projetos por Status", fontsize=12)
        st.pyplot(fig2)

    # Tabela dinâmica por setor
    st.subheader("Resumo por Setor")
    st.dataframe(valores_por_setor)

else:
    st.write("Por favor, faça o upload de um arquivo Excel para visualizar o dashboard.")
