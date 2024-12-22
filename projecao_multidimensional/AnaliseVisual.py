import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")



# Define o número da disciplina para o arquivo que deseja ler
numeros_disciplinas = ["02","05","06","07","11","15","16"]  

# Define os modelos que você quer buscar
modelos = ["ISOMAP", "LSP", "PLMP", "t-SNE"]

debug_mode = st.toggle("Teste Iris", value=False, help="Ative para que seja mostrada a projeção apenas do dataset Iris. Todos os gráficos e filtros não relacionados à projeção serão desativados.")
col_filtr1,col_filtr2 = st.columns(2)

if not debug_mode:
    with col_filtr1:
        selectdisciplina = st.selectbox("Disciplinas de Bacharelado:", numeros_disciplinas)
    with col_filtr2:
        selectmodelo = st.selectbox("Modelo de Projeção Multidimensional:", modelos)
else:
    with col_filtr2:
        selectmodelo = st.selectbox("Modelo de Projeção Multidimensional:", modelos)

if not debug_mode:
    # Caminhos dos arquivos com base no padrão dos nomes
    arquivo_dados = f"input/GSI0{selectdisciplina}.csv"
    arquivo_isomap = f"output/Saida_ISOMAP_GSI0{selectdisciplina}.csv"
    arquivo_lsp = f"output/Saida_LSP_GSI0{selectdisciplina}.csv"
    arquivo_plmp = f"output/Saida_PLMP_GSI0{selectdisciplina}.csv"
    arquivo_tsne = f"output/Saida_t-SNE_GSI0{selectdisciplina}.csv"
else:
    arquivo_dados = "input/iris_index.csv"
    arquivo_isomap = "output/Saida_ISOMAP_iris_index.csv"
    arquivo_lsp = "output/Saida_LSP_iris_index.csv"
    arquivo_plmp = "output/Saida_PLMP_iris_index.csv"
    arquivo_tsne = "output/Saida_t-SNE_iris_index.csv"

def scatterplot(df_modelo, modelo):
    color_map = {'Aprovado': 'blue', 'Reprovado': 'orange'}
    df_modelo["color"] = df_modelo['class'].map(color_map)

    # Criando o scatterplot com Plotly
    fig = px.scatter(df_modelo, x='v1', y='v2', color='class', color_discrete_map=color_map,
                     title=f"Modelo {modelo}",
                     hover_data = ['id','class'])
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),  # Remove grid e ticks do eixo X
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),   # Remove grid e ticks do eixo Y
        plot_bgcolor="white",  # Cor de fundo do gráfico
        paper_bgcolor="white",  # Cor de fundo ao redor do gráfico
        margin=dict(t=20, b=20, l=20, r=20),  # Adicionar margem ao redor do gráfico
        shapes=[dict(
            type='rect',  # Forma retangular
            x0=0, x1=1, y0=0, y1=1,  # Define a área do retângulo
            xref='paper', yref='paper',  # Refere-se ao papel (o espaço ao redor do gráfico)
            line=dict(color="black", width=2)  # Cor e espessura da borda
        )]
    )
    # Exibindo o gráfico no Streamlit
    event = st.plotly_chart(fig, on_select="rerun")
    return event

def barrasPresencas(df):
    # Separando as colunas do eixo x (excluindo as 5 primeiras)
    df_data = df.iloc[:, 5:]
    # Contando a quantidade de cada categoria em cada coluna
    counts = {value: (df_data == value).sum() for value in [0, 1, 2]}

    presenca_map = {0: 'Ausente', 1: 'Presente', 2: 'Não Ministrada'}
    cores= {0:'red', 1:'green', 2:'blue'}
    # Criando o gráfico de barras agrupadas
    fig = go.Figure()
    for value, count_series in counts.items():
        fig.add_trace(
            go.Bar(
                x=count_series.index, 
                y=count_series.values, 
                name=presenca_map[value],
                marker=dict(color=cores[value])
            )
        )

    # Configurando o layout do gráfico
    fig.update_layout(
        barmode='group',  # Agrupamento de barras
        title="Presenças por Tópico da Disciplina",
        xaxis_title="Colunas",
        yaxis_title="Quantidade",
        legend_title="Presença",
        xaxis=dict(
        type='category',  # Define o eixo X como categórico
        categoryorder='array',  # Ordem das categorias conforme a sequência dos dados
        tickmode='array',  # Exibe as categorias como ticks
        tickvals=list(counts[0].index),  # Usando os nomes das colunas como valores do eixo X
        ),
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)



def x_y_variation(df):
    return 0

# Leitura dos arquivos
try:
    if not debug_mode:
        # Carrega o dataframe principal da disciplina
        df_dados = pd.read_csv(arquivo_dados)
        #print("\n\nDados da disciplina:\n\n", df_dados.head())

        # Carrega os dataframes dos modelos
        df_isomap = pd.read_csv(arquivo_isomap)
        df_lsp = pd.read_csv(arquivo_lsp)
        df_plmp = pd.read_csv(arquivo_plmp)
        df_tsne = pd.read_csv(arquivo_tsne)
    else:
        # Carrega o dataframe principal da disciplina
        df_dados = pd.read_csv(arquivo_dados)
        #print("\n\nDados da disciplina:\n\n", df_dados.head())

        # Carrega os dataframes dos modelos
        df_isomap = pd.read_csv(arquivo_isomap)
        df_lsp = pd.read_csv(arquivo_lsp)
        df_plmp = pd.read_csv(arquivo_plmp)
        df_tsne = pd.read_csv(arquivo_tsne)
    
except FileNotFoundError as e:
    print("Arquivo não encontrado:", e)

# Exibição dos gráficos lado a lado
if selectmodelo == "ISOMAP":
    df_modelo_selecionado = df_isomap
elif selectmodelo == "LSP":
    df_modelo_selecionado = df_lsp
elif selectmodelo == "PLMP":
    df_modelo_selecionado = df_plmp
elif selectmodelo == "t-SNE":
    df_modelo_selecionado = df_tsne



df_saida=[]

col_graficos = st.columns(2)
with col_graficos[0]:
    event = scatterplot(df_modelo_selecionado, selectmodelo)
with col_graficos[1]:
    if event['selection'].get('points') == []:
        #st.write("Nenhuma seleção foi feita")
        df_saida = df_dados

    elif event and isinstance(event, dict) and 'selection' in event and isinstance(event['selection'], dict) and isinstance(event['selection'].get('points'), list):
        selected_ids = [point['customdata'][0] for point in event['selection']['points'] if 'customdata' in point]
        filtered_df = df_dados[df_dados['IDT_MATRICULA'].isin(selected_ids)]
        #st.write("Dados da Disciplina (Filtrados pela Seleção)")
        df_saida = filtered_df
    else:
        st.write("Os dados de seleção não foram capturados corretamente.")

    df_graf = df_saida
    # Adicionando o filtro por turma
    if not debug_mode:
        turmas = sorted(df_graf['IDT_TURMA'].unique())
        turmas = ["Todas as Turmas"] + list(turmas)  # Adicionando a opção no início da lista
        turma_selecionada = st.selectbox("Selecione a turma", options=turmas, index=0)

        # Filtrando o DataFrame apenas se uma turma específica for selecionada
        if turma_selecionada != "Todas as Turmas":
            df_graf = df_graf[df_graf['IDT_TURMA'] == turma_selecionada]
        else:
            df_graf = df_graf
        barrasPresencas(df_graf)
if not debug_mode:        
    col_metr = st.columns(5)
    with col_metr[0]:
        st.metric("Alunos:",len(df_graf))
    with col_metr[1]:
        st.metric("Aprovados:",len(df_graf[df_graf['DSC_SITUACAO_FINAL']=='Aprovado']))
    with col_metr[2]:
        st.metric("Reprovados:",len(df_graf[df_graf['DSC_SITUACAO_FINAL']=='Reprovado']))
    with col_metr[3]:
        st.metric("Total de Turmas:",len(df_graf['IDT_TURMA'].unique()))
    with col_metr[4]:
        media = df_graf['VLR_MEDIA'].sum()/len(df_graf['IDT_MATRICULA'])
        st.metric("Média das Notas:",f"{media:.2f}")


st.write("Base de dados completa:")
st.dataframe(df_saida)

    



