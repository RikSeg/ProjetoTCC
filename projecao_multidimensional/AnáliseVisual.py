import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Define o número da disciplina para o arquivo que deseja ler
numeros_disciplinas = ["02","05","06","07","11","15","16"]  

# Define os modelos que você quer buscar
modelos = ["ISOMAP", "LSP", "PLMP", "t-SNE"]

selectdisciplina = st.selectbox("Disciplinas de Bacharelado:", numeros_disciplinas)
selectmodelo = st.selectbox("Modelo de Projeção Multidimensional:", modelos)
# Caminhos dos arquivos com base no padrão dos nomes
arquivo_dados = f"input/GSI0{selectdisciplina}.csv"
arquivo_isomap = f"output/Saida_ISOMAP_GSI0{selectdisciplina}.csv"
arquivo_lsp = f"output/Saida_LSP_GSI0{selectdisciplina}.csv"
arquivo_plmp = f"output/Saida_PLMP_GSI0{selectdisciplina}.csv"
arquivo_tsne = f"output/Saida_t-SNE_GSI0{selectdisciplina}.csv"

def scatterplot(df_modelo, modelo):
    color_map = {'Aprovado': 'blue', 'Reprovado': 'orange'}
    df_modelo["color"] = df_modelo['class'].map(color_map)

    # Criando o scatterplot com Plotly
    fig = px.scatter(df_modelo, x='v1', y='v2', color='class', color_discrete_map=color_map,
                     title=f"Distribuição dos Alunos no Modelo {modelo}",
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
    
    # Criando o gráfico de barras agrupadas
    fig = go.Figure()
    for value, count_series in counts.items():
        fig.add_trace(
            go.Bar(
                x=count_series.index, 
                y=count_series.values, 
                name=presenca_map[value]
            )
        )

    # Configurando o layout do gráfico
    fig.update_layout(
        barmode='group',  # Agrupamento de barras
        title="Quantidade de cada Status por Coluna",
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




col1, col2 = st.columns(2)
with col1:
    event = scatterplot(df_modelo_selecionado, selectmodelo)
with col2:
    if event['selection'].get('points') == []:
        st.write("Nenhuma seleção foi feita")
        st.dataframe(df_dados)
        subcol1,subcol2,subcol3 = st.columns(3)
        with subcol1:
            st.metric("Alunos:",len(df_dados))
        with subcol2:
            st.metric("Aprovados:",len(df_dados[df_dados['DSC_SITUACAO_FINAL']=='Aprovado']))
        with subcol3:
            st.metric("Reprovados:",len(df_dados[df_dados['DSC_SITUACAO_FINAL']=='Reprovado']))
        barrasPresencas(df_dados)
    elif event and isinstance(event, dict) and 'selection' in event and isinstance(event['selection'], dict) and isinstance(event['selection'].get('points'), list):
        selected_ids = [point['customdata'][0] for point in event['selection']['points'] if 'customdata' in point]
        filtered_df = df_dados[df_dados['IDT_MATRICULA'].isin(selected_ids)]
        st.write("Dados da Disciplina (Filtrados pela Seleção)")
        st.dataframe(filtered_df)

        subcol1,subcol2,subcol3 = st.columns(3)
        with subcol1:
            st.metric("Alunos:",len(filtered_df))
        with subcol2:
            st.metric("Aprovados:",len(filtered_df[filtered_df['DSC_SITUACAO_FINAL']=='Aprovado']))
        with subcol3:
            st.metric("Reprovados:",len(filtered_df[filtered_df['DSC_SITUACAO_FINAL']=='Reprovado']))
        barrasPresencas(filtered_df)
    else:
        st.write("Os dados de seleção não foram capturados corretamente.")
    
        



