import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Dashboard de Análise de Dados AliExpress")

# --- Gerenciamento de Estado para Navegação (simulando links) ---
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Visão Geral dos Dados"

def set_page(page_name):
    st.session_state.selected_page = page_name

# --- Menu Lateral para Navegação (mais clean) ---
st.sidebar.title("Navegação")

if st.sidebar.button("Visão Geral dos Dados", key="nav_overview"):
    set_page("Visão Geral dos Dados")
if st.sidebar.button("Análises Univariadas", key="nav_univariate"):
    set_page("Análises Univariadas")
if st.sidebar.button("Análises Multivariadas", key="nav_multivariate"):
    set_page("Análises Multivariadas")

st.title('Dashboard de Análise de Dados de Produtos AliExpress')

# --- Carregamento dos Dados (feito uma vez no início) ---
try:
    df = pd.read_csv('bases_tratadas/dados_tratados.csv', sep=';')
except FileNotFoundError:
    st.error("Erro: O arquivo 'dados_tratados.csv' não foi encontrado. Por favor, verifique o caminho.")
    st.stop()

# Seleção de Colunas Numéricas (para uso em Análises Univariadas e Multivariadas)
df_num = df.select_dtypes(include=['number'])
lista_de_colunas_numericas = df_num.columns.tolist()

# Verifica se existem colunas numéricas antes de prosseguir com as análises
if not lista_de_colunas_numericas:
    st.error("Não foram encontradas colunas numéricas no seu DataFrame para realizar análises.")
    st.stop()

# --- Conteúdo Principal Baseado na Seleção do Menu Lateral ---

if st.session_state.selected_page == "Visão Geral dos Dados":
    st.subheader('Visão Geral dos Dados')
    st.write("Aqui você pode visualizar os dados originais e verificar a presença de valores nulos, que são cruciais para a qualidade das análises dos produtos do AliExpress.")

    st.markdown('#### Dados Originais dos Produtos AliExpress')
    st.dataframe(df)

    st.markdown('#### Análise de Nulos')
    aux = df.isnull().sum().reset_index()
    aux.columns = ['Variável', 'Quantidade de Nulos']
    st.dataframe(aux)
    if aux['Quantidade de Nulos'].sum() == 0:
        st.info("Ótimo! Não há valores nulos nos seus dados de produtos.")
    else:
        st.warning("Atenção! Existem valores nulos em algumas variáveis. Isso pode impactar a precisão das análises de preços e descontos.")

elif st.session_state.selected_page == "Análises Univariadas":
    st.subheader('Análises Univariadas')
    st.write('Nesta seção, explore as características individuais de cada variável numérica, como preços e quantidades, dos produtos do AliExpress.')

    st.write('**Medidas Resumo de Todas as Colunas Numéricas**')
    st.dataframe(df_num.describe())

    st.write('---')
    st.write('**Análise Detalhada por Coluna Numérica**')

    coluna_escolhida = st.selectbox('Escolha a coluna para análise detalhada', lista_de_colunas_numericas, key="uni_col_select")

    # Calcula as medidas resumo para a coluna escolhida
    media = round(df_num[coluna_escolhida].mean(), 2)
    desvio = round(df_num[coluna_escolhida].std(), 2)
    mediana = round(df_num[coluna_escolhida].quantile(0.5), 2)
    maximo = round(df_num[coluna_escolhida].max(), 2)
    minimo = round(df_num[coluna_escolhida].min(), 2)

    # Cria um DataFrame para apresentar as medidas em forma de tabela
    dados_medidas = {
        'Medida': ['Média', 'Mediana', 'Desvio Padrão', 'Valor Mínimo', 'Valor Máximo'],
        'Valor': [media, mediana, desvio, minimo, maximo]
    }
    df_medidas = pd.DataFrame(dados_medidas)

    st.write(f"**Medidas Resumo para a Coluna: '{coluna_escolhida.replace('_', ' ').title()}'**")
    st.dataframe(df_medidas.set_index('Medida'))

    # --- Textos Explicativos para Análise Univariada ---
    st.markdown('### Interpretação da Coluna Selecionada')

    st.write(f"Você selecionou a coluna **'{coluna_escolhida.replace('_', ' ').title()}'** para análise. Esta coluna representa uma característica numérica dos produtos do AliExpress.")

    st.markdown('#### Análise da Média e Mediana:')
    st.write(f"A **média** para '{coluna_escolhida.replace('_', ' ').title()}' é **{media}**. A **mediana** é **{mediana}**.")
    if abs(media - mediana) < 0.1 * media:
        st.write(f"Como a média e a mediana são **próximas**, isso sugere que a distribuição dos dados de '{coluna_escolhida.replace('_', ' ').title()}' é **aproximadamente simétrica**. A maioria dos valores dos produtos está concentrada em torno do centro, sem uma forte influência de preços ou quantidades extremamente altas ou baixas.")
    elif media > mediana:
        st.write(f"A **média ({media}) é maior que a mediana ({mediana})**. Isso indica que a distribuição de '{coluna_escolhida.replace('_', ' ').title()}' é **assimétrica à direita (positivamente assimétrica)**. Provavelmente, existem alguns produtos com valores mais altos (preços mais caros, quantidades maiores) que estão 'puxando' a média para cima em relação à mediana. Isso é comum em dados de preços e vendas, onde a maioria dos itens tem um preço/quantidade, mas alguns poucos são muito mais caros/vendidos.")
    else:
        st.write(f"A **média ({media}) é menor que a mediana ({mediana})**. Isso indica que a distribuição de '{coluna_escolhida.replace('_', ' ').title()}' é **assimétrica à esquerda (negativamente assimétrica)**. Provavelmente, existem alguns produtos com valores mais baixos que estão 'puxando' a média para baixo. Isso é menos comum em preços, mas pode acontecer em outros tipos de dados.")

    st.markdown('#### Análise do Desvio Padrão:')
    st.write(f"O **desvio padrão** de '{coluna_escolhida.replace('_', ' ').title()}' é **{desvio}**.")
    st.write(f"Este valor mede a dispersão dos dados em torno da média. Um desvio padrão de **{desvio}** significa que, em média, os valores individuais dos produtos se desviam cerca de {desvio} da média de {media}.")
    if desvio / media < 0.2:
        st.write(f"Um desvio padrão relativamente baixo em comparação com a média indica que os preços ou quantidades dos produtos estão **bem concentrados** e pouco dispersos, sugerindo uma homogeneidade maior nos dados.")
    elif desvio / media > 0.5:
        st.write(f"Um desvio padrão mais alto sugere que os dados de '{coluna_escolhida.replace('_', ' ').title()}' estão **mais espalhados** em torno da média, indicando maior variabilidade nos preços ou quantidades dos produtos.")

    st.markdown('#### Valores Mínimo e Máximo:')
    st.write(f"O **valor mínimo** encontrado para '{coluna_escolhida.replace('_', ' ').title()}' é **{minimo}** e o **valor máximo** é **{maximo}**.")
    st.write("Esses valores fornecem o range completo dos dados observados para essa coluna, mostrando a amplitude de preços ou quantidades de produtos no AliExpress.")

    # --- Gráficos Univariados ---
    st.markdown('### Visualização da Distribuição')
    st.write('#### Histograma')
    fig = px.histogram(df_num, x=coluna_escolhida, title=f'Histograma de {coluna_escolhida.replace("_", " ").title()}')
    st.plotly_chart(fig)
    st.write(f"O **histograma** acima mostra a frequência de cada faixa de valores para a coluna **'{coluna_escolhida.replace('_', ' ').title()}'**. Ele permite visualizar a forma da distribuição dos preços ou quantidades dos produtos: se a maioria dos itens está em uma faixa específica de valores, ou se há múltiplos picos de concentração.")

    st.write('#### Boxplot')
    fig2 = px.box(df_num, x=coluna_escolhida, title=f'Boxplot de {coluna_escolhida.replace("_", " ").title()}') # Horizontal
    st.plotly_chart(fig2)
    st.write(f"O **boxplot** de **'{coluna_escolhida.replace('_', ' ').title()}'** exibe a mediana (preço/quantidade central), os quartis (intervalo onde 50% dos produtos se encontram), e os potenciais outliers (produtos com preços ou quantidades atípicas). É uma ferramenta valiosa para identificar rapidamente a centralidade, dispersão e a presença de valores incomuns nos dados do AliExpress.")

    if 'preco_com_desconto' in df_num.columns:
        preco_minimo_desconto = df_num['preco_com_desconto'].min()
        st.write(f"---")
        st.write(f"**Observação:** O **Preço Mínimo com Desconto** (da coluna 'preco_com_desconto') no dataset de produtos AliExpress é de **R$ {round(preco_minimo_desconto, 2)}**.")

elif st.session_state.selected_page == "Análises Multivariadas":
    st.subheader('Análises Multivariadas')
    st.write('Nesta seção, você pode investigar a relação entre duas variáveis numéricas, como os preços com e sem desconto dos produtos do AliExpress.')

    st.markdown('### Gráficos de Relação entre Variáveis')
    lista_de_escolhas_multivariada = st.multiselect(
        'Escolha **duas** colunas numéricas para avaliar a relação entre elas:',
        lista_de_colunas_numericas,
        key="multi_col_select"
    )

    if len(lista_de_escolhas_multivariada) == 2:
        coluna_x = lista_de_escolhas_multivariada[0]
        coluna_y = lista_de_escolhas_multivariada[1]

        # Invertendo os eixos para Preço Sem Desconto (X) vs Preço Com Desconto (Y)
        # Se 'preco_sem_desconto' e 'preco_com_desconto' estiverem nas escolhas,
        # vamos garantir que o preço original (sem desconto) esteja no eixo X para uma análise mais intuitiva.
        if 'preco_sem_desconto' in lista_de_escolhas_multivariada and 'preco_com_desconto' in lista_de_escolhas_multivariada:
            st.markdown('#### Gráfico de Dispersão (Preço Original vs Preço com Desconto)')
            fig3 = px.scatter(df_num, x='preco_sem_desconto', y='preco_com_desconto',
                              title=f'Dispersão: Preço Original vs Preço com Desconto no AliExpress',
                              labels={'preco_sem_desconto': 'Preço Sem Desconto (R$)',
                                      'preco_com_desconto': 'Preço Com Desconto (R$)'})
            st.plotly_chart(fig3)
            # Ajustando as colunas para o texto de interpretação a seguir
            coluna_x_interpret = 'preco_sem_desconto'
            coluna_y_interpret = 'preco_com_desconto'
        else:
            st.markdown('#### Gráfico de Dispersão')
            fig3 = px.scatter(df_num, x=coluna_x, y=coluna_y,
                              title=f'Dispersão entre {coluna_x.replace("_", " ").title()} e {coluna_y.replace("_", " ").title()}',
                              labels={coluna_x: coluna_x.replace('_', ' ').title(),
                                      coluna_y: coluna_y.replace('_', ' ').title()})
            st.plotly_chart(fig3)
            coluna_x_interpret = coluna_x
            coluna_y_interpret = coluna_y

        # Parâmetros
        bins = 5
        coluna_y = 'preco_com_desconto'
        coluna_de_faixa = 'preco_sem_desconto'

        # Criar os rótulos
        labels = [f'Faixa {i+1}' for i in range(bins)]

        # Criar faixas com ordenação correta
        faixas = pd.cut(df_num[coluna_de_faixa], bins=bins, labels=labels, include_lowest=True)
        faixas = faixas.astype(pd.api.types.CategoricalDtype(categories=labels, ordered=True))

        # Adicionar a coluna de faixas no DataFrame
        df_num['Faixa de Preço Sem Desconto'] = faixas

        # Criar o boxplot com Plotly
        st.markdown('#### Boxplot da Variável Y (Horizontal)')
        fig4 = px.box(df_num,
                    x=coluna_x,
                    y='Faixa de Preço Sem Desconto',
                    title=f'Distribuição de {coluna_y.replace("_", " ").title()} por Faixa de {coluna_de_faixa.replace("_", " ").title()}',
                    labels={coluna_y: coluna_y.replace('_', ' ').title(),
                            'Faixa de Preço Sem Desconto': 'Faixa de Preço Sem Desconto'})

        st.plotly_chart(fig4)



        # --- Textos Explicativos para Análises Multivariadas ---
        st.markdown('### Interpretação das Variáveis Selecionadas')

        st.write(f"Você selecionou as colunas **'{coluna_x_interpret.replace('_', ' ').title()}'** e **'{coluna_y_interpret.replace('_', ' ').title()}'** para analisar a relação entre elas nos dados de produtos do AliExpress.")

        st.markdown('#### Análise do Gráfico de Dispersão:')
        if coluna_x_interpret == 'preco_sem_desconto' and coluna_y_interpret == 'preco_com_desconto':
            st.write(f"O **gráfico de dispersão** mostra a relação entre o **Preço Sem Desconto** (original) e o **Preço Com Desconto** (final) dos produtos do AliExpress.")
            st.write("Cada ponto representa um produto. Idealmente, os pontos devem formar uma linha reta diagonal ascendente, indicando que o preço com desconto é uma proporção direta do preço original. Isso demonstra a consistência na aplicação dos descontos.")
            st.markdown("- **Tendência:** Espere uma **forte tendência positiva e linear**. Produtos mais caros sem desconto devem ter preços mais altos com desconto.")
            st.markdown("- **Força da Relação:** A maioria dos pontos deve estar bem agrupada ao redor de uma linha imaginária. Pontos muito distantes dessa linha podem ser **outliers** que merecem investigação (ex: erros de preço, descontos incomuns ou muito agressivos, produtos com políticas de preço muito diferentes).")
            st.markdown("- **Outliers:** Analise os pontos que se desviam. Por exemplo, um produto com um 'Preço Sem Desconto' muito alto, mas um 'Preço Com Desconto' relativamente baixo, indica um **desconto massivo**.")
        else:
            st.write(f"O **gráfico de dispersão** visualiza como os valores de **'{coluna_x_interpret.replace('_', ' ').title()}'** se relacionam com os de **'{coluna_y_interpret.replace('_', ' ').title()}'** nos produtos do AliExpress. Cada ponto representa uma observação. Procure por:")
            st.markdown("- **Tendência:** Se os pontos formam um padrão que sobe (relação positiva), desce (relação negativa) ou se não há um padrão claro (sem relação linear).")
            st.markdown("- **Força da Relação:** Quão próximos os pontos estão de formar uma linha. Pontos mais agrupados indicam uma relação mais forte.")
            st.markdown("- **Outliers:** Pontos que se destacam significativamente da nuvem principal, que podem merecer uma investigação mais aprofundada por representarem valores atípicos de produtos.")

        st.markdown('#### Coeficiente de Correlação:')
        correlacao = df_num[coluna_x_interpret].corr(df_num[coluna_y_interpret])
        st.write(f"O coeficiente de correlação (Pearson) entre '{coluna_x_interpret.replace('_', ' ').title()}' e '{coluna_y_interpret.replace('_', ' ').title()}' é de **{correlacao:.2f}**.")

        if coluna_x_interpret == 'preco_sem_desconto' and coluna_y_interpret == 'preco_com_desconto':
            if correlacao > 0.9:
                st.write(f"Com um coeficiente de **{correlacao:.2f}**, há uma **correlação extremamente forte e positiva** entre o preço original e o preço com desconto. Isso é esperado, pois o preço final é diretamente derivado do preço inicial. Valores muito próximos de 1.0 indicam alta consistência na aplicação dos descontos no AliExpress.")
            elif correlacao >= 0.7:
                st.write(f"A correlação de **{correlacao:.2f}** é **forte e positiva**. Indica que, em geral, quanto maior o preço original de um produto, maior será seu preço com desconto. A leve distância de 1.0 pode ser explicada por variações nas porcentagens de desconto aplicadas a diferentes produtos, ou por outliers.")
            else:
                st.write(f"Uma correlação de **{correlacao:.2f}** é **moderada a baixa** para preços com e sem desconto. Isso pode sugerir **inconsistências significativas** na aplicação dos descontos ou a presença de muitos outliers que distorcem a relação linear esperada. Vale a pena investigar os produtos que fogem muito do padrão.")
        else: # Interpretação genérica para outras combinações de colunas
            if correlacao > 0.7:
                st.write(f"Isso sugere uma **forte correlação positiva**: quando **'{coluna_x_interpret.replace('_', ' ').title()}'** aumenta, **'{coluna_y_interpret.replace('_', ' ').title()}'** tende a aumentar significativamente.")
            elif correlacao < -0.7:
                st.write(f"Isso sugere uma **forte correlação negativa**: quando **'{coluna_x_interpret.replace('_', ' ').title()}'** aumenta, **'{coluna_y_interpret.replace('_', ' ').title()}'** tende a diminuir significativamente.")
            elif 0.3 <= correlacao <= 0.7:
                st.write(f"Isso sugere uma **correlação positiva moderada**: há uma tendência de **'{coluna_x_interpret.replace('_', ' ').title()}'** e **'{coluna_y_interpret.replace('_', ' ').title()}'** aumentarem juntos, mas com alguma dispersão.")
            elif -0.7 <= correlacao <= -0.3:
                st.write(f"Isso sugere uma **correlação negativa moderada**: há uma tendência de **'{coluna_x_interpret.replace('_', ' ').title()}'** aumentar enquanto **'{coluna_y_interpret.replace('_', ' ').title()}'** diminui, mas com alguma dispersão.")
            else:
                st.write(f"A correlação é **baixa ou nula**: não há uma relação linear forte aparente entre **'{coluna_x_interpret.replace('_', ' ').title()}'** e **'{coluna_y_interpret.replace('_', ' ').title()}'**. Outros tipos de relações (não-lineares) podem existir, mas não são capturados por este coeficiente.")

    elif len(lista_de_escolhas_multivariada) > 2:
        st.error('Por favor, escolha **somente 2 colunas** para os gráficos de relação.')
    elif len(lista_de_escolhas_multivariada) < 2 and len(lista_de_escolhas_multivariada) > 0:
        st.info('Por favor, escolha **mais uma coluna** para visualizar os gráficos de relação.')
    else:
        st.info('Selecione duas colunas para visualizar os gráficos de dispersão e caixa.')
        