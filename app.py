import streamlit as st
import pandas as pd
import pydeck as pdk

data_url = "https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv"

@st.cache
def load_data():
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = pd.read_csv(data_url, index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data


# carregar os dados
df = load_data()
labels = df.classificacao.unique().tolist()


# Sidebar
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()
# st.sidebar.info("Dados de ocorrências aeronáuticas da aviação civil brasileira entre 2008-2018.")
st.sidebar.subheader("Ano")
year_to_filter = st.sidebar.slider('Escolha o ano desejado', 2008, 2018, 2017)
st.sidebar.subheader("Classificação")
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()
label_to_filter = st.sidebar.multiselect(
    label="Escolha a classificação da ocorrência",
    options=labels,
    default=labels
)
filtered_df = df[(df.data.dt.year == year_to_filter) & (df.classificacao.isin(label_to_filter))]
info_sidebar.info("{} ocorrências selecionadas.".format(filtered_df.shape[0], year_to_filter))

st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")
# acidentes_por_ano = df.data.dt.year.value_counts().sort_index()
# st.sidebar.subheader("Evolução")
# st.sidebar.bar_chart(acidentes_por_ano, height=170)


# Main
st.title("CENIPA - Acidentes Aeronáuticos")
st.markdown(f"""
            ℹ️ Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
            para o ano de **{year_to_filter}**.
            """)

# raw data
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df)


# mapa
st.subheader("Mapa de ocorrências")
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=-3.142991,
        longitude=-59.996365,
        zoom=5,
        pitch=50
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_df,
            disk_resolution=12,
            radius=30000,
            get_position='[longitude,latitude]',
            get_fill_color='[255, 255, 255, 255]',
            get_line_color="[255, 255, 255]",
            auto_highlight=True,
            elevation_scale=1500,
            # elevation_range=[0, 3000],
            # get_elevation="norm_price",
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='[255, 255, 255, 30]',
            get_radius=60000,
        ),
    ],
))
