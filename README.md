# Dashboard de Vendas Interativo com Streamlit 🛍️📊

Este projeto é um dashboard de vendas interativo desenvolvido como parte do curso de Streamlit da Alura. Ele visa demonstrar a criação de uma aplicação web para visualização e análise de dados de vendas de forma dinâmica e intuitiva.

## 📜 Sobre o Projeto

O dashboard permite aos usuários explorar dados de vendas, aplicando filtros e visualizando informações através de gráficos e tabelas. A aplicação consome dados de uma API e os processa para apresentar insights sobre receita, quantidade de vendas e desempenho dos vendedores.

**Funcionalidades Principais:**

* **Dashboard Principal (`Dashboard.py`)**:
    * Visualização de métricas chave como receita total e quantidade total de vendas.
    * Filtros interativos por:
        * Região (Brasil, Centro-Oeste, Nordeste, Norte, Sudeste, Sul).
        * Ano (com opção para visualizar todo o período).
        * Vendedores.
    * Navegação em abas:
        * **Receita**:
            * Mapa de receita por estado.
            * Gráfico de linha de receita mensal, com diferenciação por ano.
            * Gráfico de barras dos top estados por receita.
            * Gráfico de barras de receita por categoria de produto.
        * **Quantidade de Vendas**:
            * Mapa de quantidade de vendas por estado.
            * Gráfico de linha de vendas mensais, com diferenciação por ano.
            * Gráfico de barras dos top estados por quantidade de vendas.
            * Gráfico de barras de quantidade de vendas por categoria de produto.
        * **Vendedores**:
            * Gráficos de barras configuráveis para exibir os top N vendedores por receita e por quantidade de vendas.
* **Página de Dados Brutos (`pages/Dados brutos.py`)**:
    * Exibição dos dados completos em formato tabular.
    * Seleção de colunas para visualização.
    * Filtros avançados por:
        * Nome do produto.
        * Categoria do produto.
        * Faixa de preço do produto.
        * Faixa de valor do frete.
        * Intervalo de data da compra.
        * Vendedor.
        * Local da compra.
        * Avaliação da compra (1 a 5 estrelas).
        * Tipo de pagamento.
        * Quantidade de parcelas.
    * Contagem de linhas e colunas da tabela filtrada.
    * Opção para fazer o download dos dados filtrados em formato CSV.

## 🛠️ Tecnologias Utilizadas

* **Python**
* **Streamlit**: Para a criação da interface web interativa.
* **Pandas**: Para manipulação e análise de dados.
* **Plotly Express**: Para a geração de gráficos interativos.
* **Requests**: Para realizar requisições HTTP à API de dados.

## 🚀 Como Executar

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/leoarjo/dashboard_vendas.git](https://github.com/leoarjo/dashboard_vendas.git)
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd dashboard_vendas
    ```
3.  Crie um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```
4.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
5.  Execute a aplicação Streamlit:
    ```bash
    streamlit run Dashboard.py
    ```
    A aplicação estará disponível em seu navegador.

## 📊 Fonte dos Dados

Os dados são obtidos em tempo real através da API: `https://labdados.com/produtos`.

## ✨ Aprendizados

Este projeto foi uma excelente oportunidade para aprender e aplicar os conceitos de desenvolvimento de dashboards web com Streamlit, manipulação de dados com Pandas e criação de visualizações interativas com Plotly Express. O curso da Alura forneceu uma base sólida para transformar dados brutos em insights acionáveis.

## 🙏 Agradecimentos

Agradeço à Alura pelo excelente curso e aos instrutores pelo conhecimento compartilhado.
