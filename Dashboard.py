import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide')

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.title('DASHBOARD DE VENDAS :shopping_trolley:')

url = 'https://labdados.com/produtos'
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''

todos_anos = st.sidebar.checkbox('Dados de todo o período', value = True)
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao':regiao.lower(), 
                'ano':ano}

response = requests.get(url, params = query_string)
# Request > Json > Dataframe
dados = pd.DataFrame.from_dict(response.json()) # transformando requisição em JSON e depois em DataFrame
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]

## Tabelas
### Tabelas de receita
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending=False)

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending = False)

### Tabelas de quantidade de vendas
vendas_estados = dados.groupby('Local da compra').size().reset_index(name='Quantidade de vendas')
vendas_estados = vendas_estados.merge(
    dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']],
    on='Local da compra',
    how='left'
).sort_values('Quantidade de vendas', ascending=False)

vendas_mensais = dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME')).size().reset_index(name = 'Quantidade de vendas')
vendas_mensais['Ano'] = vendas_mensais['Data da Compra'].dt.year
vendas_mensais['Mes'] = vendas_mensais['Data da Compra'].dt.month_name()

vendas_categoria = dados.groupby('Categoria do Produto').size().reset_index(name='Quantidade de vendas')
vendas_categoria = vendas_categoria.sort_values('Quantidade de vendas', ascending = False)

### Tabelas vendedores
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

## Gráficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Receita por estado')

fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mes',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, receita_mensal.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita mensal')

fig_receita_mensal.update_layout(yaxis_title = 'Receita')

fig_receita_estados = px.bar(receita_estados.head(), 
                             x = 'Local da compra',
                             y = 'Preço',
                             text_auto = True,
                             title = 'Top estados (receita)')

fig_receita_estados.update_layout(yaxis_title = 'Receita')

fig_receita_categorias = px.bar(receita_categorias,
                                text_auto = True,
                                title = 'Receita por categoria')

fig_receita_categorias.update_layout(yaxis_title = 'Receita')

fig_mapa_qtd_vendas = px.scatter_geo(vendas_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Quantidade de vendas',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Vendas por estado')

fig_vendas_mensais = px.line(vendas_mensais,
                             x = 'Mes',
                             y = 'Quantidade de vendas',
                             markers = True,
                             range_y = (0, vendas_mensais.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Vendas mensais')

fig_receita_mensal.update_layout(yaxis_title = 'Vendas')

fig_vendas_categoria = px.bar(vendas_categoria,
                                x = 'Categoria do Produto',
                                y = 'Quantidade de vendas',
                                text_auto = True,
                                title = 'Quantidade de vendas por categoria')

fig_vendas_estados = px.bar(vendas_estados.head(),
                            x = 'Local da compra',
                            y = 'Quantidade de vendas',
                            text_auto = True,
                            title = 'Top estados (quantidade de vendas)')

## Visualização no streamlit

aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])

with aba1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width = True)
        st.plotly_chart(fig_receita_estados, use_container_width = True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width = True)
        st.plotly_chart(fig_receita_categorias, use_container_width = True)

with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_qtd_vendas, use_container_width = True)
        st.plotly_chart(fig_vendas_estados, use_container_width = True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_vendas_mensais, use_container_width = True)
        st.plotly_chart(fig_vendas_categoria, use_container_width = True)

with aba3:
    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores), 
                                        x = 'sum', 
                                        y = vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores).index, 
                                        text_auto = True, 
                                        title = f'Top {qtd_vendedores} vendedores (receita)')
        st.plotly_chart(fig_receita_vendedores)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores), 
                                        x = 'count', 
                                        y = vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores).index, 
                                        text_auto = True, 
                                        title = f'Top {qtd_vendedores} vendedores (quantidade de vendas)')
        st.plotly_chart(fig_vendas_vendedores)