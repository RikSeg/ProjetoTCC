# T.C.C.: 
## Aplicação de técnicas de visualização de informação para análise do desempenho acadêmico dos alunos de graduação da FACOM-UFU.
### O que é?
- Este projeto é um Dashboard desenvolvido para visualizar alguns modelos de Projeção Multidimensional sobre os dados de presenças em tópicos de aulas descritos na ementa de disciplinas da Faculdade de Computação da Universidade Federal de Uberlândia (FACOM) e verificar quais modelos de projeção possuem melhor desempenho.

- **OBS:** Todos os dados utilizados foram devidamente anonimizados pela DICOA-UFU (Divisão de Controle Acadêmico de Universidade Federal de Uberlândia), com objetivo de apenas manter os dados necessários para o TCC e respeitando a LGPD.

### Como foi elaborado?
- A ferramenta de visualização foi desenvolvida utilizando a linguagem Python na versão 3.12.2 e as bibliotecas Streamlit para desenvolvimento da interface, Plotly para representações gráficas e filtros, Pandas para manipulação e transformação de dados, Scikit-learn, Scipy e Numpy para desenvolver o script de execução dos modelos de projeção sobre as bases de disciplinas(executa_projecao.py). Ele é executado antes do programa, para transformar as bases de dados nas bases das projeções. 

### Bibliotecas
- Lista escrita no arquivo "requirements.txt"

### Execução
Preparação do repositório local:
- ``git clone <repo>`` (clona o repositório do github)
- ``cd <repo>`` (acessa o repositório)
- ``pip install virtualenv`` (Se já não tiver a biblioteca instalada)
- ``virtualenv venv`` para criar um novo ambiente virtual (aqui chamado de 'venv')
- ``source venv/bin/activate`` para entrar no ambiente virtual
- ``pip install -r requirements.txt`` para instalar as bibliotecas dos requisitos

- "cd projecão_multidimensional"
- execute "streamlit run AnaliseVisual.py"
- OBS.: O streamlit abrirá a aplicação no navegador
